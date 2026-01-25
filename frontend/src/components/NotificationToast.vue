<template>
  <TransitionGroup name="toast" tag="div" class="fixed top-4 right-4 z-50 space-y-2">
    <div
      v-for="notification in notifications"
      :key="notification.id"
      class="min-w-[300px] max-w-md rounded-lg shadow-lg p-4 flex items-start space-x-3"
      :class="{
        'bg-green-50 border border-green-200': notification.type === 'success',
        'bg-red-50 border border-red-200': notification.type === 'error',
        'bg-blue-50 border border-blue-200': notification.type === 'info'
      }"
    >
      <div class="flex-shrink-0">
        <svg
          v-if="notification.type === 'success'"
          class="w-5 h-5 text-green-600"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
        <svg
          v-else-if="notification.type === 'error'"
          class="w-5 h-5 text-red-600"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
        <svg
          v-else
          class="w-5 h-5 text-blue-600"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>
      <div class="flex-1">
        <p
          class="text-sm font-medium"
          :class="{
            'text-green-800': notification.type === 'success',
            'text-red-800': notification.type === 'error',
            'text-blue-800': notification.type === 'info'
          }"
        >
          {{ notification.message }}
        </p>
      </div>
      <button
        @click="removeNotification(notification.id)"
        class="flex-shrink-0 text-gray-400 hover:text-gray-600"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
  </TransitionGroup>
</template>

<script setup lang="ts">
import { notifications, removeNotification } from '@/composables/useNotifications'
</script>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(100%);
}
</style>
