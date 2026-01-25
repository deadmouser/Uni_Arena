<template>
  <div>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-6">Live Scores</h1>
      
      <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
        <p class="font-semibold">Error loading live scores:</p>
        <p>{{ error }}</p>
        <p class="text-sm mt-2">Make sure the backend server is running at http://localhost:8000</p>
      </div>
      <div v-else-if="loading" class="text-center py-12">
        <p class="text-gray-600">Loading live matches...</p>
      </div>
      <div v-else-if="liveMatches.length === 0" class="text-center py-12">
        <p class="text-gray-600">No live matches at the moment</p>
        <p class="text-sm text-gray-500 mt-2">Run the seed script to add sample data: <code class="bg-gray-100 px-2 py-1 rounded">python backend/seed_data.py</code></p>
      </div>
      
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="match in liveMatches"
          :key="match.id"
          class="card hover:shadow-lg transition-shadow cursor-pointer"
          @click="$router.push(`/matches/${match.id}`)"
        >
          <div class="flex justify-between items-center mb-4">
            <span class="px-2 py-1 bg-red-500 text-white text-xs font-semibold rounded">LIVE</span>
            <span class="text-sm text-gray-500">{{ formatTime(match.scheduled_time) }}</span>
          </div>
          
          <div class="space-y-4">
            <div class="flex justify-between items-center">
              <div class="flex-1">
                <p class="font-semibold">{{ getTeamName(match.home_team_id) || 'TBD' }}</p>
              </div>
              <div class="text-2xl font-bold text-primary-600">
                {{ getScore(match.id)?.home_score || 0 }}
              </div>
            </div>
            
            <div class="flex justify-between items-center">
              <div class="flex-1">
                <p class="font-semibold">{{ getTeamName(match.away_team_id) || 'TBD' }}</p>
              </div>
              <div class="text-2xl font-bold text-primary-600">
                {{ getScore(match.id)?.away_score || 0 }}
              </div>
            </div>
          </div>
          
          <div v-if="getScore(match.id)?.period" class="mt-4 text-sm text-gray-500">
            {{ getScore(match.id)?.period }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'
import type { Match, Score } from '@/types'

const router = useRouter()
const liveMatches = ref<Match[]>([])
const scores = ref<Map<number, Score>>(new Map())
const loading = ref(true)
const error = ref<string | null>(null)
let scoreUpdateInterval: number | null = null

const fetchLiveMatches = async () => {
  try {
    error.value = null
    const matches = await api.getMatches(undefined, undefined, 'live')
    liveMatches.value = matches
    
    // Fetch scores for all live matches
    for (const match of matches) {
      try {
        const score = await api.getScore(match.id)
        scores.value.set(match.id, score)
      } catch (err) {
        console.error(`Failed to fetch score for match ${match.id}`, err)
      }
    }
  } catch (err: any) {
    console.error('Failed to fetch live matches', err)
    error.value = err.response?.data?.detail || err.message || 'Failed to fetch live matches. Please check if the backend server is running.'
  } finally {
    loading.value = false
  }
}

const updateScores = async () => {
  for (const match of liveMatches.value) {
    try {
      const score = await api.getScore(match.id)
      scores.value.set(match.id, score)
    } catch (error) {
      console.error(`Failed to update score for match ${match.id}`, error)
    }
  }
}

const getScore = (matchId: number): Score | undefined => {
  return scores.value.get(matchId)
}

const getTeamName = (teamId: number | null): string => {
  // This would need to be implemented with a teams store or API call
  return teamId ? `Team ${teamId}` : 'TBD'
}

const formatTime = (dateString: string): string => {
  const date = new Date(dateString)
  return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
}

onMounted(() => {
  fetchLiveMatches()
  // Update scores every 5 seconds
  scoreUpdateInterval = window.setInterval(updateScores, 5000)
})

onUnmounted(() => {
  if (scoreUpdateInterval) {
    clearInterval(scoreUpdateInterval)
  }
})
</script>
