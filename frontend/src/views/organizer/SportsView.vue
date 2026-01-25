<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold text-gray-900">Sports Management</h2>
      <button @click="openTemplateModal" class="btn btn-primary">Add New Sport</button>
    </div>
    
    <div v-if="loading" class="text-center py-12">
      <p class="text-gray-600">Loading sports...</p>
    </div>
    
    <div v-else-if="sports.length === 0" class="text-center py-12 bg-white rounded-lg shadow">
      <h3 class="text-lg font-medium text-gray-900 mb-2">No Sports Added Yet</h3>
      <p class="text-gray-500 mb-4">Start by adding a sport from our templates.</p>
      <button @click="openTemplateModal" class="btn btn-primary">Add Sport</button>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="sport in sports" :key="sport.id" class="card hover:shadow-md transition-shadow">
        <div class="flex justify-between items-start mb-2">
          <h3 class="text-xl font-bold text-gray-900">{{ sport.name }}</h3>
          <span class="px-2 py-1 text-xs font-semibold rounded uppercase"
            :class="{
              'bg-blue-100 text-blue-800': sport.sport_type === 'team',
              'bg-green-100 text-green-800': sport.sport_type === 'individual',
              'bg-purple-100 text-purple-800': sport.sport_type === 'mixed'
            }"
          >
            {{ sport.sport_type }}
          </span>
        </div>
        <p class="text-sm text-gray-500 mb-4">Code: {{ sport.code }}</p>
        
        <div class="space-y-2 mb-4">
          <p v-if="sport.min_players_per_team" class="text-sm text-gray-600">
            <span class="font-medium">Players:</span> {{ sport.min_players_per_team }} - {{ sport.max_players_per_team }}
          </p>
        </div>

        <div class="border-t pt-4 mt-4">
          <h4 class="text-sm font-semibold text-gray-700 mb-2">Rules & Config</h4>
          <p class="text-xs text-gray-500 line-clamp-3">
            {{ getRulesSummary(sport) }}
          </p>
        </div>
      </div>
    </div>
    
    <!-- Template Selection Modal -->
    <div v-if="showTemplateModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] flex flex-col">
        <div class="p-6 border-b flex justify-between items-center">
          <h3 class="text-xl font-bold text-gray-900">Select Sport Template</h3>
          <button @click="showTemplateModal = false" class="text-gray-400 hover:text-gray-500">
            <span class="sr-only">Close</span>
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div class="p-6 overflow-y-auto flex-grow bg-gray-50">
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div 
              v-for="template in templates" 
              :key="template.code"
              class="bg-white p-6 rounded-lg border-2 cursor-pointer transition-all hover:border-primary-500 hover:shadow-lg"
              :class="selectedTemplate?.code === template.code ? 'border-primary-500 ring-2 ring-primary-200' : 'border-transparent shadow-sm'"
              @click="selectTemplate(template)"
            >
              <div class="flex justify-between items-start mb-2">
                <h4 class="text-lg font-bold text-gray-900">{{ template.name }}</h4>
                <span class="text-xs font-semibold px-2 py-1 rounded bg-gray-100 text-gray-600">{{ template.sport_type }}</span>
              </div>
              <p class="text-sm text-gray-500 mb-4">{{ template.description }}</p>
              
              <div class="space-y-2">
                <div class="text-xs text-gray-500">
                  <strong>Match Config:</strong> 
                  {{ template.match_config.scoring_type }} based
                </div>
                <div class="text-xs text-gray-500">
                  <strong>Mandatory Rules:</strong> {{ template.mandatory_rules.length }}
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="p-6 border-t bg-white flex justify-end space-x-4">
          <button @click="showTemplateModal = false" class="btn btn-secondary">Cancel</button>
          <button 
            @click="createSportFromTemplate" 
            :disabled="!selectedTemplate || submitting"
            class="btn btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="submitting">Creating...</span>
            <span v-else>Add {{ selectedTemplate ? selectedTemplate.name : 'Sport' }}</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/services/api'
import type { Sport } from '@/types'
import { useNotifications } from '@/composables/useNotifications'

const { success, error } = useNotifications()

const sports = ref<Sport[]>([])
const templates = ref<any[]>([])
const loading = ref(true)
const submitting = ref(false)
const showTemplateModal = ref(false)
const selectedTemplate = ref<any | null>(null)

const fetchSports = async () => {
  try {
    loading.value = true
    const institution = await api.getMyInstitution()
    sports.value = await api.getSports(institution.id)
  } catch (err: any) {
    console.error('Failed to fetch sports', err)
    error('Failed to load sports')
  } finally {
    loading.value = false
  }
}

const fetchTemplates = async () => {
  try {
    templates.value = await api.getSportTemplates()
  } catch (err: any) {
    console.error('Failed to fetch templates', err)
  }
}

const openTemplateModal = () => {
  selectedTemplate.value = null
  showTemplateModal.value = true
  if (templates.value.length === 0) {
    fetchTemplates()
  }
}

const selectTemplate = (template: any) => {
  selectedTemplate.value = template
}

const createSportFromTemplate = async () => {
  if (!selectedTemplate.value) return

  try {
    submitting.value = true
    const institution = await api.getMyInstitution()
    
    await api.createSport({
      name: selectedTemplate.value.name,
      code: selectedTemplate.value.code,
      sport_type: selectedTemplate.value.sport_type,
      institution_id: institution.id,
      template_code: selectedTemplate.value.code
    })
    
    success(`${selectedTemplate.value.name} added successfully! Rules and configurations have been applied.`)
    showTemplateModal.value = false
    await fetchSports()
  } catch (err: any) {
    error(err.response?.data?.detail || 'Failed to create sport')
  } finally {
    submitting.value = false
  }
}

const getRulesSummary = (sport: any) => {
  try {
    const rules = typeof sport.rules === 'string' ? JSON.parse(sport.rules) : sport.rules
    if (Array.isArray(rules) && rules.length > 0) {
      return rules.slice(0, 3).join('. ') + (rules.length > 3 ? '...' : '')
    }
    return 'No specific rules configured.'
  } catch (e) {
    return 'Rules available'
  }
}

onMounted(() => {
  fetchSports()
})
</script>
