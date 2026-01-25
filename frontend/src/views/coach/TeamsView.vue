<template>
  <div>
    <h2 class="text-2xl font-bold text-gray-900 mb-6">My Teams</h2>
    <div v-if="loading" class="text-center py-12">
      <p class="text-gray-600">Loading teams...</p>
    </div>
    <div v-else-if="teams.length === 0" class="text-center py-12">
      <p class="text-gray-600">No teams assigned</p>
    </div>
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="team in teams" :key="team.id" class="card">
        <h3 class="text-xl font-semibold mb-4">{{ team.name }}</h3>
        <RouterLink :to="`/coach/teams/${team.id}/players`" class="btn btn-primary">
          Manage Players
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import api from '@/services/api'
import type { Team } from '@/types'

const teams = ref<Team[]>([])
const loading = ref(true)

const fetchTeams = async () => {
  try {
    teams.value = await api.getTeams()
  } catch (error) {
    console.error('Failed to fetch teams', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchTeams()
})
</script>
