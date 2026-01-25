<template>
  <div>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-6">Tournaments</h1>
      <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
        <p class="font-semibold">Error loading tournaments:</p>
        <p>{{ error }}</p>
        <p class="text-sm mt-2">Make sure the backend server is running at http://localhost:8000</p>
      </div>
      <div v-else-if="loading" class="text-center py-12">
        <p class="text-gray-600">Loading tournaments...</p>
      </div>
      <div v-else-if="tournaments.length === 0" class="text-center py-12">
        <p class="text-gray-600">No tournaments found</p>
        <p class="text-sm text-gray-500 mt-2">Run the seed script to add sample data: <code class="bg-gray-100 px-2 py-1 rounded">python backend/seed_data.py</code></p>
      </div>
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="tournament in tournaments"
          :key="tournament.id"
          class="card hover:shadow-lg transition-shadow"
        >
          <div class="flex justify-between items-center mb-4">
            <span class="px-2 py-1 rounded text-xs font-semibold"
              :class="{
                'bg-green-500 text-white': tournament.status === 'ongoing',
                'bg-blue-500 text-white': tournament.status === 'upcoming',
                'bg-gray-500 text-white': tournament.status === 'completed'
              }"
            >
              {{ tournament.status.toUpperCase() }}
            </span>
            <span v-if="tournament.is_public" class="text-xs text-gray-500">Public</span>
          </div>
          <h3 class="text-xl font-semibold mb-2">{{ tournament.name }}</h3>
          <p v-if="tournament.description" class="text-gray-600 mb-4 text-sm">{{ tournament.description }}</p>
          <div class="text-sm text-gray-500">
            <p>Start: {{ formatDate(tournament.start_date) }}</p>
            <p v-if="tournament.end_date">End: {{ formatDate(tournament.end_date) }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/services/api'
import type { Tournament } from '@/types'

const tournaments = ref<Tournament[]>([])
const loading = ref(true)
const error = ref<string | null>(null)

const fetchTournaments = async () => {
  try {
    error.value = null
    tournaments.value = await api.getTournaments(undefined, true)
  } catch (err: any) {
    console.error('Failed to fetch tournaments', err)
    error.value = err.response?.data?.detail || err.message || 'Failed to fetch tournaments. Please check if the backend server is running.'
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString: string): string => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

onMounted(() => {
  fetchTournaments()
})
</script>
