import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  base: '/',
  root: './client',
  build: { outDir: '../dist/public', assetsDir: 'assets', emptyOutDir: true },
  plugins: [react()],
})
