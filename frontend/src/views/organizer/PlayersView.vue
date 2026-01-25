<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold text-gray-900">Players</h2>
      <button @click="showCreateModal = true" class="btn btn-primary">Add Player</button>
    </div>
    
    <div v-if="loading" class="text-center py-12">
      <p class="text-gray-600">Loading players...</p>
    </div>
    
    <div v-else class="card overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">User ID</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Team</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Jersey</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Position</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="player in players" :key="player.id">
            <td class="px-6 py-4 whitespace-nowrap">{{ player.user_id }}</td>
            <td class="px-6 py-4 whitespace-nowrap">{{ player.team_id || 'No Team' }}</td>
            <td class="px-6 py-4 whitespace-nowrap">{{ player.jersey_number || '-' }}</td>
            <td class="px-6 py-4 whitespace-nowrap">{{ player.position || '-' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <!-- Create Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-md w-full">
        <h3 class="text-xl font-semibold mb-4">Add Player</h3>
        <form @submit.prevent="handleCreate">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">User ID</label>
              <input v-model.number="formData.user_id" type="number" required class="input" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Team ID</label>
              <input v-model.number="formData.team_id" type="number" class="input" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Jersey Number</label>
              <input v-model.number="formData.jersey_number" type="number" class="input" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Position</label>
              <input v-model="formData.position" type="text" class="input" />
            </div>
          </div>
          <div class="flex space-x-4 mt-6">
            <button type="submit" class="btn btn-primary flex-1">Create</button>
            <button type="button" @click="showCreateModal = false" class="btn btn-secondary flex-1">Cancel</button>
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

const players = ref<Player[]>([])
const loading = ref(true)
const showCreateModal = ref(false)
const formData = ref({
  user_id: 0,
  team_id: null as number | null,
  jersey_number: null as number | null,
  position: null as string | null
})

const fetchPlayers = async () => {
  try {
    players.value = await api.getPlayers()
  } catch (error) {
    console.error('Failed to fetch players', error)
  } finally {
    loading.value = false
  }
}

const handleCreate = async () => {
  try {
    await api.createPlayer(formData.value)
    showCreateModal.value = false
    formData.value = { user_id: 0, team_id: null, jersey_number: null, position: null }
    await fetchPlayers()
  } catch (error) {
    console.error('Failed to create player', error)
  }
}

onMounted(() => {
  fetchPlayers()
})
</script>
