from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.auth import User
from models.tournament import Tournament
from schemas.tournament import TournamentResponse
from dependencies import get_current_user_required as get_current_user
from security.admin_service import is_admin

router = APIRouter(prefix="/admin/tournaments", tags=["Admin Tournaments"])


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Dependency to require admin role"""
    if not is_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


@router.get("", response_model=List[TournamentResponse])
async def list_all_tournaments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """List all tournaments across all institutions (Admin only)"""
    tournaments = db.query(Tournament).offset(skip).limit(limit).all()
    return tournaments


@router.delete("/{tournament_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tournament(
    tournament_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Delete any tournament (Admin only)"""
    tournament = db.query(Tournament).filter(Tournament.id == tournament_id).first()
    if not tournament:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tournament not found"
        )
    
    db.delete(tournament)
    db.commit()
    return None
