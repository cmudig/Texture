import "./app.postcss";
import App from "./App.svelte";
import * as vg from "@uwdata/vgplot";

const app = new App({
  target: document.getElementById("app") as Element,
  props: {},
});

export default app;
