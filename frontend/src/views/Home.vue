<template>
  <div class="home-page">
    <h1>欢迎使用 Novel Reader</h1>
    <p>您已成功登录</p>
    <button @click="handleLogout">登出</button>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}
</script>
