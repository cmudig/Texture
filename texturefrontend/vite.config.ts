import { defineConfig } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [svelte()],
  // base: "/Texture/",
  build: {
    outDir: "../texture/frontend",
    // manifest: true,
    emptyOutDir: true,
  },
});
