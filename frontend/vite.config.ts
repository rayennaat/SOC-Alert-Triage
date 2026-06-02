import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    tailwindcss(),
    react()
  ],
  server: {
    port: 5173,
    host: true, // Listen on all addresses (important for ngrok)
    strictPort: false,
    // Allow ngrok and other hosts
    allowedHosts: [
      '.ngrok-free.app', // Allow all ngrok hosts
      '.ngrok.io',       // Allow ngrok.io domains
      'localhost',       // Keep localhost
      '127.0.0.1',       // Keep local IP
    ],
    // Optional: Proxy configuration if needed
    // proxy: {
    //   '/api': {
    //     target: 'http://localhost:8080',
    //     changeOrigin: true,
    //   }
    // }
  }
})