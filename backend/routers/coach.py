from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import json
from database import get_db
from models.auth import User, UserRole
from models.team import Team
from models.player import Player
from models.match import Match, MatchStatus
from models.lineup import Lineup, LineupPlayer
from models.score import Score, ScoreUpdate
from models.sport import Sport
from schemas.lineup import LineupCreate, LineupResponse, LineupPlayerBase
from schemas.player import PlayerResponse
from schemas.team import TeamResponse
from schemas.score import ScoreUpdate as ScoreUpdateSchema, ScoreResponse
from dependencies import get_current_user_required as get_current_user
from security.admin_service import is_admin_or_organizer
from services.sport_scoring import (
    get_sport_code, get_scoring_handler, parse_additional_info,
    serialize_additional_info, SportCode, ScoreAction
)

router = APIRouter(prefix="/coach", tags=["Coach"])


def require_coach(current_user: User = Depends(get_current_user)) -> User:
    """Dependency to require coach role"""
    if current_user.role not in [UserRole.COACH, UserRole.ADMIN, UserRole.ORGANIZER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Coach, Admin, or Organizer access required"
        )
    return current_user


@router.get("/teams", response_model=List[TeamResponse])
async def get_my_teams(
    db: Session = Depends(get_db),
    coach: User = Depends(require_coach)
):
    """Get teams coached by the current coach"""
    teams = db.query(Team).filter(Team.coach_id == coach.id).all()
    return teams


@router.get("/teams/{team_id}/players", response_model=List[PlayerResponse])
async def get_team_players(
    team_id: int,
    db: Session = Depends(get_db),
    coach: User = Depends(require_coach)
):
    """Get players in a team (coach can view)"""
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found"
        )
    
    # Verify coach has access to this team
    if team.coach_id != coach.id and not is_admin_or_organizer(coach):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this team"
        )
    
    players = db.query(Player).filter(Player.team_id == team_id).all()
    return players


@router.post("/matches/{match_id}/lineups", response_model=LineupResponse, status_code=status.HTTP_201_CREATED)
async def create_lineup(
    match_id: int,
    lineup_data: LineupCreate,
    db: Session = Depends(get_db),
    coach: User = Depends(require_coach)
):
    """Create a line-up for a match (Coach only)"""
    # Verify match exists
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found"
        )
    
    # Verify coach has access to the team
    team = db.query(Team).filter(Team.id == lineup_data.team_id).first()
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found"
        )
    
    if team.coach_id != coach.id and not is_admin_or_organizer(coach):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to manage this team's line-up"
        )
    
    # Check if lineup already exists
    existing = db.query(Lineup).filter(
        Lineup.match_id == match_id,
        Lineup.team_id == lineup_data.team_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Line-up already exists for this match and team"
        )
    
    # Create lineup
    lineup_dict = lineup_data.dict()
    players_data = lineup_dict.pop("players")
    
    db_lineup = Lineup(**lineup_dict)
    db.add(db_lineup)
    db.flush()
    
    # Add players to lineup
    for player_data in players_data:
        db.add(LineupPlayer(lineup_id=db_lineup.id, **player_data))
    
    db.commit()
    db.refresh(db_lineup)
    return db_lineup


@router.get("/matches/{match_id}/lineups", response_model=List[LineupResponse])
async def get_match_lineups(
    match_id: int,
    db: Session = Depends(get_db),
    coach: User = Depends(require_coach)
):
    """Get line-ups for a match"""
    lineups = db.query(Lineup).filter(Lineup.match_id == match_id).all()
    return lineups


@router.get("/lineups/{lineup_id}", response_model=LineupResponse)
async def get_lineup(
    lineup_id: int,
    db: Session = Depends(get_db),
    coach: User = Depends(require_coach)
):
    """Get a specific line-up with players"""
    lineup = db.query(Lineup).filter(Lineup.id == lineup_id).first()
    if not lineup:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Line-up not found"
        )
    return lineup


@router.patch("/lineups/{lineup_id}/players", response_model=LineupResponse)
async def update_lineup_players(
    lineup_id: int,
    players: List[dict],
    db: Session = Depends(get_db),
    coach: User = Depends(require_coach)
):
    """Update players in a line-up"""
    lineup = db.query(Lineup).filter(Lineup.id == lineup_id).first()
    if not lineup:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Line-up not found"
        )
    
    # Verify coach has access
    team = db.query(Team).filter(Team.id == lineup.team_id).first()
    if team.coach_id != coach.id and not is_admin_or_organizer(coach):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this line-up"
        )
    
    # Delete existing players
    db.query(LineupPlayer).filter(LineupPlayer.lineup_id == lineup_id).delete()
    
    # Add new players
    for player_data in players:
        db.add(LineupPlayer(lineup_id=lineup_id, **player_data))
    
    db.commit()
    db.refresh(lineup)
    return lineup


@router.post("/matches/{match_id}/score", response_model=ScoreResponse)
async def update_match_score(
    match_id: int,
    score_update: ScoreUpdateSchema,
    db: Session = Depends(get_db),
    coach: User = Depends(require_coach)
):
    """Update match score with sport-specific logic (Coach can update scores for their team's matches)"""
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found"
        )
    
    # Get sport information
    sport = db.query(Sport).filter(Sport.id == match.sport_id).first()
    if not sport:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sport not found"
        )
    
    # Verify coach has access to one of the teams in the match
    has_access = False
    if match.home_team_id:
        home_team = db.query(Team).filter(Team.id == match.home_team_id).first()
        if home_team and home_team.coach_id == coach.id:
            has_access = True
    
    if match.away_team_id:
        away_team = db.query(Team).filter(Team.id == match.away_team_id).first()
        if away_team and away_team.coach_id == coach.id:
            has_access = True
    
    if not has_access and not is_admin_or_organizer(coach):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update scores for this match"
        )
    
    # Get or create score record
    score = db.query(Score).filter(Score.match_id == match_id).first()
    if not score:
        score = Score(match_id=match_id, home_score=0, away_score=0)
        db.add(score)
        db.flush()
    
    # Parse current additional_info
    current_data = parse_additional_info(score.additional_info)
    
    # Get sport-specific scoring handler
    sport_code = get_sport_code(sport.name)
    handler = get_scoring_handler(sport_code)
    
    # Initialize sport-specific data if not present
    if handler and not current_data:
        current_data = handler.get_default_score()
    
    # Determine team from score_update or use default
    team = score_update.team or ("home" if score_update.home_score is not None else "away")
    
    # Process sport-specific scoring actions
    if handler and score_update.action:
        action = score_update.action.lower()
        
        if sport_code == SportCode.CRICKET:
            if action == "add_run" and score_update.points:
                current_data = handler.add_run(current_data, score_update.points, team)
                # Update main score
                if team == "home":
                    score.home_score = current_data.get("home_runs", score.home_score)
                else:
                    score.away_score = current_data.get("away_runs", score.away_score)
            elif action == "wicket":
                current_data = handler.add_wicket(current_data, team, score_update.player_id)
                # Update period to show wickets
                home_runs, home_wickets = handler.get_score_display(current_data, "home")
                away_runs, away_wickets = handler.get_score_display(current_data, "away")
                score.period = f"{home_wickets}/{away_wickets} wickets"
        
        elif sport_code == SportCode.FOOTBALL:
            if action == "goal":
                current_data = handler.add_goal(current_data, team, score_update.player_id)
                if team == "home":
                    score.home_score = current_data.get("home_goals", score.home_score)
                else:
                    score.away_score = current_data.get("away_goals", score.away_score)
            elif action in ["yellow_card", "red_card"]:
                current_data = handler.add_card(current_data, team, action.replace("_card", ""), score_update.player_id)
            elif action == "foul":
                current_data = handler.add_foul(current_data, team)
        
        elif sport_code == SportCode.BASKETBALL:
            if action == "point" and score_update.points:
                point_type = score_update.sport_specific_data.get("point_type", "field_goal") if score_update.sport_specific_data else "field_goal"
                current_data = handler.add_points(current_data, team, score_update.points, point_type)
                if team == "home":
                    score.home_score = current_data.get("home_points", score.home_score)
                else:
                    score.away_score = current_data.get("away_points", score.away_score)
                # Update period (quarter)
                if "quarter" in current_data:
                    score.period = f"Q{current_data['quarter']}"
            elif action == "foul":
                current_data = handler.add_foul(current_data, team)
            elif action == "timeout":
                current_data = handler.use_timeout(current_data, team)
        
        elif sport_code == SportCode.CHESS:
            if action == "move":
                current_data = handler.add_move(current_data, team)
            elif action in ["checkmate", "resign", "draw"]:
                result = f"{team}_win" if action != "draw" else "draw"
                current_data = handler.set_result(current_data, result)
                if result == "draw":
                    score.home_score = 0.5
                    score.away_score = 0.5
                elif "white" in team or team == "home":
                    score.home_score = 1
                    score.away_score = 0
                else:
                    score.home_score = 0
                    score.away_score = 1
        
        elif sport_code == SportCode.VOLLEYBALL:
            if action == "set_point":
                set_num = score_update.sport_specific_data.get("set_num") if score_update.sport_specific_data else None
                current_data = handler.add_point(current_data, team, set_num)
                # Update main score with sets won
                home_sets = handler.get_sets_won(current_data, "home")
                away_sets = handler.get_sets_won(current_data, "away")
                score.home_score = home_sets
                score.away_score = away_sets
                # Update period
                current_set = current_data.get("current_set", 1)
                score.period = f"Set {current_set}"
            elif action == "service_error":
                team_key = f"{team}_service_errors"
                if team_key not in current_data:
                    current_data[team_key] = 0
                current_data[team_key] += 1
        
        elif sport_code == SportCode.BADMINTON:
            if action == "set_point":
                set_num = score_update.sport_specific_data.get("set_num") if score_update.sport_specific_data else None
                current_data = handler.add_point(current_data, team, set_num)
                # Update main score with sets won
                home_sets = handler.get_sets_won(current_data, "home")
                away_sets = handler.get_sets_won(current_data, "away")
                score.home_score = home_sets
                score.away_score = away_sets
                # Update period
                current_set = current_data.get("current_set", 1)
                score.period = f"Set {current_set}"
            elif action == "service_error":
                team_key = f"{team}_service_errors"
                if team_key not in current_data:
                    current_data[team_key] = 0
                current_data[team_key] += 1
    
    # Handle direct score updates (fallback for non-sport-specific updates)
    if score_update.home_score is not None:
        score.home_score = score_update.home_score
    if score_update.away_score is not None:
        score.away_score = score_update.away_score
    if score_update.period:
        score.period = score_update.period
    
    # Update additional_info with sport-specific data
    if current_data:
        score.additional_info = serialize_additional_info(current_data)
    elif score_update.additional_info:
        score.additional_info = score_update.additional_info
    
    # Create score update history
    db_score_update = ScoreUpdate(
        match_id=match_id,
        home_score=score.home_score,
        away_score=score.away_score,
        period=score.period,
        update_type=score_update.update_type or score_update.action,
        description=score_update.description,
        updated_at=datetime.utcnow()
    )
    db.add(db_score_update)
    
    # Update match status to LIVE if not already
    if match.status == MatchStatus.SCHEDULED:
        match.status = MatchStatus.LIVE
        if not match.actual_start_time:
            match.actual_start_time = datetime.utcnow()
    
    db.commit()
    db.refresh(score)
    return score


@router.patch("/matches/{match_id}/end", response_model=dict)
async def end_match(
    match_id: int,
    db: Session = Depends(get_db),
    coach: User = Depends(require_coach)
):
    """End a match (Coach can end matches for their team)"""
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found"
        )
    
    # Verify coach has access
    has_access = False
    if match.home_team_id:
        home_team = db.query(Team).filter(Team.id == match.home_team_id).first()
        if home_team and home_team.coach_id == coach.id:
            has_access = True
    
    if match.away_team_id:
        away_team = db.query(Team).filter(Team.id == match.away_team_id).first()
        if away_team and away_team.coach_id == coach.id:
            has_access = True
    
    if not has_access and not is_admin_or_organizer(coach):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to end this match"
        )
    
    match.status = MatchStatus.COMPLETED
    match.actual_end_time = datetime.utcnow()
    
    db.commit()
    db.refresh(match)
    return {"message": "Match ended successfully", "match_id": match_id}


@router.get("/matches/{match_id}/players", response_model=List[PlayerResponse])
async def get_match_players(
    match_id: int,
    db: Session = Depends(get_db),
    coach: User = Depends(require_coach)
):
    """Get players currently playing in a match"""
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found"
        )
    
    # Get players from lineups
    lineups = db.query(Lineup).filter(Lineup.match_id == match_id).all()
    player_ids = set()
    
    for lineup in lineups:
        lineup_players = db.query(LineupPlayer).filter(LineupPlayer.lineup_id == lineup.id).all()
        for lp in lineup_players:
            if lp.player_id:
                player_ids.add(lp.player_id)
    
    players = db.query(Player).filter(Player.id.in_(list(player_ids))).all()
    return players


@router.get("/matches/{match_id}/score/details")
async def get_score_details(
    match_id: int,
    db: Session = Depends(get_db),
    coach: User = Depends(require_coach)
):
    """Get detailed sport-specific score information"""
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found"
        )
    
    sport = db.query(Sport).filter(Sport.id == match.sport_id).first()
    if not sport:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sport not found"
        )
    
    score = db.query(Score).filter(Score.match_id == match_id).first()
    if not score:
        return {
            "sport_code": get_sport_code(sport.name).value if get_sport_code(sport.name) else None,
            "sport_name": sport.name,
            "score_data": {}
        }
    
    score_data = parse_additional_info(score.additional_info)
    
    return {
        "sport_code": get_sport_code(sport.name).value if get_sport_code(sport.name) else None,
        "sport_name": sport.name,
        "score_data": score_data,
        "home_score": score.home_score,
        "away_score": score.away_score,
        "period": score.period
    }
