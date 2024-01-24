import * as vg from "@uwdata/vgplot";
import type { ColumnSummary } from "../shared/types";
import type { JoinInfo } from "../backendapi";

export async function getCount(
  datasetName: string,
  joinDsInfo?: JoinInfo,
  selection?: any,
): Promise<number> {
  let fromClause = datasetName;

  if (joinDsInfo) {
    fromClause = vg.fromJoinDistinct({
      table: datasetName,
      rightTable: joinDsInfo.joinDatasetName,
      joinKey: joinDsInfo.joinKey,
    });
  }

  let q = vg.Query.from(fromClause).select({ count: vg.count() });
  if (selection) {
    q = q.where(selection.predicate());
  }

  let r = await vg.coordinator().query(q, { type: "json" });
  let datasetSize = r[0]?.["count"];
  return datasetSize;
}

export async function getColSummaries(
  datasetName: string,
): Promise<ColumnSummary[]> {
  let q = vg.sql`summarize ${vg.column(datasetName)}`;
  let r = await vg.coordinator().query(q, { type: "json" });

  return r;
}
