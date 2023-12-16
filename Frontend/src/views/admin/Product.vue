<!-- ProductPage.vue -->
<template>
  <div>
    <div class="container">
      <div class="row">
        <div class="col-lg-12">
          <h1 class="text-center text-white m-3">Manage Products</h1>

          <div>
            <!-- Button trigger modal -->
            <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addProductModal">
              Add New Product
            </button>

            <div class="row">
              <div class="col-lg-3 mt-3 " v-for="(product, index) in products" :key="index">
                <div class="card m-1">
                  <!-- Display product information -->
                  <img :src="product.image" class="card-img-top" alt="..." style="height: 400px" />
                  <div class="card-body">
                    <!-- image -->

                    <h5 class="card-title ">{{ product.name }}</h5>
                    <p>Category: {{ product.category_name }}</p>
                    <p>Price: {{ product.price }}</p>
                    <p>Quantity: {{ product.quantity }}</p>
                    <p>SI Unit: {{ product.si_unit }}</p>
                    <p>Best Before: {{ product.best_before }}</p>

                    <!-- Add/Edit/Delete buttons for the product -->
                    <button class="btn btn-outline-secondary btn-sm m-1" @click="openEditProductModal(product)"
                      data-bs-toggle="modal" data-bs-target="#editProductModal">
                      Edit Product
                    </button>
                    <button class="btn btn-outline-danger btn-sm m-1" @click="deleteProduct(product.id)">
                      Delete
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Product Modal -->
    <div class="modal fade text-dark" id="addProductModal" tabindex="-1" aria-labelledby="addProductModalLabel"
      aria-hidden="true">
      <!-- Add Product Modal Content -->
      <!-- Add Product Modal Content -->
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="addProductModalLabel">Add New Product</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <!-- Add Product Form -->
            <form @submit.prevent="addProduct">
              <!-- Product Name -->
              <div class="mb-3">
                <label for="productName" class="form-label">Product Name</label>
                <input type="text" class="form-control" id="productName" v-model="newProduct.name" required />
              </div>

              <!-- Category -->
              <div class="mb-3">
                <label for="productCategory" class="form-label">Category</label>
                <select class="form-select" id="productCategory" v-model="newProduct.category_id" required>
                  <!-- Populate with categories dynamically if available -->
                  <option v-for="category in categories" :key="category.id" :value="category.id">
                    {{ category.name }}
                  </option>
                </select>
              </div>

              <!-- Price -->
              <div class="mb-3">
                <label for="productPrice" class="form-label">Price</label>
                <input type="number" class="form-control" id="productPrice" v-model="newProduct.price" required />
              </div>

              <!-- Quantity -->
              <div class="mb-3">
                <label for="productQuantity" class="form-label">Quantity</label>
                <input type="number" class="form-control" id="productQuantity" v-model="newProduct.quantity" required />
              </div>

              <!-- SI Unit -->
              <div class="mb-3">
                <label for="productSIUnit" class="form-label">SI Unit</label>
                <input type="text" class="form-control" id="productSIUnit" v-model="newProduct.si_unit" required />
              </div>

              <!-- Best Before -->
              <div class="mb-3">
                <label for="productBestBefore" class="form-label">Best Before</label>
                <input type="date" class="form-control" id="productBestBefore" v-model="newProduct.best_before"
                  required />
              </div>

              <button type="submit" class="btn btn-primary">Add Product</button>
            </form>
          </div>
        </div>
      </div>

      <!-- Similar structure to the existing modals for adding and editing categories -->
    </div>

    <!-- Add Product Modal Content -->

    <!-- Edit Product Modal -->
    <div class="modal fade text-dark" id="editProductModal" tabindex="-1" aria-labelledby="editProductModalLabel"
      aria-hidden="true">
      <!-- Edit Product Modal Content -->
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="editProductModalLabel">Edit Product</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <!-- Edit Product Form -->
            <form @submit.prevent="editProduct">
              <!-- Product Name -->
              <div class="mb-3">
                <label for="editProductName" class="form-label">Product Name</label>
                <input type="text" class="form-control" id="editProductName" v-model="editedProduct.name" required />
              </div>

              <!-- Category -->
              <div class="mb-3">
                <label for="editProductCategory" class="form-label">Category</label>
                <select class="form-select" id="editProductCategory" v-model="editedProduct.category_id" required>
                  <!-- Populate with categories dynamically if available -->
                  <option v-for="category in categories" :key="category.id" :value="category.id">
                    {{ category.name }}
                  </option>
                </select>
              </div>

              <!-- Price -->
              <div class="mb-3">
                <label for="editProductPrice" class="form-label">Price</label>
                <input type="number" class="form-control" id="editProductPrice" v-model="editedProduct.price" required />
              </div>

              <!-- Quantity -->
              <div class="mb-3">
                <label for="editProductQuantity" class="form-label">Quantity</label>
                <input type="number" class="form-control" id="editProductQuantity" v-model="editedProduct.quantity"
                  required />
              </div>

              <!-- SI Unit -->
              <div class="mb-3">
                <label for="editProductSIUnit" class="form-label">SI Unit</label>
                <input type="text" class="form-control" id="editProductSIUnit" v-model="editedProduct.si_unit" required />
              </div>

              <!-- Best Before -->
              <div class="mb-3">
                <label for="editProductBestBefore" class="form-label">Best Before</label>
                <input type="date" class="form-control" id="editProductBestBefore" v-model="editedProduct.best_before"
                  required />
              </div>

              <button type="submit" class="btn btn-primary">Update Product</button>
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
  name: 'ProductPage',

  data() {
    return {
      products: [],
      newProduct: {
        name: '',
        category_id: null,
        price: null,
        quantity: null,
        si_unit: '',
        best_before: null
        // Add other properties as needed for the new product form
      },
      editedProduct: {
        id: null,
        name: '',
        category_id: null,
        price: null,
        quantity: null,
        si_unit: '',
        best_before: null,
        created_by: null
      },
      categories: [] // Assuming you have a list of categories
    }
  },

  methods: {
    async getProducts() {
      try {
        const response = await axios.get('http://localhost:5000/product', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`
          }
        })
        this.products = response.data
      } catch (error) {
        console.error('Error fetching products', error)
      }
    },

    async getCategories() {
      try {
        const response = await axios.get('http://localhost:5000/category', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`
          }
        })
        this.categories = response.data
      } catch (error) {
        console.error('Error fetching categories', error)
      }
    },

    async addProduct() {
      try {
        const imageUrl = await window.get_Url(this.newProduct.name)
        this.newProduct.created_by = localStorage.getItem('username')
        this.newProduct.image = imageUrl
        console.log('Adding product', this.newProduct)

        const response = await axios.post('http://localhost:5000/product', this.newProduct, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`
          }
        })

        // Handle success (you might want to refresh the product list or perform other actions)
        console.log('Product added successfully', response.data)
        this.getProducts()
        // Close the modal
        // $('#addProductModal').modal('hide')

        // Reset the newProduct object for the next addition
        this.newProduct = {
          name: '',
          category_id: null,
          price: null,
          quantity: null,
          si_unit: '',
          best_before: null
          // Add other properties as needed for the new product form
        }

        // Optionally, refresh the product list
      } catch (error) {
        // Handle errors
        console.error('Error adding product', error)
      }
    },

    getCategoryName(categoryId) {
      // Fetch and return the category name based on the category_id
      const category = this.categories.find((cat) => cat.id === categoryId)
      return category ? category.name : 'Unknown Category'
    },

    async deleteProduct(id) {
      try {
        await axios.delete(`http://localhost:5000/product/${id}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`
          }
        })
        this.getProducts()
      } catch (error) {
        console.error('Error deleting product', error)
      }
    },
    openEditProductModal(product) {
      // Set the editedProduct object based on the selected product
      this.editedProduct = { ...product }
    },

    async editProduct() {
      try {
        // Perform the edit operation using axios or your preferred method
        const imageUrl = await window.get_Url(this.editedProduct.name)
        this.editedProduct.image = imageUrl
        const response = await axios.put(
          `http://localhost:5000/product/${this.editedProduct.id}`,
          this.editedProduct,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('access_token')}`
            }
          }
        )

        // Handle success (you might want to refresh the product list or perform other actions)
        console.log('Product updated successfully', response.data)
        this.getProducts()

        // Close the modal
        // $('#editProductModal').modal('hide')

        // Reset the editedProduct object
        this.editedProduct = {
          id: null,
          name: '',
          category_id: null,
          price: null,
          quantity: null,
          si_unit: '',
          best_before: null
        }

        // Optionally, refresh the product list
      } catch (error) {
        // Handle errors
        console.error('Error updating product', error)
      }
    }
  },

  mounted() {
    this.getProducts()
    this.getCategories()
  }
}
</script>

<style scoped>
.card {
  font-family: 'Poppins', sans-serif;
}

.card {
  position: relative;
  animation: scaleUp 0.9s ease forwards;
  transition: transform 0.3s ease;
  z-index: 2;
  /* Ensure the card is above the pseudo-element */
}

.card::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  background: inherit;
  /* Inherit the background from the card */
  filter: blur(0);
  transition: filter 0.3s ease;
  z-index: -1;

  /* Place this pseudo-element behind the content of the card */
}

.card:hover::before {
  filter: blur(5px);
  /* Apply the blur effect on hover */
}

@keyframes scaleUp {
  from {
    transform: scale(0);
  }

  to {
    transform: scale(1);
  }
}
</style>
