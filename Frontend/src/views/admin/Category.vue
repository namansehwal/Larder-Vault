<template>
  <div>
    <div class="container">
      <div class="row">
        <div class="col-lg-12">
          <h3 class="text-center text-white">Manage Category</h3>

          <div>
            <!-- Button trigger modal -->
            <button
              type="button"
              class="btn btn-primary"
              data-bs-toggle="modal"
              data-bs-target="#exampleModal"
            >
              Add New Category
            </button>

            <div class="row">
              <div
                class="col-lg-3 col-md-4 col-sm-6"
                v-for="(category, index) in categories"
                :key="index"
              >
                <div class="card m-1">
                  <img
                    :src="`${category.image}`"
                    class="card-img-top"
                    alt="..."
                    style="height: 200px"
                  />
                  <div class="card-body">
                    <h5 class="card-title">{{ category.name }}</h5>
                    <button
                      class="btn btn-outline-secondary btn-sm m-1"
                      @click="openEditModal(category)"
                      data-bs-toggle="modal"
                      data-bs-target="#editModal"
                    >
                      Edit Name
                    </button>
                    <button
                      class="btn btn-outline-danger btn-sm m-1"
                      @click="deleteCategory(category.id)"
                    >
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

    <!-- Modal -->
    <!-- Edit Modal -->
    <div
      class="modal fade text-dark"
      id="editModal"
      tabindex="-1"
      aria-labelledby="editModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="editModalLabel">Edit Category Name</h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <!-- Form for editing category name -->
            <form @submit.prevent="submitEditForm">
              <div class="mb-3">
                <label for="editCategoryName" class="form-label">New Category Name</label>
                <input
                  type="text"
                  class="form-control"
                  id="editCategoryName"
                  v-model="editedCategoryName"
                  required
                />
              </div>
              <button type="submit" class="btn btn-primary">Save Changes</button>
            </form>
          </div>
        </div>
      </div>
    </div>
    <!-- Modal -->
    <div
      class="modal fade text-dark"
      id="exampleModal"
      tabindex="-1"
      aria-labelledby="exampleModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLabel">Add New Category</h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <!-- Form for adding a new category -->
            <form @submit.prevent="submitForm">
              <div class="mb-3">
                <label for="categoryName" class="form-label">Category Name</label>
                <input
                  type="text"
                  class="form-control"
                  id="categoryName"
                  v-model="categoryName"
                  required
                />
              </div>
              <button type="submit" class="btn btn-primary">Add Category</button>
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
  name: 'Category',

  data() {
    return {
      categories: [],
      categoryName: '',
      editedCategoryId: null,
      editedCategoryName: ''
    }
  },
  methods: {
    async getCategories() {
      // make await call to get all categories
      ;(async () => {
        try {
          const res = await axios.get('http://localhost:5000/category', {
            headers: {
              'Content-Type': 'application/json',
              'Allow-Cross-Origin-Origin': '*',
              Authorization: 'Bearer ' + localStorage.getItem('access_token')
            }
          })
          this.categories = res.data
        } catch (err) {
          console.log(err)
        }
      })()
    },
    deleteCategory(id) {
      // make await call to delete category
      ;(async () => {
        try {
          await axios.delete(`http://localhost:5000/category/${id}`, {
            headers: {
              'Content-Type': 'application/json',
              'Access-Control-Allow-Origin': '*',
              Authorization: 'Bearer ' + localStorage.getItem('access_token')
            }
          })
          this.getCategories()
        } catch (err) {
          console.log(err)
        }
      })()
    },
    openEditModal(category) {
      // Set the edited category and open the modal
      this.editedCategoryId = category.id
      this.editedCategoryName = category.name
      // add class to modal to make it visible
      document.getElementById('editModal').classList.add('hidden')
    },
    submitForm() {
      // make await call to add category
      ;(async () => {
        try {
          const imageUrl = await window.get_Url(this.categoryName)

          await axios
            .post(
              'http://localhost:5000/category',
              {
                name: this.categoryName,
                image: imageUrl,
                created_by: localStorage.getItem('username')
              },
              {
                headers: {
                  'Content-Type': 'application/json',
                  'Access-Control-Allow-Origin': '*',
                  Authorization: 'Bearer ' + localStorage.getItem('access_token')
                }
              }
            )
            .then((res) => alert(res.data.message))
            .catch((err) => alert(err.response.data.message))
            .finally(() => {
              this.getCategories()
            })

          this.categoryName = ''
        } catch (err) {
          console.log(err)
        }
      })()
    },
    submitEditForm() {
      // make await call to update category name
      ;(async () => {
        try {
          const img = await window.get_Url(this.editedCategoryName)
          await axios.put(
            `http://localhost:5000/category/${this.editedCategoryId}`,
            {
              name: this.editedCategoryName,
              image: img,
              created_by: localStorage.getItem('username')
            },
            {
              headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                Authorization: 'Bearer ' + localStorage.getItem('access_token')
              }
            }
          )

          this.getCategories()
        } catch (err) {
          console.log(err)
        }
      })()
    }
  },
  mounted() {
    this.getCategories()
  }
}
</script>

<style scoped></style>
