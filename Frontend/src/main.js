import './assets/main.css'

import { createApp } from 'vue'

import App from './App.vue'
import router from './router'

window.get_Url = async function (imageName) {
  try {
    const width = 1920
    const height = 1080
    const Unsplash_key = 'sij8Cd-zp0CEPyIarmyvh_tBnMI1nihIMiRKOG_oizo'
    const response = await fetch(
      `https://api.unsplash.com/photos/random?query=${imageName}&client_id=${Unsplash_key}&w=${width}&h=${height}`
    ).then((res) => res.json())

    return response.urls.regular
  } catch (error) {
    console.error('Error fetching image from Unsplash:', error)
    return null
  }
}

const app = createApp(App)

app.use(router)

app.mount('#app')
