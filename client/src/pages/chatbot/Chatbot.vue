<template>
  <div class="flex w-full flex-col h-full bg-gray-50">
    <!-- Chat Messages Container -->
    <div class="flex-1 overflow-y-auto p-4 space-y-4">
      <div
        v-for="(message, index) in messages"
        :key="index"
        :class="['flex items-start gap-3', message.isUser ? 'flex-row-reverse' : 'flex-row']"
      >
        <!-- Avatar -->
        <div class="flex-shrink-0">
          <img
            :src="message.avatar"
            alt="Avatar"
            class="w-8 h-8 rounded-full"
          />
        </div>

        <!-- Message Content -->
        <div :class="['max-w-xs lg:max-w-md', message.isUser ? 'items-end' : 'items-start']">
          <div
            :class="['rounded-2xl px-4 py-2', message.isUser ? 'bg-blue-500 text-white' : 'bg-white text-gray-800 border border-gray-200']"
          >
            <p class="text-sm">{{ message.text }}</p>
          </div>
          <p class="text-xs text-gray-500 mt-1">
            {{ formatDateTime(message.timestamp) }}
          </p>
        </div>
      </div>
    </div>

    <!-- Input Area -->
    <div class="border-t border-gray-200 bg-white p-4">
      <form @submit.prevent="sendMessage" class="flex gap-2">
        <input
          v-model="newMessage"
          type="text"
          placeholder="Type your message..."
          class="flex-1 rounded-full border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
        <button
          type="submit"
          :disabled="!newMessage.trim()"
          class="rounded-full bg-blue-500 px-6 py-2 text-white font-medium hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Send
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

// Props with default avatar
const props = defineProps({
  userAvatar: {
    type: String,
    default: ''
  },
  botAvatar: {
    type: String,
    default: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=40&h=40&fit=crop&crop=face'
  }
})

// Reactive data
const messages = ref([])
const newMessage = ref('')

// Generate random avatar if not provided
const finalUserAvatar = ref(props.userAvatar || generateRandomAvatar())

// Initialize with welcome message
onMounted(() => {
  messages.value.push({
    text: 'Hello! How can I help you today?',
    isUser: false,
    timestamp: new Date(),
    avatar: props.botAvatar
  })
})

// Generate random avatar from Unsplash
function generateRandomAvatar() {
  const randomId = Math.floor(Math.random() * 1000)
  return `https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=40&h=40&fit=crop&crop=face&id=${randomId}`
}

// Format datetime as "HH:MM · DD/MM"
function formatDateTime(timestamp) {
  const date = new Date(timestamp)
  const hours = date.getHours().toString().padStart(2, '0')
  const minutes = date.getMinutes().toString().padStart(2, '0')
  const day = date.getDate().toString().padStart(2, '0')
  const month = (date.getMonth() + 1).toString().padStart(2, '0')
  return `${hours}:${minutes} · ${day}/${month}`
}

// Send message to API and handle response
async function sendMessage() {
  if (!newMessage.value.trim()) return

  const userMessage = {
    text: newMessage.value,
    isUser: true,
    timestamp: new Date(),
    avatar: finalUserAvatar.value
  }

  messages.value.push(userMessage)
  const currentMessage = newMessage.value
  newMessage.value = ''

  try {
    const response = await fetch('http://localhost:8000/api/v1/chatbot', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message: currentMessage })
    })

    if (!response.ok) throw new Error('Network response was not ok')

    const data = await response.json()

    const botMessage = {
      text: data.response || 'Thank you for your message!',
      isUser: false,
      timestamp: new Date(),
      avatar: props.botAvatar
    }

    messages.value.push(botMessage)
  } catch (error) {
    console.error('Error sending message:', error)

    const errorMessage = {
      text: 'Sorry, I encountered an error. Please try again.',
      isUser: false,
      timestamp: new Date(),
      avatar: props.botAvatar
    }

    messages.value.push(errorMessage)
  }
}
</script>
