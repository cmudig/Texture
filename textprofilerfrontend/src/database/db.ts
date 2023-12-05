import * as vg from "@uwdata/vgplot";

export class DatabaseConnection {
  wasm: any;

  constructor(name?: string, filename?: string) {
    if (name && filename) {
      this.initAndLoad(name, filename);
    }
  }

  async initAndLoad(name: string, filename: string) {
    // TODO probably dont need to call setDatabaseConnector every time?
    console.log("Init and load: ", name);
    // await vg.coordinator().clear();

    await this.setDatabaseConnector("wasm");
    const file_path = location.origin + "/" + filename;
    await vg.coordinator().exec(vg.loadParquet(name, file_path));

    // let r = await vg
    //   .coordinator()
    //   .query(`SELECT COUNT(*) FROM ${name}`, { type: "json" });
    // console.log("query result is: ", r);
  }

  private async setDatabaseConnector(type: string, options?: any) {
    let connector;
    switch (type) {
      case "socket":
        connector = vg.socketConnector(options);
        break;
      case "rest":
        connector = vg.restConnector(options);
        break;
      case "wasm":
        connector = this.wasm || (this.wasm = await vg.wasmConnector(options));
        break;
      default:
        throw new Error(`Unrecognized connector type: ${type}`);
    }
    vg.coordinator().databaseConnector(connector);
  }
}
