/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type TaskFormat = {
  name: string;
  type: TaskFormat.type;
  num_replies: TaskFormat.num_replies;
};

export namespace TaskFormat {
  export enum type {
    NUMBER = "number",
    STRING = "string",
    BOOL = "bool",
  }

  export enum num_replies {
    SINGLE = "single",
    MULTIPLE = "multiple",
  }
}
