<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold text-gray-900">Teams</h2>
      <button @click="showCreateModal = true" class="btn btn-primary">Create Team</button>
    </div>
    
    <div v-if="loading" class="text-center py-12">
      <p class="text-gray-600">Loading teams...</p>
    </div>
    
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="team in teams" :key="team.id" class="card">
        <h3 class="text-xl font-semibold mb-2">{{ team.name }}</h3>
        <p v-if="team.code" class="text-sm text-gray-500 mb-4">{{ team.code }}</p>
        <div class="text-sm text-gray-600">
          <p>Sport ID: {{ team.sport_id }}</p>
          <p>Institution ID: {{ team.institution_id }}</p>
        </div>
      </div>
    </div>
    
    <!-- Create Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-md w-full">
        <h3 class="text-xl font-semibold mb-4">Create Team</h3>
        <form @submit.prevent="handleCreate">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Name</label>
              <input v-model="formData.name" type="text" required class="input" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Code</label>
              <input v-model="formData.code" type="text" class="input" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Sport ID</label>
              <input v-model.number="formData.sport_id" type="number" required class="input" />
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
import type { Team } from '@/types'

const teams = ref<Team[]>([])
const loading = ref(true)
const showCreateModal = ref(false)
const formData = ref({
  name: '',
  code: '',
  institution_id: 0,
  sport_id: 0
})

const fetchTeams = async () => {
  try {
    const institution = await api.getMyInstitution()
    teams.value = await api.getTeams(undefined, institution.id)
  } catch (error) {
    console.error('Failed to fetch teams', error)
  } finally {
    loading.value = false
  }
}

const handleCreate = async () => {
  try {
    const institution = await api.getMyInstitution()
    await api.createTeam({
      ...formData.value,
      institution_id: institution.id
    })
    showCreateModal.value = false
    formData.value = { name: '', code: '', institution_id: 0, sport_id: 0 }
    await fetchTeams()
  } catch (error) {
    console.error('Failed to create team', error)
  }
}

onMounted(() => {
  fetchTeams()
})
</script>
