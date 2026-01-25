"""
Sport-specific scoring logic and utilities
Handles scoring rules for different sports: Cricket, Football, Basketball, Chess, Volleyball, Badminton
"""
import json
from typing import Dict, Any, Optional
from enum import Enum


class SportCode(str, Enum):
    CRICKET = "CRICKET"
    FOOTBALL = "FOOTBALL"
    BASKETBALL = "BASKETBALL"
    CHESS = "CHESS"
    VOLLEYBALL = "VOLLEYBALL"
    BADMINTON = "BADMINTON"


class ScoreAction(str, Enum):
    """Types of scoring actions"""
    ADD_RUN = "add_run"  # Cricket: +1, +2, +3, +4, +6
    WICKET = "wicket"  # Cricket: Player out
    GOAL = "goal"  # Football: Goal scored
    YELLOW_CARD = "yellow_card"  # Football: Yellow card
    RED_CARD = "red_card"  # Football: Red card
    FOUL = "foul"  # Football/Basketball: Foul
    POINT = "point"  # Basketball: +1, +2, +3
    FREE_THROW = "free_throw"  # Basketball: Free throw
    TIMEOUT = "timeout"  # Basketball: Timeout
    MOVE = "move"  # Chess: Move made
    CHECKMATE = "checkmate"  # Chess: Checkmate
    RESIGN = "resign"  # Chess: Resignation
    DRAW = "draw"  # Chess: Draw
    SET_POINT = "set_point"  # Volleyball/Badminton: Point in set
    SET_WON = "set_won"  # Volleyball/Badminton: Set won
    SERVICE_ERROR = "service_error"  # Volleyball/Badminton: Service error
    UNDO = "undo"  # Undo last action


def parse_additional_info(additional_info: Optional[str]) -> Dict[str, Any]:
    """Parse additional_info JSON string to dict"""
    if not additional_info:
        return {}
    try:
        return json.loads(additional_info)
    except (json.JSONDecodeError, TypeError):
        return {}


def serialize_additional_info(data: Dict[str, Any]) -> str:
    """Serialize dict to JSON string for additional_info"""
    return json.dumps(data)


def get_sport_code(sport_name: str) -> Optional[SportCode]:
    """Get sport code from sport name"""
    name_upper = sport_name.upper().strip()
    for code in SportCode:
        if code.value in name_upper or name_upper in code.value:
            return code
    return None


class CricketScoring:
    """Cricket scoring logic"""
    
    @staticmethod
    def get_default_score() -> Dict[str, Any]:
        return {
            "runs": 0,
            "wickets": 0,
            "overs": 0.0,
            "current_batters": [],
            "extras": 0
        }
    
    @staticmethod
    def add_run(current_data: Dict[str, Any], runs: int, team: str) -> Dict[str, Any]:
        """Add runs to team score"""
        team_key = f"{team}_runs"
        if team_key not in current_data:
            current_data[team_key] = 0
        current_data[team_key] += runs
        return current_data
    
    @staticmethod
    def add_wicket(current_data: Dict[str, Any], team: str, player_id: Optional[int] = None) -> Dict[str, Any]:
        """Add wicket to team"""
        team_key = f"{team}_wickets"
        if team_key not in current_data:
            current_data[team_key] = 0
        current_data[team_key] += 1
        
        # Remove player from current batters if specified
        batters_key = f"{team}_current_batters"
        if batters_key in current_data and player_id:
            if player_id in current_data[batters_key]:
                current_data[batters_key].remove(player_id)
        
        return current_data
    
    @staticmethod
    def get_score_display(current_data: Dict[str, Any], team: str) -> tuple[int, int]:
        """Get (runs, wickets) for display"""
        runs = current_data.get(f"{team}_runs", 0)
        wickets = current_data.get(f"{team}_wickets", 0)
        return runs, wickets


class FootballScoring:
    """Football scoring logic"""
    
    @staticmethod
    def get_default_score() -> Dict[str, Any]:
        return {
            "goals": 0,
            "yellow_cards": 0,
            "red_cards": 0,
            "fouls": 0,
            "corners": 0,
            "offsides": 0
        }
    
    @staticmethod
    def add_goal(current_data: Dict[str, Any], team: str, player_id: Optional[int] = None) -> Dict[str, Any]:
        """Add goal to team"""
        team_key = f"{team}_goals"
        if team_key not in current_data:
            current_data[team_key] = 0
        current_data[team_key] += 1
        return current_data
    
    @staticmethod
    def add_card(current_data: Dict[str, Any], team: str, card_type: str, player_id: Optional[int] = None) -> Dict[str, Any]:
        """Add yellow/red card"""
        team_key = f"{team}_{card_type}s"
        if team_key not in current_data:
            current_data[team_key] = 0
        current_data[team_key] += 1
        return current_data
    
    @staticmethod
    def add_foul(current_data: Dict[str, Any], team: str) -> Dict[str, Any]:
        """Add foul"""
        team_key = f"{team}_fouls"
        if team_key not in current_data:
            current_data[team_key] = 0
        current_data[team_key] += 1
        return current_data


class BasketballScoring:
    """Basketball scoring logic"""
    
    @staticmethod
    def get_default_score() -> Dict[str, Any]:
        return {
            "points": 0,
            "fouls": 0,
            "timeouts": 3,  # Default 3 timeouts per half
            "quarter": 1,
            "field_goals": 0,
            "free_throws": 0,
            "three_pointers": 0
        }
    
    @staticmethod
    def add_points(current_data: Dict[str, Any], team: str, points: int, point_type: str = "field_goal") -> Dict[str, Any]:
        """Add points to team"""
        team_key = f"{team}_points"
        if team_key not in current_data:
            current_data[team_key] = 0
        current_data[team_key] += points
        
        # Track point type
        type_key = f"{team}_{point_type}s"
        if type_key not in current_data:
            current_data[type_key] = 0
        current_data[type_key] += 1
        
        return current_data
    
    @staticmethod
    def add_foul(current_data: Dict[str, Any], team: str) -> Dict[str, Any]:
        """Add foul"""
        team_key = f"{team}_fouls"
        if team_key not in current_data:
            current_data[team_key] = 0
        current_data[team_key] += 1
        return current_data
    
    @staticmethod
    def use_timeout(current_data: Dict[str, Any], team: str) -> Dict[str, Any]:
        """Use timeout"""
        team_key = f"{team}_timeouts"
        if team_key not in current_data:
            current_data[team_key] = 3
        if current_data[team_key] > 0:
            current_data[team_key] -= 1
        return current_data


class ChessScoring:
    """Chess scoring logic"""
    
    @staticmethod
    def get_default_score() -> Dict[str, Any]:
        return {
            "moves": 0,
            "time_remaining_white": 1800,  # 30 minutes in seconds
            "time_remaining_black": 1800,
            "result": None,  # "white_win", "black_win", "draw"
            "game_status": "ongoing"  # "ongoing", "checkmate", "resigned", "draw"
        }
    
    @staticmethod
    def add_move(current_data: Dict[str, Any], player: str) -> Dict[str, Any]:
        """Record move"""
        current_data["moves"] = current_data.get("moves", 0) + 1
        return current_data
    
    @staticmethod
    def set_result(current_data: Dict[str, Any], result: str) -> Dict[str, Any]:
        """Set game result"""
        current_data["result"] = result
        current_data["game_status"] = result
        return current_data


class VolleyballScoring:
    """Volleyball scoring logic"""
    
    @staticmethod
    def get_default_score() -> Dict[str, Any]:
        return {
            "sets_won": 0,
            "current_set": 1,
            "set_scores": {},  # {1: {"home": 0, "away": 0}, ...}
            "service_errors": 0,
            "attack_errors": 0
        }
    
    @staticmethod
    def add_point(current_data: Dict[str, Any], team: str, set_num: Optional[int] = None) -> Dict[str, Any]:
        """Add point in current set"""
        if set_num is None:
            set_num = current_data.get("current_set", 1)
        
        set_key = f"set_{set_num}"
        if set_key not in current_data["set_scores"]:
            current_data["set_scores"][set_key] = {"home": 0, "away": 0}
        
        current_data["set_scores"][set_key][team] += 1
        
        # Check if set is won (first to 25 with 2-point lead, or 15 in 5th set)
        home_score = current_data["set_scores"][set_key]["home"]
        away_score = current_data["set_scores"][set_key]["away"]
        target = 15 if set_num == 5 else 25
        
        if (team == "home" and home_score >= target and home_score - away_score >= 2) or \
           (team == "away" and away_score >= target and away_score - home_score >= 2):
            # Set won
            team_key = f"{team}_sets_won"
            if team_key not in current_data:
                current_data[team_key] = 0
            current_data[team_key] += 1
            
            # Move to next set if not final set
            if set_num < 5:
                current_data["current_set"] = set_num + 1
        
        return current_data
    
    @staticmethod
    def get_sets_won(current_data: Dict[str, Any], team: str) -> int:
        """Get sets won by team"""
        return current_data.get(f"{team}_sets_won", 0)


class BadmintonScoring:
    """Badminton scoring logic"""
    
    @staticmethod
    def get_default_score() -> Dict[str, Any]:
        return {
            "sets_won": 0,
            "current_set": 1,
            "set_scores": {},  # {1: {"home": 0, "away": 0}, ...}
            "service_errors": 0
        }
    
    @staticmethod
    def add_point(current_data: Dict[str, Any], team: str, set_num: Optional[int] = None) -> Dict[str, Any]:
        """Add point in current set"""
        if set_num is None:
            set_num = current_data.get("current_set", 1)
        
        set_key = f"set_{set_num}"
        if set_key not in current_data["set_scores"]:
            current_data["set_scores"][set_key] = {"home": 0, "away": 0}
        
        current_data["set_scores"][set_key][team] += 1
        
        # Check if set is won (first to 21, or 30 if tied at 20-20)
        home_score = current_data["set_scores"][set_key]["home"]
        away_score = current_data["set_scores"][set_key]["away"]
        
        if (team == "home" and home_score >= 21 and home_score - away_score >= 2) or \
           (team == "away" and away_score >= 21 and away_score - home_score >= 2) or \
           (home_score >= 30 or away_score >= 30):
            # Set won
            team_key = f"{team}_sets_won"
            if team_key not in current_data:
                current_data[team_key] = 0
            current_data[team_key] += 1
            
            # Move to next set if not final set (best of 3)
            if set_num < 3:
                current_data["current_set"] = set_num + 1
        
        return current_data
    
    @staticmethod
    def get_sets_won(current_data: Dict[str, Any], team: str) -> int:
        """Get sets won by team"""
        return current_data.get(f"{team}_sets_won", 0)


def get_scoring_handler(sport_code: Optional[SportCode]):
    """Get the appropriate scoring handler for a sport"""
    handlers = {
        SportCode.CRICKET: CricketScoring,
        SportCode.FOOTBALL: FootballScoring,
        SportCode.BASKETBALL: BasketballScoring,
        SportCode.CHESS: ChessScoring,
        SportCode.VOLLEYBALL: VolleyballScoring,
        SportCode.BADMINTON: BadmintonScoring,
    }
    return handlers.get(sport_code) if sport_code else None
