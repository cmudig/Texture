import "./app.postcss";
import App from "./App.svelte";
import * as vg from "@uwdata/vgplot";

// console.log("trying to load data...");

// const wasm = await vg.wasmConnector({ log: true });
// let r = vg.coordinator().databaseConnector(wasm);

// console.log("set up connector...");

// const d = await vg
//   .coordinator()
//   .exec(vg.loadParquet("opus", "opus100_en_es.parquet"));

// console.log("loaded data!");

async function loadDataset({ name, path }: { name: string; path: string }) {
  // await database connection if not initialized, and then load the dataset
  const wasm = await vg.wasmConnector({ log: true });
  let conn = vg.coordinator().databaseConnector(wasm);
  console.log("made connector...");

  // TODO how to get ref to static files?

  await conn.db.registerFileURL(
    "dolly15k.parquet",
    `../static/dolly15k.parquet`,
    4,
    false
  );

  console.log("registeed file url");

  // const conn = await db.connect();

  // let p = await conn.db.registerFileURL(n, pathy, 4, false);

  // console.log("registed as: ", p);

  const d = await vg
    .coordinator()
    .exec(vg.loadParquet(name, "dolly15k.parquet"));

  console.log("loaded file");

  return d;
}

// async function loadDataset2() {
//   // create an in-memory DuckDB instance
//   // to open a database file, pass the path as the first argument
//   const db = new DuckDB();

//   // execute a query without a returned result, await completion
//   await db.exec(`CREATE TABLE myTable AS SELECT * FROM 'dolly15k.parquet'`);

//   // query for data, return as an array of JavaScript objects
//   const res = await db.query(`SELECT COUNT(*) FROM myTable`);

//   // query for data, return as a binary Apache Arrow buffer
//   const buf = await db.arrowBuffer(`SELECT AVG(value) FROM myTable`);

//   // shut down the DuckDB instance
//   db.close();
// }

let d = loadDataset({
  name: "dolly15k",
  path: "/dolly15k.parquet",
});

const app = new App({
  target: document.getElementById("app") as Element,
  props: {
    dbConnection: d,
  },
});

export default app;
