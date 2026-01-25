from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.institution import Institution
from models.sport import Sport
from schemas.institution import InstitutionResponse
from schemas.sport import SportResponse

router = APIRouter(prefix="/institutions", tags=["Institutions"])


@router.get("", response_model=List[InstitutionResponse])
async def list_institutions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all active institutions (Public)"""
    institutions = db.query(Institution).filter(Institution.is_active == True).offset(skip).limit(limit).all()
    return institutions


@router.get("/{institution_id}", response_model=InstitutionResponse)
async def get_institution(
    institution_id: int,
    db: Session = Depends(get_db)
):
    """Get institution details by ID (Public)"""
    institution = db.query(Institution).filter(Institution.id == institution_id).first()
    if not institution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Institution not found"
        )
    return institution


@router.get("/{institution_id}/sports", response_model=List[SportResponse])
async def list_institution_sports(
    institution_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all sports for a specific institution (Public)"""
    # First check if institution exists
    institution = db.query(Institution).filter(Institution.id == institution_id).first()
    if not institution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Institution not found"
        )
        
    sports = db.query(Sport).filter(
        Sport.institution_id == institution_id,
        Sport.is_active == True
    ).offset(skip).limit(limit).all()
    
    return sports
