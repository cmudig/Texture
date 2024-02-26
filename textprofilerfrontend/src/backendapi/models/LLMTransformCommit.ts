/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { TaskFormat } from "./TaskFormat";

export type LLMTransformCommit = {
  userPrompt: string;
  taskFormat: TaskFormat;
  columnName: string;
  tableName: string;
  newColumnName: string;
  exampleData: Array<string>;
  exampleResponse: Array<Record<string, any>>;
};
