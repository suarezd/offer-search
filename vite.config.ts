import { defineConfig } from "vite";
import { resolve } from "path";
import { cpSync } from "fs";

export default defineConfig({
  build: {
    outDir: "dist",
    emptyOutDir: true,
    rollupOptions: {
      input: {
        background: resolve(__dirname, "src/background.ts"),
        popup: resolve(__dirname, "src/popup/popup.ts"),
      },
      output: {
        entryFileNames: "[name].js",
      },
    },
  },
  publicDir: false,
  plugins: [
    {
      name: "copy-all-files",
      writeBundle() {
        cpSync("src/manifest.json", "dist/manifest.json");
        cpSync("src/popup/popup.html", "dist/popup/popup.html");
        cpSync("src/popup/popup.css", "dist/popup/popup.css");
        cpSync("public/icons", "dist/icons", { recursive: true });
      },
    },
  ],
});