<template>
  <div>
    <h2 class="text-2xl font-bold text-gray-900 mb-6">Institution Profile</h2>
    
    <div v-if="loading" class="text-center py-12">
      <p class="text-gray-600">Loading institution...</p>
    </div>
    
    <div v-else-if="institution" class="card max-w-2xl">
      <form @submit.prevent="handleUpdate">
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Name</label>
            <input v-model="formData.name" type="text" required class="input" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Code</label>
            <input v-model="formData.code" type="text" required class="input" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Logo URL</label>
            <input v-model="formData.logo_url" type="url" class="input" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input v-model="formData.contact_email" type="email" class="input" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Phone</label>
            <input v-model="formData.contact_phone" type="tel" class="input" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Address</label>
            <textarea v-model="formData.address" class="input" rows="3"></textarea>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
            <textarea v-model="formData.description" class="input" rows="4"></textarea>
          </div>
        </div>
        <div class="mt-6">
          <button type="submit" class="btn btn-primary">Update Institution</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/services/api'
import type { Institution } from '@/types'

const institution = ref<Institution | null>(null)
const loading = ref(true)
const formData = ref({
  name: '',
  code: '',
  logo_url: '',
  contact_email: '',
  contact_phone: '',
  address: '',
  description: ''
})

const fetchInstitution = async () => {
  try {
    institution.value = await api.getMyInstitution()
    formData.value = {
      name: institution.value.name,
      code: institution.value.code,
      logo_url: institution.value.logo_url || '',
      contact_email: institution.value.contact_email || '',
      contact_phone: institution.value.contact_phone || '',
      address: institution.value.address || '',
      description: institution.value.description || ''
    }
  } catch (error) {
    console.error('Failed to fetch institution', error)
  } finally {
    loading.value = false
  }
}

const handleUpdate = async () => {
  try {
    institution.value = await api.updateMyInstitution(formData.value)
  } catch (error) {
    console.error('Failed to update institution', error)
  }
}

onMounted(() => {
  fetchInstitution()
})
</script>
