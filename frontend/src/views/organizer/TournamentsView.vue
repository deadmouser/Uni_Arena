<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <div>
        <h2 class="text-2xl font-bold text-gray-900">Tournaments</h2>
        <p class="text-sm text-gray-600 mt-1">Total: {{ tournaments.length }}</p>
      </div>
      <button @click="showCreateModal = true" class="btn btn-primary">Add Tournament</button>
    </div>
    
    <!-- Filter Tabs -->
    <div class="mb-6 flex space-x-2 border-b border-gray-200">
      <button
        @click="selectedFilter = 'all'"
        class="px-4 py-2 font-medium text-sm border-b-2 transition-colors"
        :class="selectedFilter === 'all' ? 'border-primary-500 text-primary-600' : 'border-transparent text-gray-500 hover:text-gray-700'"
      >
        All ({{ tournaments.length }})
      </button>
      <button
        @click="selectedFilter = 'upcoming'"
        class="px-4 py-2 font-medium text-sm border-b-2 transition-colors"
        :class="selectedFilter === 'upcoming' ? 'border-primary-500 text-primary-600' : 'border-transparent text-gray-500 hover:text-gray-700'"
      >
        Upcoming ({{ filteredTournaments('upcoming').length }})
      </button>
      <button
        @click="selectedFilter = 'ongoing'"
        class="px-4 py-2 font-medium text-sm border-b-2 transition-colors"
        :class="selectedFilter === 'ongoing' ? 'border-primary-500 text-primary-600' : 'border-transparent text-gray-500 hover:text-gray-700'"
      >
        Ongoing ({{ filteredTournaments('ongoing').length }})
      </button>
      <button
        @click="selectedFilter = 'completed'"
        class="px-4 py-2 font-medium text-sm border-b-2 transition-colors"
        :class="selectedFilter === 'completed' ? 'border-primary-500 text-primary-600' : 'border-transparent text-gray-500 hover:text-gray-700'"
      >
        Completed ({{ filteredTournaments('completed').length }})
      </button>
    </div>
    
    <div v-if="loading" class="text-center py-12">
      <p class="text-gray-600">Loading tournaments...</p>
    </div>
    
    <div v-else-if="displayedTournaments.length === 0" class="text-center py-12">
      <p class="text-gray-600">No tournaments found</p>
    </div>
    
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="tournament in displayedTournaments" :key="tournament.id" class="card">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-xl font-semibold">{{ tournament.name }}</h3>
          <span class="px-2 py-1 text-xs font-semibold rounded"
            :class="{
              'bg-green-100 text-green-800': tournament.status === 'ongoing',
              'bg-blue-100 text-blue-800': tournament.status === 'upcoming',
              'bg-gray-100 text-gray-800': tournament.status === 'completed'
            }"
          >
            {{ tournament.status }}
          </span>
        </div>
        <p v-if="tournament.description" class="text-gray-600 mb-4">{{ tournament.description }}</p>
        <div class="text-sm text-gray-500">
          <p>Start: {{ formatDate(tournament.start_date) }}</p>
          <p v-if="tournament.end_date">End: {{ formatDate(tournament.end_date) }}</p>
        </div>
      </div>
    </div>
    
    <!-- Create Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-md w-full">
        <h3 class="text-xl font-semibold mb-4">Create Tournament</h3>
        <form @submit.prevent="handleCreate">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Name</label>
              <input v-model="formData.name" type="text" required class="input" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
              <textarea v-model="formData.description" class="input" rows="3"></textarea>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Start Date</label>
              <input v-model="formData.start_date" type="datetime-local" required class="input" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">End Date</label>
              <input v-model="formData.end_date" type="datetime-local" class="input" />
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
import { ref, onMounted, computed } from 'vue'
import api from '@/services/api'
import type { Tournament } from '@/types'

const tournaments = ref<Tournament[]>([])
const loading = ref(true)
const showCreateModal = ref(false)
const selectedFilter = ref<'all' | 'upcoming' | 'ongoing' | 'completed'>('all')
const formData = ref({
  name: '',
  description: '',
  start_date: '',
  end_date: '',
  institution_id: 0,
  is_public: true
})

const filteredTournaments = (filter: string) => {
  if (filter === 'all') return tournaments.value
  return tournaments.value.filter(t => t.status === filter)
}

const displayedTournaments = computed(() => {
  return filteredTournaments(selectedFilter.value)
})

const fetchTournaments = async () => {
  try {
    // Fetch tournaments for the organizer's institution
    const institution = await api.getMyInstitution()
    tournaments.value = await api.getTournaments(institution.id)
  } catch (error) {
    console.error('Failed to fetch tournaments', error)
  } finally {
    loading.value = false
  }
}

const handleCreate = async () => {
  try {
    // Get institution ID from user's institution
    const institution = await api.getMyInstitution()
    await api.createTournament({
      ...formData.value,
      institution_id: institution.id,
      start_date: new Date(formData.value.start_date).toISOString(),
      end_date: formData.value.end_date ? new Date(formData.value.end_date).toISOString() : undefined
    })
    showCreateModal.value = false
    formData.value = { name: '', description: '', start_date: '', end_date: '', institution_id: 0, is_public: true }
    await fetchTournaments()
  } catch (error) {
    console.error('Failed to create tournament', error)
  }
}

const formatDate = (dateString: string): string => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

onMounted(() => {
  fetchTournaments()
})
</script>
