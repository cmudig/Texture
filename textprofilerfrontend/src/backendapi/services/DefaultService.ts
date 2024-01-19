/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Body_upload_dataset } from "../models/Body_upload_dataset";
import type { DatasetInfo } from "../models/DatasetInfo";
import type { DatasetUploadResponse } from "../models/DatasetUploadResponse";
import type { DatasetVerifyResponse } from "../models/DatasetVerifyResponse";
import type { DuckQueryData } from "../models/DuckQueryData";
import type { ErrorResponse } from "../models/ErrorResponse";
import type { ExecResponse } from "../models/ExecResponse";
import type { JsonResponse } from "../models/JsonResponse";

import type { CancelablePromise } from "../core/CancelablePromise";
import type { BaseHttpRequest } from "../core/BaseHttpRequest";

export class DefaultService {
  constructor(public readonly httpRequest: BaseHttpRequest) {}

  /**
   * Root Status
   * @returns string Successful Response
   * @throws ApiError
   */
  public rootStatus(): CancelablePromise<string> {
    return this.httpRequest.request({
      method: "GET",
      url: "/",
    });
  }

  /**
   * Read Dataset Info
   * Get the datasets available along with a summary of their columns
   * @returns DatasetInfo Successful Response
   * @throws ApiError
   */
  public readDatasetInfo(): CancelablePromise<Record<string, DatasetInfo>> {
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

  /**
   * Upload Dataset
   * @param formData
   * @returns DatasetUploadResponse Successful Response
   * @throws ApiError
   */
  public uploadDataset(
    formData: Body_upload_dataset,
  ): CancelablePromise<DatasetUploadResponse> {
    return this.httpRequest.request({
      method: "POST",
      url: "/upload_dataset",
      formData: formData,
      mediaType: "multipart/form-data",
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Verify Schema
   * @param originalName
   * @param requestBody
   * @returns DatasetVerifyResponse Successful Response
   * @throws ApiError
   */
  public verifySchema(
    originalName: string,
    requestBody: DatasetInfo,
  ): CancelablePromise<DatasetVerifyResponse> {
    return this.httpRequest.request({
      method: "POST",
      url: "/verify_schema",
      query: {
        originalName: originalName,
      },
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    });
  }
}
