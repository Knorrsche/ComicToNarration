import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  base: '/comic/',
  server: {
    host: true,
    allowedHosts: ['projects.cairo.thws.de'],
  },
})
