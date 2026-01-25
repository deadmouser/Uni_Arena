# Uni Arena Backend

A FastAPI-based backend for managing sports tournaments and matches in institutions.

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL (via Supabase)
- **Authentication**: JWT (JSON Web Tokens)
- **ORM**: SQLAlchemy
- **Password Hashing**: bcrypt

## Features

- ✅ User authentication and authorization (JWT)
- ✅ Institution management
- ✅ Sport management
- ✅ Team and Player management
- ✅ Auto-generated match schedules (Round-Robin & Knockout)
- ✅ Live score updates
- ✅ Match management
- ✅ Score history tracking

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the backend directory:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/uni_arena
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
PROJECT_NAME=Uni Arena
API_V1_PREFIX=/api/v1
```

### 3. Database Setup

The database tables will be automatically created when you run the application for the first time (via `Base.metadata.create_all()` in `main.py`).

For production, consider using Alembic for migrations:

```bash
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### 4. Run the Application

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## API Endpoints

### Authentication (`/api/v1/auth`)

- `POST /register` - Register a new user
- `POST /login` - Login (OAuth2 form)
- `POST /login/json` - Login (JSON)
- `GET /me` - Get current user info

### Admin (`/api/v1/admin`)

- `POST /institutions` - Create institution
- `GET /institutions` - List institutions
- `GET /institutions/{id}` - Get institution
- `POST /users` - Create user
- `GET /users` - List users

### Organizer (`/api/v1/organizer`)

- `POST /sports` - Create sport
- `GET /sports` - List sports
- `POST /teams` - Create team
- `GET /teams` - List teams
- `POST /players` - Create player
- `GET /players` - List players

### Matches (`/api/v1/matches`)

- `POST /schedules` - Create schedule (auto-generates matches)
- `GET /schedules` - List schedules
- `GET /schedules/{id}` - Get schedule
- `POST /` - Create match manually
- `GET /` - List matches
- `GET /{id}` - Get match
- `PATCH /{id}` - Update match
- `POST /{id}/score` - Update match score (live)
- `GET /{id}/score` - Get current score
- `GET /{id}/score/history` - Get score history

## User Roles

- **admin**: Full system access
- **organizer**: Can manage sports, teams, matches for their institution
- **player**: Can view matches and scores
- **viewer**: Read-only access

## Schedule Types

### Round-Robin
Each team/player plays against every other team/player once.

### Knockout
Single-elimination tournament where winners advance to the next round.

## Database Models

- **User**: System users (admin, organizer, player, viewer)
- **Institution**: Educational institutions
- **Sport**: Sports types (individual, team, mixed)
- **Team**: Teams for team sports
- **Player**: Players (linked to users)
- **Match**: Individual matches
- **Schedule**: Tournament schedules
- **Score**: Current match scores
- **ScoreUpdate**: History of score updates

## Example Usage

### 1. Register a User

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "username": "admin",
    "password": "securepassword",
    "full_name": "Admin User",
    "role": "admin"
  }'
```

### 2. Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login/json" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "securepassword"
  }'
```

### 3. Create an Institution (Admin)

```bash
curl -X POST "http://localhost:8000/api/v1/admin/institutions" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "University of Example",
    "code": "UOE",
    "address": "123 Main St",
    "contact_email": "contact@uoe.edu"
  }'
```

### 4. Create a Sport (Organizer)

```bash
curl -X POST "http://localhost:8000/api/v1/organizer/sports" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Football",
    "code": "FOOTBALL",
    "sport_type": "team",
    "institution_id": 1,
    "max_players_per_team": 11,
    "min_players_per_team": 11
  }'
```

### 5. Create a Schedule (Auto-generates matches)

```bash
curl -X POST "http://localhost:8000/api/v1/matches/schedules" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Football Tournament 2024",
    "schedule_type": "round_robin",
    "sport_id": 1,
    "start_date": "2024-02-01T09:00:00Z",
    "team_ids": [1, 2, 3, 4]
  }'
```

### 6. Update Live Score

```bash
curl -X POST "http://localhost:8000/api/v1/matches/1/score" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "home_score": 2,
    "away_score": 1,
    "period": "2nd Half",
    "update_type": "goal",
    "description": "Goal by Player X"
  }'
```

## Development

### Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── config.py               # Configuration settings
├── database.py             # Database connection and session
├── dependencies.py         # FastAPI dependencies
├── models/                 # SQLAlchemy models
│   ├── auth.py
│   ├── institution.py
│   ├── sport.py
│   ├── team.py
│   ├── player.py
│   ├── match.py
│   ├── schedule.py
│   └── score.py
├── schemas/                # Pydantic schemas
│   ├── auth.py
│   ├── institution.py
│   ├── sport.py
│   ├── team.py
│   ├── player.py
│   ├── match.py
│   ├── schedule.py
│   └── score.py
├── routers/                # API route handlers
│   ├── auth.py
│   ├── admin.py
│   ├── organizer.py
│   └── matches.py
├── security/               # Security utilities
│   ├── auth_service.py
│   └── admin_service.py
└── services/               # Business logic
    └── scheduling_service.py
```

## Notes

- All timestamps are stored in UTC
- JWT tokens expire after 30 minutes (configurable)
- CORS is configured for local development
- Database tables are auto-created on first run (use migrations for production)
