import * as vg from "@uwdata/vgplot";
// @ts-ignore
import { tableFromIPC } from "apache-arrow";

import type { ColumnSummary } from "../shared/types";
import type {
  DefaultService,
  ExecResponse,
  JsonResponse,
  ErrorResponse,
  DuckQueryData,
  DatasetSchema,
} from "../backendapi";

type DuckQueryResult = ExecResponse | JsonResponse | ErrorResponse;

export class DatabaseConnection {
  private wasm: any;
  private backendService: DefaultService;

  // ready flags
  isReady: boolean = false;
  private onReadyPromise?: Promise<void>;
  private onReadyResolve?: () => void;

  constructor(backendService: DefaultService) {
    this.backendService = backendService;
    this.isReady = false;
    this.init("custom");
  }

  get api() {
    return this.backendService;
  }

  private whenReady(): Promise<void> {
    if (this.isReady) {
      return Promise.resolve();
    } else {
      if (!this.onReadyPromise) {
        this.onReadyPromise = new Promise((resolve) => {
          this.onReadyResolve = resolve;
        });
      }
      return this.onReadyPromise;
    }
  }

  private async init(connectorType: string) {
    await this.setDatabaseConnector(connectorType);

    this.isReady = true;
    if (this.onReadyResolve) {
      this.onReadyResolve();
    }
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
      case "custom":
        connector = {
          query: (query: any) => {
            return new Promise((resolve, reject) =>
              this.send(query, resolve, reject),
            );
          },
        };
        break;
      default:
        throw new Error(`Unrecognized connector type: ${type}`);
    }
    vg.coordinator().databaseConnector(connector);
  }

  /**
   * @param query the query to send
   * @param  resolve the promise resolve callback
   * @param reject the promise reject callback
   */
  async send(
    query: Record<any, unknown>,
    resolve: (value: any) => void,
    reject: (reason?: any) => void,
  ) {
    await this.whenReady();

    let uuid = "1234";

    try {
      uuid =
        globalThis?.crypto?.randomUUID() ??
        Math.random().toString(36).substring(2, 15); // in case not served in https
    } catch (e) {
      uuid = Math.random().toString(36).substring(2, 15);
    }

    // console.log(`[SEND] query (uuid=${uuid})`, queryInfo);

    let requestData = { ...query, uuid } as DuckQueryData;

    if (requestData.type === "arrow") {
      this.backendService.duckdbQueryArrow(requestData).then((result) => {
        this.receive_arrow(result, resolve, reject, requestData);
      });
    } else {
      this.backendService.duckdbQueryJson(requestData).then((result) => {
        this.receive_json(result, resolve, reject, requestData);
      });
    }
  }

  receive_json(
    result: DuckQueryResult,
    resolveFunc: (value: any) => void,
    rejectFunc: (reason?: any) => void,
    requestData: DuckQueryData,
  ) {
    // console.log(
    //   query.query.sql,
    //   (performance.now() - query.startTime).toFixed(1)
    // );

    if (result.type === "error") {
      rejectFunc(result.error);
      console.error(
        "[recieve_json] ERROR: ",
        result.error,
        "from request",
        requestData,
      );
    } else if (result.type === "json") {
      resolveFunc(result.result);
    } else {
      resolveFunc({});
    }
  }

  async receive_arrow(
    result: any,
    resolveFunc: (value: any) => void,
    rejectFunc: (reason?: any) => void,
    requestData: DuckQueryData,
  ) {
    try {
      const table = await tableFromIPC(result);
      resolveFunc(table);
    } catch (e) {
      console.error("[receive_arrow] ERROR: ", e, "from request", requestData);
      rejectFunc(e);
    }
  }

  reset() {
    vg.coordinator().clear();
  }

  // custom queries: TODO in futre put these under api as well somehow? or in new api method or something

  async getCount(datasetName: string, selection?: any): Promise<number> {
    // any time applying where from predicate need to nename to source
    let q = vg.Query.from({ source: datasetName }).select({
      count: vg.count(),
    });
    if (selection) {
      q = q.where(selection.predicate({ from: datasetName }));
    }

    let r = await vg.coordinator().query(q, { type: "json" });
    let datasetSize = r[0]?.["count"];
    return datasetSize;
  }

  async getColSummaries(
    datasetName: string,
  ): Promise<Map<string, ColumnSummary>> {
    let q = vg.sql`summarize ${vg.column(datasetName)}`;
    let r: ColumnSummary[] = await vg.coordinator().query(q, { type: "json" });

    const resultMap = new Map<string, any>();

    for (const item of r) {
      const columnName = item.column_name;
      resultMap.set(columnName, item);
    }

    return resultMap;
  }

  /**
   * Retrieves documents from the database based on the provided dataset information and IDs.
   * @param dsInfo - The dataset information.
   * @param ids - An array of IDs to retrieve documents for. The order of the IDs in the array will be preserved in the returned array of documents.
   * @returns A promise that resolves to an array of retrieved documents.
   */
  async getDocsByID(dsInfo: DatasetSchema, ids: any[]): Promise<any[]> {
    let fromClause = dsInfo.name;
    const pk_name = dsInfo.primary_key.name;

    let selectQString = vg.Query.from(fromClause).select("*").toString();
    let numericIds = ids.map((id) => Number(id));

    let q = vg.sql`${selectQString} WHERE ${vg.column(pk_name)} IN (${numericIds})`;

    let r = await vg.coordinator().query(q, { type: "json" });

    // sort result to ensure order of ids is preserved
    r.sort((a, b) => {
      return ids.indexOf(a[pk_name]) - ids.indexOf(b[pk_name]);
    });

    return r;
  }

  async getValues(
    tableName: string,
    idxColName: string,
    colName: string,
    indices: number[],
  ): Promise<any[]> {
    let q = vg.Query.from(tableName)
      .select([idxColName, colName])
      .where(vg.sql`${idxColName} IN (${indices})`);
    // console.log("query is: ", q.toString());
    let r = await vg.coordinator().query(q, { type: "json" });

    return r;
  }

  async getColCount(tableName: string, cName: string): Promise<number> {
    let q = vg.Query.from(tableName).select({
      count: vg.sql`COUNT(DISTINCT CASE WHEN ${vg.column(cName)} IS NULL THEN 'null' ELSE ${vg.column(cName)} END)`,
    });
    let r = await vg.coordinator().query(q, { type: "json" });
    return r[0]?.["count"];
  }

  async getIndex(
    datasetName: string,
    selection?: any,
    indexCol = "id",
  ): Promise<number[]> {
    let q = vg.Query.from({ source: datasetName }).select(indexCol);
    if (selection) {
      q = q.where(selection.predicate({ from: datasetName }));
    }

    let r = await vg.coordinator().query(q, { type: "json" });

    // get only numbers
    let col = r.map((item) => item[indexCol]);
    return col;
  }
}
