<script lang="ts">
  import * as vg from "@uwdata/vgplot";
  import type { DatasetInfo } from "./types";

  // selectors
  let wasm: any;
  let selectedValue: string = "opus";

  let sidebarElement: HTMLElement;
  let tableElement: HTMLElement;

  const datasets: { [key: string]: DatasetInfo } = {
    dolly: {
      name: "dolly",
      filename: "dolly15k.parquet",
      textColumns: ["instruction", "context", "response"],
      metaColumns: ["category"], // in the dataset, not derived
    },
    opus: {
      name: "opus",
      filename: "opus100_en_es.parquet",
      textColumns: ["en", "es"],
    },
    squad: {
      name: "squad",
      filename: "squad_validation.parquet",
      textColumns: ["context", "question", "answers[0]"],
      metaColumns: ["title"], // in the dataset, not derived
    },
  };

  const heuristicMetaCols = [
    "text_length",
    "num_words",
    "max_word_length",
    "avg_word_length",
    "perc_special_chars",
  ];

  const modelMetaCols = [
    "dist_from_mean_embed_all-mpnet-base-v2",
    "outlier_score_ECOD_all-mpnet-base-v2",
    "outlier_score_IForest_all-mpnet-base-v2",
    "dist_from_mean_embed_all-MiniLM-L6-v2",
    "outlier_score_ECOD_all-MiniLM-L6-v2",
    "outlier_score_IForest_all-MiniLM-L6-v2",
    "dist_from_mean_embed_distiluse-base-multilingual-cased-v1",
    "outlier_score_ECOD_distiluse-base-multilingual-cased-v1",
    "outlier_score_IForest_distiluse-base-multilingual-cased-v1",
  ];

  async function setDatabaseConnector(type: string, options?: any) {
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

  function getChart(columnName: string, datasetName: string, b: any) {
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

  function getChartGroup(
    baseColName: string,
    datasetName: string,
    b: any,
    makeHeuristic = true
  ) {
    // Model charts
    const model_charts = modelMetaCols.map((m) => {
      const columnName = `${baseColName}_${m}`;
      return getChart(columnName, datasetName, b);
    });

    const modelDiv = document.createElement("div");
    modelDiv.classList.add("ml-5");
    const modelHeader = document.createElement("h3");
    modelHeader.textContent = "Model";
    modelDiv.appendChild(modelHeader);
    modelDiv.appendChild(vg.vconcat(model_charts));

    // layout
    const mainDiv = document.createElement("div");
    const h2Element = document.createElement("h2");
    h2Element.textContent = baseColName;
    h2Element.classList.add("font-bold");
    h2Element.classList.add("text-xl");
    mainDiv.appendChild(h2Element);

    if (makeHeuristic) {
      // Heuristic charts
      const heuristic_charts = heuristicMetaCols.map((m) => {
        const columnName = `${baseColName}_${m}`;
        return getChart(columnName, datasetName, b);
      });

      const heuristicDiv = document.createElement("div");
      heuristicDiv.classList.add("ml-5");
      const heuristicHeader = document.createElement("h3");
      heuristicHeader.textContent = "Heuristic";
      heuristicDiv.appendChild(heuristicHeader);
      heuristicDiv.appendChild(vg.vconcat(heuristic_charts));
      mainDiv.appendChild(heuristicDiv);
    }

    mainDiv.appendChild(modelDiv);

    return mainDiv;
  }

  async function run({ name, filename, textColumns }: DatasetInfo) {
    // set up database
    await setDatabaseConnector("wasm");
    const file_path = location.origin + "/" + filename;
    await vg.coordinator().exec(vg.loadParquet(name, file_path));

    // let r = await vg.coordinator().query(`DESCRIBE SELECT * FROM ${name}`);
    // console.log("describe result is: ", r);

    // construct charts
    const brush = vg.Selection.crossfilter();
    let allCharts = [getChartGroup("joint", name, brush, false)];
    allCharts.push(
      ...textColumns.map((c) => getChartGroup(c, name, brush, true))
    );
    const profiles = vg.vconcat(allCharts);
    const tableChart = vg.table({
      from: name,
      height: 1200,
      width: "100%",
      filterBy: brush,
      columns: textColumns,
    });

    return { sidebar: profiles, table: tableChart };
  }

  async function setDataset() {
    console.log("setting dataset: ", selectedValue);
    const info = datasets[selectedValue];
    const result = await run(info);

    sidebarElement.replaceChildren(result.sidebar);
    tableElement.replaceChildren(result.table);

    console.log("updated sidebar: ", sidebarElement);
    console.log("updatd table: ", tableElement);
  }

  setDataset();
</script>

<div class="bg-gradient-to-r from-blue-100 to-blue-700 p-5 flex gap-2 flex-row">
  <span
    class="self-center whitespace-nowrap text-2xl font-semibold text-blue-900"
    >Text Clean</span
  >
  <div class="grow" />
  <div class="self-center">
    <span class="text-white text-xl pr-2">Dataset: </span>
    <select
      class="h-10 text-gray-900 bg-gray-50 border border-gray-300 rounded-lg focus:ring-primary-500 focus:border-primary-500"
      bind:value={selectedValue}
      on:change={setDataset}
    >
      <option value="opus">Opus</option>
      <option value="dolly">Dolly</option>
      <option value="squad">Squad</option>
    </select>
  </div>
</div>

<div class="wrapper">
  <div id="sidebar">
    <div bind:this={sidebarElement} />
  </div>
  <div id="tableview">
    <div bind:this={tableElement} />
  </div>
</div>

<style global>
  .wrapper {
    display: flex;
    flex-direction: row;
    border: 2px solid #e2e8f0;
    padding: 5px;
  }

  #sidebar {
    width: 30%;
    flex: 1;
    overflow: scroll;
    height: 1200px;
  }

  #tableview {
    margin-left: 10px;
    width: 70%;
    flex: 2;
  }
</style>
