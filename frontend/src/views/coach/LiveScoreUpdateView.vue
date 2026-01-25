<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
    <!-- Header with End Match Button -->
    <div class="bg-white shadow-md sticky top-0 z-10">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div class="flex justify-between items-center">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">{{ match?.home_team?.name || 'Team 1' }} vs {{ match?.away_team?.name || 'Team 2' }}</h1>
            <p class="text-sm text-gray-600 mt-1">{{ match?.sport?.name || 'Match' }} - {{ formatDate(match?.scheduled_time) }}</p>
          </div>
          <button
            @click="handleEndMatch"
            :disabled="match?.status === 'completed'"
            class="px-6 py-3 bg-red-600 text-white font-semibold rounded-lg shadow-lg hover:bg-red-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors flex items-center space-x-2"
          >
            <span>End Match</span>
          </button>
        </div>
      </div>
    </div>

    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Score Display -->
      <div class="bg-white rounded-xl shadow-lg p-8 mb-6">
        <div class="grid grid-cols-2 gap-8">
          <!-- Home Team Score -->
          <div class="text-center">
            <h3 class="text-lg font-semibold text-gray-700 mb-4">{{ match?.home_team?.name || 'Home Team' }}</h3>
            <div class="text-7xl font-bold text-primary-600 mb-2">{{ getDisplayScore('home') }}</div>
            <div v-if="getSecondaryScore('home')" class="text-xl text-gray-600 mb-2">{{ getSecondaryScore('home') }}</div>
          </div>

          <!-- Away Team Score -->
          <div class="text-center">
            <h3 class="text-lg font-semibold text-gray-700 mb-4">{{ match?.away_team?.name || 'Away Team' }}</h3>
            <div class="text-7xl font-bold text-primary-600 mb-2">{{ getDisplayScore('away') }}</div>
            <div v-if="getSecondaryScore('away')" class="text-xl text-gray-600 mb-2">{{ getSecondaryScore('away') }}</div>
          </div>
        </div>

        <!-- Period/Over/Set Info -->
        <div v-if="score.period || getPeriodInfo()" class="mt-6 text-center">
          <span class="px-4 py-2 bg-gray-100 rounded-lg text-gray-700 font-medium">{{ score.period || getPeriodInfo() }}</span>
        </div>
      </div>

      <!-- Sport-Specific Controls -->
      <!-- CRICKET -->
      <div v-if="sportCode === 'CRICKET'" class="bg-white rounded-xl shadow-lg p-8 mb-6">
        <h2 class="text-xl font-bold text-gray-900 mb-6 text-center">Cricket Scoring</h2>
        <div class="grid grid-cols-2 gap-4">
          <!-- Home Team -->
          <div>
            <h3 class="text-lg font-semibold text-gray-700 mb-4 text-center">{{ match?.home_team?.name || 'Home Team' }}</h3>
            <div class="grid grid-cols-3 gap-3 mb-4">
              <button
                v-for="runs in [1, 2, 3, 4, 6]"
                :key="`home-run-${runs}`"
                @click="addCricketRun('home', runs)"
                class="px-6 py-4 bg-primary-600 text-white font-bold text-xl rounded-lg hover:bg-primary-700 transition-colors shadow-md"
              >
                +{{ runs }}
              </button>
            </div>
            <button
              @click="showOutModal = true; selectedTeam = 'home'"
              class="w-full px-6 py-3 bg-red-500 text-white font-semibold rounded-lg hover:bg-red-600 transition-colors shadow-md"
            >
              WICKET
            </button>
          </div>

          <!-- Away Team -->
          <div>
            <h3 class="text-lg font-semibold text-gray-700 mb-4 text-center">{{ match?.away_team?.name || 'Away Team' }}</h3>
            <div class="grid grid-cols-3 gap-3 mb-4">
              <button
                v-for="runs in [1, 2, 3, 4, 6]"
                :key="`away-run-${runs}`"
                @click="addCricketRun('away', runs)"
                class="px-6 py-4 bg-primary-600 text-white font-bold text-xl rounded-lg hover:bg-primary-700 transition-colors shadow-md"
              >
                +{{ runs }}
              </button>
            </div>
            <button
              @click="showOutModal = true; selectedTeam = 'away'"
              class="w-full px-6 py-3 bg-red-500 text-white font-semibold rounded-lg hover:bg-red-600 transition-colors shadow-md"
            >
              WICKET
            </button>
          </div>
        </div>
      </div>

      <!-- FOOTBALL -->
      <div v-if="sportCode === 'FOOTBALL'" class="bg-white rounded-xl shadow-lg p-8 mb-6">
        <h2 class="text-xl font-bold text-gray-900 mb-6 text-center">Football Scoring</h2>
        <div class="grid grid-cols-2 gap-4">
          <!-- Home Team -->
          <div>
            <h3 class="text-lg font-semibold text-gray-700 mb-4 text-center">{{ match?.home_team?.name || 'Home Team' }}</h3>
            <div class="space-y-3">
              <button
                @click="addFootballGoal('home')"
                class="w-full px-6 py-4 bg-green-600 text-white font-bold text-xl rounded-lg hover:bg-green-700 transition-colors shadow-md"
              >
                GOAL ⚽
              </button>
              <button
                @click="showCardModal = true; selectedTeam = 'home'; cardType = 'yellow'"
                class="w-full px-6 py-3 bg-yellow-500 text-white font-semibold rounded-lg hover:bg-yellow-600 transition-colors shadow-md"
              >
                Yellow Card 🟨
              </button>
              <button
                @click="showCardModal = true; selectedTeam = 'home'; cardType = 'red'"
                class="w-full px-6 py-3 bg-red-600 text-white font-semibold rounded-lg hover:bg-red-700 transition-colors shadow-md"
              >
                Red Card 🟥
              </button>
              <button
                @click="addFootballFoul('home')"
                class="w-full px-6 py-3 bg-orange-500 text-white font-semibold rounded-lg hover:bg-orange-600 transition-colors shadow-md"
              >
                Foul
              </button>
            </div>
          </div>

          <!-- Away Team -->
          <div>
            <h3 class="text-lg font-semibold text-gray-700 mb-4 text-center">{{ match?.away_team?.name || 'Away Team' }}</h3>
            <div class="space-y-3">
              <button
                @click="addFootballGoal('away')"
                class="w-full px-6 py-4 bg-green-600 text-white font-bold text-xl rounded-lg hover:bg-green-700 transition-colors shadow-md"
              >
                GOAL ⚽
              </button>
              <button
                @click="showCardModal = true; selectedTeam = 'away'; cardType = 'yellow'"
                class="w-full px-6 py-3 bg-yellow-500 text-white font-semibold rounded-lg hover:bg-yellow-600 transition-colors shadow-md"
              >
                Yellow Card 🟨
              </button>
              <button
                @click="showCardModal = true; selectedTeam = 'away'; cardType = 'red'"
                class="w-full px-6 py-3 bg-red-600 text-white font-semibold rounded-lg hover:bg-red-700 transition-colors shadow-md"
              >
                Red Card 🟥
              </button>
              <button
                @click="addFootballFoul('away')"
                class="w-full px-6 py-3 bg-orange-500 text-white font-semibold rounded-lg hover:bg-orange-600 transition-colors shadow-md"
              >
                Foul
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- BASKETBALL -->
      <div v-if="sportCode === 'BASKETBALL'" class="bg-white rounded-xl shadow-lg p-8 mb-6">
        <h2 class="text-xl font-bold text-gray-900 mb-6 text-center">Basketball Scoring</h2>
        <div class="grid grid-cols-2 gap-4">
          <!-- Home Team -->
          <div>
            <h3 class="text-lg font-semibold text-gray-700 mb-4 text-center">{{ match?.home_team?.name || 'Home Team' }}</h3>
            <div class="grid grid-cols-3 gap-3 mb-4">
              <button
                @click="addBasketballPoint('home', 1)"
                class="px-4 py-3 bg-blue-600 text-white font-bold rounded-lg hover:bg-blue-700 transition-colors shadow-md"
              >
                +1
              </button>
              <button
                @click="addBasketballPoint('home', 2)"
                class="px-4 py-3 bg-green-600 text-white font-bold rounded-lg hover:bg-green-700 transition-colors shadow-md"
              >
                +2
              </button>
              <button
                @click="addBasketballPoint('home', 3)"
                class="px-4 py-3 bg-purple-600 text-white font-bold rounded-lg hover:bg-purple-700 transition-colors shadow-md"
              >
                +3
              </button>
            </div>
            <div class="space-y-2">
              <button
                @click="addBasketballFoul('home')"
                class="w-full px-4 py-2 bg-orange-500 text-white font-semibold rounded-lg hover:bg-orange-600 transition-colors shadow-md"
              >
                Foul
              </button>
              <button
                @click="useBasketballTimeout('home')"
                class="w-full px-4 py-2 bg-gray-500 text-white font-semibold rounded-lg hover:bg-gray-600 transition-colors shadow-md"
              >
                Timeout
              </button>
            </div>
          </div>

          <!-- Away Team -->
          <div>
            <h3 class="text-lg font-semibold text-gray-700 mb-4 text-center">{{ match?.away_team?.name || 'Away Team' }}</h3>
            <div class="grid grid-cols-3 gap-3 mb-4">
              <button
                @click="addBasketballPoint('away', 1)"
                class="px-4 py-3 bg-blue-600 text-white font-bold rounded-lg hover:bg-blue-700 transition-colors shadow-md"
              >
                +1
              </button>
              <button
                @click="addBasketballPoint('away', 2)"
                class="px-4 py-3 bg-green-600 text-white font-bold rounded-lg hover:bg-green-700 transition-colors shadow-md"
              >
                +2
              </button>
              <button
                @click="addBasketballPoint('away', 3)"
                class="px-4 py-3 bg-purple-600 text-white font-bold rounded-lg hover:bg-purple-700 transition-colors shadow-md"
              >
                +3
              </button>
            </div>
            <div class="space-y-2">
              <button
                @click="addBasketballFoul('away')"
                class="w-full px-4 py-2 bg-orange-500 text-white font-semibold rounded-lg hover:bg-orange-600 transition-colors shadow-md"
              >
                Foul
              </button>
              <button
                @click="useBasketballTimeout('away')"
                class="w-full px-4 py-2 bg-gray-500 text-white font-semibold rounded-lg hover:bg-gray-600 transition-colors shadow-md"
              >
                Timeout
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- CHESS -->
      <div v-if="sportCode === 'CHESS'" class="bg-white rounded-xl shadow-lg p-8 mb-6">
        <h2 class="text-xl font-bold text-gray-900 mb-6 text-center">Chess Game</h2>
        <div class="grid grid-cols-2 gap-4">
          <!-- Home Team (White) -->
          <div>
            <h3 class="text-lg font-semibold text-gray-700 mb-4 text-center">{{ match?.home_team?.name || 'White' }}</h3>
            <div class="space-y-3">
              <button
                @click="recordChessMove('home')"
                class="w-full px-6 py-4 bg-gray-700 text-white font-semibold rounded-lg hover:bg-gray-800 transition-colors shadow-md"
              >
                Record Move
              </button>
              <button
                @click="endChessGame('home', 'checkmate')"
                class="w-full px-6 py-3 bg-green-600 text-white font-semibold rounded-lg hover:bg-green-700 transition-colors shadow-md"
              >
                Checkmate (Win)
              </button>
              <button
                @click="endChessGame('home', 'resign')"
                class="w-full px-6 py-3 bg-red-600 text-white font-semibold rounded-lg hover:bg-red-700 transition-colors shadow-md"
              >
                Resign (Loss)
              </button>
            </div>
          </div>

          <!-- Away Team (Black) -->
          <div>
            <h3 class="text-lg font-semibold text-gray-700 mb-4 text-center">{{ match?.away_team?.name || 'Black' }}</h3>
            <div class="space-y-3">
              <button
                @click="recordChessMove('away')"
                class="w-full px-6 py-4 bg-gray-700 text-white font-semibold rounded-lg hover:bg-gray-800 transition-colors shadow-md"
              >
                Record Move
              </button>
              <button
                @click="endChessGame('away', 'checkmate')"
                class="w-full px-6 py-3 bg-green-600 text-white font-semibold rounded-lg hover:bg-green-700 transition-colors shadow-md"
              >
                Checkmate (Win)
              </button>
              <button
                @click="endChessGame('away', 'resign')"
                class="w-full px-6 py-3 bg-red-600 text-white font-semibold rounded-lg hover:bg-red-700 transition-colors shadow-md"
              >
                Resign (Loss)
              </button>
            </div>
          </div>
        </div>
        <div class="mt-6 text-center">
          <button
            @click="endChessGame('draw', 'draw')"
            class="px-8 py-3 bg-yellow-500 text-white font-semibold rounded-lg hover:bg-yellow-600 transition-colors shadow-md"
          >
            Draw Game
          </button>
        </div>
      </div>

      <!-- VOLLEYBALL -->
      <div v-if="sportCode === 'VOLLEYBALL'" class="bg-white rounded-xl shadow-lg p-8 mb-6">
        <h2 class="text-xl font-bold text-gray-900 mb-6 text-center">Volleyball Scoring</h2>
        <div class="mb-4 text-center">
          <span class="px-4 py-2 bg-blue-100 rounded-lg text-blue-800 font-medium">Set {{ currentSet || 1 }}</span>
        </div>
        <div class="grid grid-cols-2 gap-4">
          <!-- Home Team -->
          <div>
            <h3 class="text-lg font-semibold text-gray-700 mb-4 text-center">{{ match?.home_team?.name || 'Home Team' }}</h3>
            <div class="space-y-3">
              <button
                @click="addVolleyballPoint('home')"
                class="w-full px-6 py-4 bg-primary-600 text-white font-bold text-xl rounded-lg hover:bg-primary-700 transition-colors shadow-md"
              >
                +1 Point
              </button>
              <button
                @click="addServiceError('home')"
                class="w-full px-6 py-3 bg-red-500 text-white font-semibold rounded-lg hover:bg-red-600 transition-colors shadow-md"
              >
                Service Error
              </button>
            </div>
          </div>

          <!-- Away Team -->
          <div>
            <h3 class="text-lg font-semibold text-gray-700 mb-4 text-center">{{ match?.away_team?.name || 'Away Team' }}</h3>
            <div class="space-y-3">
              <button
                @click="addVolleyballPoint('away')"
                class="w-full px-6 py-4 bg-primary-600 text-white font-bold text-xl rounded-lg hover:bg-primary-700 transition-colors shadow-md"
              >
                +1 Point
              </button>
              <button
                @click="addServiceError('away')"
                class="w-full px-6 py-3 bg-red-500 text-white font-semibold rounded-lg hover:bg-red-600 transition-colors shadow-md"
              >
                Service Error
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- BADMINTON -->
      <div v-if="sportCode === 'BADMINTON'" class="bg-white rounded-xl shadow-lg p-8 mb-6">
        <h2 class="text-xl font-bold text-gray-900 mb-6 text-center">Badminton Scoring</h2>
        <div class="mb-4 text-center">
          <span class="px-4 py-2 bg-blue-100 rounded-lg text-blue-800 font-medium">Set {{ currentSet || 1 }}</span>
        </div>
        <div class="grid grid-cols-2 gap-4">
          <!-- Home Team -->
          <div>
            <h3 class="text-lg font-semibold text-gray-700 mb-4 text-center">{{ match?.home_team?.name || 'Home Team' }}</h3>
            <div class="space-y-3">
              <button
                @click="addBadmintonPoint('home')"
                class="w-full px-6 py-4 bg-primary-600 text-white font-bold text-xl rounded-lg hover:bg-primary-700 transition-colors shadow-md"
              >
                +1 Point
              </button>
              <button
                @click="addServiceError('home')"
                class="w-full px-6 py-3 bg-red-500 text-white font-semibold rounded-lg hover:bg-red-600 transition-colors shadow-md"
              >
                Service Error
              </button>
            </div>
          </div>

          <!-- Away Team -->
          <div>
            <h3 class="text-lg font-semibold text-gray-700 mb-4 text-center">{{ match?.away_team?.name || 'Away Team' }}</h3>
            <div class="space-y-3">
              <button
                @click="addBadmintonPoint('away')"
                class="w-full px-6 py-4 bg-primary-600 text-white font-bold text-xl rounded-lg hover:bg-primary-700 transition-colors shadow-md"
              >
                +1 Point
              </button>
              <button
                @click="addServiceError('away')"
                class="w-full px-6 py-3 bg-red-500 text-white font-semibold rounded-lg hover:bg-red-600 transition-colors shadow-md"
              >
                Service Error
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Undo Button -->
      <div class="flex justify-center mb-6">
        <button
          @click="handleUndo"
          :disabled="scoreHistory.length === 0"
          class="px-8 py-4 bg-yellow-500 text-white font-semibold rounded-lg hover:bg-yellow-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors shadow-md flex items-center space-x-2"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h10a8 8 0 018 8v2M3 10l6 6m-6-6l6-6" />
          </svg>
          <span>Undo Last Action</span>
        </button>
      </div>

      <!-- Score History -->
      <div class="bg-white rounded-xl shadow-lg p-6">
        <h2 class="text-xl font-bold text-gray-900 mb-4">Score History</h2>
        <div v-if="scoreHistory.length === 0" class="text-center text-gray-500 py-8">
          No score updates yet
        </div>
        <div v-else class="space-y-2">
          <div
            v-for="(update, index) in scoreHistory.slice().reverse()"
            :key="index"
            class="flex justify-between items-center p-3 bg-gray-50 rounded-lg"
          >
            <div>
              <span class="font-semibold">{{ update.description || 'Score update' }}</span>
              <span class="text-sm text-gray-600 ml-2">{{ formatTime(update.updated_at) }}</span>
            </div>
            <div class="text-lg font-bold">
              {{ update.home_score }} - {{ update.away_score }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Out/Wicket Modal -->
    <div v-if="showOutModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click="showOutModal = false">
      <div class="bg-white rounded-xl shadow-2xl p-8 max-w-md w-full mx-4" @click.stop>
        <h3 class="text-2xl font-bold text-gray-900 mb-6">{{ sportCode === 'CRICKET' ? 'Select Player Out (Wicket)' : 'Select Player' }}</h3>
        <div v-if="loadingPlayers" class="text-center py-8">
          <p class="text-gray-600">Loading players...</p>
        </div>
        <div v-else-if="players.length === 0" class="text-center py-8">
          <p class="text-gray-600">No players found</p>
        </div>
        <div v-else class="space-y-3 max-h-96 overflow-y-auto">
          <button
            v-for="player in players"
            :key="player.id"
            @click="handlePlayerOut(player)"
            class="w-full px-4 py-3 bg-gray-100 hover:bg-red-100 rounded-lg text-left transition-colors"
          >
            <div class="font-semibold">{{ player.full_name || player.user?.full_name || `Player ${player.id}` }}</div>
            <div class="text-sm text-gray-600">Jersey #{{ player.jersey_number || 'N/A' }}</div>
          </button>
        </div>
        <div class="mt-6 flex justify-end">
          <button
            @click="showOutModal = false"
            class="px-6 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400 transition-colors"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>

    <!-- Card Modal (Football) -->
    <div v-if="showCardModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click="showCardModal = false">
      <div class="bg-white rounded-xl shadow-2xl p-8 max-w-md w-full mx-4" @click.stop>
        <h3 class="text-2xl font-bold text-gray-900 mb-6">Select Player for {{ cardType === 'yellow' ? 'Yellow' : 'Red' }} Card</h3>
        <div v-if="loadingPlayers" class="text-center py-8">
          <p class="text-gray-600">Loading players...</p>
        </div>
        <div v-else-if="players.length === 0" class="text-center py-8">
          <p class="text-gray-600">No players found</p>
        </div>
        <div v-else class="space-y-3 max-h-96 overflow-y-auto">
          <button
            v-for="player in players"
            :key="player.id"
            @click="handleCard(player)"
            class="w-full px-4 py-3 bg-gray-100 hover:bg-yellow-100 rounded-lg text-left transition-colors"
          >
            <div class="font-semibold">{{ player.full_name || player.user?.full_name || `Player ${player.id}` }}</div>
            <div class="text-sm text-gray-600">Jersey #{{ player.jersey_number || 'N/A' }}</div>
          </button>
        </div>
        <div class="mt-6 flex justify-end">
          <button
            @click="showCardModal = false"
            class="px-6 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400 transition-colors"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/services/api'
import type { Match, Score, Player } from '@/types'

const route = useRoute()
const router = useRouter()
const matchId = parseInt(route.params.id as string)

const match = ref<Match | null>(null)
const score = ref<Score>({ id: 0, match_id: matchId, home_score: 0, away_score: 0, created_at: new Date().toISOString() })
const scoreDetails = ref<any>({})
const scoreHistory = ref<any[]>([])
const players = ref<Player[]>([])
const loadingPlayers = ref(false)
const showOutModal = ref(false)
const showCardModal = ref(false)
const selectedTeam = ref<'home' | 'away'>('home')
const cardType = ref<'yellow' | 'red'>('yellow')
const currentSet = ref(1)

const sportCode = computed(() => {
  return scoreDetails.value?.sport_code || match.value?.sport?.code?.toUpperCase() || null
})

const fetchMatch = async () => {
  try {
    match.value = await api.getMatch(matchId)
    await fetchScore()
    await fetchScoreDetails()
    await fetchScoreHistory()
  } catch (error) {
    console.error('Failed to fetch match', error)
  }
}

const fetchScore = async () => {
  try {
    score.value = await api.getScore(matchId)
  } catch (error) {
    console.error('Failed to fetch score', error)
  }
}

const fetchScoreDetails = async () => {
  try {
    scoreDetails.value = await api.getScoreDetails(matchId)
    if (scoreDetails.value.score_data?.current_set) {
      currentSet.value = scoreDetails.value.score_data.current_set
    }
  } catch (error) {
    console.error('Failed to fetch score details', error)
  }
}

const fetchScoreHistory = async () => {
  try {
    scoreHistory.value = await api.getScoreHistory(matchId)
  } catch (error) {
    console.error('Failed to fetch score history', error)
  }
}

const fetchPlayers = async () => {
  loadingPlayers.value = true
  try {
    players.value = await api.getMatchPlayers(matchId)
  } catch (error) {
    console.error('Failed to fetch players', error)
  } finally {
    loadingPlayers.value = false
  }
}

// Cricket
const addCricketRun = async (team: 'home' | 'away', runs: number) => {
  try {
    const teamName = team === 'home' ? match.value?.home_team?.name : match.value?.away_team?.name
    await api.updateMatchScore(matchId, {
      action: 'add_run',
      team,
      points: runs,
      description: `${teamName} scored ${runs} run${runs > 1 ? 's' : ''}`,
      update_type: 'score'
    })
    await fetchScore()
    await fetchScoreDetails()
    await fetchScoreHistory()
  } catch (error: any) {
    console.error('Failed to add run', error)
    alert(error.response?.data?.detail || 'Failed to add run')
  }
}

// Football
const addFootballGoal = async (team: 'home' | 'away') => {
  try {
    const teamName = team === 'home' ? match.value?.home_team?.name : match.value?.away_team?.name
    await api.updateMatchScore(matchId, {
      action: 'goal',
      team,
      description: `${teamName} scored a goal`,
      update_type: 'goal'
    })
    await fetchScore()
    await fetchScoreDetails()
    await fetchScoreHistory()
  } catch (error: any) {
    console.error('Failed to add goal', error)
    alert(error.response?.data?.detail || 'Failed to add goal')
  }
}

const addFootballFoul = async (team: 'home' | 'away') => {
  try {
    const teamName = team === 'home' ? match.value?.home_team?.name : match.value?.away_team?.name
    await api.updateMatchScore(matchId, {
      action: 'foul',
      team,
      description: `Foul by ${teamName}`,
      update_type: 'foul'
    })
    await fetchScoreDetails()
    await fetchScoreHistory()
  } catch (error: any) {
    console.error('Failed to add foul', error)
    alert(error.response?.data?.detail || 'Failed to add foul')
  }
}

// Basketball
const addBasketballPoint = async (team: 'home' | 'away', points: number) => {
  try {
    const teamName = team === 'home' ? match.value?.home_team?.name : match.value?.away_team?.name
    const pointType = points === 1 ? 'free_throw' : points === 2 ? 'field_goal' : 'three_pointer'
    await api.updateMatchScore(matchId, {
      action: 'point',
      team,
      points,
      sport_specific_data: { point_type: pointType },
      description: `${teamName} scored ${points} point${points > 1 ? 's' : ''}`,
      update_type: 'score'
    })
    await fetchScore()
    await fetchScoreDetails()
    await fetchScoreHistory()
  } catch (error: any) {
    console.error('Failed to add point', error)
    alert(error.response?.data?.detail || 'Failed to add point')
  }
}

const addBasketballFoul = async (team: 'home' | 'away') => {
  try {
    const teamName = team === 'home' ? match.value?.home_team?.name : match.value?.away_team?.name
    await api.updateMatchScore(matchId, {
      action: 'foul',
      team,
      description: `Foul by ${teamName}`,
      update_type: 'foul'
    })
    await fetchScoreDetails()
    await fetchScoreHistory()
  } catch (error: any) {
    console.error('Failed to add foul', error)
    alert(error.response?.data?.detail || 'Failed to add foul')
  }
}

const useBasketballTimeout = async (team: 'home' | 'away') => {
  try {
    const teamName = team === 'home' ? match.value?.home_team?.name : match.value?.away_team?.name
    await api.updateMatchScore(matchId, {
      action: 'timeout',
      team,
      description: `Timeout called by ${teamName}`,
      update_type: 'timeout'
    })
    await fetchScoreDetails()
    await fetchScoreHistory()
  } catch (error: any) {
    console.error('Failed to use timeout', error)
    alert(error.response?.data?.detail || 'Failed to use timeout')
  }
}

// Chess
const recordChessMove = async (team: 'home' | 'away') => {
  try {
    await api.updateMatchScore(matchId, {
      action: 'move',
      team,
      description: `${team === 'home' ? 'White' : 'Black'} made a move`,
      update_type: 'move'
    })
    await fetchScoreDetails()
    await fetchScoreHistory()
  } catch (error: any) {
    console.error('Failed to record move', error)
    alert(error.response?.data?.detail || 'Failed to record move')
  }
}

const endChessGame = async (team: 'home' | 'away' | 'draw', result: string) => {
  try {
    let description = ''
    if (result === 'draw') {
      description = 'Game ended in a draw'
    } else {
      const winner = team === 'home' ? match.value?.home_team?.name : match.value?.away_team?.name
      description = `${winner} won by ${result}`
    }
    
    await api.updateMatchScore(matchId, {
      action: result,
      team: team === 'draw' ? 'home' : team,
      description,
      update_type: result
    })
    await fetchScore()
    await fetchScoreDetails()
    await fetchScoreHistory()
  } catch (error: any) {
    console.error('Failed to end game', error)
    alert(error.response?.data?.detail || 'Failed to end game')
  }
}

// Volleyball
const addVolleyballPoint = async (team: 'home' | 'away') => {
  try {
    const teamName = team === 'home' ? match.value?.home_team?.name : match.value?.away_team?.name
    await api.updateMatchScore(matchId, {
      action: 'set_point',
      team,
      sport_specific_data: { set_num: currentSet.value },
      description: `${teamName} scored a point in Set ${currentSet.value}`,
      update_type: 'score'
    })
    await fetchScore()
    await fetchScoreDetails()
    await fetchScoreHistory()
    // Update current set if changed
    if (scoreDetails.value.score_data?.current_set) {
      currentSet.value = scoreDetails.value.score_data.current_set
    }
  } catch (error: any) {
    console.error('Failed to add point', error)
    alert(error.response?.data?.detail || 'Failed to add point')
  }
}

// Badminton
const addBadmintonPoint = async (team: 'home' | 'away') => {
  try {
    const teamName = team === 'home' ? match.value?.home_team?.name : match.value?.away_team?.name
    await api.updateMatchScore(matchId, {
      action: 'set_point',
      team,
      sport_specific_data: { set_num: currentSet.value },
      description: `${teamName} scored a point in Set ${currentSet.value}`,
      update_type: 'score'
    })
    await fetchScore()
    await fetchScoreDetails()
    await fetchScoreHistory()
    // Update current set if changed
    if (scoreDetails.value.score_data?.current_set) {
      currentSet.value = scoreDetails.value.score_data.current_set
    }
  } catch (error: any) {
    console.error('Failed to add point', error)
    alert(error.response?.data?.detail || 'Failed to add point')
  }
}

const addServiceError = async (team: 'home' | 'away') => {
  try {
    const teamName = team === 'home' ? match.value?.home_team?.name : match.value?.away_team?.name
    await api.updateMatchScore(matchId, {
      action: 'service_error',
      team,
      description: `Service error by ${teamName}`,
      update_type: 'error'
    })
    await fetchScoreDetails()
    await fetchScoreHistory()
  } catch (error: any) {
    console.error('Failed to add service error', error)
    alert(error.response?.data?.detail || 'Failed to add service error')
  }
}

const handlePlayerOut = async (player: Player) => {
  try {
    const playerName = player.full_name || player.user?.full_name || `Player ${player.id}`
    const teamName = selectedTeam.value === 'home' ? match.value?.home_team?.name : match.value?.away_team?.name
    
    if (sportCode.value === 'CRICKET') {
      await api.updateMatchScore(matchId, {
        action: 'wicket',
        team: selectedTeam.value,
        player_id: player.id,
        description: `${playerName} is out (${teamName})`,
        update_type: 'wicket'
      })
    } else {
      await api.updateMatchScore(matchId, {
        action: 'out',
        team: selectedTeam.value,
        player_id: player.id,
        description: `${playerName} is out (${teamName})`,
        update_type: 'out'
      })
    }
    
    showOutModal.value = false
    await fetchScore()
    await fetchScoreDetails()
    await fetchScoreHistory()
  } catch (error: any) {
    console.error('Failed to record out', error)
    alert(error.response?.data?.detail || 'Failed to record out')
  }
}

const handleCard = async (player: Player) => {
  try {
    const playerName = player.full_name || player.user?.full_name || `Player ${player.id}`
    const teamName = selectedTeam.value === 'home' ? match.value?.home_team?.name : match.value?.away_team?.name
    
    await api.updateMatchScore(matchId, {
      action: cardType.value === 'yellow' ? 'yellow_card' : 'red_card',
      team: selectedTeam.value,
      player_id: player.id,
      description: `${playerName} received a ${cardType.value} card (${teamName})`,
      update_type: cardType.value === 'yellow' ? 'yellow_card' : 'red_card'
    })
    
    showCardModal.value = false
    await fetchScoreDetails()
    await fetchScoreHistory()
  } catch (error: any) {
    console.error('Failed to record card', error)
    alert(error.response?.data?.detail || 'Failed to record card')
  }
}

const handleEndMatch = async () => {
  if (!confirm('Are you sure you want to end this match?')) {
    return
  }
  
  try {
    await api.endMatch(matchId)
    alert('Match ended successfully')
    router.push('/coach/matches')
  } catch (error: any) {
    console.error('Failed to end match', error)
    alert(error.response?.data?.detail || 'Failed to end match')
  }
}

const handleUndo = async () => {
  if (scoreHistory.value.length < 2) {
    alert('Nothing to undo')
    return
  }
  
  // Get the second-to-last score update
  const previousUpdate = scoreHistory.value[scoreHistory.value.length - 2]
  
  try {
    await api.updateMatchScore(matchId, {
      home_score: previousUpdate.home_score,
      away_score: previousUpdate.away_score,
      action: 'undo',
      description: 'Undo last action',
      update_type: 'undo'
    })
    
    await fetchScore()
    await fetchScoreDetails()
    await fetchScoreHistory()
  } catch (error: any) {
    console.error('Failed to undo', error)
    alert(error.response?.data?.detail || 'Failed to undo')
  }
}

const getDisplayScore = (team: 'home' | 'away'): number => {
  if (sportCode.value === 'CRICKET') {
    const teamKey = team === 'home' ? 'home_runs' : 'away_runs'
    return scoreDetails.value.score_data?.[teamKey] || score.value[team === 'home' ? 'home_score' : 'away_score'] || 0
  }
  return score.value[team === 'home' ? 'home_score' : 'away_score'] || 0
}

const getSecondaryScore = (team: 'home' | 'away'): string => {
  if (sportCode.value === 'CRICKET') {
    const wickets = scoreDetails.value.score_data?.[`${team}_wickets`] || 0
    return `${wickets} wickets`
  }
  return ''
}

const getPeriodInfo = (): string => {
  if (sportCode.value === 'VOLLEYBALL' || sportCode.value === 'BADMINTON') {
    return `Set ${currentSet.value}`
  }
  return ''
}

const formatDate = (dateString?: string): string => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}

const formatTime = (dateString?: string): string => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
}

onMounted(() => {
  fetchMatch()
})

// Watch for modal opening
watch(showOutModal, (newVal) => {
  if (newVal) {
    fetchPlayers()
  }
})

watch(showCardModal, (newVal) => {
  if (newVal) {
    fetchPlayers()
  }
})
</script>
