<template>
  <div>
    <Navbar />

    <RouterView> </RouterView>
  </div>
</template>

<script>
import { RouterView } from 'vue-router'
import Navbar from './Navbar.vue'
export default {
  name: 'UserMain',
  components: {
    RouterView,
    Navbar
  }
}
</script>

<style></style>
