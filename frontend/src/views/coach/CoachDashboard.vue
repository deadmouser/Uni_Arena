<template>
  <div>
    <div class="card mb-6">
      <h2 class="text-xl font-semibold mb-4">My Teams</h2>
      <div v-if="teams.length === 0" class="text-gray-600">
        <p>No teams assigned yet</p>
      </div>
      <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div v-for="team in teams" :key="team.id" class="bg-gray-50 p-4 rounded-lg">
          <h3 class="font-semibold">{{ team.name }}</h3>
          <p class="text-sm text-gray-600">Sport ID: {{ team.sport_id }}</p>
        </div>
      </div>
    </div>
    
    <div class="card">
      <h2 class="text-xl font-semibold mb-4">Upcoming Matches</h2>
      <div v-if="matches.length === 0" class="text-gray-600">
        <p>No upcoming matches</p>
      </div>
      <div v-else class="space-y-4">
        <div v-for="match in matches" :key="match.id" class="bg-gray-50 p-4 rounded-lg">
          <div class="flex justify-between items-center">
            <div>
              <p class="font-semibold">Match #{{ match.match_number || match.id }}</p>
              <p class="text-sm text-gray-600">{{ formatDateTime(match.scheduled_time) }}</p>
            </div>
            <RouterLink :to="`/matches/${match.id}`" class="btn btn-primary text-sm">View</RouterLink>
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
import type { Team, Match } from '@/types'

const teams = ref<Team[]>([])
const matches = ref<Match[]>([])

const fetchData = async () => {
  try {
    // Note: These endpoints need to be implemented in the backend
    // For now, using placeholder
    teams.value = await api.getTeams().catch(() => [])
    matches.value = await api.getMatches(undefined, undefined, 'scheduled').catch(() => [])
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
