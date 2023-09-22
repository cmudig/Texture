<script lang="ts">
  import * as vg from "@uwdata/vgplot";

  // selectors
  let wasm: any;
  let selectedValue: string = "opus";

  let sidebarElement: HTMLElement;
  let tableElement: HTMLElement;

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

  function getChartGroup(baseColName: string, datasetName: string, b) {
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

  async function run({ name, filename, textColumns }: any) {
    await setDatabaseConnector("wasm");

    const file_path = location.origin + "/" + filename;

    console.log("FILE PATH: ", file_path);

    await vg.coordinator().exec(vg.loadParquet(name, file_path));

    const brush = vg.Selection.crossfilter();

    let allCharts = textColumns.map((c) => getChartGroup(c, name, brush));

    const profiles = vg.vconcat(allCharts);

    const tableChart = vg.table({
      from: name,
      height: 1200,
      width: "100%",
      filterBy: brush,
      columns: textColumns,
    });

    console.log("created sidebar: ", profiles);
    console.log("created table: ", tableChart);

    return { sidebar: profiles, table: tableChart };
  }

  async function setDataset() {
    console.log("setting dataset: ", selectedValue);
    const info = datasets[selectedValue];
    const result = await run(info);

    sidebarElement.replaceChildren(result.sidebar);
    tableElement.replaceChildren(result.table);

    // sidebarElement = result.sidebar;
    // tableElement = result.table;

    console.log("sidebar: ", sidebarElement);
    console.log("table: ", tableElement);
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
    <h2 class="text-xl">Profiles</h2>
    <div bind:this={sidebarElement} />
  </div>
  <div id="tableview">
    <h2 class="text-xl">Data Table</h2>
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
    /* overflow-y: scroll; */
    flex: 1;
    overflow: scroll;
    box-sizing: border-box;
    height: 1200px;
  }

  #tableview {
    margin-left: 10px;
    width: 70%;
    flex: 2;
    box-sizing: border-box;
  }
</style>
