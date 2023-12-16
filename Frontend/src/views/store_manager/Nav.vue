// base nav bar for admin with logo and links to admin pages and logout button. Add bootstrap
classes for styling.
<script>
import axios from 'axios'

export default {
  name: 'SM_Nav',
  data: function () {
    return {
      role: localStorage.getItem('role'),
      show: false
    }
  },
  methods: {
    toggleNavbar() {
      this.show = !this.show
    },
    downloadReport() {
      alert('Downloading the report...');
      (async () => {
        try {
          const res = await axios.get('http://localhost:5000/get-csv', {
            headers: {
              'Content-Type': 'application/json',
              'Access-Control-Allow-Origin': '*',
              Authorization: 'Bearer ' + localStorage.getItem('access_token')
            }
          })
          const blob = new Blob([res.data], { type: 'text/csv' });
          const link = document.createElement('a');
          link.href = window.URL.createObjectURL(blob);
          link.download = 'report.csv';
          link.click();



        } catch (err) {
          console.log(err)
        }
      })();


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
      <img src="https://raw.githubusercontent.com/namansehwal/Assets/main/a1.png" alt="Ecomart Logo"
        class="navbar-logo" />
    </router-link>
    <div class="container">
      <button class="navbar-toggler" type="button" @click="toggleNavbar">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div :class="{ collapse: !show, 'navbar-collapse': true }" id="navbarSupportedContent">
        <ul class="navbar-nav mx-auto">
          <li class="nav-item">
            <router-link class="nav-link" to="/store_manager/product">Products</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/store_manager/category">Category</router-link>
          </li>
          <li class="nav-item">
            <i class="nav-link" @click="downloadReport"> Report</i>
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

