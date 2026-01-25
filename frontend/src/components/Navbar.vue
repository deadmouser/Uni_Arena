<template>
  <nav class="bg-white shadow-lg">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <div class="flex">
          <div class="flex-shrink-0 flex items-center">
            <RouterLink to="/" class="flex items-center space-x-2">
              <img
                v-if="institution?.logo_url"
                :src="institution.logo_url"
                alt="Logo"
                class="h-8 w-8 object-contain rounded"
              />
              <span class="text-2xl font-bold text-primary-600">Uni Arena</span>
            </RouterLink>
          </div>
          <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
            <RouterLink
              v-for="item in navItems"
              :key="item.name"
              :to="item.to"
              class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
              active-class="border-primary-500 text-gray-900"
            >
              {{ item.name }}
            </RouterLink>
          </div>
        </div>
        <div class="flex items-center">
          <div v-if="authStore.isAuthenticated" class="flex items-center space-x-4">
            <RouterLink to="/notifications" class="relative">
              <BellIcon class="h-6 w-6 text-gray-500" />
              <span v-if="unreadCount > 0" class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                {{ unreadCount }}
              </span>
            </RouterLink>
            <div class="flex items-center space-x-2">
              <span class="text-sm text-gray-700">{{ authStore.user?.full_name || authStore.user?.username }}</span>
              <button @click="handleLogout" class="btn btn-secondary text-sm">
                Logout
              </button>
            </div>
          </div>
          <div v-else class="flex items-center space-x-2">
            <RouterLink to="/login" class="btn btn-secondary">Login</RouterLink>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { BellIcon } from '@heroicons/vue/24/outline'
import api from '@/services/api'
import type { Institution } from '@/types'

const authStore = useAuthStore()
const unreadCount = ref(0)
const institution = ref<Institution | null>(null)

const navItems = computed(() => {
  const items = [
    { name: 'Home', to: '/' },
  ]

  if (authStore.isAdmin) {
    items.push(
      { name: 'Dashboard', to: '/admin' },
      { name: 'Institutions', to: '/admin/institutions' },
      { name: 'Tournaments', to: '/admin/tournaments' },
      { name: 'Users', to: '/admin/users' }
    )
  } else if (authStore.isCoach) {
     items.push(
      { name: 'Dashboard', to: '/coach' },
      { name: 'My Teams', to: '/coach/teams' },
      { name: 'Line-ups', to: '/coach/lineups' }
    )
  } else {
    items.push(
      { name: 'Matches', to: '/viewer/matches' },
      { name: 'Tournaments', to: '/viewer/tournaments' },
      { name: 'Live Scores', to: '/viewer/live-scores' }
    )
  }

  return items
})

const handleLogout = () => {
  authStore.logout()
  window.location.href = '/'
}

onMounted(async () => {
  if (authStore.isAuthenticated) {
    try {
      const [unreadRes, institutionRes] = await Promise.all([
        api.getUnreadCount(),
        authStore.user?.institution_id ? api.getInstitution(authStore.user.institution_id) : Promise.resolve(null)
      ])
      unreadCount.value = unreadRes.unread_count
      institution.value = institutionRes
    } catch (error) {
      console.error('Failed to fetch navbar data', error)
    }
  }
})
</script>
