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
import { updateSelectionMap } from "./shared/selection";

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
export const derivedViewNames: Writable<Map<any, string>> = writable(new Map());
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
      let v = databaseConnection
        .getCount($datasetInfo.name, $mosaicSelection)
        .then((v) => set(v));
    } else {
      set(undefined);
    }
  },
);

export const filteredIndices: Readable<number[]> = derived(
  [mosaicSelection, datasetInfo],
  ([$mosaicSelection, $datasetInfo], set) => {
    if ($mosaicSelection && $datasetInfo) {
      $mosaicSelection.addEventListener("value", async () => {
        databaseConnection
          .getIndex(
            $datasetInfo.name,
            $mosaicSelection,
            $datasetInfo.primary_key.name,
          )
          .then((v) => set(v));
      });
      databaseConnection
        .getIndex(
          $datasetInfo.name,
          $mosaicSelection,
          $datasetInfo.primary_key.name,
        )
        .then((v) => set(v));
    } else {
      set([]);
    }
  },
);

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
