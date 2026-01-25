<template>
  <div>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
      <div class="card">
        <h3 class="text-lg font-semibold text-gray-500 mb-2">Total Institutions</h3>
        <p class="text-3xl font-bold text-primary-600">{{ institutionsCount }}</p>
      </div>
      <div class="card">
        <h3 class="text-lg font-semibold text-gray-500 mb-2">Total Users</h3>
        <p class="text-3xl font-bold text-primary-600">{{ usersCount }}</p>
      </div>
      <div class="card">
        <h3 class="text-lg font-semibold text-gray-500 mb-2">Active Matches</h3>
        <p class="text-3xl font-bold text-primary-600">{{ activeMatches }}</p>
      </div>
    </div>
    
    <!-- Quick Actions moved to Navbar -->
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const institutionsCount = ref(0)
const usersCount = ref(0)
const activeMatches = ref(0)

onMounted(async () => {
  try {
    const [institutions, users, matches] = await Promise.all([
      api.getInstitutions(),
      api.getUsers(),
      api.getMatches(undefined, undefined, 'live')
    ])
    institutionsCount.value = institutions.length
    usersCount.value = users.length
    activeMatches.value = matches.length
  } catch (error) {
    console.error('Failed to fetch dashboard data', error)
  }
})
</script>
