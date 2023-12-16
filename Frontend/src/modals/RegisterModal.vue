<template>
  <div>
    <div
      class="modal fade"
      id="signupModal"
      tabindex="-1"
      role="dialog"
      aria-labelledby="signupModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog" role="document">
        <div class="modal-content bg-dark text-light">
          <div class="modal-header">
            <h5 class="modal-title" id="signupModalLabel">
              New Account Creation for
              <button class="btn btn-primary btn-sm">
                {{ isStoreManager ? 'Store Manager' : 'User' }}
              </button>
            </h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="signup">
              <div class="mb-3">
                <label for="email" class="form-label">Email:</label>
                <input v-model="email" type="email" class="form-control" id="email" required />
              </div>

              <div class="mb-3">
                <label for="username" class="form-label">Username:</label>
                <input v-model="username" type="text" class="form-control" id="username" required />
              </div>

              <div class="mb-3">
                <label for="password" class="form-label">Password:</label>
                <input
                  v-model="password"
                  type="password"
                  class="form-control"
                  id="password"
                  required
                />
              </div>

              <!-- Toggle button for switching between User and Store Manager -->
              <div class="mb-3 form-check form-switch">
                <input
                  v-model="isStoreManager"
                  type="checkbox"
                  class="form-check-input"
                  id="toggleRole"
                />
                <label class="form-check-label" for="toggleRole"
                  ><i><b>Switch Role. </b></i></label
                >
              </div>

              <button type="submit" class="btn btn-success">Sign Up</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      email: '',
      username: '',
      password: '',
      isStoreManager: false
    }
  },
  methods: {
    signup() {
      const endpoint = this.isStoreManager
        ? 'http://localhost:5000/register/store-manager'
        : 'http://localhost:5000/register/user'

      axios
        .post(endpoint, {
          email: this.email,
          username: this.username,
          password: this.password,
          is_approved: this.isStoreManager ? 0 : 1
        })
        .then((response) => {
          if (response.status === 201) {
            alert(response.data.message)
            window.location.reload()
          } else {
            alert('Registration failed. Please try again.')
          }
        })
        .catch((error) => {
          alert(error.response.data.message)
        })
    }
  }
}
</script>
<style scoped></style>
