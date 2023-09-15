import * as vg from "@uwdata/vgplot";

const view = document.querySelector('#view');

let wasm;

async function setDatabaseConnector(type, options) {
  let connector;
  switch (type) {
    case 'socket':
      connector = vg.socketConnector(options);
      break;
    case 'rest':
      connector = vg.restConnector(options);
      break;
    case 'wasm':
      connector = (wasm || (wasm = await vg.wasmConnector(options)));
      break;
    default:
      throw new Error(`Unrecognized connector type: ${type}`);
  }
  console.log('Database Connector', type);
  vg.coordinator().databaseConnector(connector);
}

async function run() {
  await setDatabaseConnector("rest");

  await vg.coordinator().exec(
    `CREATE TEMP TABLE IF NOT EXISTS flights10m AS SELECT GREATEST(-60, LEAST(ARR_DELAY, 180))::DOUBLE AS delay, DISTANCE AS distance, DEP_TIME AS time FROM 'https://uwdata.github.io/mosaic-datasets/data/flights-10m.parquet'`
  );

  const $brush = vg.Selection.crossfilter();

  const child = vg.vconcat(
    vg.plot(
      vg.rectY(
        vg.from("flights10m", { filterBy: $brush }),
        { x: vg.bin("delay"), y: vg.count(), fill: "steelblue", inset: 0.5 }
      ),
      vg.intervalX({ as: $brush }),
      vg.xDomain(vg.Fixed),
      vg.marginLeft(75),
      vg.width(600),
      vg.height(200)
    ),
    vg.plot(
      vg.rectY(
        vg.from("flights10m", { filterBy: $brush }),
        { x: vg.bin("time"), y: vg.count(), fill: "steelblue", inset: 0.5 }
      ),
      vg.intervalX({ as: $brush }),
      vg.xDomain(vg.Fixed),
      vg.marginLeft(75),
      vg.width(600),
      vg.height(200)
    ),
    vg.plot(
      vg.rectY(
        vg.from("flights10m", { filterBy: $brush }),
        { x: vg.bin("distance"), y: vg.count(), fill: "steelblue", inset: 0.5 }
      ),
      vg.intervalX({ as: $brush }),
      vg.xDomain(vg.Fixed),
      vg.marginLeft(75),
      vg.width(600),
      vg.height(200)
    ),
    vg.table({ from: "flights10m", filterBy: $brush })
  );

  view.replaceChildren(child)

}

run()