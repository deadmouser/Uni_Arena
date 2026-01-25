<template>
  <div>
    <Navbar />
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div class="text-center">
        <h1 class="text-4xl font-extrabold text-gray-900 sm:text-5xl md:text-6xl">
          Welcome to <span class="text-primary-600">Uni Arena</span>
        </h1>
        <p class="mt-3 max-w-md mx-auto text-base text-gray-500 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl">
          Sports Management System for Institutions - Manage tournaments, track live scores, and organize sports events
        </p>
        <div class="mt-5 max-w-md mx-auto sm:flex sm:justify-center md:mt-8">
          <div class="rounded-md shadow">
            <RouterLink
              to="/viewer/matches"
              class="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 md:py-4 md:text-lg md:px-10"
            >
              View Matches
            </RouterLink>
          </div>
          <div class="mt-3 rounded-md shadow sm:mt-0 sm:ml-3">
            <RouterLink
              to="/viewer/live-scores"
              class="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-primary-600 bg-white hover:bg-gray-50 md:py-4 md:text-lg md:px-10"
            >
              Live Scores
            </RouterLink>
          </div>
        </div>
      </div>

      <div class="mt-20 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
        <div class="card">
          <h3 class="text-xl font-semibold mb-2">Tournaments</h3>
          <p class="text-gray-600">Browse and view all upcoming and ongoing tournaments</p>
          <RouterLink to="/viewer/tournaments" class="text-primary-600 hover:text-primary-700 mt-4 inline-block">
            View Tournaments →
          </RouterLink>
        </div>
        <div class="card">
          <h3 class="text-xl font-semibold mb-2">Live Scores</h3>
          <p class="text-gray-600">Get real-time updates on match scores and events</p>
          <RouterLink to="/viewer/live-scores" class="text-primary-600 hover:text-primary-700 mt-4 inline-block">
            View Live Scores →
          </RouterLink>
        </div>
        <div class="card">
          <h3 class="text-xl font-semibold mb-2">Match Schedules</h3>
          <p class="text-gray-600">Check out upcoming matches and their schedules</p>
          <RouterLink to="/viewer/matches" class="text-primary-600 hover:text-primary-700 mt-4 inline-block">
            View Schedules →
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
import Navbar from '@/components/Navbar.vue'
</script>
