<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Create your account
        </h2>
      </div>
      <form class="mt-8 space-y-6" @submit.prevent="handleRegister">
        <div v-if="authStore.error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
          {{ authStore.error }}
        </div>
        <div class="space-y-4">
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
            <input
              id="email"
              v-model="formData.email"
              name="email"
              type="email"
              required
              class="mt-1 input"
              placeholder="Email address"
            />
          </div>
          <div>
            <label for="username" class="block text-sm font-medium text-gray-700">Username</label>
            <input
              id="username"
              v-model="formData.username"
              name="username"
              type="text"
              required
              class="mt-1 input"
              placeholder="Username"
            />
          </div>
          <div>
            <label for="full_name" class="block text-sm font-medium text-gray-700">Full Name</label>
            <input
              id="full_name"
              v-model="formData.full_name"
              name="full_name"
              type="text"
              class="mt-1 input"
              placeholder="Full Name"
            />
          </div>
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
            <input
              id="password"
              v-model="formData.password"
              name="password"
              type="password"
              required
              class="mt-1 input"
              placeholder="Password"
            />
          </div>
          <div>
            <label for="role" class="block text-sm font-medium text-gray-700">Role</label>
            <select
              id="role"
              v-model="formData.role"
              name="role"
              class="mt-1 input"
            >
              <option value="viewer">Viewer</option>
              <option value="player">Player</option>
            </select>
          </div>
        </div>

        <div>
          <button
            type="submit"
            :disabled="authStore.loading"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
          >
            <span v-if="authStore.loading">Creating account...</span>
            <span v-else>Register</span>
          </button>
        </div>

        <div class="text-center">
          <RouterLink to="/login" class="text-primary-600 hover:text-primary-500">
            Already have an account? Sign in
          </RouterLink>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { RouterLink } from 'vue-router'

const router = useRouter()
const authStore = useAuthStore()

const formData = ref({
  email: '',
  username: '',
  full_name: '',
  password: '',
  role: 'viewer'
})

const handleRegister = async () => {
  try {
    await authStore.register(formData.value)
    router.push('/login')
  } catch (error) {
    // Error is handled by the store
  }
}
</script>
