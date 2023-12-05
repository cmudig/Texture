/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type Column = {
  name: string;
  type: Column.type;
};

export namespace Column {
  export enum type {
    TEXT = "text",
    NUMBER = "number",
    DATE = "date",
    CATEGORICAL = "categorical",
  }
}
