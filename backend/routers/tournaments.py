from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models.auth import User
from models.tournament import Tournament, TournamentSport
from schemas.tournament import TournamentCreate, TournamentResponse, TournamentUpdate
from dependencies import get_current_user
from typing import Optional
from security.admin_service import is_admin_or_organizer

router = APIRouter(prefix="/tournaments", tags=["Tournaments"])


def require_organizer(current_user: User = Depends(get_current_user)) -> User:
    """Dependency to require organizer or admin role"""
    if not is_admin_or_organizer(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Organizer or Admin access required"
        )
    return current_user


@router.post("", response_model=TournamentResponse, status_code=status.HTTP_201_CREATED)
async def create_tournament(
    tournament_data: TournamentCreate,
    db: Session = Depends(get_db),
    organizer: User = Depends(require_organizer)
):
    """Create a new tournament (Organizer only)"""
    tournament_dict = tournament_data.dict()
    sport_ids = tournament_dict.pop("sport_ids", None)
    
    db_tournament = Tournament(**tournament_dict)
    db.add(db_tournament)
    db.flush()
    
    # Add sports to tournament
    if sport_ids:
        for sport_id in sport_ids:
            db.add(TournamentSport(tournament_id=db_tournament.id, sport_id=sport_id))
    
    db.commit()
    db.refresh(db_tournament)
    return db_tournament


@router.get("", response_model=List[TournamentResponse])
async def list_tournaments(
    institution_id: Optional[int] = None,
    is_public: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """List tournaments (public endpoint)"""
    query = db.query(Tournament)
    if institution_id:
        query = query.filter(Tournament.institution_id == institution_id)
    if is_public is not None:
        query = query.filter(Tournament.is_public == is_public)
    tournaments = query.offset(skip).limit(limit).all()
    return tournaments


@router.get("/{tournament_id}", response_model=TournamentResponse)
async def get_tournament(
    tournament_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """Get tournament by ID (public endpoint)"""
    tournament = db.query(Tournament).filter(Tournament.id == tournament_id).first()
    if not tournament:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tournament not found"
        )
    
    # Check if tournament is public or user has access
    if not tournament.is_public and not current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tournament is not public"
        )
    
    return tournament


@router.patch("/{tournament_id}", response_model=TournamentResponse)
async def update_tournament(
    tournament_id: int,
    tournament_update: TournamentUpdate,
    db: Session = Depends(get_db),
    organizer: User = Depends(require_organizer)
):
    """Update a tournament (Organizer only)"""
    tournament = db.query(Tournament).filter(Tournament.id == tournament_id).first()
    if not tournament:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tournament not found"
        )
    
    update_data = tournament_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(tournament, field, value)
    
    db.commit()
    db.refresh(tournament)
    return tournament
