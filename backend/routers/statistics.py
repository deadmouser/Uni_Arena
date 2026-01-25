from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.auth import User
from models.player import Player
from models.team import Team
from models.statistics import PlayerStatistics, TeamStatistics
from schemas.statistics import PlayerStatisticsResponse, TeamStatisticsResponse
from dependencies import get_current_user_required as get_current_user

router = APIRouter(prefix="/statistics", tags=["Statistics"])


@router.get("/players/{player_id}", response_model=PlayerStatisticsResponse)
async def get_player_statistics(
    player_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get player statistics"""
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player not found"
        )
    
    stats = db.query(PlayerStatistics).filter(PlayerStatistics.player_id == player_id).first()
    if not stats:
        # Create default stats if not exists
        stats = PlayerStatistics(player_id=player_id)
        db.add(stats)
        db.commit()
        db.refresh(stats)
    
    return stats


@router.get("/teams/{team_id}", response_model=TeamStatisticsResponse)
async def get_team_statistics(
    team_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get team statistics"""
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found"
        )
    
    stats = db.query(TeamStatistics).filter(TeamStatistics.team_id == team_id).first()
    if not stats:
        # Create default stats if not exists
        stats = TeamStatistics(team_id=team_id)
        db.add(stats)
        db.commit()
        db.refresh(stats)
    
    return stats


@router.get("/players/me", response_model=PlayerStatisticsResponse)
async def get_my_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user's player statistics"""
    if not current_user.player_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User is not a player"
        )
    
    player_id = current_user.player_profile.id
    stats = db.query(PlayerStatistics).filter(PlayerStatistics.player_id == player_id).first()
    if not stats:
        stats = PlayerStatistics(player_id=player_id)
        db.add(stats)
        db.commit()
        db.refresh(stats)
    
    return stats
