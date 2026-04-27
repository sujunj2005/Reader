<template>
  <div class="novel-detail" :class="{ 'night-mode': readingStore.nightMode }">
    <div class="novel-header">
      <h1>{{ novel.title }}</h1>
      <p class="author">{{ novel.author }}</p>
      <button @click="goBack" class="back-btn">返回</button>
    </div>

    <div class="chapter-list">
      <h2>章节列表</h2>
      <div v-if="lastProgress" class="continue-reading">
        <button @click="readChapter(lastProgress.chapter_id)">继续阅读</button>
      </div>
      <ul>
        <li v-for="chapter in chapters" :key="chapter.id">
          <router-link :to="{ name: 'Reader', params: { novelId: novel.id, chapterId: chapter.id } }">
            {{ chapter.title }}
          </router-link>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useReadingStore } from '../stores/reading'
import api from '../api'

const route = useRoute()
const router = useRouter()
const readingStore = useReadingStore()
const novel = ref({})
const chapters = ref([])
const lastProgress = ref(null)

onMounted(async () => {
  await readingStore.loadNovel(route.params.novelId)
  novel.value = readingStore.currentNovel
  chapters.value = readingStore.chapters

  if (readingStore.isAuthenticated) {
    try {
      const response = await api.get(`/reading/progress/${route.params.novelId}`)
      lastProgress.value = response.data
    } catch {
      lastProgress.value = null
    }
  }
})

const readChapter = (chapterId) => {
  router.push({ name: 'Reader', params: { novelId: novel.value.id, chapterId } })
}

const goBack = () => {
  router.push('/')
}
</script>
