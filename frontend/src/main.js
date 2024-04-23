import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'

import "bootstrap/dist/css/bootstrap.css"
import "bootstrap-icons/font/bootstrap-icons.css"
import "./assets/tinypip.scss"

axios.defaults.withCredentials = true;
axios.defaults.baseURL = "http://localhost:8000"

createApp(App).mount('#app')
