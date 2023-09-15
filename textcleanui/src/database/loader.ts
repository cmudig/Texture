import * as vg from "@uwdata/vgplot";

export class DatabaseConnection {
  _connection: Promise<any> | undefined;

  constructor(options: { name: string; path: string }) {
    // this._connection = this.initConnection();
    this._connection = undefined;
    this.loadDataset(options);
  }

  private async initConnection() {
    const wasm = await vg.wasmConnector({ log: true });
    let r = vg.coordinator().databaseConnector(wasm);
    console.log("Connection initialized...", r);
    return r;
  }

  async getConnection(): Promise<any> {
    if (this._connection === undefined) {
      this._connection = this.initConnection();
    }
    return this._connection;
  }

  async loadDataset({ name, path }: { name: string; path: string }) {
    // await database connection if not initialized, and then load the dataset
    let c = await this.getConnection();

    console.log("connection is: ", c);

    let n = "opus100_en_es.parquet";
    let pathy = "./assets/opus100_en_es.parquet";

    let p = await c.db.registerFileURL(n, pathy, 4, false);

    console.log("registed as: ", p);

    const d = await vg.coordinator().exec(vg.loadParquet("opus100_en_es", n));

    return d;
  }
}
