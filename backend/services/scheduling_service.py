from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from models.sport import Sport, SportType
from models.team import Team
from models.player import Player
from models.match import Match, MatchStatus, MatchParticipation
from models.schedule import Schedule, ScheduleType
from datetime import time


def generate_round_robin_schedule(
    db: Session,
    schedule: Schedule,
    team_ids: Optional[List[int]] = None,
    player_ids: Optional[List[int]] = None,
    matches_per_day: int = 4,
    start_time: time = time(9, 0),  # 9 AM default
    match_duration_minutes: int = 90
) -> List[Match]:
    """
    Generate round-robin schedule for teams or players.
    Each team/player plays against every other team/player once.
    """
    matches = []
    sport = db.query(Sport).filter(Sport.id == schedule.sport_id).first()
    if not sport:
        return matches
    
    participants = []
    
    if sport.sport_type == SportType.TEAM:
        if not team_ids:
            teams = db.query(Team).filter(Team.sport_id == sport.id).all()
            team_ids = [team.id for team in teams]
        participants = team_ids
    else:  # INDIVIDUAL or MIXED
        if not player_ids:
            players = db.query(Player).join(Team).filter(Team.sport_id == sport.id).all()
            player_ids = [player.id for player in players]
        participants = player_ids
    
    if len(participants) < 2:
        return matches
    
    # Generate all possible matchups
    matchups = []
    for i in range(len(participants)):
        for j in range(i + 1, len(participants)):
            matchups.append((participants[i], participants[j]))
    
    # Schedule matches across days
    current_date = schedule.start_date.date()
    matches_today = 0
    match_number = 1
    
    for home_id, away_id in matchups:
        # Calculate match time
        match_time = datetime.combine(current_date, start_time)
        match_time += timedelta(minutes=matches_today * match_duration_minutes)
        
        # Create match
        match_data = {
            "match_number": f"M{match_number:03d}",
            "scheduled_time": match_time,
            "status": MatchStatus.SCHEDULED,
            "sport_id": sport.id,
            "schedule_id": schedule.id,
            "created_by": sport.organizer_id
        }
        
        if sport.sport_type == SportType.TEAM:
            match_data["home_team_id"] = home_id
            match_data["away_team_id"] = away_id
        
        db_match = Match(**match_data)
        db.add(db_match)
        db.flush()  # Flush to get the match ID
        
        # For individual sports, create participations
        if sport.sport_type != SportType.TEAM:
            db.add(MatchParticipation(match_id=db_match.id, player_id=home_id, is_home=True))
            db.add(MatchParticipation(match_id=db_match.id, player_id=away_id, is_home=False))
        
        matches.append(db_match)
        match_number += 1
        matches_today += 1
        
        # Move to next day if we've reached matches_per_day
        if matches_today >= matches_per_day:
            matches_today = 0
            current_date += timedelta(days=1)
            # Update start_date if needed
            if current_date > schedule.start_date.date():
                schedule.start_date = datetime.combine(current_date, start_time)
    
    return matches


def generate_knockout_schedule(
    db: Session,
    schedule: Schedule,
    team_ids: Optional[List[int]] = None,
    player_ids: Optional[List[int]] = None,
    matches_per_day: int = 4,
    start_time: time = time(9, 0),
    match_duration_minutes: int = 90
) -> List[Match]:
    """
    Generate knockout tournament schedule.
    Teams/players are paired and winners advance.
    """
    matches = []
    sport = db.query(Sport).filter(Sport.id == schedule.sport_id).first()
    if not sport:
        return matches
    
    participants = []
    
    if sport.sport_type == SportType.TEAM:
        if not team_ids:
            teams = db.query(Team).filter(Team.sport_id == sport.id).all()
            team_ids = [team.id for team in teams]
        participants = team_ids
    else:
        if not player_ids:
            players = db.query(Player).join(Team).filter(Team.sport_id == sport.id).all()
            player_ids = [player.id for player in players]
        participants = player_ids
    
    if len(participants) < 2:
        return matches
    
    # Ensure number of participants is power of 2 (add byes if needed)
    import math
    next_power_of_2 = 2 ** math.ceil(math.log2(len(participants)))
    byes = next_power_of_2 - len(participants)
    
    # Round names
    round_names = ["Final", "Semi-Final", "Quarter-Final"]
    round_index = 0
    
    current_participants = participants.copy()
    current_date = schedule.start_date.date()
    matches_today = 0
    match_number = 1
    
    while len(current_participants) > 1:
        round_name = round_names[round_index] if round_index < len(round_names) else f"Round {round_index + 1}"
        next_round_participants = []
        
        # Pair participants
        for i in range(0, len(current_participants), 2):
            if i + 1 < len(current_participants):
                home_id = current_participants[i]
                away_id = current_participants[i + 1]
                
                # Calculate match time
                match_time = datetime.combine(current_date, start_time)
                match_time += timedelta(minutes=matches_today * match_duration_minutes)
                
                match_data = {
                    "match_number": f"{round_name}-{match_number}",
                    "scheduled_time": match_time,
                    "status": MatchStatus.SCHEDULED,
                    "sport_id": sport.id,
                    "schedule_id": schedule.id,
                    "created_by": sport.organizer_id
                }
                
                if sport.sport_type == SportType.TEAM:
                    match_data["home_team_id"] = home_id
                    match_data["away_team_id"] = away_id
                
                db_match = Match(**match_data)
                db.add(db_match)
                db.flush()
                
                if sport.sport_type != SportType.TEAM:
                    db.add(MatchParticipation(match_id=db_match.id, player_id=home_id, is_home=True))
                    db.add(MatchParticipation(match_id=db_match.id, player_id=away_id, is_home=False))
                
                matches.append(db_match)
                match_number += 1
                matches_today += 1
                
                # For now, winner is placeholder (will be updated when match completes)
                next_round_participants.append(home_id)  # Placeholder
                
                if matches_today >= matches_per_day:
                    matches_today = 0
                    current_date += timedelta(days=1)
            else:
                # Bye - participant advances automatically
                next_round_participants.append(current_participants[i])
        
        current_participants = next_round_participants
        round_index += 1
    
    return matches
