/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CancelablePromise } from "../core/CancelablePromise";
import type { BaseHttpRequest } from "../core/BaseHttpRequest";

export class DefaultService {
  constructor(public readonly httpRequest: BaseHttpRequest) {}

  /**
   * Read Root
   * @returns string Successful Response
   * @throws ApiError
   */
  public readRoot(): CancelablePromise<string> {
    return this.httpRequest.request({
      method: "GET",
      url: "/",
    });
  }

  /**
   * Read Item
   * @param itemId
   * @param q
   * @returns any Successful Response
   * @throws ApiError
   */
  public readItem(itemId: number, q?: string | null): CancelablePromise<any> {
    return this.httpRequest.request({
      method: "GET",
      url: "/items/{item_id}",
      path: {
        item_id: itemId,
      },
      query: {
        q: q,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }
}
