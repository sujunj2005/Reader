<template>
  <div class="search-page">
    <h1>搜索小说</h1>
    <div class="search-bar">
      <input
        v-model="searchQuery"
        @input="debounceSearch"
        type="text"
        placeholder="输入小说标题或作者..."
      />
    </div>

    <div class="search-results">
      <div v-for="novel in searchResults" :key="novel.id" class="novel-result">
        <router-link :to="{ name: 'NovelDetail', params: { novelId: novel.id } }">
          <h3>{{ novel.title }}</h3>
          <p v-if="novel.author">{{ novel.author }}</p>
          <p v-if="novel.description">{{ novel.description.substring(0, 100) }}...</p>
        </router-link>
        <button v-if="!isInBookshelf(novel.id)" @click="addToBookshelf(novel.id)">加入书架</button>
        <span v-else class="in-bookshelf">已在书架</span>
      </div>
      <p v-if="searchQuery && searchResults.length === 0" class="no-results">未找到相关小说</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useBookshelfStore } from '../stores/bookshelf'

const bookshelfStore = useBookshelfStore()
const searchQuery = ref('')
const searchResults = computed(() => bookshelfStore.searchResults)
const searchTimer = ref(null)

const debounceSearch = () => {
  if (searchTimer.value) clearTimeout(searchTimer.value)
  searchTimer.value = setTimeout(() => {
    bookshelfStore.searchNovels(searchQuery.value)
  }, 300)
}

const isInBookshelf = (novelId) => {
  return bookshelfStore.novels.some(n => n.novel_id === novelId)
}

const addToBookshelf = async (novelId) => {
  await bookshelfStore.addToBookshelf(novelId)
}
</script>
