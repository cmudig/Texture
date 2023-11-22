import * as vg from "@uwdata/vgplot";

export async function getCount(datasetName: string): Promise<number> {
  let q = vg.Query.from(datasetName).select({ count: vg.count() });
  let r = await vg.coordinator().query(q, { type: "json" });
  let datasetSize = r[0]?.["count"];
  return datasetSize;
}
