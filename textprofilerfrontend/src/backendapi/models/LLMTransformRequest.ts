/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { TaskFormat } from "./TaskFormat";

export type LLMTransformRequest = {
  userPrompt: string;
  taskFormat: TaskFormat;
  columnData: Array<string>;
  exampleData?: Array<string> | null;
  exampleResponse?: Array<any> | null;
};
