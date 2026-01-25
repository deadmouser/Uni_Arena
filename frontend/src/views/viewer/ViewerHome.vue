<template>
  <div>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-6">Welcome to Uni Arena</h1>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <RouterLink to="/viewer/matches" class="card hover:shadow-lg transition-shadow">
          <h2 class="text-xl font-semibold mb-2">Matches</h2>
          <p class="text-gray-600">View all matches and schedules</p>
        </RouterLink>
        <RouterLink to="/viewer/tournaments" class="card hover:shadow-lg transition-shadow">
          <h2 class="text-xl font-semibold mb-2">Tournaments</h2>
          <p class="text-gray-600">Browse tournaments</p>
        </RouterLink>
        <RouterLink to="/viewer/live-scores" class="card hover:shadow-lg transition-shadow">
          <h2 class="text-xl font-semibold mb-2">Live Scores</h2>
          <p class="text-gray-600">Real-time match scores</p>
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>
