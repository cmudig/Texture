/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type Column = {
  name: string;
  type: Column.type;
  derived_from?: string | null;
  table_name?: string | null;
  derived_how?: "model" | "code" | null;
};

export namespace Column {
  export enum type {
    TEXT = "text",
    NUMBER = "number",
    DATE = "date",
    CATEGORICAL = "categorical",
    LIST = "list",
  }
}
