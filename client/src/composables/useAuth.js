// composables/useAuth.js
import { ref } from 'vue'
import { authClient } from '@/lib/auth-client'

// Global reactive user state
const user = ref(null)

export function useAuth() {
  const login = async (email, password) => {
    const { data, error } = await authClient.auth.signInWithPassword({ email, password })
    if (data?.user) user.value = data.user
    return { data, error }
  }

  const logout = async () => {
    const { error } = await authClient.auth.signOut()
    user.value = null
    return { error }
  }

  // Check active session on initialization
  authClient.auth.getSession().then(({ data }) => {
    // Add null check here
    if (data && data.session) {
      user.value = data.session.user || null
    } else {
      user.value = null
    }
  }).catch((error) => {
    console.error('Error getting session:', error)
    user.value = null
  })

  authClient.auth.onAuthStateChange((_event, session) => {
    user.value = session?.user || null
  })

  return { user, login, logout }
}
