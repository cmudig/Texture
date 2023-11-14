import "./app.postcss";
import App from "./App.svelte";
import { DatabaseConnection } from "./database/db";

let databaseConnection = new DatabaseConnection();

const app = new App({
  target: document.getElementById("app") as Element,
  props: {
    databaseConnection,
  },
});

export default app;
