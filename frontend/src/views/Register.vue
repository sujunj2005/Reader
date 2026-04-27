<template>
  <div class="register-page">
    <h2>注册</h2>
    <form @submit.prevent="handleRegister">
      <input v-model="email" type="email" placeholder="邮箱" required />
      <input v-model="password" type="password" placeholder="密码 (至少8位)" required minlength="8" />
      <input v-model="confirmPassword" type="password" placeholder="确认密码" required />
      <button type="submit" :disabled="authStore.loading || password !== confirmPassword">注册</button>
    </form>
    <router-link to="/login">已有账号？登录</router-link>
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
const confirmPassword = ref('')

const handleRegister = async () => {
  if (password.value !== confirmPassword.value) return
  await authStore.register(email.value, password.value)
  router.push('/')
}
</script>
