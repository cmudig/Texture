import * as vg from "@uwdata/vgplot";
// @ts-ignore
import { v4 as uuidv4 } from "uuid";
import type { Column } from "../backendapi";
import type { SelectionRange } from "../shared/types";

export function getUUID() {
  return uuidv4();
}

export async function getDatasetName(
  mainDSName: string,
  cName: string,
  pltNullsFlag: boolean,
) {
  let viewName = vg.column(`${mainDSName}NoNulls${cName}`);

  if (!pltNullsFlag) {
    await vg
      .coordinator()
      .exec(
        vg.sql`create view if not exists ${viewName} as select * from ${vg.column(
          mainDSName,
        )} where ${vg.column(cName)} is not null;`,
      );

    return viewName;
  }

  return mainDSName;
}

/**
 * Check if value is in sel
 * @param value value to check
 * @param sel selection array of numbers or strings
 * @param type type of value
 * @returns boolean on if value is in range
 */
export function shouldHighlight(
  value: any,
  sel: any[],
  type?: Column.type,
): boolean {
  if (type === "text" || type === "categorical") {
    return sel.includes(value);
  } else if (type === "number" || type === "date") {
    const v = Number(value);
    return v >= Number(sel[0]) && v <= Number(sel[1]);
  }
  return false;
}
