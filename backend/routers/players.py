from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.auth import User, UserRole
from models.team import Team
from models.player import Player
from models.notification import Notification, NotificationType
from schemas.player import PlayerResponse
from dependencies import get_current_user_required as get_current_user

router = APIRouter(prefix="/players", tags=["Players"])


def require_player(current_user: User = Depends(get_current_user)) -> User:
    """Dependency to require player role"""
    if current_user.role != UserRole.PLAYER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Player access required"
        )
    return current_user


@router.post("/teams/{team_id}/join", response_model=PlayerResponse)
async def join_team(
    team_id: int,
    db: Session = Depends(get_db),
    player: User = Depends(require_player)
):
    """Request to join a team (Player only)"""
    # Check if user has a player profile
    if not player.player_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not have a player profile"
        )
    
    # Check if team exists
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found"
        )
    
    # Check if player is already in a team for this sport
    existing_player = db.query(Player).filter(
        Player.user_id == player.id,
        Player.team_id.isnot(None)
    ).first()
    
    if existing_player and existing_player.team_id != team_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Player is already in another team"
        )
    
    # Add player to team
    player.player_profile.team_id = team_id
    db.commit()
    db.refresh(player.player_profile)
    
    # Create notification for team coach/organizer
    if team.coach_id:
        notification = Notification(
            user_id=team.coach_id,
            title="New Team Join Request",
            message=f"{player.full_name or player.username} has joined team {team.name}",
            notification_type=NotificationType.TEAM_JOIN,
            link_url=f"/teams/{team_id}"
        )
        db.add(notification)
        db.commit()
    
    return player.player_profile


@router.get("/me", response_model=PlayerResponse)
async def get_my_profile(
    db: Session = Depends(get_db),
    player: User = Depends(require_player)
):
    """Get current player's profile"""
    if not player.player_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not have a player profile"
        )
    return player.player_profile
