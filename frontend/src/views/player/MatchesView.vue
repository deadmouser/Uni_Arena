<template>
  <div>
    <h2 class="text-2xl font-bold text-gray-900 mb-6">My Matches</h2>
    <div v-if="loading" class="text-center py-12">
      <p class="text-gray-600">Loading matches...</p>
    </div>
    <div v-else-if="matches.length === 0" class="text-center py-12">
      <p class="text-gray-600">No matches found</p>
    </div>
    <div v-else class="space-y-4">
      <div
        v-for="match in matches"
        :key="match.id"
        class="card hover:shadow-lg transition-shadow cursor-pointer"
        @click="$router.push(`/matches/${match.id}`)"
      >
        <div class="flex justify-between items-center">
          <div>
            <h3 class="text-lg font-semibold">Match #{{ match.match_number || match.id }}</h3>
            <p class="text-sm text-gray-600 mt-1">{{ formatDateTime(match.scheduled_time) }}</p>
            <p v-if="match.venue_name" class="text-sm text-gray-600">{{ match.venue_name }}</p>
          </div>
          <span class="px-3 py-1 rounded text-sm font-semibold"
            :class="{
              'bg-red-100 text-red-800': match.status === 'live',
              'bg-blue-100 text-blue-800': match.status === 'scheduled',
              'bg-gray-100 text-gray-800': match.status === 'completed'
            }"
          >
            {{ match.status.toUpperCase() }}
          </span>
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

const fetchMatches = async () => {
  try {
    matches.value = await api.getMatches()
  } catch (error) {
    console.error('Failed to fetch matches', error)
  } finally {
    loading.value = false
  }
}

const formatDateTime = (dateString: string): string => {
  const date = new Date(dateString)
  return date.toLocaleString('en-US', { month: 'short', day: 'numeric', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}

onMounted(() => {
  fetchMatches()
})
</script>
