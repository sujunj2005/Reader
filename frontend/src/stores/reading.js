import { defineStore } from 'pinia'
import api from '../api'

export const useReadingStore = defineStore('reading', {
  state: () => ({
    currentNovel: null,
    chapters: [],
    currentChapter: null,
    bookmarks: [],
    history: [],
    settings: JSON.parse(localStorage.getItem('readingSettings') || '{}'),
    progress: null,
  }),

  getters: {
    nightMode: (state) => state.settings.nightMode || false,
    fontSize: (state) => state.settings.fontSize || 'medium',
    lineHeight: (state) => state.settings.lineHeight || 1.8,
  },

  actions: {
    async loadNovel(novelId) {
      const response = await api.get(`/reading/novels/${novelId}/chapters`)
      this.currentNovel = { id: response.data.id, title: response.data.title, author: response.data.author }
      this.chapters = response.data.chapters
    },

    async loadProgress(novelId) {
      try {
        const response = await api.get(`/reading/progress/${novelId}`)
        this.progress = response.data
      } catch {
        this.progress = null
      }
    },

    async saveProgress(novelId, chapterId, scrollPosition = 0) {
      try {
        const response = await api.post('/reading/progress', {
          novel_id: novelId,
          chapter_id: chapterId,
          scroll_position: scrollPosition,
        })
        this.progress = response.data
      } catch (e) {
        console.error('Failed to save progress:', e)
      }
    },

    async loadBookmarks() {
      const response = await api.get('/reading/bookmarks')
      this.bookmarks = response.data
    },

    async addBookmark(novelId, chapterId, note = '') {
      const response = await api.post('/reading/bookmarks', {
        novel_id: novelId,
        chapter_id: chapterId,
        note,
      })
      this.bookmarks.unshift(response.data)
    },

    async removeBookmark(bookmarkId) {
      await api.delete(`/reading/bookmarks/${bookmarkId}`)
      this.bookmarks = this.bookmarks.filter(b => b.id !== bookmarkId)
    },

    updateSettings(newSettings) {
      this.settings = { ...this.settings, ...newSettings }
      localStorage.setItem('readingSettings', JSON.stringify(this.settings))
    },
  },
})
