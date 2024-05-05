/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Column } from "./Column";

export type DatasetInfo = {
  name: string;
  columns: Array<Column>;
  primary_key: Column;
  origin: DatasetInfo.origin;
  has_embeddings?: boolean;
  has_projection?: boolean;
};

export namespace DatasetInfo {
  export enum origin {
    EXAMPLE = "example",
    UPLOADED = "uploaded",
  }
}
