<template>
  <div>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
      <div class="card">
        <h3 class="text-lg font-semibold text-gray-500 mb-2">Upcoming Matches</h3>
        <p class="text-3xl font-bold text-primary-600">{{ upcomingMatches.length }}</p>
      </div>
      <div class="card">
        <h3 class="text-lg font-semibold text-gray-500 mb-2">Matches Played</h3>
        <p class="text-3xl font-bold text-primary-600">{{ stats?.matches_played || 0 }}</p>
      </div>
    </div>
    
    <div class="card mb-6">
      <h2 class="text-xl font-semibold mb-4">Upcoming Matches</h2>
      <div v-if="upcomingMatches.length === 0" class="text-gray-600">
        <p>No upcoming matches</p>
      </div>
      <div v-else class="space-y-4">
        <div v-for="match in upcomingMatches" :key="match.id" class="bg-gray-50 p-4 rounded-lg">
          <div class="flex justify-between items-center">
            <div>
              <p class="font-semibold">Match #{{ match.match_number || match.id }}</p>
              <p class="text-sm text-gray-600">{{ formatDateTime(match.scheduled_time) }}</p>
              <p v-if="match.venue_name" class="text-sm text-gray-600">{{ match.venue_name }}</p>
            </div>
            <RouterLink :to="`/matches/${match.id}`" class="btn btn-primary text-sm">View Details</RouterLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import api from '@/services/api'
import type { Match } from '@/types'

const upcomingMatches = ref<Match[]>([])
const stats = ref<any>(null)

const fetchData = async () => {
  try {
    upcomingMatches.value = await api.getMatches(undefined, undefined, 'scheduled')
    stats.value = await api.getMyStatistics().catch(() => null)
  } catch (error) {
    console.error('Failed to fetch data', error)
  }
}

const formatDateTime = (dateString: string): string => {
  const date = new Date(dateString)
  return date.toLocaleString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}

onMounted(() => {
  fetchData()
})
</script>
