from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import datetime
from database import get_db
from models.auth import User
from models.match import Match, MatchStatus, MatchParticipation
from models.schedule import Schedule, ScheduleType
from models.score import Score, ScoreUpdate
from schemas.match import MatchCreate, MatchResponse, MatchUpdate
from schemas.schedule import ScheduleCreate, ScheduleResponse
from schemas.score import ScoreUpdate as ScoreUpdateSchema, ScoreResponse
from dependencies import get_current_user
from typing import Optional
from security.admin_service import is_admin_or_organizer
from services.scheduling_service import generate_round_robin_schedule, generate_knockout_schedule

router = APIRouter(prefix="/matches", tags=["Matches"])


def require_organizer(current_user: User = Depends(get_current_user)) -> User:
    """Dependency to require organizer or admin role"""
    if not is_admin_or_organizer(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Organizer or Admin access required"
        )
    return current_user


@router.post("/schedules", response_model=ScheduleResponse, status_code=status.HTTP_201_CREATED)
async def create_schedule(
    schedule_data: ScheduleCreate,
    db: Session = Depends(get_db),
    organizer: User = Depends(require_organizer)
):
    """Create a new schedule and auto-generate matches"""
    db_schedule = Schedule(**schedule_data.dict())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    
    # Auto-generate matches based on schedule type
    if schedule_data.schedule_type == ScheduleType.ROUND_ROBIN:
        generate_round_robin_schedule(
            db, db_schedule,
            team_ids=schedule_data.team_ids,
            player_ids=schedule_data.player_ids
        )
    elif schedule_data.schedule_type == ScheduleType.KNOCKOUT:
        generate_knockout_schedule(
            db, db_schedule,
            team_ids=schedule_data.team_ids,
            player_ids=schedule_data.player_ids
        )
    
    db.commit()
    return db_schedule


@router.get("/schedules", response_model=List[ScheduleResponse])
async def list_schedules(
    sport_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """List all schedules (public endpoint)"""
    query = db.query(Schedule)
    if sport_id:
        query = query.filter(Schedule.sport_id == sport_id)
    schedules = query.offset(skip).limit(limit).all()
    return schedules


@router.get("/schedules/{schedule_id}", response_model=ScheduleResponse)
async def get_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get schedule by ID"""
    schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found"
        )
    return schedule


@router.post("", response_model=MatchResponse, status_code=status.HTTP_201_CREATED)
async def create_match(
    match_data: MatchCreate,
    db: Session = Depends(get_db),
    organizer: User = Depends(require_organizer)
):
    """Create a new match manually"""
    match_dict = match_data.dict()
    player_ids = match_dict.pop("player_ids", None)
    
    db_match = Match(**match_dict, created_by=organizer.id)
    db.add(db_match)
    db.flush()
    
    # Add player participations for individual sports
    if player_ids:
        for i, player_id in enumerate(player_ids[:2]):  # Max 2 players
            db.add(MatchParticipation(
                match_id=db_match.id,
                player_id=player_id,
                is_home=(i == 0)
            ))
    
    db.commit()
    db.refresh(db_match)
    return db_match


@router.get("", response_model=List[MatchResponse])
async def list_matches(
    sport_id: int = None,
    schedule_id: int = None,
    status: Optional[MatchStatus] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """List matches (public endpoint - no authentication required)"""
    try:
        query = db.query(Match)
        if sport_id:
            query = query.filter(Match.sport_id == sport_id)
        if schedule_id:
            query = query.filter(Match.schedule_id == schedule_id)
        if status:
            query = query.filter(Match.status == status)
        matches = query.offset(skip).limit(limit).all()
        return matches
    except Exception as e:
        import traceback
        error_detail = f"{str(e)}\n{traceback.format_exc()}"
        raise HTTPException(status_code=500, detail=error_detail)


@router.get("/{match_id}", response_model=MatchResponse)
async def get_match(
    match_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """Get match by ID (public endpoint)"""
    match = db.query(Match).options(
        joinedload(Match.sport),
        joinedload(Match.home_team),
        joinedload(Match.away_team)
    ).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found"
        )
    return match


@router.patch("/{match_id}", response_model=MatchResponse)
async def update_match(
    match_id: int,
    match_update: MatchUpdate,
    db: Session = Depends(get_db),
    organizer: User = Depends(require_organizer)
):
    """Update a match"""
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found"
        )
    
    update_data = match_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(match, field, value)
    
    # If status changes to LIVE, set actual_start_time
    if match_update.status == MatchStatus.LIVE and not match.actual_start_time:
        match.actual_start_time = datetime.utcnow()
    
    # If status changes to COMPLETED, set actual_end_time
    if match_update.status == MatchStatus.COMPLETED and not match.actual_end_time:
        match.actual_end_time = datetime.utcnow()
    
    db.commit()
    db.refresh(match)
    return match


@router.post("/{match_id}/score", response_model=ScoreResponse)
async def update_score(
    match_id: int,
    score_update: ScoreUpdateSchema,
    db: Session = Depends(get_db),
    organizer: User = Depends(require_organizer)
):
    """Update match score (live score updates)"""
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found"
        )
    
    # Get or create score record
    score = db.query(Score).filter(Score.match_id == match_id).first()
    if not score:
        score = Score(match_id=match_id, home_score=0, away_score=0)
        db.add(score)
    
    # Update score
    if score_update.home_score is not None:
        score.home_score = score_update.home_score
    if score_update.away_score is not None:
        score.away_score = score_update.away_score
    if score_update.period:
        score.period = score_update.period
    if score_update.additional_info:
        score.additional_info = score_update.additional_info
    
    # Create score update history
    db_score_update = ScoreUpdate(
        match_id=match_id,
        home_score=score.home_score,
        away_score=score.away_score,
        period=score_update.period,
        update_type=score_update.update_type,
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


@router.get("/{match_id}/score", response_model=ScoreResponse)
async def get_match_score(
    match_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """Get current match score (public endpoint)"""
    score = db.query(Score).filter(Score.match_id == match_id).first()
    if not score:
        # Return default score if not set
        return ScoreResponse(
            id=0,
            match_id=match_id,
            home_score=0,
            away_score=0,
            created_at=datetime.utcnow()
        )
    return score


@router.get("/{match_id}/score/history", response_model=List[dict])
async def get_score_history(
    match_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """Get score update history for a match (public endpoint)"""
    score_updates = db.query(ScoreUpdate).filter(
        ScoreUpdate.match_id == match_id
    ).order_by(ScoreUpdate.created_at).all()
    
    return [
        {
            "id": update.id,
            "home_score": update.home_score,
            "away_score": update.away_score,
            "period": update.period,
            "update_type": update.update_type,
            "description": update.description,
            "updated_at": update.updated_at.isoformat() if update.updated_at else None
        }
        for update in score_updates
    ]
