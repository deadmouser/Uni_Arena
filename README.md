# Uni_Arena 🏟️

**Uni Arena** is a comprehensive sports management system designed for educational institutions to manage tournaments, teams, players, matches, and scores. It provides role-based dashboards for administrators, organizers, coaches, players, and viewers.

## 🚀 Key Features

- **Multi-Institution Support**: Manage multiple institutions within a single platform.
- **Tournament Management**: Create and manage tournaments with multiple sports.
- **Team & Player Management**: Organize teams and track player statistics.
- **Match Scheduling**: Schedule and track matches with real-time score updates.
- **Role-Based Access Control**: Dedicated dashboards for Admins, Organizers, Coaches, Players, and Viewers.
- **Real-time Updates**: Live match scores and notifications via Supabase Realtime.
- **Analytics**: Detailed statistics and activity trends.

## 🛠️ Technology Stack

### Frontend
- **Framework**: Vue.js 3 + TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **State Management**: Pinia
- **HTTP Client**: Axios

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL (via Supabase)
- **ORM**: SQLAlchemy
- **Authentication**: JWT + Supabase Auth
- **Validation**: Pydantic

## 📋 Prerequisites

- **Node.js**: v18+
- **Python**: v3.10+
- **Supabase Account**: For database and authentication

## ⚡ Setup & Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Uni_Arena
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Copy .env.example to .env and configure your Supabase credentials
cp .env.example .env
```

### 3. Frontend Setup
```bash
cd ../frontend

# Install dependencies
npm install
```

## 🏃‍♂️ Running the Application

### Start the Backend Server
```bash
# In the backend directory
uvicorn main:app --reload
```
The API will be available at `http://localhost:8000`.
API Documentation (Swagger UI): `http://localhost:8000/docs`

### Start the Frontend Development Server
```bash
# In the frontend directory
npm run dev
```
The application will be accessible at `http://localhost:5173`.

## 👥 User Roles

- **Admin**: System-wide administration.
- **Organizer**: Manages tournaments, sports, and venues.
- **Coach**: Manages team rosters and strategies.
- **Player**: Views profile, stats, and upcoming matches.
- **Viewer**: Public access to match schedules and scores.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
