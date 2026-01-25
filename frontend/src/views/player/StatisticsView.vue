<template>
  <div>
    <h2 class="text-2xl font-bold text-gray-900 mb-6">My Statistics</h2>
    <div v-if="loading" class="text-center py-12">
      <p class="text-gray-600">Loading statistics...</p>
    </div>
    <div v-else-if="stats" class="card max-w-2xl">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-6 mb-6">
        <div>
          <h3 class="text-sm font-medium text-gray-500 mb-1">Matches Played</h3>
          <p class="text-2xl font-bold text-primary-600">{{ stats.matches_played }}</p>
        </div>
        <div>
          <h3 class="text-sm font-medium text-gray-500 mb-1">Won</h3>
          <p class="text-2xl font-bold text-green-600">{{ stats.matches_won }}</p>
        </div>
        <div>
          <h3 class="text-sm font-medium text-gray-500 mb-1">Lost</h3>
          <p class="text-2xl font-bold text-red-600">{{ stats.matches_lost }}</p>
        </div>
        <div>
          <h3 class="text-sm font-medium text-gray-500 mb-1">Drawn</h3>
          <p class="text-2xl font-bold text-gray-600">{{ stats.matches_drawn }}</p>
        </div>
      </div>
    </div>
    <div v-else class="card">
      <p class="text-gray-600">No statistics available yet</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const stats = ref<any>(null)
const loading = ref(true)

const fetchStats = async () => {
  try {
    stats.value = await api.getMyStatistics()
  } catch (error) {
    console.error('Failed to fetch statistics', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchStats()
})
</script>
