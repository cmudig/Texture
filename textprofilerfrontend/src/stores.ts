import { type Writable, type Readable, writable, derived } from "svelte/store";

import type { FilterWrapper, SelectionMap } from "./shared/types";
import { getCount } from "./database/queries";

export const filters: Writable<FilterWrapper> = writable({
  brush: undefined,
  datasetName: "",
});

export const showBackgroundDist: Writable<boolean> = writable(true);

let initialSM: SelectionMap = {};

export const selectionDisplay = derived(
  filters,
  ($filters, set) => {
    if ($filters.brush) {
      $filters.brush.addEventListener("value", () => {
        let v = updateValue($filters.brush);
        set(v);
      });
      // event listener not triggered on initial set so call manually
      let v = updateValue($filters.brush);
      set(v);
    } else {
      set({});
    }
  },
  initialSM
);

export const filteredCount: Readable<number | undefined> = derived(
  filters,
  ($filters, set) => {
    if ($filters.brush && $filters.datasetName) {
      $filters.brush.addEventListener("value", async () => {
        let v = await getCount($filters.datasetName, $filters.brush);
        set(v);
      });
      // event listener not triggered on initial set so call manually
      let v = getCount($filters.datasetName, $filters.brush).then((v) =>
        set(v)
      );
    } else {
      set(undefined);
    }
  }
);

function updateValue(mosaicSelection: any): SelectionMap {
  if (mosaicSelection?.clauses) {
    let r = mosaicSelection.clauses.reduce((d: SelectionMap, clause: any) => {
      try {
        let colName = clause.predicate.columns[0];
        let v = clause.value;
        let val = Array.isArray(v) ? v.flat() : [v];

        d[colName] = val;
      } catch (error) {
        console.error(error);
      }

      return d;
    }, {});

    // Just get predicate as string
    // let smap2 = mosaicSelection.clauses.map((c: any) => ({
    //   value: c.value,
    //   sql: String(c.predicate),
    // }));

    return r;
  }

  return {};
}
