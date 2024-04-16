/** @type {import('tailwindcss').Config}*/
const config = {
  content: [
    "./src/**/*.{html,js,svelte,ts}",
    "./node_modules/flowbite-svelte/**/*.{html,js,svelte,ts}",
  ],

  plugins: [require("flowbite/plugin")],

  // See for other easy color schemes: https://flowbite-svelte.com/docs/pages/colors
  theme: {
    extend: {
      colors: {
        // sky
        primary: {
          50: "#f0f9ff",
          100: "#e0f2fe",
          200: "#bae6fd",
          300: "#7dd4fc",
          400: "#38bdf8",
          500: "#0ea4e9",
          600: "#0285c7",
          700: "#0369a1",
          800: "#075985",
          900: "#0c4a6e",
        },

        // slate
        secondary: {
          50: "#f8fafc",
          100: "#f1f5f9",
          200: "#e2e8f0",
          300: "#cbd5e1",
          400: "#94a3b8",
          500: "#64748b",
          600: "#475569",
          700: "#334155",
          800: "#1e293b",
          900: "#0f172a",
        },

        // amber 
        highlight: {
          50: "#fffbeb",
          100: "#fef3c7",
          200: "#fde68a",
          300: "#fcd34d",
          400: "#fbbf24",
          500: "#f59e0b",
          600: "#d97706",
          700: "#b45309",
          800: "#92400e",
          900: "#78350f",
        },
      },
    },
  },
};

module.exports = config;
