from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.auth import User
from models.venue import Venue
from schemas.venue import VenueCreate, VenueResponse
from dependencies import get_current_user_required as get_current_user
from security.admin_service import is_admin_or_organizer

router = APIRouter(prefix="/venues", tags=["Venues"])


def require_organizer(current_user: User = Depends(get_current_user)) -> User:
    """Dependency to require organizer or admin role"""
    if not is_admin_or_organizer(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Organizer or Admin access required"
        )
    return current_user


@router.post("", response_model=VenueResponse, status_code=status.HTTP_201_CREATED)
async def create_venue(
    venue_data: VenueCreate,
    db: Session = Depends(get_db),
    organizer: User = Depends(require_organizer)
):
    """Create a new venue (Organizer only)"""
    db_venue = Venue(**venue_data.dict())
    db.add(db_venue)
    db.commit()
    db.refresh(db_venue)
    return db_venue


@router.get("", response_model=List[VenueResponse])
async def list_venues(
    institution_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List venues (all authenticated users)"""
    query = db.query(Venue)
    if institution_id:
        query = query.filter(Venue.institution_id == institution_id)
    venues = query.offset(skip).limit(limit).all()
    return venues


@router.get("/{venue_id}", response_model=VenueResponse)
async def get_venue(
    venue_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get venue by ID"""
    venue = db.query(Venue).filter(Venue.id == venue_id).first()
    if not venue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venue not found"
        )
    return venue


@router.patch("/{venue_id}", response_model=VenueResponse)
async def update_venue(
    venue_id: int,
    venue_update: VenueCreate,
    db: Session = Depends(get_db),
    organizer: User = Depends(require_organizer)
):
    """Update a venue (Organizer only)"""
    venue = db.query(Venue).filter(Venue.id == venue_id).first()
    if not venue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venue not found"
        )
    
    update_data = venue_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(venue, field, value)
    
    db.commit()
    db.refresh(venue)
    return venue
