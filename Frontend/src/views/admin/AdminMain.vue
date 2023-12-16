<template>
  <div>
    <AdminNav />

    <RouterView> </RouterView>
  </div>
</template>

<script>
import { RouterView } from 'vue-router'
import AdminNav from './AdminNav.vue'
export default {
  name: 'AdminMain',
  components: {
    RouterView,
    AdminNav
  }
}
</script>

<style></style>
