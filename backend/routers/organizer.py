from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.auth import User
from models.institution import Institution
from models.sport import Sport
from models.team import Team
from models.player import Player
from schemas.institution import InstitutionUpdate, InstitutionResponse
from schemas.sport import SportCreate, SportResponse
from schemas.team import TeamCreate, TeamResponse
from schemas.player import PlayerCreate, PlayerResponse
from dependencies import get_current_user_required as get_current_user
from security.admin_service import is_admin_or_organizer, can_manage_institution

router = APIRouter(prefix="/organizer", tags=["Organizer"])


def require_organizer(current_user: User = Depends(get_current_user)) -> User:
    """Dependency to require organizer or admin role"""
    if not is_admin_or_organizer(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Organizer or Admin access required"
        )
    return current_user


from services.sport_templates import get_template, get_all_templates
import json


from services.sport_templates import get_template, get_all_templates
import json

@router.post("/sports", response_model=SportResponse, status_code=status.HTTP_201_CREATED)
async def create_sport(
    sport_data: SportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_organizer)
):
    """Create a new sport (Organizer only)"""
    # Check if sport code already exists
    existing = db.query(Sport).filter(Sport.code == sport_data.code).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sport code already exists"
        )
    
    # Prepare data
    data = sport_data.dict(exclude={"template_code"})
    data["organizer_id"] = current_user.id
    
    # If template code is provided, populate from template
    if sport_data.template_code:
        template = get_template(sport_data.template_code)
        if template:
            # Override fields with template data
            data["name"] = template["name"]
            data["code"] = template["code"]
            data["sport_type"] = template["sport_type"]
            data["min_players_per_team"] = template["min_players_per_team"]
            data["max_players_per_team"] = template["max_players_per_team"]
            data["description"] = template["description"]
            
            # Identify mandatory rules (cannot be removed)
            data["mandatory_rules"] = json.dumps(template["mandatory_rules"])
            
            # Initial rules (mandatory + optional)
            data["rules"] = json.dumps(template["rules"])
            
            # Match configuration
            data["match_config"] = json.dumps(template["match_config"])
    
    # Check if code exists again if it was changed by template
    # Check if code already exists (either user-provided or from template)
    existing = db.query(Sport).filter(
        Sport.code == data["code"],
        Sport.institution_id == sport_data.institution_id
    ).first()
    if existing:
        # If standard code exists, append institution ID to make unique
        data["code"] = f"{data['code']}_{sport_data.institution_id}"

    db_sport = Sport(**data)
    db.add(db_sport)
    db.commit()
    db.refresh(db_sport)
    
    return db_sport


@router.get("/sports/templates")
async def list_sport_templates(
    current_user: User = Depends(require_organizer)
):
    """List available sport templates"""
    return get_all_templates()


@router.get("/sports", response_model=List[SportResponse])
async def list_sports(
    institution_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    organizer: User = Depends(require_organizer)
):
    """List sports"""
    query = db.query(Sport)
    if institution_id:
        query = query.filter(Sport.institution_id == institution_id)
    sports = query.offset(skip).limit(limit).all()
    return sports


@router.post("/teams", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
async def create_team(
    team_data: TeamCreate,
    db: Session = Depends(get_db),
    organizer: User = Depends(require_organizer)
):
    """Create a new team"""
    db_team = Team(**team_data.dict())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    
    return db_team


@router.get("/teams", response_model=List[TeamResponse])
async def list_teams(
    sport_id: int = None,
    institution_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    organizer: User = Depends(require_organizer)
):
    """List teams"""
    query = db.query(Team)
    if sport_id:
        query = query.filter(Team.sport_id == sport_id)
    if institution_id:
        query = query.filter(Team.institution_id == institution_id)
    teams = query.offset(skip).limit(limit).all()
    return teams


@router.post("/players", response_model=PlayerResponse, status_code=status.HTTP_201_CREATED)
async def create_player(
    player_data: PlayerCreate,
    db: Session = Depends(get_db),
    organizer: User = Depends(require_organizer)
):
    """Create a new player"""
    db_player = Player(**player_data.dict())
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    
    return db_player


@router.get("/players", response_model=List[PlayerResponse])
async def list_players(
    team_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    organizer: User = Depends(require_organizer)
):
    """List players"""
    query = db.query(Player)
    if team_id:
        query = query.filter(Player.team_id == team_id)
    players = query.offset(skip).limit(limit).all()
    return players


@router.get("/institution", response_model=InstitutionResponse)
async def get_my_institution(
    db: Session = Depends(get_db),
    organizer: User = Depends(require_organizer)
):
    """Get organizer's institution"""
    if not organizer.institution_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organizer is not associated with an institution"
        )
    
    institution = db.query(Institution).filter(Institution.id == organizer.institution_id).first()
    if not institution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Institution not found"
        )
    return institution


@router.patch("/institution", response_model=InstitutionResponse)
async def update_institution_profile(
    institution_update: InstitutionUpdate,
    db: Session = Depends(get_db),
    organizer: User = Depends(require_organizer)
):
    """Update institution profile and logo (Organizer only)"""
    if not organizer.institution_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organizer is not associated with an institution"
        )
    
    institution = db.query(Institution).filter(Institution.id == organizer.institution_id).first()
    if not institution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Institution not found"
        )
    
    if not can_manage_institution(organizer, institution.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to manage this institution"
        )
    
    update_data = institution_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(institution, field, value)
    
    db.commit()
    db.refresh(institution)
    return institution
