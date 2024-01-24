import * as vg from "@uwdata/vgplot";
// @ts-ignore
import { v4 as uuidv4 } from "uuid";

export function formatNumber(value: number | undefined) {
  if (value != undefined) {
    return value.toLocaleString("en-US", { maximumFractionDigits: 1 });
  }
  return value;
}

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
