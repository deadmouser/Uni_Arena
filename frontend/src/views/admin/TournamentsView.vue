<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold text-gray-900">Manage Tournaments</h2>
      <!-- Future: Add ability for admin to feature tournaments or other global actions -->
    </div>
    
    <div v-if="loading" class="text-center py-12">
      <p class="text-gray-600">Loading tournaments...</p>
    </div>
    
    <div v-else class="card overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Institution ID</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Start Date</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Visibility</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="tournament in tournaments" :key="tournament.id">
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm font-medium text-gray-900">{{ tournament.name }}</div>
              <div class="text-xs text-gray-500">{{ tournament.description?.substring(0, 30) }}...</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-900">{{ tournament.institution_id }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-900">{{ formatDate(tournament.start_date) }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span class="px-2 py-1 text-xs font-semibold rounded" :class="getStatusClass(tournament.status)">
                {{ tournament.status }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span :class="tournament.is_public ? 'text-green-600' : 'text-gray-600'" class="text-sm font-medium">
                {{ tournament.is_public ? 'Public' : 'Private' }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
              <button
                @click="confirmDelete(tournament)"
                class="text-red-600 hover:text-red-900"
              >
                Delete
              </button>
            </td>
          </tr>
          <tr v-if="tournaments.length === 0">
            <td colspan="6" class="px-6 py-12 text-center text-gray-500">
              No tournaments found.
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4">
        <h3 class="text-xl font-semibold mb-4 text-red-600">Delete Tournament</h3>
        <p class="text-gray-700 mb-6">
          Are you sure you want to delete <strong>{{ tournamentToDelete?.name }}</strong>? This action cannot be undone.
        </p>
        <div class="flex space-x-4">
          <button
            @click="handleDelete"
            :disabled="submitting"
            class="btn bg-red-600 hover:bg-red-700 text-white flex-1"
          >
            <span v-if="submitting">Deleting...</span>
            <span v-else>Delete</span>
          </button>
          <button
            @click="showDeleteModal = false; tournamentToDelete = null"
            :disabled="submitting"
            class="btn btn-secondary flex-1"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/services/api'
import { useNotifications } from '@/composables/useNotifications'
import type { Tournament } from '@/types'

const { success, error } = useNotifications()

const tournaments = ref<Tournament[]>([])
const loading = ref(true)
const showDeleteModal = ref(false)
const submitting = ref(false)
const tournamentToDelete = ref<Tournament | null>(null)

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString()
}

const getStatusClass = (status: string) => {
  switch (status) {
    case 'upcoming': return 'bg-blue-100 text-blue-800'
    case 'ongoing': return 'bg-green-100 text-green-800'
    case 'completed': return 'bg-gray-100 text-gray-800'
    case 'cancelled': return 'bg-red-100 text-red-800'
    default: return 'bg-gray-100 text-gray-800'
  }
}

const fetchTournaments = async () => {
  try {
    loading.value = true
    tournaments.value = await api.getAdminTournaments()
  } catch (err: any) {
    error(err.response?.data?.detail || 'Failed to fetch tournaments')
  } finally {
    loading.value = false
  }
}

const confirmDelete = (tournament: Tournament) => {
  tournamentToDelete.value = tournament
  showDeleteModal.value = true
}

const handleDelete = async () => {
  if (!tournamentToDelete.value) return
  
  try {
    submitting.value = true
    await api.deleteAdminTournament(tournamentToDelete.value.id)
    success('Tournament deleted successfully')
    showDeleteModal.value = false
    tournamentToDelete.value = null
    await fetchTournaments()
  } catch (err: any) {
    error(err.response?.data?.detail || 'Failed to delete tournament')
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  fetchTournaments()
})
</script>
