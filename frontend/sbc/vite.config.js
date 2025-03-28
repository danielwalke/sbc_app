import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  base: "/sbc-shap",
  server: {
    host: true,
    port: 4173,
    preview: {
      allowedHosts: ["daniel-walke.com"]
    },
    cors: {
      origin: ['daniel-walke.com', 'http:localhost:4173', 'http://localhost:5173', "https://mdoa-tools.bi.denbi.de/", "mdoa-tools.bi.denbi.de"],
      methods: ['GET', 'POST'],
      allowedHeaders: ['Content-Type']
    },
    allowedHosts: ['daniel-walke.com', "https://mdoa-tools.bi.denbi.de/", "mdoa-tools.bi.denbi.de"]
  }
})