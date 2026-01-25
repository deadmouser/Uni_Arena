import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/HomeView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/auth/LoginView.vue'),
      meta: { requiresAuth: false, redirectIfAuthenticated: true }
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('@/views/DashboardView.vue'),
      meta: { requiresAuth: true }
    },
    // Admin routes
    {
      path: '/admin',
      component: () => import('@/layouts/AdminLayout.vue'),
      meta: { requiresAuth: true, requiresRole: 'admin' },
      children: [
        {
          path: '',
          name: 'admin-dashboard',
          component: () => import('@/views/admin/AdminDashboard.vue')
        },
        {
          path: 'institutions',
          name: 'admin-institutions',
          component: () => import('@/views/admin/InstitutionsView.vue')
        },
        {
          path: 'tournaments',
          name: 'admin-tournaments',
          component: () => import('../views/admin/TournamentsView.vue')
        },
        {
          path: 'users',
          name: 'admin-users',
          component: () => import('@/views/admin/UsersView.vue')
        }
      ]
    },
    // Organizer routes
    {
      path: '/organizer',
      component: () => import('@/layouts/OrganizerLayout.vue'),
      meta: { requiresAuth: true, requiresRole: ['admin', 'organizer'] },
      children: [
        {
          path: '',
          name: 'organizer-dashboard',
          component: () => import('@/views/organizer/OrganizerDashboard.vue')
        },
        {
          path: 'institution',
          name: 'organizer-institution',
          component: () => import('@/views/organizer/InstitutionView.vue')
        },
        {
          path: 'sports',
          name: 'organizer-sports',
          component: () => import('@/views/organizer/SportsView.vue')
        },
        {
          path: 'teams',
          name: 'organizer-teams',
          component: () => import('@/views/organizer/TeamsView.vue')
        },
        {
          path: 'players',
          name: 'organizer-players',
          component: () => import('@/views/organizer/PlayersView.vue')
        },
        {
          path: 'venues',
          name: 'organizer-venues',
          component: () => import('@/views/organizer/VenuesView.vue')
        },
        {
          path: 'tournaments',
          name: 'organizer-tournaments',
          component: () => import('@/views/organizer/TournamentsView.vue')
        },
        {
          path: 'schedules',
          name: 'organizer-schedules',
          component: () => import('@/views/organizer/SchedulesView.vue')
        }
      ]
    },
    // Coach routes
    {
      path: '/coach',
      component: () => import('@/layouts/CoachLayout.vue'),
      meta: { requiresAuth: true, requiresRole: ['admin', 'organizer', 'coach'] },
      children: [
        {
          path: '',
          name: 'coach-dashboard',
          component: () => import('@/views/coach/CoachDashboard.vue')
        },
        {
          path: 'matches/:id/live-score',
          name: 'coach-live-score',
          component: () => import('@/views/coach/LiveScoreUpdateView.vue')
        },
        {
          path: 'teams',
          name: 'coach-teams',
          component: () => import('@/views/coach/TeamsView.vue')
        },
        {
          path: 'lineups',
          name: 'coach-lineups',
          component: () => import('@/views/coach/LineupsView.vue')
        }
      ]
    },
    // Player routes
    {
      path: '/player',
      component: () => import('@/layouts/PlayerLayout.vue'),
      meta: { requiresAuth: true, requiresRole: 'player' },
      children: [
        {
          path: '',
          name: 'player-dashboard',
          component: () => import('@/views/player/PlayerDashboard.vue')
        },
        {
          path: 'profile',
          name: 'player-profile',
          component: () => import('@/views/player/ProfileView.vue')
        },
        {
          path: 'matches',
          name: 'player-matches',
          component: () => import('@/views/player/MatchesView.vue')
        },
        {
          path: 'statistics',
          name: 'player-statistics',
          component: () => import('@/views/player/StatisticsView.vue')
        }
      ]
    },
    // Viewer routes
    {
      path: '/viewer',
      component: () => import('@/layouts/ViewerLayout.vue'),
      meta: { requiresAuth: false },
      children: [
        {
          path: '',
          name: 'viewer-home',
          component: () => import('@/views/viewer/ViewerHome.vue')
        },
        {
          path: 'matches',
          name: 'viewer-matches',
          component: () => import('@/views/viewer/MatchesView.vue')
        },
        {
          path: 'tournaments',
          name: 'viewer-tournaments',
          component: () => import('@/views/viewer/TournamentsView.vue')
        },
        {
          path: 'live-scores',
          name: 'viewer-live-scores',
          component: () => import('@/views/viewer/LiveScoresView.vue')
        }
      ]
    },
    // Match detail (public)
    {
      path: '/matches/:id',
      name: 'match-detail',
      component: () => import('@/views/MatchDetailView.vue'),
      meta: { requiresAuth: false }
    }
  ]
})

router.beforeEach((to, _from, next) => {
  const authStore = useAuthStore()

  // Check if route requires authentication
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
    return
  }

  // Redirect if already authenticated and trying to access auth pages
  if (to.meta.redirectIfAuthenticated && authStore.isAuthenticated) {
    // Redirect to role-specific dashboard
    const userRole = authStore.user?.role
    if (userRole === 'admin') {
      next({ name: 'admin-dashboard' })
    } else if (userRole === 'organizer') {
      next({ name: 'organizer-dashboard' })
    } else if (userRole === 'coach') {
      next({ name: 'coach-dashboard' })
    } else if (userRole === 'player') {
      next({ name: 'player-dashboard' })
    } else {
      next({ name: 'dashboard' })
    }
    return
  }

  // Check role requirements
  if (to.meta.requiresRole) {
    const requiredRoles = Array.isArray(to.meta.requiresRole)
      ? to.meta.requiresRole
      : [to.meta.requiresRole]

    const userRole = authStore.user?.role
    if (!userRole || !requiredRoles.includes(userRole)) {
      next({ name: 'dashboard' })
      return
    }
  }

  next()
})

export default router
