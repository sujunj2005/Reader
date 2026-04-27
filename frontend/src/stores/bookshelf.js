import { defineStore } from 'pinia'
import api from '../api'

export const useBookshelfStore = defineStore('bookshelf', {
  state: () => ({
    novels: [],
    searchResults: [],
    tags: [],
    loading: false,
  }),

  actions: {
    async loadBookshelf() {
      this.loading = true
      try {
        const response = await api.get('/bookshelf')
        this.novels = response.data
      } finally {
        this.loading = false
      }
    },

    async addToBookshelf(novelId, status = 'reading') {
      const response = await api.post('/bookshelf', { novel_id: novelId, status })
      this.novels.push(response.data)
    },

    async removeFromBookshelf(userNovelId) {
      await api.delete(`/bookshelf/${userNovelId}`)
      this.novels = this.novels.filter(n => n.user_novel_id !== userNovelId)
    },

    async updateStatus(userNovelId, status) {
      await api.put(`/bookshelf/${userNovelId}`, { status })
      const novel = this.novels.find(n => n.user_novel_id === userNovelId)
      if (novel) novel.status = status
    },

    async searchNovels(query) {
      if (!query.trim()) {
        this.searchResults = []
        return
      }
      const response = await api.get('/novels/search', { params: { q: query } })
      this.searchResults = response.data
    },

    async loadTags() {
      const response = await api.get('/tags')
      this.tags = response.data
    },
  },
})
