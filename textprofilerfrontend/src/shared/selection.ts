import type { SelectionMap } from "./types";

export function updateSelectionMap(mosaicSelection: any): SelectionMap {
  if (mosaicSelection?.clauses) {
    let r = mosaicSelection.clauses.reduce((d: SelectionMap, clause: any) => {
      console.log("Clause is: ", clause);
      try {
        let colNames = clause.predicate.columns;
        let v = clause.value;
        let val = Array.isArray(v) ? v.flat() : [v];

        colNames.forEach((c: string) => {
          if (c in d) {
            d[c] = [...d[c], ...val];
          } else {
            d[c] = val;
          }
        });
      } catch (error) {
        console.error(error);
      }

      return d;
    }, {});

    console.log("SelectionMap is now", r);

    return r;
  }

  return {};
}
