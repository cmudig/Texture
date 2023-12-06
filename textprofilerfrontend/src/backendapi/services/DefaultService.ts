/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { DatasetInfo } from "../models/DatasetInfo";
import type { DuckQueryData } from "../models/DuckQueryData";
import type { ErrorResponse } from "../models/ErrorResponse";
import type { ExecResponse } from "../models/ExecResponse";
import type { JsonResponse } from "../models/JsonResponse";

import type { CancelablePromise } from "../core/CancelablePromise";
import type { BaseHttpRequest } from "../core/BaseHttpRequest";

export class DefaultService {
  constructor(public readonly httpRequest: BaseHttpRequest) {}

  /**
   * Read All Dataset Names
   * @returns string Successful Response
   * @throws ApiError
   */
  public readAllDatasetNames(): CancelablePromise<Array<string>> {
    return this.httpRequest.request({
      method: "GET",
      url: "/dataset_names",
    });
  }

  /**
   * Read Dataset Info
   * Get the datasets available along with a summary of their columns
   * @returns DatasetInfo Successful Response
   * @throws ApiError
   */
  public readDatasetInfo(): CancelablePromise<Array<DatasetInfo>> {
    return this.httpRequest.request({
      method: "GET",
      url: "/all_dataset_info",
    });
  }

  /**
   * Duckdb Query Json
   * Execute a query on the database
   * @param requestBody
   * @returns any Successful Response
   * @throws ApiError
   */
  public duckdbQueryJson(
    requestBody: DuckQueryData,
  ): CancelablePromise<ExecResponse | JsonResponse | ErrorResponse> {
    return this.httpRequest.request({
      method: "POST",
      url: "/duckdb_query_json",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Duckdb Query Arrow
   * Execute a query on the database
   * @param requestBody
   * @returns any Successful Response
   * @throws ApiError
   */
  public duckdbQueryArrow(requestBody: DuckQueryData): CancelablePromise<any> {
    return this.httpRequest.request({
      method: "POST",
      url: "/duckdb_query_arrow",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    });
  }
}
