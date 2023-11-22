import { type Writable, writable, derived } from "svelte/store";
import type { FilterWrapper, SelectionMap } from "./shared/types";

export const filters: Writable<FilterWrapper> = writable({
  brush: undefined,
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

function updateValue(mosaicSelection: any): SelectionMap {
  if (mosaicSelection?.clauses) {
    let r = mosaicSelection.clauses.reduce((d: SelectionMap, clause: any) => {
      let colName = clause.predicate.columns[0];
      let val = clause.value.flat();
      d[colName] = val;
      return d;
    }, {});

    return r;
  }
  return {};
}
