import "./app.postcss";
import App from "./App.svelte";

// NOTE: for dev mode to clear console on hot reload
if (import.meta.hot) {
  import.meta.hot.on("vite:beforeUpdate", () => console.clear());
}

const app = new App({
  target: document.getElementById("app") as Element,
  props: {},
});

export default app;
