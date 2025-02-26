import { defineConfig } from "vitepress";

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "Texture",
  base: "/Texture/",
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
          { text: "Quickstart & Install", link: "/quickstart" },
          { text: "UI Configuration", link: "/ui-config" },
          { text: "Table Configuration", link: "/table-config" },
        ],
      },
      {
        text: "Examples",
        items: [
          { text: "Paper abstracts", link: "/demo-1" },
          { text: "Social media topics", link: "/demo-2" },
          { text: "LLM output comparison", link: "/demo-3" },
        ],
      },
    ],

    socialLinks: [
      { icon: "github", link: "https://github.com/cmudig/Texture" },
    ],
  },
});
