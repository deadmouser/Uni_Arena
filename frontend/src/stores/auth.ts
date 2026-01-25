import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '@/types'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Initialize from localStorage
  const initAuth = () => {
    const storedToken = localStorage.getItem('access_token')
    const storedUser = localStorage.getItem('user')
    
    if (storedToken && storedUser) {
      token.value = storedToken
      try {
        user.value = JSON.parse(storedUser)
      } catch (e) {
        console.error('Failed to parse user from localStorage', e)
      }
    }
  }

  // Computed properties
  const isAuthenticated = computed(() => !!token.value && !!user.value)
  const isAdmin = computed(() => user.value?.role === 'admin')
  const isOrganizer = computed(() => user.value?.role === 'organizer')
  const isCoach = computed(() => user.value?.role === 'coach')
  const isPlayer = computed(() => user.value?.role === 'player')
  const isViewer = computed(() => user.value?.role === 'viewer')

  // Actions
  const login = async (email: string, password: string) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.login(email, password)
      token.value = response.access_token
      user.value = response.user
      localStorage.setItem('access_token', response.access_token)
      localStorage.setItem('user', JSON.stringify(response.user))
      return response
    } catch (err: any) {
      // Better error handling
      if (err.code === 'ECONNREFUSED' || err.code === 'ERR_NETWORK' || err.message?.includes('Network Error')) {
        error.value = 'Network Error: Cannot connect to backend server. Make sure the backend is running at http://localhost:8000'
      } else if (err.response?.status === 401) {
        error.value = err.response?.data?.detail || 'Incorrect email or password'
      } else if (err.response?.data?.detail) {
        error.value = err.response.data.detail
      } else {
        error.value = err.message || 'Login failed. Please try again.'
      }
      throw err
    } finally {
      loading.value = false
    }
  }

  // Registration is disabled - only admins can create users
  // const register = async (userData: {
  //   email: string
  //   username: string
  //   password: string
  //   full_name?: string
  //   role?: string
  //   institution_id?: number
  // }) => {
  //   loading.value = true
  //   error.value = null
  //   try {
  //     const newUser = await api.register(userData)
  //     return newUser
  //   } catch (err: any) {
  //     error.value = err.response?.data?.detail || 'Registration failed'
  //     throw err
  //   } finally {
  //     loading.value = false
  //   }
  // }

  const logout = () => {
    user.value = null
    token.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
  }

  const fetchCurrentUser = async () => {
    loading.value = true
    error.value = null
    try {
      const currentUser = await api.getCurrentUser()
      user.value = currentUser
      localStorage.setItem('user', JSON.stringify(currentUser))
      return currentUser
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch user'
      logout()
      throw err
    } finally {
      loading.value = false
    }
  }

  // Initialize on store creation
  initAuth()

  return {
    user,
    token,
    loading,
    error,
    isAuthenticated,
    isAdmin,
    isOrganizer,
    isCoach,
    isPlayer,
    isViewer,
    login,
    // register, // Disabled - only admins can create users
    logout,
    fetchCurrentUser,
    initAuth
  }
})
