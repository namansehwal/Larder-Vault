<template>
  <div class="login">
    <div class="container-fluid">
      <div class="row justify-content-center align-items-center min-vh-100">
        <!-- Background Image with Overlayed Login Form -->
        <div class="col-12 col-md-8 p-0">
          <div class="row g-0">
            <!-- Background Image Section -->
            <div class="col-lg-4 d-none d-lg-block login-bg-image"
              style="background-image: url('https://raw.githubusercontent.com/namansehwal/Assets/main/login.webp');">
            </div>

            <!-- Login Form Section -->
            <div class="col-12 col-lg-6">
              <div class="login__container border rounded p-4 shadow-lg animate__animated animate__zoomIn bg-white">
                <h1 class="text-center text-success mb-4">Login For the Larder Vault</h1>
                <form @submit.prevent="login">
                  <div class="mb-3">
                    <label for="username" class="form-label text-dark">Username:</label>
                    <input type="text" id="username" class="form-control text-dark" v-model="username"
                      placeholder="Enter your UserName Here!" />
                  </div>
                  <div class="mb-3">
                    <label for="password" class="form-label text-dark">Password:</label>
                    <input type="password" id="password" class="form-control text-dark" v-model="password"
                      placeholder="********" />
                  </div>
                  <button type="submit" class="login__signInButton btn btn-success w-100 mb-2">Login</button>
                  <button type="button" class="login__registerButton btn btn-outline-primary w-100"
                    @click="registerModal = true" data-bs-toggle="modal" data-bs-target="#signupModal">
                    Create your Account
                  </button>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <RegisterModal v-if="registerModal" />
  </div>
</template>



<style scoped>
.login-bg-image {
  background-size: cover;
  background-position: center;
}

.login__container {
  font-family: 'Roboto', sans-serif;
  /* Changed to Roboto font */
  animation-duration: 1s;
  /* Adjust animation duration */
}

/* Add any additional styles for animations and fonts here */
</style>



<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import RegisterModal from '../modals/RegisterModal.vue'

const router = useRouter()

const username = ref('')
const password = ref('')

const registerModal = ref(false)

const login = async () => {
  const form_details = {
    username: username.value,
    password: password.value
  }

  try {
    const { data } = await axios.post('http://localhost:5000/login', form_details, {
      headers: { 'Content-Type': 'application/json' }
    })

    localStorage.clear()

    if (data.access_token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${data.access_token}`
      localStorage.setItem('access_token', data.access_token)
    }

    try {
      const response = await axios.get('http://localhost:5000/user_details')
      const { role, email, username, id } = response.data.logged_in_as

      localStorage.setItem('role', role)
      localStorage.setItem('email', email)
      localStorage.setItem('username', username)
      localStorage.setItem('id', id)
      localStorage.setItem('expires_at', Date.now() + 3600000)

      if (JSON.stringify(role) === '"admin"') {
        router.push('/admin/dashboard')
      }
      else if (JSON.stringify(role) === '"store-manager"') {
        router.push('/store_manager/product')
      }
      else if (JSON.stringify(role) === '"user"') {
        router.push('/user/product')
      }
    } catch (error) {
      console.error('Error fetching user details:', error)
    }
  } catch (error) {
    alert(error.response.data.message)
  }
}
</script>

