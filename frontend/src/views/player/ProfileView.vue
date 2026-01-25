<template>
  <div>
    <h2 class="text-2xl font-bold text-gray-900 mb-6">My Profile</h2>
    <div v-if="loading" class="text-center py-12">
      <p class="text-gray-600">Loading profile...</p>
    </div>
    <div v-else-if="profile" class="card max-w-2xl">
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">User ID</label>
          <p class="text-gray-900">{{ profile.user_id }}</p>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Team ID</label>
          <p class="text-gray-900">{{ profile.team_id || 'Not assigned to a team' }}</p>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Jersey Number</label>
          <p class="text-gray-900">{{ profile.jersey_number || 'Not set' }}</p>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Position</label>
          <p class="text-gray-900">{{ profile.position || 'Not set' }}</p>
        </div>
        <div v-if="!profile.team_id" class="mt-6">
          <button @click="showJoinTeamModal = true" class="btn btn-primary">Join a Team</button>
        </div>
      </div>
    </div>
    
    <!-- Join Team Modal -->
    <div v-if="showJoinTeamModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-md w-full">
        <h3 class="text-xl font-semibold mb-4">Join Team</h3>
        <form @submit.prevent="handleJoinTeam">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Team ID</label>
              <input v-model.number="teamId" type="number" required class="input" />
            </div>
          </div>
          <div class="flex space-x-4 mt-6">
            <button type="submit" class="btn btn-primary flex-1">Join</button>
            <button type="button" @click="showJoinTeamModal = false" class="btn btn-secondary flex-1">Cancel</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/services/api'
import type { Player } from '@/types'

const profile = ref<Player | null>(null)
const loading = ref(true)
const showJoinTeamModal = ref(false)
const teamId = ref(0)

const fetchProfile = async () => {
  try {
    profile.value = await api.getMyProfile()
  } catch (error) {
    console.error('Failed to fetch profile', error)
  } finally {
    loading.value = false
  }
}

const handleJoinTeam = async () => {
  try {
    await api.joinTeam(teamId.value)
    showJoinTeamModal.value = false
    teamId.value = 0
    await fetchProfile()
  } catch (error) {
    console.error('Failed to join team', error)
  }
}

onMounted(() => {
  fetchProfile()
})
</script>
