<template>
  <div class="min-h-screen bg-gray-50">
    <Navbar />
    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <div class="mb-6">
          <h1 class="text-3xl font-bold text-gray-900">Player Dashboard</h1>
        </div>
        <nav class="flex space-x-2 mb-6">
          <RouterLink
            to="/player"
            class="px-4 py-2 rounded-lg font-medium"
            active-class="bg-primary-600 text-white"
            :class="$route.name === 'player-dashboard' ? 'bg-primary-600 text-white' : 'bg-white text-gray-700 hover:bg-gray-100'"
          >
            Dashboard
          </RouterLink>
          <RouterLink
            to="/player/profile"
            class="px-4 py-2 rounded-lg font-medium"
            active-class="bg-primary-600 text-white"
            :class="$route.name === 'player-profile' ? 'bg-primary-600 text-white' : 'bg-white text-gray-700 hover:bg-gray-100'"
          >
            Profile
          </RouterLink>
          <RouterLink
            to="/player/matches"
            class="px-4 py-2 rounded-lg font-medium"
            active-class="bg-primary-600 text-white"
            :class="$route.name === 'player-matches' ? 'bg-primary-600 text-white' : 'bg-white text-gray-700 hover:bg-gray-100'"
          >
            Matches
          </RouterLink>
          <RouterLink
            to="/player/statistics"
            class="px-4 py-2 rounded-lg font-medium"
            active-class="bg-primary-600 text-white"
            :class="$route.name === 'player-statistics' ? 'bg-primary-600 text-white' : 'bg-white text-gray-700 hover:bg-gray-100'"
          >
            Statistics
          </RouterLink>
        </nav>
        <RouterView />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import Navbar from '@/components/Navbar.vue'
</script>
