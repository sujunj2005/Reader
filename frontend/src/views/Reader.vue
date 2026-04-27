<template>
  <div class="reader" :class="readerClasses">
    <div class="reader-header">
      <button @click="goBack" class="back-btn">返回</button>
      <span class="chapter-title">{{ chapterTitle }}</span>
      <div class="settings-toggle" @click="showSettings = !showSettings">⚙️</div>
    </div>

    <div v-if="showSettings" class="settings-panel">
      <div class="setting-item">
        <label>字体大小</label>
        <select v-model="fontSize" @change="applySetting('fontSize', $event.target.value)">
          <option value="small">小</option>
          <option value="medium">中</option>
          <option value="large">大</option>
          <option value="xlarge">特大</option>
        </select>
      </div>
      <div class="setting-item">
        <label>行间距</label>
        <select v-model="lineHeight" @change="applySetting('lineHeight', parseFloat($event.target.value))">
          <option value="1.5">1.5x</option>
          <option value="1.8">1.8x</option>
          <option value="2.0">2.0x</option>
        </select>
      </div>
      <div class="setting-item">
        <label>夜间模式</label>
        <input type="checkbox" v-model="nightMode" @change="applySetting('nightMode', $event.target.checked)" />
      </div>
    </div>

    <div ref="contentRef" class="chapter-content" @scroll="handleScroll">
      <p v-for="(para, idx) in paragraphs" :key="idx">{{ para }}</p>
    </div>

    <div class="chapter-nav">
      <button 
        :disabled="currentChapterIndex <= 0" 
        @click="prevChapter"
      >上一章</button>
      <button 
        :disabled="currentChapterIndex >= chapters.length - 1" 
        @click="nextChapter"
      >下一章</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useReadingStore } from '../stores/reading'

const route = useRoute()
const router = useRouter()
const readingStore = useReadingStore()
const contentRef = ref(null)
const showSettings = ref(false)
const scrollTimer = ref(null)
const scrollPosition = ref(0)

const chapter = computed(() => {
  return readingStore.chapters.find(ch => ch.id === route.params.chapterId)
})

const chapterTitle = computed(() => chapter.value?.title || '')
const paragraphs = computed(() => {
  if (!chapter.value?.content) return []
  return chapter.value.content.split('\n').filter(p => p.trim())
})

const currentChapterIndex = computed(() => {
  return readingStore.chapters.findIndex(ch => ch.id === route.params.chapterId)
})

const nightMode = ref(readingStore.nightMode)
const fontSize = ref(readingStore.fontSize)
const lineHeight = ref(readingStore.lineHeight)

const readerClasses = computed(() => ({
  'night-mode': nightMode.value,
  [`font-${fontSize.value}`]: true,
}))

onMounted(async () => {
  await readingStore.loadNovel(route.params.novelId)
  if (readingStore.isAuthenticated) {
    await readingStore.loadProgress(route.params.novelId)
    if (readingStore.progress && readingStore.progress.chapter_id !== route.params.chapterId) {
      // Optionally redirect to last read chapter
    }
  }
})

const applySetting = (key, value) => {
  readingStore.updateSettings({ [key]: value })
}

const handleScroll = () => {
  scrollPosition.value = contentRef.value?.scrollTop || 0
  if (scrollTimer.value) clearTimeout(scrollTimer.value)
  scrollTimer.value = setTimeout(() => {
    if (chapter.value) {
      readingStore.saveProgress(route.params.novelId, chapter.value.id, scrollPosition.value)
    }
  }, 1000)
}

const navigateToChapter = (index) => {
  if (index >= 0 && index < readingStore.chapters.length) {
    router.push({
      name: 'Reader',
      params: { novelId: route.params.novelId, chapterId: readingStore.chapters[index].id }
    })
  }
}

const prevChapter = () => navigateToChapter(currentChapterIndex.value - 1)
const nextChapter = () => navigateToChapter(currentChapterIndex.value + 1)
const goBack = () => router.push({ name: 'NovelDetail', params: { novelId: route.params.novelId } })

onBeforeUnmount(() => {
  if (scrollTimer.value) clearTimeout(scrollTimer.value)
  if (chapter.value) {
    readingStore.saveProgress(route.params.novelId, chapter.value.id, scrollPosition.value)
  }
})
</script>
