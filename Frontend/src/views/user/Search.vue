<template>
  <div class="container mt-5 ">
    <div class="row">
      <div class="col-md-12">
        <form @submit.prevent="searchProducts" class="form-inline w-100">
          <div class="form-group">
            <label for="searchCriteria">Search by:</label>
            <select v-model="searchCriteria" class="form-control" id="searchCriteria">
              <option value="category">Category</option>
              <option value="price">Price</option>
              <option value="manufactureDate">Expiry Date</option>
            </select>
          </div>
          <div v-if="searchCriteria === 'category'" class="form-group col-md-7">
            <label for="category">Category:</label>
            <select v-model="searchValue" class="form-control" id="category" :placeholder="'Select a category'">
              <option value="" disabled>Select a category</option>
              <option v-for="category in categories" :key="category.id" :value="category.id">
                {{ category.name }}
              </option>
            </select>
          </div>
          <div v-else class="form-group col-md-7"
            :style="{ 'max-width': searchCriteria === 'manufactureDate' ? '100%' : 'initial' }">
            <label :for="searchCriteria">{{ capitalize(searchCriteria) }}:</label>
            <input :type="inputType" v-model="searchValue" class="form-control" :id="searchCriteria"
              :placeholder="'Enter ' + capitalize(searchCriteria)" />
          </div>
          <button type="submit" class="btn btn-primary mt-3">Search</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      searchCriteria: 'category',
      searchValue: '',
      categories: [] // New property to store categories
    }
  },
  created() {
    this.fetchCategories()
  },
  methods: {
    async fetchCategories() {
      try {
        const response = await axios.get('http://localhost:5000/category')
        this.categories = response.data
      } catch (error) {
        console.error('Error fetching categories:', error)
      }
    },
    searchProducts() {
      // Define the query parameter keys based on the selected search criteria
      const queryParamKeys = {
        category: 'category_id',
        price: 'price',
        manufactureDate: 'best_before'
      }

      // Build the params object with the correct key
      const params = {
        [queryParamKeys[this.searchCriteria]]: this.searchValue
      }

      // Redirect to the same page with the updated query params
      this.$router.push({ name: 'UserProduct', query: params })
    },
    capitalize(str) {
      return str.charAt(0).toUpperCase() + str.slice(1)
    }
  },
  computed: {
    inputType() {
      // Determine the input type based on the selected search criteria
      return this.searchCriteria === 'manufactureDate' ? 'date' : 'text'
    }
  }
}
</script>
<style scoped>
.form-inline {
  display: flex;
  align-items: center;
}

.form-group {
  margin-right: 1rem;
}
</style>
