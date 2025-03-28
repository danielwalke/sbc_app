import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  base: "/sbc-shap",
  server: {
    host: true,
    port: 8080,
    preview: {
      allowedHosts: ["daniel-walke.com", "https://mdoa-tools.bi.denbi.de/"] // Ersetze "domain.com" mit deiner tatsächlichen Domain
    }
  }
})
