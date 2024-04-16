/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Column } from "./Column";

export type DatasetInfo = {
  name: string;
  columns: Array<Column>;
  origin: DatasetInfo.origin;
  primary_key: Column;
};

export namespace DatasetInfo {
  export enum origin {
    EXAMPLE = "example",
    UPLOADED = "uploaded",
  }
}
