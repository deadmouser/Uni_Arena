# Login Credentials

**⚠️ IMPORTANT: Registration is disabled. Only administrators can create accounts.**

After running the seed script (`python seed_data.py`), use these credentials to login:

## Quick Reference Table

| Role | Email | Password | Institution |
|------|-------|----------|-------------|
| **Admin** | `admin@uniarena.com` | `admin123` | N/A |
| **Organizer** | `organizer@use.edu` | `organizer123` | University of Sports Excellence |
| **Coach** | `coach@use.edu` | `coach123` | University of Sports Excellence |

---

## 🔐 Admin Account
- **Email:** `admin@uniarena.com`
- **Password:** `admin123`
- **Role:** Admin
- **Access:** 
  - Full system access
  - Create and manage institutions
  - Create users (organizers, coaches, players)
  - View all system data

## 🔐 Organizer Account
- **Email:** `organizer@use.edu`
- **Password:** `organizer123`
- **Role:** Organizer
- **Institution:** University of Sports Excellence (USE)
- **Access:** 
  - Manage institution profile and logo
  - Add sports, teams, players, coaches
  - Create and manage tournaments
  - Create venues and schedules
  - View all institution data

## 🔐 Coach Account
- **Email:** `coach@use.edu`
- **Password:** `coach123`
- **Role:** Coach
- **Institution:** University of Sports Excellence (USE)
- **Access:** 
  - Manage assigned teams
  - Create and manage line-ups
  - View team matches and schedules
  - Monitor team performance

## 🔐 Player Account (for testing)
- **Email:** `player1@use.edu`
- **Password:** `player123`
- **Role:** Player
- **Team:** USE Lions (Football)
- **Access:** View profile, matches, statistics, join teams

## 📊 Sample Data Created

The seed script creates:

- **2 Institutions:**
  - University of Sports Excellence (USE)
  - Athletic Academy (AA)

- **4 Sports:**
  - Football (Team sport, 11 players)
  - Basketball (Team sport, 5 players)
  - Tennis (Individual)
  - Badminton (Mixed)

- **3 Teams:**
  - USE Lions (Football)
  - AA Eagles (Football)
  - USE Warriors (Basketball)

- **5 Players:**
  - player1@use.edu - Forward (Jersey #10)
  - player2@use.edu - Midfielder (Jersey #7)
  - player3@use.edu - Defender (Jersey #4)
  - player4@athletic.edu - Goalkeeper (Jersey #1)
  - player5@athletic.edu - Midfielder (Jersey #8)

- **2 Venues:**
  - Main Stadium (Capacity: 10,000)
  - Basketball Court (Capacity: 5,000)

- **1 Tournament:**
  - Inter-University Sports Championship 2024

- **1 Schedule:**
  - Football League 2024 (Round-Robin)

- **5 Matches:**
  - 1 Live match (with score: 2-1)
  - 1 Completed match (final score: 3-1)
  - 3 Scheduled matches

## 🚀 How to Run Seed Script

```bash
cd backend
python seed_data.py
```

The script will:
1. Create all database tables (if they don't exist)
2. Insert sample data
3. Display login credentials at the end

## ⚠️ Note

If you run the script multiple times, you may get errors about duplicate entries. To reset:
1. Delete the database file: `uni_arena.db` (for SQLite)
2. Run the seed script again
