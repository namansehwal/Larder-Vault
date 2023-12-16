<template>
    <div>
      <SM_Nav />
  
      <RouterView> </RouterView>
    </div>
  </template>
  
  <script>
  import { RouterView } from 'vue-router'
  import SM_Nav from './Nav.vue'
  export default {
    name: 'SM_Main',
    components: {
      RouterView,
      SM_Nav
    }
  }
  </script>
  
  <style></style>
  