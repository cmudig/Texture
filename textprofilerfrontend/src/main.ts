import "./app.postcss";
import App from "./App.svelte";

const app = new App({
  target: document.getElementById("app") as Element,
  props: {},
});

export default app;
