<template>
  <div id="wrapper">
    <div class="d-flex flex-column" id="content-wrapper">
      <div id="content">
        <div class="container-fluid">
          <div class="d-sm-flex justify-content-between align-items-center mb-4"></div>
          <div class="row">
            <div class="col-md-6 col-xl-3 mb-4">
              <div class="card shadow border-start-primary py-2">
                <div class="card-body">
                  <div class="row align-items-center no-gutters">
                    <div class="col me-2">
                      <div class="text-uppercase text-primary fw-bold text-xs mb-1">
                        <span class="fs-5">Total Sales</span>
                      </div>
                      <div class="text-dark fw-bold h5 mb-0">
                        <span>₹ {{ res.total_sales }}</span>
                      </div>
                    </div>
                    <div class="col-auto">
                      <i class="fas fa-calendar fa-2x text-gray-300"></i>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="col-md-6 col-xl-3 mb-4">
              <div class="card shadow border-start-success py-2">
                <div class="card-body">
                  <div class="row align-items-center no-gutters">
                    <div class="col me-2">
                      <div class="text-uppercase text-success fw-bold text-xs mb-1">
                        <span class="fs-5">Earnings </span>
                      </div>
                      <div class="text-dark fw-bold h5 mb-0">
                        <span>₹ {{ res.total_earnings }}</span>
                      </div>
                    </div>
                    <div class="col-auto">
                      <i class="fas fa-dollar-sign fa-2x text-gray-300"></i>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="col-md-6 col-xl-3 mb-4">
              <div class="card shadow border-start-info py-2">
                <div class="card-body">
                  <div class="row align-items-center no-gutters">
                    <div class="col me-2">
                      <div class="text-uppercase text-info fw-bold text-xs mb-1">
                        <span class="fs-5">Products</span>
                      </div>
                      <div class="row g-0 align-items-center">
                        <div class="col-auto">
                          <div class="text-dark fw-bold h5 mb-0 me-3">
                            <span>{{ res.total_products }} ({{ res.out_of_stock }} Out Of Stock)</span>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div class="col-auto">
                      <i class="fas fa-clipboard-list fa-2x text-gray-300"></i>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="col-md-6 col-xl-3 mb-4">
              <div class="card shadow border-start-warning py-2">
                <div class="card-body">
                  <div class="row align-items-center no-gutters">
                    <div class="col me-2">
                      <div class="text-uppercase text-warning fw-bold text-xs mb-1">
                        <span class="fs-5">User's Count</span>
                      </div>
                      <div class="text-dark fw-bold h5 mb-0">
                        <span>{{ res.total_user }}</span>
                      </div>
                    </div>
                    <div class="col-auto">
                      <i class="fas fa-comments fa-2x text-gray-300"></i>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="row">
            <div class="col-lg-7 col-xl-8">
              <div class="card shadow mb-4">
                <div class="card-header d-flex justify-content-between align-items-center">
                  <h6 class="text-primary fw-bold m-1">Top 10 most selling products.</h6>

                </div>
                <div class="card-body m-2">
                  <div class="chart-area" style="width: 1100px; height: 550px">
                    <canvas id="barchart"></canvas>
                  </div>
                </div>
              </div>
            </div>
            <div class="col-lg-5 col-xl-4">
              <div class="card shadow mb-4">
                <div class="card-header d-flex justify-content-between align-items-center">
                  <h6 class="text-primary fw-bold m-1">Number of products in each category</h6>

                </div>
                <div class="card-body">
                  <div class="chart-area" style="width: 100%; height: 100%">
                    <canvas id="polar-chart"></canvas>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import Chart from 'chart.js/auto'

export default {
  data() {
    return {
      items: [],
      res: {} // Initialize an empty object to store the dictionary
    }
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    async fetchData() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/summary')
        this.items = Object.entries(response.data).map(([name, value]) => ({ name, value }))

        // Convert items to a dictionary
        this.res = this.items.reduce((obj, item) => {
          obj[item.name] = item.value
          return obj
        }, {})
        this.renderBarChart()
        this.renderPolarChart()
      } catch (error) {
        console.error(error)
      }
    },
    shuffleArray(array) {
      for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]]; // swap elements
      }
      return array;
    },
    renderPolarChart() {
      const ctx = document.getElementById('polar-chart').getContext('2d');
      const categories = this.res.categories;

      new Chart(ctx, {
        type: 'polarArea',
        data: {
          labels: this.shuffleArray(categories.map((category) => category.name)),
          datasets: [{
            data: this.shuffleArray(categories.map((category) => category.product_count)),

            backgroundColor: this.shuffleArray([
              'rgba(255, 99, 132, 0.5)',
              'rgba(255, 159, 64, 0.5)',
              'rgba(255, 205, 86, 0.5)',
              'rgba(75, 192, 192, 0.5)',
              'rgba(54, 162, 235, 0.5)',
              'rgba(153, 102, 255, 0.5)',
              'rgba(201, 203, 207, 0.5)'
            ]),
            borderWidth: 1
          }]
        },

      });
    },
    renderBarChart() {
      const ctx = document.getElementById('barchart').getContext('2d');
      const products = this.res.top_products;

      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: products.map(product => product.name),
          datasets: [{
            label: 'Sales',
            data: products.map(product => product.quantity),
            backgroundColor: this.shuffleArray([
              'rgba(255, 99, 132, 0.5)',
              'rgba(54, 162, 235, 0.5)',
              'rgba(255, 206, 86, 0.5)',
              'rgba(75, 192, 192, 0.5)',
              'rgba(153, 102, 255, 0.5)',
              'rgba(255, 159, 64, 0.5)',
              'rgba(199, 199, 199, 0.5)',
              'rgba(83, 102, 255, 0.5)',
              'rgba(40, 159, 64, 0.5)',
              'rgba(255, 99, 132, 0.5)'
            ]),

            borderWidth: 1
          }]
        },
        options: {
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      });
    }
  }
}
</script>

<style scoped></style>
