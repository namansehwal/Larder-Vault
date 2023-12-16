// base nav bar for admin with logo and links to admin pages and logout button. Add bootstrap
classes for styling.
<script>
export default {
  name: 'AdminNav',
  data: function () {
    return {
      role: localStorage.getItem('role'),
      show: false
    }
  },
  methods: {
    toggleNavbar() {
      this.show = !this.show
    }
  }
}
</script>
<style scoped>
.navbar-logo {
  max-height: 150px;
  width: auto;
  margin-left: 13px;
  margin-top: -35px;
  margin-bottom: -35px;
  

}
.nav-link {
  font-size: 1.4em;
}
</style>
<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <router-link class="navbar-brand fs-4" to="/admin/dashboard">
      <img  src="https://raw.githubusercontent.com/namansehwal/Assets/main/a1.png" alt="Ecomart Logo" class="navbar-logo"/>
    </router-link>
    <div class="container">
      <button class="navbar-toggler" type="button" @click="toggleNavbar">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div :class="{ collapse: !show, 'navbar-collapse': true }" id="navbarSupportedContent">
        <ul class="navbar-nav mx-auto">
          <!-- Products and Category are visible for both admin and store-manager -->
          <li class="nav-item">
            <router-link class="nav-link" to="/admin/product">Products</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/admin/category">Category</router-link>
          </li>
          <!-- Requests is visible only for admin -->
          <li class="nav-item" >
            <router-link class="nav-link" to="/admin/requests">Requests</router-link>
          </li>
       
        </ul>
        <form class="">
          <button class="btn btn-outline-danger" type="button">
            <router-link class="nav-link" to="/admin/dashboard">
              Role: {{ role.toUpperCase() }}
            </router-link>
          </button>
          <button class="btn btn-danger m-3" type="button">
            <router-link class="nav-link" to="/logout">Logout</router-link>
          </button>
        </form>
      </div>
    </div>
  </nav>
</template>
