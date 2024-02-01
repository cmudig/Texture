import * as vg from "@uwdata/vgplot";
import type { ColumnSummary } from "../shared/types";
import type { JoinInfo } from "../backendapi";
// @ts-ignore
import { tableFromIPC } from "apache-arrow";

import type {
  DefaultService,
  ExecResponse,
  JsonResponse,
  ErrorResponse,
  DuckQueryData,
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

    const uuid = globalThis.crypto.randomUUID();

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

  async getCount(
    datasetName: string,
    joinDsInfo?: JoinInfo,
    selection?: any,
  ): Promise<number> {
    let fromClause = datasetName;

    if (joinDsInfo) {
      fromClause = vg.fromJoinDistinct({
        table: datasetName,
        rightTable: joinDsInfo.joinDatasetName,
        joinKey: joinDsInfo.joinKey,
      });
    }

    let q = vg.Query.from(fromClause).select({ count: vg.count() });
    if (selection) {
      q = q.where(selection.predicate());
    }

    let r = await vg.coordinator().query(q, { type: "json" });
    let datasetSize = r[0]?.["count"];
    return datasetSize;
  }

  async getColSummaries(datasetName: string): Promise<ColumnSummary[]> {
    let q = vg.sql`summarize ${vg.column(datasetName)}`;
    let r = await vg.coordinator().query(q, { type: "json" });

    return r;
  }
}
