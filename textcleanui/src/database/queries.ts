import * as vg from "@uwdata/vgplot";
import type { ColumnSummary } from "../shared/types";

export async function getCount(
  datasetName: string,
  selection?: vg.Selection
): Promise<number> {
  let q = vg.Query.from(datasetName).select({ count: vg.count() });
  if (selection) {
    q = q.where(selection.predicate());
  }

  let r = await vg.coordinator().query(q, { type: "json" });
  let datasetSize = r[0]?.["count"];
  return datasetSize;
}

export async function getColSummaries(
  datasetName: string
): Promise<ColumnSummary[]> {
  let q = vg.sql`summarize ${datasetName}`;
  let r = await vg.coordinator().query(q, { type: "json" });

  return r;
}
