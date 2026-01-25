<template>
  <div class="min-h-screen bg-gray-50">
    <Navbar />
    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <div class="mb-6">
          <h1 class="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
        </div>
        <!-- Secondary nav removed - items moved to top Navbar -->
        <RouterView />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import Navbar from '@/components/Navbar.vue'
</script>
