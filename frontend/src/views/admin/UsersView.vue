<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold text-gray-900">Users</h2>
      <button @click="openCreateModal" class="btn btn-primary">Create User</button>
    </div>
    
    <div v-if="loading" class="text-center py-12">
      <p class="text-gray-600">Loading users...</p>
    </div>
    
    <div v-else class="card overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Username</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Role</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="user in users" :key="user.id">
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm font-medium text-gray-900">{{ user.full_name || user.username }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-900">{{ user.email }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-500">{{ user.username }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span class="px-2 py-1 text-xs font-semibold rounded" :class="getRoleClass(user.role)">
                {{ user.role }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span :class="user.is_active ? 'text-green-600' : 'text-red-600'" class="text-sm font-medium">
                {{ user.is_active ? 'Active' : 'Inactive' }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
              <div class="flex space-x-2">
                <button
                  @click="openEditModal(user)"
                  class="text-blue-600 hover:text-blue-900"
                >
                  Edit
                </button>
                <button
                  @click="confirmDelete(user)"
                  :disabled="user.id === currentUserId"
                  class="text-red-600 hover:text-red-900 disabled:text-gray-400 disabled:cursor-not-allowed"
                >
                  Delete
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <!-- Create/Edit Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click.self="closeModal">
      <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4 max-h-[90vh] overflow-y-auto">
        <h3 class="text-xl font-semibold mb-4">{{ editingUser ? 'Edit User' : 'Create User' }}</h3>
        <form @submit.prevent="handleSubmit">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Email *</label>
              <input v-model="formData.email" type="email" required class="input" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Username *</label>
              <input v-model="formData.username" type="text" required class="input" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
              <input v-model="formData.full_name" type="text" class="input" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Role *</label>
              <select v-model="formData.role" class="input" required>
                <option value="admin">Admin</option>
                <option value="organizer">Organizer</option>
                <option value="coach">Coach</option>
                <option value="player">Player</option>
                <option value="viewer">Viewer</option>
              </select>
            </div>
            <div v-if="!editingUser">
              <label class="block text-sm font-medium text-gray-700 mb-1">Password *</label>
              <input v-model="formData.password" type="password" required class="input" />
            </div>
            <div v-else>
              <label class="block text-sm font-medium text-gray-700 mb-1">New Password (leave blank to keep current)</label>
              <input v-model="formData.password" type="password" class="input" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Institution ID (optional)</label>
              <input v-model.number="formData.institution_id" type="number" class="input" />
            </div>
            <div v-if="editingUser" class="flex items-center">
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
              <span v-if="submitting">{{ editingUser ? 'Updating...' : 'Creating...' }}</span>
              <span v-else>{{ editingUser ? 'Update' : 'Create' }}</span>
            </button>
            <button type="button" @click="closeModal" :disabled="submitting" class="btn btn-secondary flex-1">Cancel</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4">
        <h3 class="text-xl font-semibold mb-4 text-red-600">Delete User</h3>
        <p class="text-gray-700 mb-6">
          Are you sure you want to delete <strong>{{ userToDelete?.full_name || userToDelete?.username }}</strong> ({{ userToDelete?.email }})? This action cannot be undone.
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
            @click="showDeleteModal = false; userToDelete = null"
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
import { ref, onMounted, computed } from 'vue'
import api from '@/services/api'
import { useAuthStore } from '@/stores/auth'
import { useNotifications } from '@/composables/useNotifications'
import type { User } from '@/types'

const { success, error } = useNotifications()
const authStore = useAuthStore()

const users = ref<User[]>([])
const loading = ref(true)
const showModal = ref(false)
const showDeleteModal = ref(false)
const submitting = ref(false)
const editingUser = ref<User | null>(null)
const userToDelete = ref<User | null>(null)

const currentUserId = computed(() => authStore.user?.id)

const formData = ref({
  email: '',
  username: '',
  full_name: '',
  password: '',
  role: 'viewer' as User['role'],
  institution_id: null as number | null,
  is_active: true
})

const getRoleClass = (role: string) => {
  const classes: Record<string, string> = {
    admin: 'bg-purple-100 text-purple-800',
    organizer: 'bg-blue-100 text-blue-800',
    coach: 'bg-green-100 text-green-800',
    player: 'bg-yellow-100 text-yellow-800',
    viewer: 'bg-gray-100 text-gray-800'
  }
  return classes[role] || classes.viewer
}

const resetForm = () => {
  formData.value = {
    email: '',
    username: '',
    full_name: '',
    password: '',
    role: 'viewer',
    institution_id: null,
    is_active: true
  }
  editingUser.value = null
}

const openCreateModal = () => {
  resetForm()
  showModal.value = true
}

const openEditModal = (user: User) => {
  editingUser.value = user
  formData.value = {
    email: user.email,
    username: user.username,
    full_name: user.full_name || '',
    password: '',
    role: user.role,
    institution_id: user.institution_id || null,
    is_active: user.is_active
  }
  showModal.value = true
}

const closeModal = () => {
  if (!submitting.value) {
    showModal.value = false
    resetForm()
  }
}

const confirmDelete = (user: User) => {
  userToDelete.value = user
  showDeleteModal.value = true
}

const fetchUsers = async () => {
  try {
    loading.value = true
    users.value = await api.getUsers()
  } catch (err: any) {
    error(err.response?.data?.detail || 'Failed to fetch users')
  } finally {
    loading.value = false
  }
}

const handleSubmit = async () => {
  try {
    submitting.value = true
    const submitData: any = {
      email: formData.value.email,
      username: formData.value.username,
      full_name: formData.value.full_name || undefined,
      role: formData.value.role,
      institution_id: formData.value.institution_id || undefined,
      is_active: formData.value.is_active
    }
    
    // Only include password if provided (for updates) or required (for creates)
    if (!editingUser.value || formData.value.password) {
      submitData.password = formData.value.password
    }
    
    if (editingUser.value) {
      await api.updateUser(editingUser.value.id, submitData)
      success('User updated successfully')
    } else {
      await api.createUser(submitData)
      success('User created successfully')
    }
    closeModal()
    await fetchUsers()
  } catch (err: any) {
    error(err.response?.data?.detail || `Failed to ${editingUser.value ? 'update' : 'create'} user`)
  } finally {
    submitting.value = false
  }
}

const handleDelete = async () => {
  if (!userToDelete.value) return
  
  try {
    submitting.value = true
    await api.deleteUser(userToDelete.value.id)
    success('User deleted successfully')
    showDeleteModal.value = false
    userToDelete.value = null
    await fetchUsers()
  } catch (err: any) {
    error(err.response?.data?.detail || 'Failed to delete user')
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  fetchUsers()
})
</script>
