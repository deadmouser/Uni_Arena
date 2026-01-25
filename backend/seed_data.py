"""
Script to seed the database with sample data
Run this script to populate the database with test data
"""
import sys
import io
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models.auth import User, UserRole
from models.institution import Institution
from models.sport import Sport, SportType
from models.team import Team
from models.player import Player
from models.venue import Venue
from models.tournament import Tournament, TournamentStatus
from models.schedule import Schedule, ScheduleType
from models.match import Match, MatchStatus
from models.score import Score
from security.auth_service import get_password_hash
from datetime import datetime, timedelta

# Set UTF-8 encoding for Windows compatibility
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Create all tables
Base.metadata.create_all(bind=engine)

# Force output to be unbuffered
sys.stdout.reconfigure(line_buffering=True) if hasattr(sys.stdout, 'reconfigure') else None

def seed_data():
    db: Session = SessionLocal()
    
    try:
        print("🌱 Starting database seeding...")
        
        # 1. Create Institutions (check if they exist first)
        print("📚 Creating institutions...")
        inst1 = db.query(Institution).filter(Institution.name == "University of Sports Excellence").first()
        if not inst1:
            inst1 = Institution(
                name="University of Sports Excellence",
                code="USE",
                address="123 Sports Avenue, City",
                contact_email="contact@use.edu",
                contact_phone="+1234567890",
                description="Premier sports university",
                logo_url="https://via.placeholder.com/150"
            )
            db.add(inst1)
            db.flush()
            print(f"✅ Created institution: {inst1.name}")
        else:
            print(f"ℹ️  Institution already exists: {inst1.name}")
        
        inst2 = db.query(Institution).filter(Institution.name == "Athletic Academy").first()
        if not inst2:
            inst2 = Institution(
                name="Athletic Academy",
                code="AA",
                address="456 Champions Road, City",
                contact_email="info@athletic.edu",
                contact_phone="+1234567891",
                description="Elite athletic training institution"
            )
            db.add(inst2)
            db.flush()
            print(f"✅ Created institution: {inst2.name}")
        else:
            print(f"ℹ️  Institution already exists: {inst2.name}")
        
        # 2. Create Users (Admin, Organizer, Coach, Players)
        print("👥 Creating users...")
        
        # Admin
        admin = db.query(User).filter(User.email == "admin@uniarena.com").first()
        if not admin:
            admin = User(
                email="admin@uniarena.com",
                username="admin",
                full_name="System Administrator",
                hashed_password=get_password_hash("admin123"),
                role=UserRole.ADMIN,
                is_active=True,
                is_verified=True
            )
            db.add(admin)
            db.flush()
            print(f"✅ Created Admin - Email: admin@uniarena.com, Password: admin123")
        else:
            print(f"ℹ️  Admin already exists")
        
        # Organizer 1
        organizer1 = db.query(User).filter(User.email == "organizer@use.edu").first()
        if not organizer1:
            organizer1 = User(
                email="organizer@use.edu",
                username="organizer1",
                full_name="John Organizer",
                hashed_password=get_password_hash("organizer123"),
                role=UserRole.ORGANIZER,
                institution_id=inst1.id,
                is_active=True,
                is_verified=True
            )
            db.add(organizer1)
            db.flush()
            print(f"✅ Created Organizer - Email: organizer@use.edu, Password: organizer123")
        else:
            print(f"ℹ️  Organizer 1 already exists")
        
        # Organizer 2
        organizer2 = db.query(User).filter(User.email == "organizer2@athletic.edu").first()
        if not organizer2:
            organizer2 = User(
                email="organizer2@athletic.edu",
                username="organizer2",
                full_name="Jane Manager",
                hashed_password=get_password_hash("organizer123"),
                role=UserRole.ORGANIZER,
                institution_id=inst2.id,
                is_active=True,
                is_verified=True
            )
            db.add(organizer2)
            db.flush()
        else:
            print(f"ℹ️  Organizer 2 already exists")
        
        # Coach 1
        coach1 = db.query(User).filter(User.email == "coach@use.edu").first()
        if not coach1:
            coach1 = User(
                email="coach@use.edu",
                username="coach1",
                full_name="Mike Coach",
                hashed_password=get_password_hash("coach123"),
                role=UserRole.COACH,
                institution_id=inst1.id,
                is_active=True,
                is_verified=True
            )
            db.add(coach1)
            db.flush()
            print(f"✅ Created Coach - Email: coach@use.edu, Password: coach123")
        else:
            print(f"ℹ️  Coach 1 already exists")
        
        # Coach 2
        coach2 = db.query(User).filter(User.email == "coach2@athletic.edu").first()
        if not coach2:
            coach2 = User(
                email="coach2@athletic.edu",
                username="coach2",
                full_name="Sarah Trainer",
                hashed_password=get_password_hash("coach123"),
                role=UserRole.COACH,
                institution_id=inst2.id,
                is_active=True,
                is_verified=True
            )
            db.add(coach2)
            db.flush()
        else:
            print(f"ℹ️  Coach 2 already exists")
        
        # Players
        players_data = [
            {"email": "player1@use.edu", "username": "player1", "name": "Alex Player", "jersey": 10},
            {"email": "player2@use.edu", "username": "player2", "name": "Bob Striker", "jersey": 7},
            {"email": "player3@use.edu", "username": "player3", "name": "Charlie Defender", "jersey": 4},
            {"email": "player4@athletic.edu", "username": "player4", "name": "David Goalkeeper", "jersey": 1},
            {"email": "player5@athletic.edu", "username": "player5", "name": "Eve Midfielder", "jersey": 8},
        ]
        
        players = []
        for p_data in players_data:
            player_user = db.query(User).filter(User.email == p_data["email"]).first()
            if not player_user:
                player_user = User(
                    email=p_data["email"],
                    username=p_data["username"],
                    full_name=p_data["name"],
                    hashed_password=get_password_hash("player123"),
                    role=UserRole.PLAYER,
                    institution_id=inst1.id if "use.edu" in p_data["email"] else inst2.id,
                    is_active=True,
                    is_verified=True
                )
                db.add(player_user)
                db.flush()
            players.append(player_user)
        
        print(f"✅ Processed {len(players)} players")
        
        # 3. Create Sports
        print("⚽ Creating sports...")
        sports_data = [
            {"name": "Football", "code": "FOOTBALL", "type": SportType.TEAM, "min": 11, "max": 11},
            {"name": "Basketball", "code": "BASKETBALL", "type": SportType.TEAM, "min": 5, "max": 5},
            {"name": "Tennis", "code": "TENNIS", "type": SportType.INDIVIDUAL, "min": 1, "max": 1},
            {"name": "Badminton", "code": "BADMINTON", "type": SportType.MIXED, "min": 1, "max": 2},
        ]
        
        sports = []
        for s_data in sports_data:
            sport = db.query(Sport).filter(
                Sport.code == s_data["code"],
                Sport.institution_id == inst1.id
            ).first()
            if not sport:
                sport = Sport(
                    name=s_data["name"],
                    code=s_data["code"],
                    sport_type=s_data["type"],
                    min_players_per_team=s_data["min"],
                    max_players_per_team=s_data["max"],
                    institution_id=inst1.id,
                    organizer_id=organizer1.id,
                    description=f"{s_data['name']} sport"
                )
                db.add(sport)
                db.flush()
            sports.append(sport)
        
        print(f"✅ Processed {len(sports)} sports")
        
        # 4. Create Teams
        print("👥 Creating teams...")
        football = next(s for s in sports if s.code == "FOOTBALL")
        basketball = next(s for s in sports if s.code == "BASKETBALL")
        
        team1 = db.query(Team).filter(Team.code == "USE-L").first()
        if not team1:
            team1 = Team(
                name="USE Lions",
                code="USE-L",
                institution_id=inst1.id,
                sport_id=football.id,
                coach_id=coach1.id
            )
            db.add(team1)
            db.flush()
        
        team2 = db.query(Team).filter(Team.code == "AA-E").first()
        if not team2:
            team2 = Team(
                name="AA Eagles",
                code="AA-E",
                institution_id=inst2.id,
                sport_id=football.id,
                coach_id=coach2.id
            )
            db.add(team2)
            db.flush()
        
        team3 = db.query(Team).filter(Team.code == "USE-W").first()
        if not team3:
            team3 = Team(
                name="USE Warriors",
                code="USE-W",
                institution_id=inst1.id,
                sport_id=basketball.id,
                coach_id=coach1.id
            )
            db.add(team3)
            db.flush()
        
        print(f"✅ Processed 3 teams")
        
        # 5. Create Players (link users to teams)
        print("🏃 Creating player profiles...")
        player_profiles = []
        for i, player_user in enumerate(players[:3]):  # First 3 players for team1
            player = db.query(Player).filter(Player.user_id == player_user.id).first()
            if not player:
                player = Player(
                    user_id=player_user.id,
                    team_id=team1.id,
                    jersey_number=players_data[i]["jersey"],
                    position=["Forward", "Midfielder", "Defender"][i]
                )
                db.add(player)
                player_profiles.append(player)
            else:
                player_profiles.append(player)
        
        for i, player_user in enumerate(players[3:], 3):  # Last 2 players for team2
            player = db.query(Player).filter(Player.user_id == player_user.id).first()
            if not player:
                player = Player(
                    user_id=player_user.id,
                    team_id=team2.id,
                    jersey_number=players_data[i]["jersey"],
                    position=["Goalkeeper", "Midfielder"][i-3]
                )
                db.add(player)
                player_profiles.append(player)
            else:
                player_profiles.append(player)
        
        db.flush()
        print(f"✅ Processed {len(player_profiles)} player profiles")
        
        # 6. Create Venues
        print("🏟️ Creating venues...")
        venue1 = db.query(Venue).filter(
            Venue.name == "Main Stadium",
            Venue.institution_id == inst1.id
        ).first()
        if not venue1:
            venue1 = Venue(
                name="Main Stadium",
                address="123 Sports Avenue, City",
                capacity=10000,
                facilities="Parking, Food Court, Restrooms",
                institution_id=inst1.id
            )
            db.add(venue1)
            db.flush()
        
        venue2 = db.query(Venue).filter(
            Venue.name == "Basketball Court",
            Venue.institution_id == inst2.id
        ).first()
        if not venue2:
            venue2 = Venue(
                name="Basketball Court",
                address="456 Champions Road, City",
                capacity=5000,
                facilities="Parking, Concessions",
                institution_id=inst2.id
            )
            db.add(venue2)
            db.flush()
        
        print(f"✅ Processed 2 venues")
        
        # 7. Create Tournament
        print("🏆 Creating tournament...")
        tournament = db.query(Tournament).filter(
            Tournament.name == "Inter-University Sports Championship 2024"
        ).first()
        if not tournament:
            tournament = Tournament(
                name="Inter-University Sports Championship 2024",
                description="Annual championship between universities",
                start_date=datetime.utcnow() + timedelta(days=1),
                end_date=datetime.utcnow() + timedelta(days=30),
                status=TournamentStatus.UPCOMING,
                is_public=True,
                institution_id=inst1.id
            )
            db.add(tournament)
            db.flush()
            print(f"✅ Created tournament: {tournament.name}")
        else:
            print(f"ℹ️  Tournament already exists: {tournament.name}")
        
        # 8. Create Schedule
        print("📅 Creating schedule...")
        schedule = db.query(Schedule).filter(
            Schedule.name == "Football League 2024"
        ).first()
        if not schedule:
            schedule = Schedule(
                name="Football League 2024",
                schedule_type=ScheduleType.ROUND_ROBIN,
                start_date=datetime.utcnow() + timedelta(days=1),
                end_date=datetime.utcnow() + timedelta(days=15),
                description="Round-robin tournament for football teams",
                sport_id=football.id,
                tournament_id=tournament.id
            )
            db.add(schedule)
            db.flush()
            print(f"✅ Created schedule: {schedule.name}")
        else:
            print(f"ℹ️  Schedule already exists: {schedule.name}")
        
        # 9. Create Matches
        print("⚽ Creating matches...")
        matches = []
        match_times = [
            datetime.utcnow() + timedelta(days=1, hours=10),
            datetime.utcnow() + timedelta(days=2, hours=14),
            datetime.utcnow() + timedelta(days=3, hours=16),
            datetime.utcnow() + timedelta(days=1, hours=18),  # Live match
        ]
        
        for i, match_time in enumerate(match_times):
            match_number = f"M{i+1:03d}"
            match = db.query(Match).filter(Match.match_number == match_number).first()
            if not match:
                status = MatchStatus.LIVE if i == 3 else MatchStatus.SCHEDULED
                match = Match(
                    match_number=match_number,
                    scheduled_time=match_time,
                    status=status,
                    venue_id=venue1.id if i < 2 else venue2.id,
                    sport_id=football.id,
                    home_team_id=team1.id,
                    away_team_id=team2.id,
                    schedule_id=schedule.id,
                    created_by=organizer1.id,
                    notes=f"Match {i+1} of the tournament"
                )
                db.add(match)
            matches.append(match)
        
        db.flush()
        print(f"✅ Processed {len(matches)} matches")
        
        # 10. Create Scores (for live match)
        print("📊 Creating scores...")
        live_match = matches[3]  # The live match
        score = db.query(Score).filter(Score.match_id == live_match.id).first()
        if not score:
            score = Score(
                match_id=live_match.id,
                home_score=2,
                away_score=1,
                period="2nd Half",
                additional_info='{"goals": [{"minute": 15, "scorer": "Alex Player"}, {"minute": 45, "scorer": "Bob Striker"}]}'
            )
            db.add(score)
        
        # Add a completed match with final score
        completed_match = db.query(Match).filter(Match.match_number == "M005").first()
        if not completed_match:
            completed_match = Match(
                match_number="M005",
                scheduled_time=datetime.utcnow() - timedelta(days=1),
                actual_start_time=datetime.utcnow() - timedelta(days=1, hours=2),
                actual_end_time=datetime.utcnow() - timedelta(days=1),
                status=MatchStatus.COMPLETED,
                venue_id=venue1.id,
                sport_id=football.id,
                home_team_id=team1.id,
                away_team_id=team2.id,
                schedule_id=schedule.id,
                created_by=organizer1.id
            )
            db.add(completed_match)
            db.flush()
        
        completed_score = db.query(Score).filter(Score.match_id == completed_match.id).first()
        if not completed_score:
            completed_score = Score(
                match_id=completed_match.id,
                home_score=3,
                away_score=1,
                period="Full Time"
            )
            db.add(completed_score)
        
        print(f"✅ Processed scores for matches")
        
        # Commit all changes
        db.commit()
        print("\n🎉 Database seeding completed successfully!")
        print("\n" + "="*60)
        print("📋 LOGIN CREDENTIALS")
        print("="*60)
        print("\n🔐 ADMIN:")
        print("   Email: admin@uniarena.com")
        print("   Password: admin123")
        print("\n🔐 ORGANIZER:")
        print("   Email: organizer@use.edu")
        print("   Password: organizer123")
        print("\n🔐 COACH:")
        print("   Email: coach@use.edu")
        print("   Password: coach123")
        print("\n🔐 PLAYER (for testing):")
        print("   Email: player1@use.edu")
        print("   Password: player123")
        print("\n" + "="*60)
        print("\n✅ Sample data includes:")
        print("   - 2 Institutions")
        print("   - Multiple users (Admin, Organizers, Coaches, Players)")
        print("   - 4 Sports (Football, Basketball, Tennis, Badminton)")
        print("   - 3 Teams")
        print("   - 5 Players")
        print("   - 2 Venues")
        print("   - 1 Tournament")
        print("   - 1 Schedule")
        print("   - 5 Matches (1 Live, 1 Completed, 3 Scheduled)")
        print("   - Scores for live and completed matches")
        print("\n")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
