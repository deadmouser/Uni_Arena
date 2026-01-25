from typing import Dict, Any, List

class SportTemplate:
    def __init__(self, code: str, name: str, type: str, min_players: int, max_players: int, rules: List[str], mandatory_rules: List[str], match_config: Dict[str, Any]):
        self.code = code
        self.name = name
        self.type = type
        self.min_players = min_players
        self.max_players = max_players
        self.rules = rules
        self.mandatory_rules = mandatory_rules
        self.match_config = match_config

    def to_dict(self):
        return {
            "name": self.name,
            "code": self.code,
            "sport_type": self.type,
            "min_players_per_team": self.min_players,
            "max_players_per_team": self.max_players,
            "description": f"Standard {self.name} configuration",
            "rules": self.rules,
            "mandatory_rules": self.mandatory_rules,
            "match_config": self.match_config
        }

TEMPLATES = {
    "FOOTBALL": SportTemplate(
        code="FOOTBALL",
        name="Football",
        type="team",
        min_players=11,
        max_players=11,
        rules=[
            "Game duration is 90 minutes (two 45-minute halves)",
            "Each team must have 11 players including 1 goalkeeper",
            "Maximum of 3 substitutions allowed per match",
            "Yellow card warning, Red card sending off",
            "Offside rule applies"
        ],
        mandatory_rules=[
            "Game duration is 90 minutes (two 45-minute halves)",
            "Offside rule applies"
        ],
        match_config={
            "periods": 2,
            "period_length": 45,
            "period_type": "half",
            "scoring_type": "goals"
        }
    ),
    "CRICKET": SportTemplate(
        code="CRICKET",
        name="Cricket",
        type="team",
        min_players=11,
        max_players=11,
        rules=[
            "T20 Format: 20 overs per innings",
            "Each bowler can bowl maximum 4 overs",
            "Powerplay for first 6 overs",
            "No ball results in Free Hit",
            "Wide ball adds 1 run and extra ball"
        ],
        mandatory_rules=[
            "Each team plays 20 overs (T20 format)",
            "Wide ball adds 1 run"
        ],
        match_config={
            "periods": 2,
            "period_length": 20,
            "period_type": "innings",
            "scoring_type": "runs/wickets"
        }
    ),
    "BASKETBALL": SportTemplate(
        code="BASKETBALL",
        name="Basketball",
        type="team",
        min_players=5,
        max_players=5,
        rules=[
            "Game duration: 4 quarters of 10 minutes",
            "24-second shot clock",
            "5 fouls per player limit",
            "3 points for shots outside arc",
            "8-second backcourt violation"
        ],
        mandatory_rules=[
            "5 players on court per team",
            "24-second shot clock"
        ],
        match_config={
            "periods": 4,
            "period_length": 10,
            "period_type": "quarter",
            "scoring_type": "points"
        }
    ),
    "BADMINTON": SportTemplate(
        code="BADMINTON",
        name="Badminton",
        type="mixed",
        min_players=1,
        max_players=2,
        rules=[
            "Standard scoring system (21 points x 3 sets)",
            "Service fault rules apply",
            "Change ends after each game",
            "Interval at 11 points"
        ],
        mandatory_rules=[
            "Winner of rally scores point",
            "Match is best of 3 games"
        ],
        match_config={
            "periods": 3,
            "period_length": 21,
            "period_type": "set",
            "scoring_type": "points"
        }
    ),
    "VOLLEYBALL": SportTemplate(
        code="VOLLEYBALL",
        name="Volleyball",
        type="team",
        min_players=6,
        max_players=6,
        rules=[
            "Best of 5 sets (first 4 to 25, 5th to 15)",
            "Maximum 3 touches per side",
            "Rotational order must be maintained",
            "Libero replacement rules",
            "Net contact is a fault"
        ],
        mandatory_rules=[
            "Maximum 3 touches per side",
            "Rotation rules apply"
        ],
        match_config={
            "periods": 5,
            "period_length": 25,
            "period_type": "set",
            "scoring_type": "points"
        }
    ),
    "CHESS": SportTemplate(
        code="CHESS",
        name="Chess",
        type="individual",
        min_players=1,
        max_players=1,
        rules=[
            "Standard time control: 10 mins + 5 sec increment",
            "Touch-move rule applies",
            "Illegal move loses the game",
            "Flag fall loses the game"
        ],
        mandatory_rules=[
            "Touch-move rule applies",
            "Checkmate ends game"
        ],
        match_config={
            "periods": 1,
            "period_length": 0,
            "period_type": "game",
            "scoring_type": "points"
        }
    )
}

def get_template(code: str) -> Dict[str, Any]:
    return TEMPLATES.get(code.upper()).to_dict() if code.upper() in TEMPLATES else None

def get_all_templates() -> List[Dict[str, Any]]:
    return [t.to_dict() for t in TEMPLATES.values()]
