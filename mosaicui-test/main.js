import * as vg from "@uwdata/vgplot";

const sidebarEl = document.querySelector("#sidebar");
const tableEl = document.querySelector("#tableview");

let wasm;

async function setDatabaseConnector(type, options) {
  let connector;
  switch (type) {
    case "socket":
      connector = vg.socketConnector(options);
      break;
    case "rest":
      connector = vg.restConnector(options);
      break;
    case "wasm":
      connector = wasm || (wasm = await vg.wasmConnector(options));
      break;
    default:
      throw new Error(`Unrecognized connector type: ${type}`);
  }
  console.log("Database Connector", type);
  vg.coordinator().databaseConnector(connector);
}

function getChart(columnName, datasetName, b) {
  const p = vg.plot(
    vg.rectY(vg.from(datasetName, { filterBy: b }), {
      x: vg.bin(columnName),
      y: vg.count(),
      fill: "steelblue",
      inset: 0.5,
    }),
    vg.intervalX({ as: b }),
    vg.xDomain(vg.Fixed),
    vg.marginLeft(55),
    vg.width(400),
    vg.height(150)
  );

  return p;
}

function getChartGroup(baseColName, datasetName, b) {
  const metaData = [
    "text_length",
    "num_words",
    "max_word_length",
    "avg_word_length",
    "perc_special_chars",
  ];

  const charts = metaData.map((m) => {
    const columnName = `${baseColName}_${m}`;
    return getChart(columnName, datasetName, b);
  });

  // layout
  const chartsVConcat = vg.vconcat(charts);

  const mainDiv = document.createElement("div");
  mainDiv.classList.add("columnProfile");
  const h3Element = document.createElement("h3");
  h3Element.textContent = baseColName;
  const chartDiv = document.createElement("div");
  chartDiv.classList.add("columnChartWrapper");

  mainDiv.appendChild(h3Element);
  chartDiv.appendChild(chartsVConcat);
  mainDiv.appendChild(chartDiv);

  return mainDiv;
}

async function run() {
  await setDatabaseConnector("wasm");

  let datasetName = "dolly";
  let textColumns = ["instruction", "context", "response", "category"];

  await vg
    .coordinator()
    .exec(
      vg.loadParquet(datasetName, location.origin + "/data/dolly15k.parquet")
    );

  const $brush = vg.Selection.crossfilter();

  let allCharts = textColumns.map((c) => getChartGroup(c, datasetName, $brush));

  const profiles = vg.vconcat(allCharts);
  sidebarEl.replaceChildren(profiles);

  const tableChart = vg.table({
    from: datasetName,
    height: 1200,
    width: "100%",
    filterBy: $brush,
    columns: textColumns,
  });

  tableEl.replaceChildren(tableChart);
}

run();
