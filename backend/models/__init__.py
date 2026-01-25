from models.base import BaseModel
from models.auth import User, UserRole
from models.institution import Institution

# Import all models to ensure they're registered with SQLAlchemy
from models.sport import Sport
from models.team import Team
from models.player import Player
from models.match import Match, MatchStatus
from models.schedule import Schedule, ScheduleType
from models.score import Score, ScoreUpdate
from models.venue import Venue
from models.tournament import Tournament, TournamentStatus, TournamentSport
from models.lineup import Lineup, LineupPlayer
from models.notification import Notification, NotificationType
from models.statistics import PlayerStatistics, TeamStatistics

__all__ = [
    "BaseModel",
    "User",
    "UserRole",
    "Institution",
    "Sport",
    "Team",
    "Player",
    "Match",
    "MatchStatus",
    "Schedule",
    "ScheduleType",
    "Score",
    "ScoreUpdate",
    "Venue",
    "Tournament",
    "TournamentStatus",
    "TournamentSport",
    "Lineup",
    "LineupPlayer",
    "Notification",
    "NotificationType",
    "PlayerStatistics",
    "TeamStatistics",
]
