/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Column } from "./Column";
import type { JoinInfo } from "./JoinInfo";

export type DatasetInfo = {
  name: string;
  column_info: Array<Column>;
  origin: DatasetInfo.origin;
  joinDatasetInfo?: JoinInfo;
};

export namespace DatasetInfo {
  export enum origin {
    EXAMPLE = "example",
    UPLOADED = "uploaded",
  }
}
