<template>
  <div>
    <Navbar />
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div v-if="loading" class="text-center py-12">
        <p class="text-gray-600">Loading match details...</p>
      </div>
      
      <div v-else-if="match" class="card">
        <div class="mb-6">
          <RouterLink to="/viewer/matches" class="text-primary-600 hover:text-primary-700 mb-4 inline-block">
            ← Back to Matches
          </RouterLink>
          <h1 class="text-3xl font-bold text-gray-900">Match Details</h1>
          <p class="text-gray-600 mt-2">{{ match.match_number || `Match #${match.id}` }}</p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <div>
            <h3 class="text-sm font-medium text-gray-500 mb-2">Status</h3>
            <span
              class="px-3 py-1 rounded-full text-sm font-semibold"
              :class="{
                'bg-green-100 text-green-800': match.status === 'live',
                'bg-blue-100 text-blue-800': match.status === 'scheduled',
                'bg-gray-100 text-gray-800': match.status === 'completed',
                'bg-red-100 text-red-800': match.status === 'cancelled'
              }"
            >
              {{ match.status.toUpperCase() }}
            </span>
          </div>
          
          <div>
            <h3 class="text-sm font-medium text-gray-500 mb-2">Scheduled Time</h3>
            <p class="text-gray-900">{{ formatDateTime(match.scheduled_time) }}</p>
          </div>
          
          <div v-if="match.venue_name">
            <h3 class="text-sm font-medium text-gray-500 mb-2">Venue</h3>
            <p class="text-gray-900">{{ match.venue_name }}</p>
          </div>
        </div>
        
        <!-- Score Display -->
        <div v-if="score" class="bg-gray-50 rounded-lg p-6 mb-6">
          <div class="text-center">
            <div v-if="match.status === 'live'" class="mb-4">
              <span class="px-3 py-1 bg-red-500 text-white text-sm font-semibold rounded">LIVE</span>
            </div>
            
            <div class="grid grid-cols-3 gap-4 items-center">
              <div class="text-right">
                <p class="text-lg font-semibold">{{ getTeamName(match.home_team_id) || 'TBD' }}</p>
              </div>
              <div class="text-center">
                <div class="text-4xl font-bold text-primary-600">
                  {{ score.home_score }} - {{ score.away_score }}
                </div>
                <div v-if="score.period" class="text-sm text-gray-500 mt-2">
                  {{ score.period }}
                </div>
              </div>
              <div class="text-left">
                <p class="text-lg font-semibold">{{ getTeamName(match.away_team_id) || 'TBD' }}</p>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Score History -->
        <div v-if="scoreHistory.length > 0" class="mb-6">
          <h2 class="text-xl font-semibold mb-4">Score History</h2>
          <div class="space-y-2">
            <div
              v-for="update in scoreHistory"
              :key="update.id"
              class="bg-gray-50 p-3 rounded"
            >
              <div class="flex justify-between items-center">
                <div>
                  <p class="font-semibold">{{ update.home_score }} - {{ update.away_score }}</p>
                  <p v-if="update.description" class="text-sm text-gray-600">{{ update.description }}</p>
                </div>
                <div class="text-sm text-gray-500">
                  {{ formatTime(update.updated_at) }}
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Match Notes -->
        <div v-if="match.notes" class="mb-6">
          <h2 class="text-xl font-semibold mb-2">Notes</h2>
          <p class="text-gray-700">{{ match.notes }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import api from '@/services/api'
import type { Match, Score } from '@/types'
import Navbar from '@/components/Navbar.vue'

const route = useRoute()
const match = ref<Match | null>(null)
const score = ref<Score | null>(null)
const scoreHistory = ref<any[]>([])
const loading = ref(true)
let updateInterval: number | null = null

const fetchMatchDetails = async () => {
  try {
    const matchId = parseInt(route.params.id as string)
    const [matchData, scoreData, historyData] = await Promise.all([
      api.getMatch(matchId),
      api.getScore(matchId).catch(() => null),
      api.getScoreHistory(matchId).catch(() => [])
    ])
    
    match.value = matchData
    score.value = scoreData
    scoreHistory.value = historyData
    
    // If match is live, update score periodically
    if (match.value.status === 'live') {
      updateInterval = window.setInterval(async () => {
        try {
          const updatedScore = await api.getScore(matchId)
          score.value = updatedScore
          const updatedHistory = await api.getScoreHistory(matchId)
          scoreHistory.value = updatedHistory
        } catch (error) {
          console.error('Failed to update score', error)
        }
      }, 5000)
    }
  } catch (error) {
    console.error('Failed to fetch match details', error)
  } finally {
    loading.value = false
  }
}

const getTeamName = (teamId: number | null): string => {
  return teamId ? `Team ${teamId}` : 'TBD'
}

const formatDateTime = (dateString: string): string => {
  const date = new Date(dateString)
  return date.toLocaleString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatTime = (dateString: string): string => {
  const date = new Date(dateString)
  return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
}

onMounted(() => {
  fetchMatchDetails()
})

onUnmounted(() => {
  if (updateInterval) {
    clearInterval(updateInterval)
  }
})
</script>
