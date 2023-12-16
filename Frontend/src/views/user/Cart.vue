<template>
  <div class="about">
    <div class="container mt-5 mb-5">
      <div class="card shadow-lg p-3 mb-5 bg-white rounded">
        <div class="row g-0">
          <div class="col-md-12">
            <h1>Shopping Cart</h1>
            <table class="table">
              <thead>
                <tr>
                  <th scope="col">#</th>
                  <th scope="col">Product Name</th>
                  <th scope="col">Price</th>
                  <th scope="col">Quantity</th>
                  <th scope="col">Subtotal</th>
                  <th scope="col">Action</th>
                </tr>
              </thead>
              <tbody id="cart-items">
                <tr v-if="cart_items.length > 0" v-for="(item, index) in cart_items" :key="index">
                  <th scope="row">{{ index + 1 }}</th>
                  <td>{{ item.product_name }}</td>
                  <td>₹{{ item.price }}</td>
                  <td class="m-3">
                    {{ item.quantity }}
                  </td>
                  <td>₹{{ item.price * item.quantity }}</td>
                  <td>
                    <button class="btn btn-danger" @click="removeProduct(item.cart_id)">
                      Remove
                    </button>
                  </td>
                </tr>
                <tr v-else>
                  <td colspan="6">Your cart is empty.</td>
                </tr>
              </tbody>
            </table>
            <div class="d-flex justify-content-end align-items-center">
              <h4 v-if="cart_items.length > 0" id="total-amount">
                Total: <i v-if="coupon_applied"> </i> ₹{{ calculateTotal(coupon_discount) }}
              </h4>
              <form v-if="cart_items.length > 0" :action="'/cart/place_order/' + user_id" method="POST">
                <input type="hidden" name="user_id" :value="user_id" />
                <input type="hidden" id="hidden-total" name="total" :value="total" />
                <button type="submit" class="btn btn-primary m-3" @click.prevent="placeOrder">
                  Place Order
                </button>
              </form>
              <button v-else class="btn btn-primary ml-3" @click="$router.push('/user/category')">Let's Shop</button>
            </div>
            <br />
            <input type="text" id="coupon_code" name="coupon_code" placeholder="Coupon Code" class=" form-group mx-sm-3"
              v-model="coupon_code" />

            <button type="button" id="apply_coupon" class="btn btn-secondary m-2" @click="applyCoupon">
              Apply Coupon
            </button>
            <h3 v-if="coupon_applied" class="ml-3 text-success">{{ couponMessage }}</h3>

          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 10vh;
    display: flex;
    align-items: center;
  }
}
</style>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      cart_items: [],
      total: 0,
      user_id: 0,
      coupon_code: '',
      coupon_applied: false,
      coupon_discount: 0,
      couponMessage: ''
    }
  },
  created() {
    this.getCartItems()
  },
  methods: {
    async getCartItems() {
      try {
        let cart_url = 'http://localhost:5000/cart/' + localStorage.getItem('id')
        const response = await axios.get(cart_url, {
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${localStorage.getItem('access_token')}`
          }
        })

        this.cart_items = response.data['cart']
      } catch (error) {
        console.error('Error fetching cart items:', error)
      }
    },
    async removeProduct(cartId) {
      try {
        let removeUrl = `http://localhost:5000/cart/${cartId}`
        const response = await axios.delete(removeUrl, {
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${localStorage.getItem('access_token')}`
          }
        })

        if (response.status === 200) {
          this.getCartItems()
        } else {
          console.error('Error removing product from cart:', response.data)
        }
      } catch (error) {
        console.error('Error removing product from cart:', error)
      }
    },
    calculateTotal(coupon_code) {
      let total = 0
      this.cart_items.forEach((item) => {
        total += item.price * item.quantity
      })
      if (coupon_code) {
        let old = ''
        let discount = total * coupon_code
        total = total - discount
        total = old + '' + total
      }
      return total
    },

    applyCoupon() {
      let coupon_code = this.coupon_code.toUpperCase()
      let total = this.calculateTotal()
      let coupon_list = [
        {
          code: 'ECOMART25',
          discount: 0.25
        },
        {
          code: 'ECOMART50',
          discount: 0.5
        },
        {
          code: 'ECOMART10',
          discount: 0.1
        },
        {
          code: 'ECOMART75',
          discount: 0.75
        },
        {
          code: 'ECOMART100',
          discount: 1
        }
      ]
      let coupon = coupon_list.find((coupon) => coupon.code === coupon_code)
      if (coupon) {
        this.coupon_applied = true
        this.coupon_discount = coupon.discount
        this.calculateTotal(coupon.discount)
        // set message Coupon appiled, 50% discount!
        this.couponMessage = 'Coupon applied, ' + coupon.discount * 100 + '% discount!'
      } else {
        this.coupon_applied = false
        this.coupon_discount = 0
        this.$set(this, 'total', total)
        this.couponMessage = 'Invalid Coupon Code'
      }
    },
    placeOrder() {
      // make a post request to place order with coupon code as coupon_code and end point as /cart/place_order/<user_id>
      (async () => {
        try {

          let placeOrderUrl = `http://localhost:5000/order/${localStorage.getItem('id')}`

          const response = await axios.post(
            placeOrderUrl,
            {
              coupon_code: this.coupon_code
            },
            {
              headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${localStorage.getItem('access_token')}`
              }
            }
          )

          if (response.status == 201) {
            alert(response.data.message)
            window.location.reload()
          } else {
            console.error('Error placing order:', response.data)
          }
        } catch (error) {
          console.error('Error placing order:', error)
        }
      })()
    },
  }
}
</script>
