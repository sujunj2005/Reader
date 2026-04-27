<template>
  <div class="bookshelf">
    <h1>我的书架</h1>
    <div class="filters">
      <select v-model="filterStatus" @change="filterNovels">
        <option value="all">全部</option>
        <option value="reading">在读</option>
        <option value="want_to_read">想读</option>
        <option value="completed">已读完</option>
        <option value="dropped">已放弃</option>
      </select>
    </div>

    <div class="novel-grid">
      <div v-for="novel in filteredNovels" :key="novel.novel_id" class="novel-card">
        <router-link :to="{ name: 'NovelDetail', params: { novelId: novel.novel_id } }">
          <h3>{{ novel.title }}</h3>
          <p v-if="novel.author">{{ novel.author }}</p>
        </router-link>
        <div class="novel-actions">
          <select :value="novel.status" @change="updateStatus(novel.user_novel_id, $event.target.value)">
            <option value="reading">在读</option>
            <option value="want_to_read">想读</option>
            <option value="completed">已读完</option>
            <option value="dropped">已放弃</option>
          </select>
          <button @click="removeNovel(novel.user_novel_id)" class="remove-btn">移除</button>
        </div>
      </div>
    </div>

    <p v-if="filteredNovels.length === 0" class="empty-message">书架是空的，去搜索喜欢的小说吧！</p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useBookshelfStore } from '../stores/bookshelf'

const bookshelfStore = useBookshelfStore()
const filterStatus = ref('all')
const filteredNovels = ref([])

onMounted(async () => {
  await bookshelfStore.loadBookshelf()
  filteredNovels.value = bookshelfStore.novels
})

const filterNovels = () => {
  if (filterStatus.value === 'all') {
    filteredNovels.value = bookshelfStore.novels
  } else {
    filteredNovels.value = bookshelfStore.novels.filter(n => n.status === filterStatus.value)
  }
}

const updateStatus = async (userNovelId, status) => {
  await bookshelfStore.updateStatus(userNovelId, status)
}

const removeNovel = async (userNovelId) => {
  await bookshelfStore.removeFromBookshelf(userNovelId)
  filterNovels()
}
</script>
