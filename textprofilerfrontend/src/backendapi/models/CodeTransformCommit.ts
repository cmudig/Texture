/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { TaskFormat } from "./TaskFormat";

export type CodeTransformCommit = {
  codeString: string;
  taskFormat: TaskFormat;
  columnName: string;
  tableName: string;
  newColumnName: string;
  applyToIndices: Array<number>;
};
