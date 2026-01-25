<template>
  <div class="min-h-screen bg-gray-50">
    <InstitutionNavbar />
    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <RouterView />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import InstitutionNavbar from '@/components/InstitutionNavbar.vue'
</script>
