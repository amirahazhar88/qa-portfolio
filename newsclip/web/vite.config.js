import { fileURLToPath, URL } from "node:url";
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url))
    },
    // The codebase imports SFCs without the .vue extension (Vue CLI legacy).
    extensions: [".mjs", ".js", ".ts", ".jsx", ".tsx", ".json", ".vue"]
  },
  server: {
    // Explicit IPv4 loopback: under bun, binding "localhost" can pick ::1
    // while Playwright's webServer readiness probe connects to 127.0.0.1.
    host: "127.0.0.1",
    port: 8080,
    strictPort: true
  }
});
