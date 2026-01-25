<template>
  <nav class="bg-white shadow-lg">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <div class="flex items-center">
          <!-- Institution Logo -->
          <div class="flex-shrink-0 flex items-center mr-4">
            <img
              v-if="institution?.logo_url"
              :src="institution.logo_url"
              :alt="institution?.name"
              class="h-10 w-10 object-contain rounded"
            />
            <div
              v-else
              class="h-10 w-10 bg-primary-600 rounded flex items-center justify-center text-white font-bold text-lg"
            >
              {{ institution?.name?.charAt(0) || 'I' }}
            </div>
          </div>
          
          <!-- Institution Name -->
          <div class="flex-shrink-0">
            <h2 class="text-xl font-bold text-gray-900">{{ institution?.name || 'Institution' }}</h2>
            <p class="text-xs text-gray-500">{{ institution?.code || '' }}</p>
          </div>
          
          <!-- Navigation Items -->
          <div class="hidden sm:ml-8 sm:flex sm:space-x-4">
            <RouterLink
              to="/organizer"
              class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-3 pt-1 border-b-2 text-sm font-medium"
              active-class="border-primary-500 text-gray-900"
            >
              Dashboard
            </RouterLink>
            <RouterLink
              to="/organizer/tournaments"
              class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-3 pt-1 border-b-2 text-sm font-medium"
              active-class="border-primary-500 text-gray-900"
            >
              Tournaments
            </RouterLink>
            <RouterLink
              to="/organizer/sports"
              class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-3 pt-1 border-b-2 text-sm font-medium"
              active-class="border-primary-500 text-gray-900"
            >
              Sports
            </RouterLink>
            <RouterLink
              to="/organizer/teams"
              class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-3 pt-1 border-b-2 text-sm font-medium"
              active-class="border-primary-500 text-gray-900"
            >
              Teams
            </RouterLink>
            <RouterLink
              to="/organizer/players"
              class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-3 pt-1 border-b-2 text-sm font-medium"
              active-class="border-primary-500 text-gray-900"
            >
              Players
            </RouterLink>
            <RouterLink
              to="/organizer/venues"
              class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-3 pt-1 border-b-2 text-sm font-medium"
              active-class="border-primary-500 text-gray-900"
            >
              Venues
            </RouterLink>
            <RouterLink
              to="/organizer/schedules"
              class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-3 pt-1 border-b-2 text-sm font-medium"
              active-class="border-primary-500 text-gray-900"
            >
              Schedules
            </RouterLink>
          </div>
        </div>
        
        <div class="flex items-center space-x-4">
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
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { BellIcon } from '@heroicons/vue/24/outline'
import api from '@/services/api'
import type { Institution } from '@/types'

const authStore = useAuthStore()
const institution = ref<Institution | null>(null)
const unreadCount = ref(0)

const fetchInstitution = async () => {
  if (authStore.isOrganizer && authStore.user?.institution_id) {
    try {
      institution.value = await api.getMyInstitution()
    } catch (error) {
      console.error('Failed to fetch institution', error)
    }
  }
}

const handleLogout = () => {
  authStore.logout()
  window.location.href = '/'
}

onMounted(async () => {
  await fetchInstitution()
  if (authStore.isAuthenticated) {
    try {
      const response = await api.getUnreadCount()
      unreadCount.value = response.unread_count
    } catch (error) {
      console.error('Failed to fetch unread count', error)
    }
  }
})
</script>
