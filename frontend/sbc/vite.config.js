import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import string from 'vite-plugin-string';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue(), string()],
  assetsInclude: ['**/*.html'],
  base: "/sbc-shap",
  server: {
    host: true,
    port: 8080
  }
})
