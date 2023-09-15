import * as vg from "@uwdata/vgplot";

// selectors
const sidebarEl = document.querySelector("#sidebar");
const tableEl = document.querySelector("#tableview");

const datasetMenu = document.querySelector("#datasetSelect");
datasetMenu.addEventListener("change", setDataset);

let wasm;

const datasets = {
  dolly: {
    name: "dolly",
    filename: "dolly15k.parquet",
    textColumns: ["instruction", "context", "response", "category"],
  },
  opus: {
    name: "opus",
    filename: "opus100_en_es.parquet",
    textColumns: ["en", "es"],
  },
  squad: {
    name: "squad",
    filename: "squad_validation.parquet",
    textColumns: ["title", "context", "question", "answers[0]"],
  },
};

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

async function run({ name, filename, textColumns }) {
  await setDatabaseConnector("wasm");

  await vg
    .coordinator()
    .exec(vg.loadParquet(name, location.origin + "/data/" + filename));

  const $brush = vg.Selection.crossfilter();

  let allCharts = textColumns.map((c) => getChartGroup(c, name, $brush));

  const profiles = vg.vconcat(allCharts);
  sidebarEl.replaceChildren(profiles);

  const tableChart = vg.table({
    from: name,
    height: 1200,
    width: "100%",
    filterBy: $brush,
    columns: textColumns,
  });

  tableEl.replaceChildren(tableChart);
}

function setDataset() {
  const info = datasets[datasetMenu.value];
  run(info);
}

setDataset();
