export enum UserRole {
  ADMIN = 'admin',
  ORGANIZER = 'organizer',
  COACH = 'coach',
  PLAYER = 'player',
  VIEWER = 'viewer'
}

export interface User {
  id: number
  email: string
  username: string
  full_name: string | null
  role: UserRole
  is_active: boolean
  is_verified: boolean
  institution_id: number | null
  created_at: string
}

export interface Token {
  access_token: string
  token_type: string
  user: User
}

export interface Institution {
  id: number
  name: string
  code: string
  address: string | null
  contact_email: string | null
  contact_phone: string | null
  logo_url: string | null
  description: string | null
  is_active: boolean
  created_at: string
}

export interface Sport {
  id: number
  name: string
  code: string
  sport_type: 'individual' | 'team' | 'mixed'
  description: string | null
  max_players_per_team: number | null
  min_players_per_team: number | null
  institution_id: number
  organizer_id: number
  is_active: boolean
  created_at: string
}

export interface Team {
  id: number
  name: string
  code: string | null
  institution_id: number
  sport_id: number
  coach_id: number | null
  is_active: boolean
  created_at: string
}

export interface Player {
  id: number
  user_id: number
  team_id: number | null
  jersey_number: number | null
  position: string | null
  is_active: boolean
  date_of_birth: string | null
  created_at: string
}

export interface Match {
  id: number
  match_number: string | null
  scheduled_time: string
  actual_start_time: string | null
  actual_end_time: string | null
  status: 'scheduled' | 'live' | 'completed' | 'cancelled' | 'postponed'
  venue_name: string | null
  venue_id: number | null
  notes: string | null
  sport_id: number
  home_team_id: number | null
  away_team_id: number | null
  schedule_id: number | null
  created_by: number
  created_at: string
  // Optional relationships (may be included by backend)
  sport?: Sport
  home_team?: Team
  away_team?: Team
}

export interface Score {
  id: number
  match_id: number
  home_score: number
  away_score: number
  period: string | null
  additional_info: string | null
  created_at: string
  updated_at: string | null
}

export interface Tournament {
  id: number
  name: string
  description: string | null
  start_date: string
  end_date: string | null
  status: 'upcoming' | 'ongoing' | 'completed' | 'cancelled'
  is_public: boolean
  institution_id: number
  is_active: boolean
  created_at: string
}

export interface Venue {
  id: number
  name: string
  address: string | null
  capacity: number | null
  facilities: string | null
  institution_id: number
  is_active: boolean
  created_at: string
}

export interface Notification {
  id: number
  user_id: number
  title: string
  message: string
  notification_type: string
  is_read: boolean
  read_at: string | null
  link_url: string | null
  created_at: string
}

export interface Schedule {
  id: number
  name: string
  schedule_type: 'round_robin' | 'knockout' | 'league' | 'custom'
  start_date: string
  end_date: string | null
  description: string | null
  sport_id: number
  tournament_id: number | null
  is_active: boolean
  created_at: string
}
