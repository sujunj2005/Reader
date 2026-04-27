import { defineStore } from 'pinia'
import api from '../api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
    refreshToken: localStorage.getItem('refreshToken') || null,
    loading: false,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
  },

  actions: {
    async login(email, password) {
      this.loading = true
      try {
        const response = await api.post('/auth/login', { email, password })
        const { access_token, refresh_token } = response.data
        this.token = access_token
        this.refreshToken = refresh_token
        localStorage.setItem('token', access_token)
        localStorage.setItem('refreshToken', refresh_token)
        await this.fetchUser()
      } finally {
        this.loading = false
      }
    },

    async register(email, password) {
      this.loading = true
      try {
        await api.post('/auth/register', { email, password })
        await this.login(email, password)
      } finally {
        this.loading = false
      }
    },

    async fetchUser() {
      try {
        const response = await api.get('/auth/me')
        this.user = response.data
      } catch {
        this.logout()
      }
    },

    async logout() {
      try {
        await api.post('/auth/logout')
      } finally {
        this.user = null
        this.token = null
        this.refreshToken = null
        localStorage.removeItem('token')
        localStorage.removeItem('refreshToken')
      }
    },
  },
})
