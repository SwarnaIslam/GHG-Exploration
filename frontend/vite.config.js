import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from "path"

import commonjs from '@rollup/plugin-commonjs';

import vue from '@vitejs/plugin-vue';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react(), commonjs(), [vue()]],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
})
