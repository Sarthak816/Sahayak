<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { createClient } from '@supabase/supabase-js';

const router = useRouter();
const isLogin = ref(true);
const user = ref(null);

// Supabase Configuration
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
  console.error('Supabase credentials are missing. Please check your .env file');
}

const supabase = createClient(supabaseUrl, supabaseAnonKey);

// Form data
const formData = ref({
  email: '',
  password: '',
  username: '',
  name: ''
});

const forgotPasswordEmail = ref('');
const showForgotPassword = ref(false);
const message = ref('');
const error = ref('');
const loading = ref(false);

// Check if user is already logged in
onMounted(async () => {
  const { data: { session } } = await supabase.auth.getSession();

  if (session) {
    await fetchUserProfile(session.user);
  }

  // Listen for auth state changes
  supabase.auth.onAuthStateChange(async (event, session) => {
    if (event === 'SIGNED_IN' && session) {
      await fetchUserProfile(session.user);
    } else if (event === 'SIGNED_OUT') {
      user.value = null;
    }
  });
});

const fetchUserProfile = async (authUser) => {
  try {
    const { data, error: profileError } = await supabase
      .from('profiles')
      .select('*')
      .eq('id', authUser.id)
      .single();

    if (profileError) throw profileError;

    user.value = {
      id: authUser.id,
      email: authUser.email,
      name: data?.name,
      username: data?.username,
    };
  } catch (err) {
    console.error('Error fetching profile:', err);
    user.value = {
      id: authUser.id,
      email: authUser.email,
    };
  }
};

const handleLogin = async () => {
  error.value = '';
  message.value = '';
  loading.value = true;

  try {
    const { data, error: signInError } = await supabase.auth.signInWithPassword({
      email: formData.value.email,
      password: formData.value.password,
    });

    if (signInError) throw signInError;

    await fetchUserProfile(data.user);

    // Redirect to dashboard
    console.log(data)
    router.push('/employee/dashboard');
  } catch (err) {
    error.value = err.message || 'Login failed';
  } finally {
    loading.value = false;
  }
};

const handleForgotPassword = async () => {
  error.value = '';
  message.value = '';
  loading.value = true;

  try {
    const { error: resetError } = await supabase.auth.resetPasswordForEmail(
      forgotPasswordEmail.value,
      {
        redirectTo: `${window.location.origin}/reset-password`,
      }
    );

    if (resetError) throw resetError;

    message.value = 'Password reset link sent to your email';
    showForgotPassword.value = false;
    forgotPasswordEmail.value = '';
  } catch (err) {
    error.value = err.message || 'Failed to send reset email';
  } finally {
    loading.value = false;
  }
};

const handleLogout = async () => {
  try {
    const { error: signOutError } = await supabase.auth.signOut();
    if (signOutError) throw signOutError;

    user.value = null;
    router.push('/login');
  } catch (err) {
    console.error('Logout error:', err);
  }
};

const toggleForm = () => {
  isLogin.value = !isLogin.value;
  error.value = '';
  message.value = '';
  formData.value = {
    email: '',
    password: '',
    username: '',
    name: ''
  };
};

const toggleForgotPassword = () => {
  showForgotPassword.value = !showForgotPassword.value;
  error.value = '';
  message.value = '';
};
</script>

<template>
  <div class="login-container">
    <!-- Logged In View -->
    <div v-if="user" class="user-info">
      <h2>Welcome, {{ user.name || user.email }}!</h2>
      <p>{{ user.email }}</p>
      <button @click="handleLogout" class="btn logout-btn" :disabled="loading">
        {{ loading ? 'Logging out...' : 'Logout' }}
      </button>
    </div>

    <!-- Login/Register Form -->
    <div v-else class="auth-form">
      <!-- Forgot Password Modal -->
      <div v-if="showForgotPassword" class="forgot-password-modal">
        <h2>Reset Password</h2>
        <p class="subtitle">Enter your email to receive a password reset link</p>

        <input
          v-model="forgotPasswordEmail"
          type="email"
          placeholder="Email"
          class="input-field"
          :disabled="loading"
        />

        <button
          @click="handleForgotPassword"
          class="btn primary-btn"
          :disabled="loading || !forgotPasswordEmail"
        >
          {{ loading ? 'Sending...' : 'Send Reset Link' }}
        </button>

        <button @click="toggleForgotPassword" class="link-btn" :disabled="loading">
          Back to Login
        </button>
      </div>

      <!-- Login/Register Forms -->
      <div v-else>
        <h2>{{ isLogin ? 'Sign In' : 'Create Account' }}</h2>

        <!-- Error/Success Messages -->
        <div v-if="error" class="message error-message">{{ error }}</div>
        <div v-if="message" class="message success-message">{{ message }}</div>

        <!-- Register Form -->
        <form v-if="!isLogin" @submit.prevent="handleRegister" class="form">
          <input
            v-model="formData.name"
            type="text"
            placeholder="Full Name"
            required
            class="input-field"
            :disabled="loading"
          />
          <input
            v-model="formData.username"
            type="text"
            placeholder="Username"
            required
            class="input-field"
            :disabled="loading"
          />
          <input
            v-model="formData.email"
            type="email"
            placeholder="Email"
            required
            class="input-field"
            :disabled="loading"
          />
          <input
            v-model="formData.password"
            type="password"
            placeholder="Password (min 6 characters)"
            required
            minlength="6"
            class="input-field"
            :disabled="loading"
          />
          <button type="submit" class="btn primary-btn" :disabled="loading">
            {{ loading ? 'Registering...' : 'Register' }}
          </button>
        </form>

        <!-- Login Form -->
        <form v-else @submit.prevent="handleLogin" class="form">
          <input
            v-model="formData.email"
            type="email"
            placeholder="Email"
            required
            class="input-field"
            :disabled="loading"
          />
          <input
            v-model="formData.password"
            type="password"
            placeholder="Password"
            required
            class="input-field"
            :disabled="loading"
          />
          <button type="submit" class="btn primary-btn" :disabled="loading">
            {{ loading ? 'Signing in...' : 'Sign In' }}
          </button>
        </form>

        <!-- Forgot Password Link -->
        <div v-if="isLogin" class="forgot-password-link">
          <button @click="toggleForgotPassword" class="link-btn" :disabled="loading">
            Forgot Password?
          </button>
        </div>

        <!-- Toggle between Login/Register -->
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  max-width: 450px;
  margin: 50px auto;
  padding: 30px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  color: #333;
  margin-bottom: 10px;
}

.subtitle {
  text-align: center;
  color: #666;
  font-size: 14px;
  margin-bottom: 20px;
}

.user-info {
  text-align: center;
}

.user-info p {
  color: #666;
  margin: 10px 0 20px;
}

.auth-form {
  width: 100%;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 20px;
}

.input-field {
  padding: 12px 16px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 15px;
  transition: border-color 0.3s;
}

.input-field:focus {
  outline: none;
  border-color: #4285f4;
}

.input-field:disabled {
  background: #f5f5f5;
  cursor: not-allowed;
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.primary-btn {
  background: #4285f4;
  color: white;
  margin-top: 10px;
}

.primary-btn:hover:not(:disabled) {
  background: #357ae8;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(66, 133, 244, 0.3);
}

.logout-btn {
  background: #dc3545;
  color: white;
}

.logout-btn:hover:not(:disabled) {
  background: #c82333;
}

.link-btn {
  background: none;
  border: none;
  color: #4285f4;
  cursor: pointer;
  font-size: 14px;
  padding: 5px;
  text-decoration: underline;
}

.link-btn:hover:not(:disabled) {
  color: #357ae8;
}

.link-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.toggle-form {
  text-align: center;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #e0e0e0;
}

.toggle-form p {
  color: #666;
  margin: 0;
}

.forgot-password-link {
  text-align: right;
  margin-top: -10px;
  margin-bottom: 10px;
}

.forgot-password-modal {
  text-align: center;
}

.message {
  padding: 12px;
  border-radius: 6px;
  margin-bottom: 15px;
  font-size: 14px;
}

.error-message {
  background: #fee;
  color: #c33;
  border: 1px solid #fcc;
}

.success-message {
  background: #efe;
  color: #3c3;
  border: 1px solid #cfc;
}
</style>
