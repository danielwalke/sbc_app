import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import { createPinia } from 'pinia'
import {router} from "./lib/router/Router.js";
import VueVideoPlayer from '@videojs-player/vue'
import 'video.js/dist/video-js.css'


const pinia = createPinia()

const app = createApp(App)

app.use(VueVideoPlayer)
app.use(pinia)
app.use(router)
app.mount('#app')
