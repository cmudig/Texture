import { defineConfig } from "vitepress";

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "Texture",
  description: "Structured Text Analytics",
  head: [["link", { rel: "icon", href: "/icon.svg" }]],
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config

    logo: "/icon.svg",
    search: {
      provider: "local",
    },

    nav: [
      { text: "Introduction", link: "/overview" },
      { text: "Examples", link: "/demo-1" },
    ],

    sidebar: [
      {
        text: "Introduction",
        items: [
          { text: "Overview", link: "/overview" },
          { text: "Quickstart", link: "/quickstart" },
          { text: "UI Configuration", link: "/ui-config" },
          { text: "Table Configuration", link: "/table-config" },
        ],
      },
      {
        text: "Examples",
        items: [
          { text: "Demo 1", link: "/demo-1" },
          { text: "Demo 2", link: "/demo-2" },
          { text: "Demo 3", link: "/demo-3" },
        ],
      },
      {
        text: "Vite",
        items: [{ text: "Vite Examples", link: "/vite-examples" }],
      },
    ],

    socialLinks: [
      { icon: "github", link: "https://github.com/cmudig/Texture" },
    ],
  },
});
