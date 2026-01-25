<template>
  <div>
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
      <div class="card">
        <h3 class="text-lg font-semibold text-gray-500 mb-2">Sports</h3>
        <p class="text-3xl font-bold text-primary-600">{{ sportsCount }}</p>
      </div>
      <div class="card">
        <h3 class="text-lg font-semibold text-gray-500 mb-2">Teams</h3>
        <p class="text-3xl font-bold text-primary-600">{{ teamsCount }}</p>
      </div>
      <div class="card">
        <h3 class="text-lg font-semibold text-gray-500 mb-2">Tournaments</h3>
        <p class="text-3xl font-bold text-primary-600">{{ tournamentsCount }}</p>
      </div>
      <div class="card">
        <h3 class="text-lg font-semibold text-gray-500 mb-2">Upcoming Matches</h3>
        <p class="text-3xl font-bold text-primary-600">{{ matchesCount }}</p>
      </div>
    </div>
    
    <!-- Quick Actions removed -->
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const sportsCount = ref(0)
const teamsCount = ref(0)
const tournamentsCount = ref(0)
const matchesCount = ref(0)

onMounted(async () => {
  try {
    const institution = await api.getMyInstitution()
    const [sports, teams, tournaments, matches] = await Promise.all([
      api.getSports(institution.id),
      api.getTeams(undefined, institution.id),
      api.getTournaments(institution.id),
      api.getMatches(undefined, undefined, 'scheduled')
    ])
    sportsCount.value = sports.length
    teamsCount.value = teams.length
    tournamentsCount.value = tournaments.length
    matchesCount.value = matches.length
  } catch (error) {
    console.error('Failed to fetch dashboard data', error)
  }
})
</script>
