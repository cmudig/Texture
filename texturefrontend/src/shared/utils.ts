import * as vg from "@uwdata/vgplot";
// @ts-ignore
import { v4 as uuidv4 } from "uuid";
import type { Column } from "../backendapi";

export function getUUID(): string {
  return String(uuidv4());
}

const randomSixDigitInt = () => Math.floor(Math.random() * 900000) + 100000;

/**
 * If we are excluding some values from a plot or want to filter out nulls, we create a view
 * and then visualize the view in the charts.
 * NOTE: this function is not used anymore; can use in future if selection resolution is not based on table name
 * or can append the null filters to the selection directly
 */
export async function getDatasetName(
  mainDSName: string,
  cName: string,
  shouldPlotNulls: boolean,
  _excludeList?: string[],
): Promise<string> {
  // if filter updates but view name does not change then mosaic might not refresh so we append random int every time
  let viewNameStr = `${mainDSName}_VIEW_${cName}_${randomSixDigitInt()}`;

  if (!shouldPlotNulls || _excludeList) {
    let baseQ = vg.sql`CREATE OR REPLACE VIEW ${vg.column(viewNameStr)} as select * from ${vg.column(mainDSName)} `;
    let whereClauses: string[] = [];

    if (!shouldPlotNulls) {
      let s = vg.sql`${vg.column(cName)} is not null`;
      whereClauses.push(s);
    }

    if (_excludeList) {
      let formattedOps = _excludeList
        .map((item) => {
          const s = item.replaceAll("'", "''");
          return `'${s}'`;
        })
        .join(", ");

      let s = vg.sql`${vg.column(cName)} NOT IN (${formattedOps})`;
      whereClauses.push(s);
    }

    let finalQ = baseQ + "WHERE " + whereClauses.join(" AND ");

    await vg.coordinator().exec(finalQ);

    return viewNameStr;
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
