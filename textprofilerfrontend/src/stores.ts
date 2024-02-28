import {
  type Writable,
  type Readable,
  writable,
  derived,
  get,
} from "svelte/store";
import type { SelectionMap } from "./shared/types";
import {
  TextProfileClient,
  DefaultService,
  type DatasetInfo,
} from "./backendapi";
import { DatabaseConnection } from "./database/db";

// ~~~~~~~~~~~~~~~  Database init ~~~~~~~~~~~~~~~
// This needs to match API url
const API_URL = "http://localhost:8000/api";
const backendService: DefaultService = new TextProfileClient({
  BASE: API_URL,
}).default;

// This isnt gonna update so not a store
export const databaseConnection = new DatabaseConnection(backendService);

// ~~~~~~~~~~~~~~~ App wide stores ~~~~~~~~~~~~~~~
export const compareSimilarID: Writable<number | undefined> = writable();
export const currentWordViewName: Writable<string> = writable();

export const mosaicSelection: Writable<any> = writable(); // vg.Selection crossfilter
export const datasetInfo: Writable<DatasetInfo> = writable();

export const showBackgroundDist: Writable<boolean> = writable(true);

export const clearColumnSelections: Writable<
  {
    clearFunc: () => void;
    sourceId: string;
    colName: string;
  }[]
> = writable([]);

export const selectionDisplay = derived(
  mosaicSelection,
  ($mosaicSelection, set) => {
    if ($mosaicSelection) {
      $mosaicSelection.addEventListener("value", () => {
        let v = updateSelectionMap($mosaicSelection);
        set(v);
      });
      // event listener not triggered on initial set so call manually
      let v = updateSelectionMap($mosaicSelection);
      set(v);
    } else {
      set({});
    }
  },
  {} as SelectionMap,
);

export const filteredCount: Readable<number | undefined> = derived(
  [mosaicSelection, datasetInfo],
  ([$mosaicSelection, $datasetInfo], set) => {
    if ($mosaicSelection && $datasetInfo) {
      $mosaicSelection.addEventListener("value", async () => {
        let v = await databaseConnection.getCount(
          $datasetInfo.name,
          $mosaicSelection,
        );
        set(v);
      });
      // event listener not triggered on initial set so call manually
      let v = databaseConnection
        .getCount($datasetInfo.name, $mosaicSelection)
        .then((v) => set(v));
    } else {
      set(undefined);
    }
  },
);

function updateSelectionMap(mosaicSelection: any): SelectionMap {
  if (mosaicSelection?.clauses) {
    let r = mosaicSelection.clauses.reduce((d: SelectionMap, clause: any) => {
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

    // Just get predicate as string
    // let smap2 = mosaicSelection.clauses.map((c: any) => ({
    //   value: c.value,
    //   sql: String(c.predicate),
    // }));

    return r;
  }

  return {};
}

export function deleteFilters(col: string) {
  const brush = get(mosaicSelection);
  const colSelections = get(clearColumnSelections);

  let contains = brush.clauses.filter((clause) =>
    clause.predicate.columns.includes(col),
  );

  contains.forEach((clause) => {
    brush.update({
      ...clause,
      value: null,
      predicate: null,
    });

    // only exists on interval selections
    if (typeof clause.source?.reset === "function") {
      clause.source.reset();
    }
  });

  colSelections.filter((c) => c.colName === col).forEach((c) => c.clearFunc());
}
