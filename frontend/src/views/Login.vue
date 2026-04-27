<template>
  <div class="login-page">
    <h2>登录</h2>
    <form @submit.prevent="handleLogin">
      <input v-model="email" type="email" placeholder="邮箱" required />
      <input v-model="password" type="password" placeholder="密码" required />
      <button type="submit" :disabled="authStore.loading">登录</button>
    </form>
    <router-link to="/register">没有账号？注册</router-link>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const email = ref('')
const password = ref('')

const handleLogin = async () => {
  await authStore.login(email.value, password.value)
  router.push('/')
}
</script>
