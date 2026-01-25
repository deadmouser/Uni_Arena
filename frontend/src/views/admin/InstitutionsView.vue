<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold text-gray-900">Institutions</h2>
      <button @click="openCreateModal" class="btn btn-primary">Create Institution</button>
    </div>
    
    <div v-if="loading" class="text-center py-12">
      <p class="text-gray-600">Loading institutions...</p>
    </div>
    
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="institution in institutions" :key="institution.id" class="card">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-xl font-semibold">{{ institution.name }}</h3>
          <span class="text-sm text-gray-500">{{ institution.code }}</span>
        </div>
        <p v-if="institution.description" class="text-gray-600 mb-4">{{ institution.description }}</p>
        <div class="text-sm text-gray-500 space-y-1 mb-4">
          <p v-if="institution.contact_email">{{ institution.contact_email }}</p>
          <p v-if="institution.address">{{ institution.address }}</p>
        </div>
        <div class="flex items-center justify-between">
          <span
            :class="institution.is_active ? 'text-green-600' : 'text-red-600'"
            class="text-sm font-medium"
          >
            {{ institution.is_active ? 'Active' : 'Inactive' }}
          </span>
          <div class="flex space-x-2">
            <button
              @click="openEditModal(institution)"
              class="px-3 py-1 text-sm bg-blue-100 text-blue-700 rounded hover:bg-blue-200 transition-colors"
            >
              Edit
            </button>
            <button
              @click="confirmDelete(institution)"
              class="px-3 py-1 text-sm bg-red-100 text-red-700 rounded hover:bg-red-200 transition-colors"
            >
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Create/Edit Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click.self="closeModal">
      <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4 max-h-[90vh] overflow-y-auto">
        <h3 class="text-xl font-semibold mb-4">{{ editingInstitution ? 'Edit Institution' : 'Create Institution' }}</h3>
        <form @submit.prevent="handleSubmit">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Name *</label>
              <input v-model="formData.name" type="text" required class="input" />
            </div>
            <!-- Code is auto-generated -->
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
              <textarea v-model="formData.description" class="input" rows="3"></textarea>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Logo</label>
              <input @change="handleFileUpload" type="file" accept="image/*" class="input" />
              <p class="text-xs text-gray-500 mt-1">Upload a logo image (JPG, PNG)</p>
            </div>
            <div v-if="editingInstitution" class="flex items-center">
              <input
                v-model="formData.is_active"
                type="checkbox"
                id="is_active"
                class="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
              />
              <label for="is_active" class="ml-2 text-sm text-gray-700">Active</label>
            </div>
          </div>
          <div class="flex space-x-4 mt-6">
            <button type="submit" :disabled="submitting" class="btn btn-primary flex-1">
              <span v-if="submitting">{{ editingInstitution ? 'Updating...' : 'Creating...' }}</span>
              <span v-else>{{ editingInstitution ? 'Update' : 'Create' }}</span>
            </button>
            <button type="button" @click="closeModal" :disabled="submitting" class="btn btn-secondary flex-1">Cancel</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4">
        <h3 class="text-xl font-semibold mb-4 text-red-600">Delete Institution</h3>
        <p class="text-gray-700 mb-6">
          Are you sure you want to delete <strong>{{ institutionToDelete?.name }}</strong>? This action cannot be undone.
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
            @click="showDeleteModal = false; institutionToDelete = null"
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
import type { Institution } from '@/types'

const { success, error } = useNotifications()

const institutions = ref<Institution[]>([])
const loading = ref(true)
const showModal = ref(false)
const showDeleteModal = ref(false)
const submitting = ref(false)
const editingInstitution = ref<Institution | null>(null)
const institutionToDelete = ref<Institution | null>(null)

  const formData = ref({
  name: '',
  contact_email: '',
  contact_phone: '',
  address: '',
  description: '',
  is_active: true
})

const logoFile = ref<File | null>(null)

const handleFileUpload = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    logoFile.value = target.files[0]
  }
}

const resetForm = () => {
  formData.value = {
    name: '',
    contact_email: '',
    contact_phone: '',
    address: '',
    description: '',
    is_active: true
  }
  logoFile.value = null
  editingInstitution.value = null
}

const openCreateModal = () => {
  resetForm()
  showModal.value = true
}

const openEditModal = (institution: Institution) => {
  editingInstitution.value = institution
  formData.value = {
    name: institution.name,
    contact_email: institution.contact_email || '',
    contact_phone: institution.contact_phone || '',
    address: institution.address || '',
    description: institution.description || '',
    is_active: institution.is_active
  }
  showModal.value = true
}

const closeModal = () => {
  if (!submitting.value) {
    showModal.value = false
    resetForm()
  }
}

const confirmDelete = (institution: Institution) => {
  institutionToDelete.value = institution
  showDeleteModal.value = true
}

const fetchInstitutions = async () => {
  try {
    loading.value = true
    institutions.value = await api.getInstitutions()
  } catch (err: any) {
    error(err.response?.data?.detail || 'Failed to fetch institutions')
  } finally {
    loading.value = false
  }
}

const handleSubmit = async () => {
  try {
    submitting.value = true
    if (editingInstitution.value) {
      await api.updateInstitution(editingInstitution.value.id, formData.value)
      success('Institution updated successfully')
    } else {
      // Create FormData for creation
      const data = new FormData()
      data.append('name', formData.value.name)
      if (formData.value.contact_email) data.append('contact_email', formData.value.contact_email)
      if (formData.value.contact_phone) data.append('contact_phone', formData.value.contact_phone)
      if (formData.value.address) data.append('address', formData.value.address)
      if (formData.value.description) data.append('description', formData.value.description)
      
      if (logoFile.value) {
        data.append('logo', logoFile.value)
      }
      
      await api.createInstitution(data)
      success('Institution created successfully')
    }
    closeModal()
    await fetchInstitutions()
  } catch (err: any) {
    error(err.response?.data?.detail || `Failed to ${editingInstitution.value ? 'update' : 'create'} institution`)
  } finally {
    submitting.value = false
  }
}

const handleDelete = async () => {
  if (!institutionToDelete.value) return
  
  try {
    submitting.value = true
    await api.deleteInstitution(institutionToDelete.value.id)
    success('Institution deleted successfully')
    showDeleteModal.value = false
    institutionToDelete.value = null
    await fetchInstitutions()
  } catch (err: any) {
    error(err.response?.data?.detail || 'Failed to delete institution')
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  fetchInstitutions()
})
</script>
