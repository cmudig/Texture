/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CodeTransformCommit } from "../models/CodeTransformCommit";
import type { CodeTransformRequest } from "../models/CodeTransformRequest";
import type { Column } from "../models/Column";
import type { DatasetSchema } from "../models/DatasetSchema";
import type { DuckQueryData } from "../models/DuckQueryData";
import type { ErrorResponse } from "../models/ErrorResponse";
import type { ExecResponse } from "../models/ExecResponse";
import type { JsonResponse } from "../models/JsonResponse";
import type { LLMTransformCommit } from "../models/LLMTransformCommit";
import type { LLMTransformRequest } from "../models/LLMTransformRequest";
import type { TransformResponse } from "../models/TransformResponse";

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
      url: "/status",
    });
  }

  /**
   * Read Dataset Info
   * Get the datasets available along with a summary of their columns
   * @returns DatasetSchema Successful Response
   * @throws ApiError
   */
  public getDatasetSchema(): CancelablePromise<DatasetSchema> {
    return this.httpRequest.request({
      method: "GET",
      url: "/get_dataset_schema",
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
   * Run Embed Search
   * @param tableName
   * @param id
   * @param queryString
   * @returns Column Successful Response
   * @throws ApiError
   */
  public runEmbedSearch(
    tableName: string,
    id?: number,
    queryString?: string,
  ): CancelablePromise<Column> {
    return this.httpRequest.request({
      method: "GET",
      url: "/run_embed_search",
      query: {
        tableName: tableName,
        id: id,
        queryString: queryString,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Get Llm Response Format
   * @param userPrompt
   * @returns TransformResponse Successful Response
   * @throws ApiError
   */
  public getLlmResponseFormat(
    userPrompt: string,
  ): CancelablePromise<TransformResponse> {
    return this.httpRequest.request({
      method: "POST",
      url: "/fetch_llm_response_format",
      query: {
        userPrompt: userPrompt,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Get Llm Transform Result
   * @param requestBody
   * @returns TransformResponse Successful Response
   * @throws ApiError
   */
  public getLlmTransformResult(
    requestBody: LLMTransformRequest,
  ): CancelablePromise<TransformResponse> {
    return this.httpRequest.request({
      method: "POST",
      url: "/fetch_llm_transform_result",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Commit Llm Transform Result
   * @param requestBody
   * @returns TransformResponse Successful Response
   * @throws ApiError
   */
  public commitLlmTransformResult(
    requestBody: LLMTransformCommit,
  ): CancelablePromise<TransformResponse> {
    return this.httpRequest.request({
      method: "POST",
      url: "/commit_llm_transform_result",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Get Code Transform Result
   * @param requestBody
   * @returns TransformResponse Successful Response
   * @throws ApiError
   */
  public getCodeTransformResult(
    requestBody: CodeTransformRequest,
  ): CancelablePromise<TransformResponse> {
    return this.httpRequest.request({
      method: "POST",
      url: "/fetch_code_transform_result",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Commit Code Transform Result
   * @param requestBody
   * @returns TransformResponse Successful Response
   * @throws ApiError
   */
  public commitCodeTransformResult(
    requestBody: CodeTransformCommit,
  ): CancelablePromise<TransformResponse> {
    return this.httpRequest.request({
      method: "POST",
      url: "/commit_code_transform_result",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Save Database To File
   * @param tableName
   * @returns boolean Successful Response
   * @throws ApiError
   */
  public saveDatabaseToFile(tableName: string): CancelablePromise<boolean> {
    return this.httpRequest.request({
      method: "POST",
      url: "/save_to_file",
      query: {
        table_name: tableName,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }
}
