/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Body_upload_dataset } from "../models/Body_upload_dataset";
import type { CodeTransformCommit } from "../models/CodeTransformCommit";
import type { CodeTransformRequest } from "../models/CodeTransformRequest";
import type { DatasetInfo } from "../models/DatasetInfo";
import type { DatasetTokenizeResponse } from "../models/DatasetTokenizeResponse";
import type { DatasetUploadResponse } from "../models/DatasetUploadResponse";
import type { DatasetVerifyResponse } from "../models/DatasetVerifyResponse";
import type { DuckQueryData } from "../models/DuckQueryData";
import type { ErrorResponse } from "../models/ErrorResponse";
import type { ExecResponse } from "../models/ExecResponse";
import type { JsonResponse } from "../models/JsonResponse";
import type { LLMTransformCommit } from "../models/LLMTransformCommit";
import type { LLMTransformRequest } from "../models/LLMTransformRequest";
import type { TransformResponse } from "../models/TransformResponse";
import type { VectorSearchResponse } from "../models/VectorSearchResponse";

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

  /**
   * Tokenize Dataset
   * @param datasetName
   * @param columnName
   * @param tokenType
   * @returns DatasetTokenizeResponse Successful Response
   * @throws ApiError
   */
  public tokenizeDataset(
    datasetName: string,
    columnName: string,
    tokenType: "word" | "token",
  ): CancelablePromise<DatasetTokenizeResponse> {
    return this.httpRequest.request({
      method: "POST",
      url: "/tokenize_dataset",
      query: {
        datasetName: datasetName,
        columnName: columnName,
        tokenType: tokenType,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Query Embed From Id
   * @param datasetName
   * @param id
   * @returns VectorSearchResponse Successful Response
   * @throws ApiError
   */
  public queryEmbedFromId(
    datasetName: string,
    id: number,
  ): CancelablePromise<VectorSearchResponse> {
    return this.httpRequest.request({
      method: "GET",
      url: "/query_embed_from_id",
      query: {
        datasetName: datasetName,
        id: id,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Query Embed From String
   * @param datasetName
   * @param queryString
   * @returns VectorSearchResponse Successful Response
   * @throws ApiError
   */
  public queryEmbedFromString(
    datasetName: string,
    queryString: string,
  ): CancelablePromise<VectorSearchResponse> {
    return this.httpRequest.request({
      method: "GET",
      url: "/query_embed_from_string",
      query: {
        datasetName: datasetName,
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