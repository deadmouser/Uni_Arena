import { ref } from 'vue'

export interface Notification {
  id: number
  type: 'success' | 'error' | 'info'
  message: string
  duration?: number
}

// Shared state for notifications
export const notifications = ref<Notification[]>([])
let notificationId = 0

const removeNotification = (id: number) => {
  const index = notifications.value.findIndex(n => n.id === id)
  if (index > -1) {
    notifications.value.splice(index, 1)
  }
}

const addNotification = (notification: Omit<Notification, 'id'>) => {
  const id = ++notificationId
  const newNotification: Notification = {
    ...notification,
    id,
    duration: notification.duration || 3000
  }
  notifications.value.push(newNotification)

  if (newNotification.duration > 0) {
    setTimeout(() => {
      removeNotification(id)
    }, newNotification.duration)
  }
}

export const useNotifications = () => {
  const success = (message: string, duration?: number) => {
    addNotification({ type: 'success', message, duration })
  }

  const error = (message: string, duration?: number) => {
    addNotification({ type: 'error', message, duration: duration || 5000 })
  }

  const info = (message: string, duration?: number) => {
    addNotification({ type: 'info', message, duration })
  }

  return {
    success,
    error,
    info
  }
}

// Export removeNotification for use in NotificationToast component
export { removeNotification }
