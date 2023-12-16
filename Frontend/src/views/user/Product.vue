<template>
  <div class="m-3">
    <!-- Recently Added Products Section -->
    <div>
      <div v-if="hasQueryParams">
        <center>
          <h1 class="mt-4">{{ search_message }}</h1>
        </center>
      </div>
      <div v-if="recentlyAdded.length && !hasQueryParams" class="mb-5">
        <h3>Recently Added Products</h3>
        <div class="row">
          <div v-for="product in recentlyAdded" :key="product.id" class="col-lg-2  ">
            <div :class="['card h-100', { 'card-out-of-stock': !isInStock(product), 'small-card': !isInStock(product) }]">
              <img :src="product.image" class="card-img-top product-image" alt="Product Image" />
              <div :class="['stock-status', { 'bg-success': isInStock(product), 'bg-danger': !isInStock(product) }]">
                {{ isInStock(product) ? product.quantity + ' In Stock' : 'Out of Stock' }}
              </div>

              <div class="card-body d-flex flex-column">
                <h5 class="card-title">{{ product.name }}</h5>

                <p class="card-text">
                  <span class="price-label">Price:</span> ₹{{ product.price }} {{ product.si_unit }}
                </p>
                <p class="card-text">
                  <label for="expiry-date">Expiry Date:</label> {{ product.best_before }}
                </p>
                <!-- Buy Button and Quantity Input -->
                <div class="mt-auto">
                  <label for="quantity">Quantity:</label>
                  <input type="number" class="form-control" v-model="product.quantityToBuy" :max="product.quantity"
                    :disabled="!isInStock(product)" />
                  <button class="btn btn-success mt-2" @click="addToCart(product)" :disabled="!isInStock(product)">Add to
                    Cart</button>

                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>


    <!-- Category-wise Products Section -->
    <div v-for="(category, categoryId) in categories" :key="categoryId">
      <hr />
      <h3>{{ category.category_name }}</h3>
      <div class="row">
        <div v-for="product in category.products" :key="product.id" class="col-lg-2 col-md-4 col-sm-6 mb-4">
          <div :class="['card h-100', { 'card-out-of-stock': !isInStock(product) }]">
            <img :src="product.image" class="card-img-top product-image" alt="Product Image" />
            <div :class="['stock-status', { 'bg-success': isInStock(product), 'bg-danger': !isInStock(product) }]">
              {{ isInStock(product) ? product.quantity + ' In Stock' : 'Out of Stock' }}
            </div>
            <div class="card-body d-flex flex-column">
              <h5 class="card-title">{{ product.name }}</h5>
              <div>
                <p class="card-text">
                  <span class="price-label">Price:</span> ₹{{ product.price }} {{ product.si_unit }}
                </p>

                <p class="card-text">
                  <label for="expiry-date">Category:</label> {{ category.category_name }}
                </p>
                <p class="card-text">
                  <label for="expiry-date">Expiry Date:</label> {{ product.best_before }}
                </p>
                <!-- Buy Button and Quantity Input -->
                <div class="mt-auto">
                  <label for="quantity">Quantity: </label>
                  <input type="number" class="form-control" v-model="product.quantityToBuy" :max="product.quantity"
                    :disabled="!isInStock(product)" />
                  <button class="btn btn-success mt-2" @click="addToCart(product)" :disabled="!isInStock(product)">Add to
                    Cart</button>


                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.card-out-of-stock .card-body {
  /* Adjust padding or margin as necessary for out-of-stock cards */
  padding-bottom: 10px;
  /* Example adjustment */
}

.product-image {
  height: 200px;
  object-fit: cover;
}

.stock-status {
  text-align: center;
  color: white;
  font-weight: bold;
  padding: 5px;
}

.card-out-of-stock {
  opacity: 0.5;

}



.price-label {
  /* font-weight: bold; */
  font-size: 1.2rem;
}

/* Additional styling as needed */


.card {
  position: relative;
  animation: scaleUp 2s ease forwards;
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

<script>
import axios from 'axios'

export default {
  data() {
    return {
      categories: {},
      recentlyAdded: [],
      queryParams: this.$route.query,
      search_message: ''
    }
  },

  mounted() {
    this.getProducts()
  },
  computed: {
    hasQueryParams() {
      // if no product is found
      if (Object.keys(this.categories).length == 0) {
        this.search_message = 'No product found'
      }
      else {
        if (this.queryParams.category_id) {
          this.search_message = 'Search results for ' + this.categories[this.queryParams.category_id].category_name + ' category'
        }
        else if (this.queryParams.price) {
          this.search_message = 'Search results for price less than ₹' + this.queryParams.price
        }
        else if (this.queryParams.best_before) {
          this.search_message = 'Search results for best before less than ' + this.queryParams.best_before
        }
      }

      return Object.keys(this.queryParams).length > 0;

    },

  },
  methods: {
    async getProducts() {
      try {
        const response = await axios.get('http://localhost:5000/product', {
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${localStorage.getItem('access_token')}`
          }
        })

        this.processProducts(response.data, this.$route.query)
        this.sortRecentlyAdded(response.data)
      } catch (error) {
        console.error('Error fetching products:', error)
      }
    },
    sortRecentlyAdded(products) {
      // Sort and limit to 5 recently added products that is last 5 products and convert product object to array
      this.recentlyAdded = Object.values(products)
        .sort((a, b) => b.id - a.id)
        .slice(0, 5)
    },
    isInStock(product) {
      return product.quantity > 0;
    },
    processProducts(products, queryParams) {
      // Assuming products is an array of products as received from the API
      this.categories = {}


      for (const product of Object.values(products)) {
        const categoryId = product.category_id.toString()

        // Check if the product matches the filter criteria
        if (
          (!queryParams.category_id || categoryId === queryParams.category_id) &&
          (!queryParams.price || parseFloat(product.price) <= parseFloat(queryParams.price)) &&
          (!queryParams.best_before || product.best_before < queryParams.best_before)
        ) {
          if (!this.categories[categoryId]) {
            this.categories[categoryId] = {
              category_name: product.category_name,
              products: []
            }
          }

          this.categories[categoryId].products.push({
            id: product.id,
            name: product.name,
            price: product.price,
            si_unit: product.si_unit,
            quantity: product.quantity,
            image: product.image,
            best_before: product.best_before,
            quantityToBuy: 1 // Default quantity to buy
          })
        }
      }
    },

    addToCart(product) {
      ; (async () => {
        try {
          let cart_url = 'http://localhost:5000/cart/' + localStorage.getItem('id')
          const response = await axios.post(
            cart_url,
            {
              product_id: product.id,
              quantity: product.quantityToBuy,
              price: product.price,
              product_name: product.name
            },
            {
              headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${localStorage.getItem('access_token')}`
              }
            }
          )
        } catch (error) {
          console.error('Error with Cart ', error)
        }
      })()
    },
    filterProduct(product) {
      // Implement your product filtering logic here based on query parameters
      if (
        this.queryParams.category_id &&
        product.category_id !== parseInt(this.queryParams.category_id)
      ) {
        return false
      }
      if (this.queryParams.price && product.price > parseFloat(this.queryParams.price)) {
        return false
      }
      // Add more filters as needed
      return true
    }
  }
}
</script>
