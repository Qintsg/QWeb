/**
 * 配置 Vite 与 Vue 前端构建入口。
 *
 * :project: QWeb
 * :file: vite.config.ts
 * :author: Qintsg
 * :date: 2026-05-12 00:00
 */
import { fileURLToPath, URL } from "node:url"

import vue from "@vitejs/plugin-vue"
import { defineConfig } from "vite"

export default defineConfig({
  plugins: [
    vue({
      template: {
        compilerOptions: {
          isCustomElement: (tag) => tag.startsWith("md-"),
        },
      },
    }),
  ],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  server: {
    host: "0.0.0.0",
    port: 3000,
    strictPort: true,
  },
  preview: {
    host: "0.0.0.0",
    port: 3000,
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes("node_modules/@material/web")) return "material-web"
          if (id.includes("node_modules/@lit") || id.includes("node_modules/lit")) return "material-web"
          if (id.includes("node_modules/vue") || id.includes("node_modules/pinia")) return "vue-vendor"
          if (id.includes("node_modules/vue-router") || id.includes("node_modules/vue-i18n")) return "vue-vendor"
        },
      },
    },
  },
})
