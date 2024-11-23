/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { DerivedSchema } from "./DerivedSchema";

export type Column = {
  name: string;
  type: Column.type;
  derivedSchema?: DerivedSchema | null;
  extra?: Record<string, any> | null;
};

export namespace Column {
  export enum type {
    TEXT = "text",
    NUMBER = "number",
    DATE = "date",
    CATEGORICAL = "categorical",
  }
}
