/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type DuckQueryData = {
  uuid: string;
  sql: string;
  type: DuckQueryData.type;
  buffers?: Array<any>;
};

export namespace DuckQueryData {
  export enum type {
    ARROW = "arrow",
    EXEC = "exec",
    JSON = "json",
  }
}
