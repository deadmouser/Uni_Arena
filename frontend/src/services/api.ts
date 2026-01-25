import axios, { AxiosInstance, AxiosError } from 'axios'
import type { User, Institution, Player, Match, Score, Tournament, Venue, Notification, Schedule } from '@/types'

// Use absolute path in development (via Vite proxy) or absolute URL from env
const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1'

class ApiService {
  private api: AxiosInstance

  constructor() {
    this.api = axios.create({
      baseURL: API_BASE_URL,
      timeout: 10000, // 10 second timeout
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // Request interceptor to add auth token
    this.api.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('access_token')
        if (token) {
          config.headers.Authorization = `Bearer ${token}`
        }
        return config
      },
      (error) => Promise.reject(error)
    )

    // Response interceptor to handle errors
    this.api.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        // Only redirect to login for 401 errors on protected routes
        // Don't redirect for public endpoints like /matches
        if (error.response?.status === 401 && error.config?.url?.includes('/auth/me')) {
          localStorage.removeItem('access_token')
          localStorage.removeItem('user')
          window.location.href = '/login'
        }
        return Promise.reject(error)
      }
    )
  }

  async getUsers(): Promise<User[]> {
    const response = await this.api.get<User[]>('/admin/users')
    return response.data
  }

  async createUser(data: Partial<User>): Promise<User> {
    const response = await this.api.post<User>('/admin/users', data)
    return response.data
  }

  async updateUser(userId: number, data: Partial<User>): Promise<User> {
    const response = await this.api.patch<User>(`/admin/users/${userId}`, data)
    return response.data
  }

  async deleteUser(userId: number): Promise<void> {
    await this.api.delete(`/admin/users/${userId}`)
  }

  async getCurrentUser(): Promise<User> {
    const response = await this.api.get<User>('/auth/me')
    return response.data
  }

  // Admin endpoints
  async createInstitution(data: Partial<Institution> | FormData): Promise<Institution> {
    // If data is FormData, let the browser set the Content-Type
    if (data instanceof FormData) {
      const response = await this.api.post<Institution>('/admin/institutions', data, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      return response.data
    }
    const response = await this.api.post<Institution>('/admin/institutions', data)
    return response.data
  }

  async getInstitutions(): Promise<Institution[]> {
    const response = await this.api.get<Institution[]>('/admin/institutions')
    return response.data
  }

  async getInstitution(institutionId: number): Promise<Institution> {
    const response = await this.api.get<Institution>(`/admin/institutions/${institutionId}`)
    return response.data
  }

  async deleteInstitution(institutionId: number): Promise<void> {
    await this.api.delete(`/admin/institutions/${institutionId}`)
  }

  async updateInstitution(institutionId: number, data: Partial<Institution>): Promise<Institution> {
    const response = await this.api.patch<Institution>(`/admin/institutions/${institutionId}`, data)
    return response.data
  }

  // Venue endpoints
  async createVenue(data: Partial<Venue>): Promise<Venue> {
    const response = await this.api.post<Venue>('/venues', data)
    return response.data
  }

  async getVenues(institutionId?: number): Promise<Venue[]> {
    const params = institutionId ? { institution_id: institutionId } : {}
    const response = await this.api.get<Venue[]>('/venues', { params })
    return response.data
  }

  // Organizer endpoints
  async getMyInstitution(): Promise<Institution> {
    const response = await this.api.get<Institution>('/organizer/institution')
    return response.data
  }

  async updateMyInstitution(data: Partial<Institution>): Promise<Institution> {
    const response = await this.api.patch<Institution>('/organizer/institution', data)
    return response.data
  }

  async getSports(institutionId?: number): Promise<any[]> {
    const params = institutionId ? { institution_id: institutionId } : {}
    const response = await this.api.get<any[]>('/organizer/sports', { params })
    return response.data
  }

  async createSport(data: any): Promise<any> {
    const response = await this.api.post<any>('/organizer/sports', data)
    return response.data
  }

  async getSportTemplates(): Promise<any[]> {
    const response = await this.api.get<any[]>('/organizer/sports/templates')
    return response.data
  }

  async getTeams(sportId?: number, institutionId?: number): Promise<any[]> {
    const params: any = {}
    if (sportId) params.sport_id = sportId
    if (institutionId) params.institution_id = institutionId
    const response = await this.api.get<any[]>('/organizer/teams', { params })
    return response.data
  }

  async getPlayers(teamId?: number): Promise<Player[]> {
    const params: any = {}
    if (teamId) params.team_id = teamId
    const response = await this.api.get<Player[]>('/organizer/players', { params })
    return response.data
  }

  async createPlayer(data: any): Promise<Player> {
    const response = await this.api.post<Player>('/organizer/players', data)
    return response.data
  }

  // Tournament endpoints
  async createTournament(data: Partial<Tournament>): Promise<Tournament> {
    const response = await this.api.post<Tournament>('/tournaments', data)
    return response.data
  }

  async getTournaments(institutionId?: number, isPublic?: boolean): Promise<Tournament[]> {
    const params: any = {}
    if (institutionId) params.institution_id = institutionId
    if (isPublic !== undefined) params.is_public = isPublic
    const response = await this.api.get<Tournament[]>('/tournaments', { params })
    return response.data
  }

  // Match endpoints
  async createSchedule(data: Partial<Schedule>): Promise<Schedule> {
    const response = await this.api.post<Schedule>('/matches/schedules', data)
    return response.data
  }

  async getSchedules(sportId?: number): Promise<Schedule[]> {
    const params = sportId ? { sport_id: sportId } : {}
    const response = await this.api.get<Schedule[]>('/matches/schedules', { params })
    return response.data
  }

  async getMatches(sportId?: number, scheduleId?: number, status?: string): Promise<Match[]> {
    const params: any = {}
    if (sportId) params.sport_id = sportId
    if (scheduleId) params.schedule_id = scheduleId
    if (status) params.status = status
    const response = await this.api.get<Match[]>('/matches', { params })
    return response.data
  }

  async getMatch(matchId: number): Promise<Match> {
    const response = await this.api.get<Match>(`/matches/${matchId}`)
    return response.data
  }

  async updateMatch(matchId: number, data: Partial<Match>): Promise<Match> {
    const response = await this.api.patch<Match>(`/matches/${matchId}`, data)
    return response.data
  }

  async updateScore(matchId: number, data: {
    home_score?: number
    away_score?: number
    period?: string
    update_type?: string
    description?: string
  }): Promise<Score> {
    const response = await this.api.post<Score>(`/matches/${matchId}/score`, data)
    return response.data
  }

  async getScore(matchId: number): Promise<Score> {
    const response = await this.api.get<Score>(`/matches/${matchId}/score`)
    return response.data
  }

  async getScoreHistory(matchId: number): Promise<any[]> {
    const response = await this.api.get<any[]>(`/matches/${matchId}/score/history`)
    return response.data
  }

  // Coach endpoints for live score updates
  async updateMatchScore(matchId: number, data: {
    home_score?: number
    away_score?: number
    period?: string
    update_type?: string
    description?: string
    additional_info?: string
    action?: string
    points?: number
    player_id?: number
    team?: 'home' | 'away'
    sport_specific_data?: Record<string, any>
  }): Promise<Score> {
    const response = await this.api.post<Score>(`/coach/matches/${matchId}/score`, data)
    return response.data
  }

  async getScoreDetails(matchId: number): Promise<{
    sport_code: string | null
    sport_name: string
    score_data: Record<string, any>
    home_score: number
    away_score: number
    period: string | null
  }> {
    const response = await this.api.get(`/coach/matches/${matchId}/score/details`)
    return response.data
  }

  async endMatch(matchId: number): Promise<{ message: string; match_id: number }> {
    const response = await this.api.patch<{ message: string; match_id: number }>(`/coach/matches/${matchId}/end`)
    return response.data
  }

  async getMatchPlayers(matchId: number): Promise<Player[]> {
    const response = await this.api.get<Player[]>(`/coach/matches/${matchId}/players`)
    return response.data
  }

  // Admin Tournaments
  async getAdminTournaments(skip = 0, limit = 100) {
    const response = await this.api.get(`/admin/tournaments`, {
      params: { skip, limit }
    })
    return response.data
  }

  async deleteAdminTournament(id: number) {
    const response = await this.api.delete(`/admin/tournaments/${id}`)
    return response.data
  }

  // Notification endpoints
  async getNotifications(isRead?: boolean): Promise<Notification[]> {
    const params = isRead !== undefined ? { is_read: isRead } : {}
    const response = await this.api.get<Notification[]>('/notifications', { params })
    return response.data
  }

  async markNotificationAsRead(notificationId: number): Promise<Notification> {
    const response = await this.api.post<Notification>(`/notifications/${notificationId}/read`)
    return response.data
  }

  async getUnreadCount(): Promise<{ unread_count: number }> {
    const response = await this.api.get<{ unread_count: number }>('/notifications/unread/count')
    return response.data
  }

  // Player endpoints
  async joinTeam(teamId: number): Promise<Player> {
    const response = await this.api.post<Player>(`/players/teams/${teamId}/join`)
    return response.data
  }

  async getMyProfile(): Promise<Player> {
    const response = await this.api.get<Player>('/players/me')
    return response.data
  }

  // Statistics endpoints
  async getPlayerStatistics(playerId: number): Promise<any> {
    const response = await this.api.get(`/statistics/players/${playerId}`)
    return response.data
  }

  async getTeamStatistics(teamId: number): Promise<any> {
    const response = await this.api.get(`/statistics/teams/${teamId}`)
    return response.data
  }

  async getMyStatistics(): Promise<any> {
    const response = await this.api.get('/statistics/players/me')
    return response.data
  }
}

export default new ApiService()
