<template>
  <div>
    <Navbar />
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <h1 class="text-3xl font-bold text-gray-900 mb-6">Dashboard</h1>
      
      <div v-if="authStore.isAuthenticated" class="space-y-6">
        <div class="card">
          <h2 class="text-xl font-semibold mb-4">Welcome, {{ authStore.user?.full_name || authStore.user?.username }}!</h2>
          <p class="text-gray-600 mb-4">Role: <span class="font-medium capitalize">{{ authStore.user?.role }}</span></p>
          
          <div class="flex space-x-4">
            <RouterLink
              v-if="authStore.isAdmin"
              to="/admin"
              class="btn btn-primary"
            >
              Admin Dashboard
            </RouterLink>
            <RouterLink
              v-if="authStore.isOrganizer"
              to="/organizer"
              class="btn btn-primary"
            >
              Organizer Dashboard
            </RouterLink>
            <RouterLink
              v-if="authStore.isCoach"
              to="/coach"
              class="btn btn-primary"
            >
              Coach Dashboard
            </RouterLink>
            <RouterLink
              v-if="authStore.isPlayer"
              to="/player"
              class="btn btn-primary"
            >
              Player Dashboard
            </RouterLink>
          </div>
        </div>
      </div>
      
      <div v-else class="text-center">
        <p class="text-gray-600 mb-4">Please log in to access your dashboard</p>
        <RouterLink to="/login" class="btn btn-primary">Login</RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Navbar from '@/components/Navbar.vue'

const authStore = useAuthStore()
</script>
