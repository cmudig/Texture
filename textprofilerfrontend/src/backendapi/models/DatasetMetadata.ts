/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Column } from "./Column";
import type { QualityInfo } from "./QualityInfo";

export type DatasetMetadata = {
  text_columns: Array<Column>;
  other_columns: Array<Column>;
  text_meta_columns: Record<string, Array<Column>>;
  text_quality_info?: Array<QualityInfo>;
};
