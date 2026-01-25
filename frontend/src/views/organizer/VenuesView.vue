<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold text-gray-900">Venues</h2>
      <button @click="showCreateModal = true" class="btn btn-primary">Create Venue</button>
    </div>
    
    <div v-if="loading" class="text-center py-12">
      <p class="text-gray-600">Loading venues...</p>
    </div>
    
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="venue in venues" :key="venue.id" class="card">
        <h3 class="text-xl font-semibold mb-2">{{ venue.name }}</h3>
        <p v-if="venue.address" class="text-gray-600 mb-2">{{ venue.address }}</p>
        <p v-if="venue.capacity" class="text-sm text-gray-500">Capacity: {{ venue.capacity }}</p>
      </div>
    </div>
    
    <!-- Create Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-md w-full">
        <h3 class="text-xl font-semibold mb-4">Create Venue</h3>
        <form @submit.prevent="handleCreate">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Name</label>
              <input v-model="formData.name" type="text" required class="input" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Address</label>
              <textarea v-model="formData.address" class="input" rows="3"></textarea>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Capacity</label>
              <input v-model.number="formData.capacity" type="number" class="input" />
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
import type { Venue } from '@/types'

const venues = ref<Venue[]>([])
const loading = ref(true)
const showCreateModal = ref(false)
const formData = ref({
  name: '',
  address: '',
  capacity: null as number | null,
  institution_id: 0
})

const fetchVenues = async () => {
  try {
    const institution = await api.getMyInstitution()
    venues.value = await api.getVenues(institution.id)
  } catch (error) {
    console.error('Failed to fetch venues', error)
  } finally {
    loading.value = false
  }
}

const handleCreate = async () => {
  try {
    const institution = await api.getMyInstitution()
    await api.createVenue({
      ...formData.value,
      institution_id: institution.id
    })
    showCreateModal.value = false
    formData.value = { name: '', address: '', capacity: null, institution_id: 0 }
    await fetchVenues()
  } catch (error) {
    console.error('Failed to create venue', error)
  }
}

onMounted(() => {
  fetchVenues()
})
</script>
