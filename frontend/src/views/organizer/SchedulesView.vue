<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold text-gray-900">Schedules</h2>
      <button @click="showCreateModal = true" class="btn btn-primary">Create Schedule</button>
    </div>
    
    <div v-if="loading" class="text-center py-12">
      <p class="text-gray-600">Loading schedules...</p>
    </div>
    
    <div v-else class="space-y-4">
      <div v-for="schedule in schedules" :key="schedule.id" class="card">
        <div class="flex justify-between items-center">
          <div>
            <h3 class="text-xl font-semibold">{{ schedule.name }}</h3>
            <p class="text-sm text-gray-500 mt-1">{{ schedule.schedule_type }}</p>
            <p class="text-sm text-gray-600 mt-2">
              {{ formatDate(schedule.start_date) }}
              <span v-if="schedule.end_date"> - {{ formatDate(schedule.end_date) }}</span>
            </p>
          </div>
          <span class="px-3 py-1 rounded text-sm font-semibold bg-primary-100 text-primary-800">
            {{ schedule.schedule_type }}
          </span>
        </div>
      </div>
    </div>
    
    <!-- Create Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-md w-full">
        <h3 class="text-xl font-semibold mb-4">Create Schedule</h3>
        <form @submit.prevent="handleCreate">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Name</label>
              <input v-model="formData.name" type="text" required class="input" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Type</label>
              <select v-model="formData.schedule_type" class="input" required>
                <option value="round_robin">Round Robin</option>
                <option value="knockout">Knockout</option>
                <option value="league">League</option>
                <option value="custom">Custom</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Start Date</label>
              <input v-model="formData.start_date" type="datetime-local" required class="input" />
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
import type { Schedule } from '@/types'

const schedules = ref<Schedule[]>([])
const loading = ref(true)
const showCreateModal = ref(false)
const formData = ref({
  name: '',
  schedule_type: 'round_robin' as 'round_robin' | 'knockout' | 'league' | 'custom',
  start_date: '',
  sport_id: 0
})

const fetchSchedules = async () => {
  try {
    schedules.value = await api.getSchedules()
  } catch (error) {
    console.error('Failed to fetch schedules', error)
  } finally {
    loading.value = false
  }
}

const handleCreate = async () => {
  try {
    await api.createSchedule({
      ...formData.value,
      start_date: new Date(formData.value.start_date).toISOString()
    })
    showCreateModal.value = false
    formData.value = { name: '', schedule_type: 'round_robin', start_date: '', sport_id: 0 }
    await fetchSchedules()
  } catch (error) {
    console.error('Failed to create schedule', error)
  }
}

const formatDate = (dateString: string): string => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}

onMounted(() => {
  fetchSchedules()
})
</script>
