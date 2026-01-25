<template>
  <div>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-6">Matches</h1>
      <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
        <p class="font-semibold">Error loading matches:</p>
        <p>{{ error }}</p>
        <p class="text-sm mt-2">Make sure the backend server is running at http://localhost:8000</p>
      </div>
      <div v-else-if="loading" class="text-center py-12">
        <p class="text-gray-600">Loading matches...</p>
      </div>
      <div v-else-if="matches.length === 0" class="text-center py-12">
        <p class="text-gray-600">No matches found</p>
        <p class="text-sm text-gray-500 mt-2">Run the seed script to add sample data: <code class="bg-gray-100 px-2 py-1 rounded">python backend/seed_data.py</code></p>
      </div>
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="match in matches"
          :key="match.id"
          class="card hover:shadow-lg transition-shadow cursor-pointer"
          @click="$router.push(`/matches/${match.id}`)"
        >
          <div class="flex justify-between items-center mb-4">
            <span class="px-2 py-1 rounded text-xs font-semibold"
              :class="{
                'bg-red-500 text-white': match.status === 'live',
                'bg-blue-500 text-white': match.status === 'scheduled',
                'bg-gray-500 text-white': match.status === 'completed'
              }"
            >
              {{ match.status.toUpperCase() }}
            </span>
            <span class="text-sm text-gray-500">{{ formatDate(match.scheduled_time) }}</span>
          </div>
          <h3 class="font-semibold mb-2">{{ getTeamName(match.home_team_id) }} vs {{ getTeamName(match.away_team_id) }}</h3>
          <p v-if="match.venue_name" class="text-sm text-gray-600">{{ match.venue_name }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'
import type { Match } from '@/types'

const router = useRouter()
const matches = ref<Match[]>([])
const loading = ref(true)
const error = ref<string | null>(null)

const fetchMatches = async () => {
  try {
    error.value = null
    loading.value = true
    matches.value = await api.getMatches()
  } catch (err: any) {
    console.error('Failed to fetch matches', err)
    // Handle different types of errors
    if (err.code === 'ECONNREFUSED' || err.code === 'ERR_NETWORK' || err.message?.includes('Network Error')) {
      error.value = 'Network Error: Cannot connect to backend server. Make sure the backend is running at http://localhost:8000'
    } else if (err.response) {
      // Server responded with error status
      error.value = err.response.data?.detail || `Server error: ${err.response.status} ${err.response.statusText}`
    } else if (err.request) {
      // Request was made but no response received
      error.value = 'No response from server. The backend may not be running or is unreachable.'
    } else {
      error.value = err.message || 'Failed to fetch matches. Please check if the backend server is running.'
    }
  } finally {
    loading.value = false
  }
}

const getTeamName = (teamId: number | null): string => {
  return teamId ? `Team ${teamId}` : 'TBD'
}

const formatDate = (dateString: string): string => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}

onMounted(() => {
  fetchMatches()
})
</script>
