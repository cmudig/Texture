/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { DatasetInfo } from "../models/DatasetInfo";

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
}
