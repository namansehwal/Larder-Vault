<template>
  <div class="container mt-3">
    <div class="row">
      <div class="col-md-3" v-for="(category, key) in categories" :key="key">
        <div class="card mb-3" style="max-width: 300px">
          <img :src="category.image" class="card-img-top" style="height: 200px; object-fit: cover" alt="Category Image" />
          <div class="card-body">
            <h5 class="card-title">{{ category.name }}</h5>
            <router-link :to="{ name: 'UserProduct', query: { category_id: category.id } }" class="btn btn-primary fs-6">
              View Products
            </router-link>
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
      categories: []
    }
  },
  mounted() {
    this.fetchCategories()
  },
  methods: {
    fetchCategories() {
      axios
        .get('http://localhost:5000/category', {
          headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
        })
        .then((response) => {
          this.categories = Object.values(response.data) // Convert object to array
        })
        .catch((error) => {
          console.error('Error fetching categories:', error)
        })
    }
  }
}
</script>

<style scoped>
/* Add your custom styling here if needed */
</style>
