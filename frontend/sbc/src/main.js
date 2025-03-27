import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import { createPinia } from 'pinia'
import {router} from "./lib/router/Router.js";
import VueVideoPlayer from '@videojs-player/vue'
import 'video.js/dist/video-js.css'
import VueMatomo from 'vue-matomo'

const pinia = createPinia()

const app = createApp(App)

app.use(VueMatomo, {
    // Configure your matomo server and site by providing
    host: 'https://piwik.cebitec.uni-bielefeld.de/',
    siteId: 29,
})
app.use(VueVideoPlayer)
app.use(pinia)
app.use(router)
app.mount('#app')