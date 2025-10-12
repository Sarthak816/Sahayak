<script setup>
import { ref, onMounted } from 'vue'
import { useAuth } from '@/composables/useAuth'

onMounted(() => {
  let { user } = useAuth()
  console.log(user.value)
})

const isOpen = ref(false)

const toggleMenu = () => {
  isOpen.value = !isOpen.value
}
</script>

<template>
  <nav class="w-full border-b border-gray-200">
    <!-- Desktop Navigation -->
    <div class="hidden md:flex flex-row items-center justify-center gap-8 px-8 py-4">
      <router-link to="/" class="text-3xl font-display">SAHAYAK</router-link>
      <router-link to="/employee/login" class="text-lg font-medium hover:text-blue-600
        transition-colors" v-if="user">Login</router-link>
      <router-link to="/employee/dashboard" class="text-lg font-medium hover:text-blue-600
        transition-colors" v-else>Dashboard</router-link>
      <router-link to="/services" class="text-lg font-medium hover:text-blue-600 transition-colors">Services</router-link>
      <router-link to="/chatbot" class="text-lg font-medium hover:text-blue-600 transition-colors">Support</router-link>
    </div>

    <!-- Mobile Navigation -->
    <div class="md:hidden">
      <div class="flex items-center justify-between px-4 py-4">
        <router-link to="/" class="text-2xl font-display">SAHAYAK</router-link>
        <button
          @click="toggleMenu"
          class="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          aria-label="Toggle menu"
        >
          <!-- Hamburger Icon -->
          <svg v-if="!isOpen" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
          <!-- Close Icon -->
          <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Mobile Menu -->
      <div v-if="isOpen" class="px-4 pb-4 flex flex-col gap-3 border-t border-gray-200 pt-3">
        <router-link to="/employee/login" class="py-2 hover:text-blue-600 transition-colors" @click="isOpen = false">Login</router-link>
        <router-link to="/services" class="py-2 hover:text-blue-600 transition-colors" @click="isOpen = false">Services</router-link>
        <router-link to="/chatbot" class="py-2 hover:text-blue-600 transition-colors" @click="isOpen = false">Support</router-link>
      </div>
    </div>
  </nav>
</template>
