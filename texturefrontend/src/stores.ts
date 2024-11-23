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
  type DatasetSchema,
} from "./backendapi";
import { DatabaseConnection } from "./database/db";
import { updateSelectionMap } from "./shared/selection";
import type { FieldInfo } from "./components/table/TableClient";

// ~~~~~~~~~~~~~~~  Database init ~~~~~~~~~~~~~~~
const API_URL = import.meta.env.DEV ? "http://localhost:8080/api" : undefined;
console.log("API_URL: ", API_URL ?? "/api");
const backendService: DefaultService = new TextProfileClient({
  BASE: API_URL,
}).default;

// This isnt gonna update so not a store
export const databaseConnection = new DatabaseConnection(backendService);

// ~~~~~~~~~~~~~~~ App wide stores ~~~~~~~~~~~~~~~
export const compareSimilarID: Writable<number | undefined> = writable();
export const mosaicSelection: Writable<any> = writable(); // vg.Selection crossfilter
export const datasetSchema: Writable<DatasetSchema> = writable();

export async function setSchema() {
  const newInfo = await databaseConnection.api.getDatasetSchema();
  datasetSchema.update((oldVal) => newInfo);
}
export const showBackgroundDistMap: Writable<Record<string, boolean>> =
  writable();
export const clearColumnSelections: Writable<
  {
    clearFunc: () => void;
    sourceId: string;
    colName: string;
  }[]
> = writable([]);
export const tableSortColStore: Writable<Writable<string | undefined>> =
  writable();
export const tableSortDescStore: Writable<Writable<boolean>> = writable();
export const tableSchemaStore: Writable<Writable<FieldInfo[]>> = writable();
export const projectionColorColumn: Writable<string | undefined> =
  writable(undefined);
export const showSegmentValues: Writable<boolean> = writable(false);

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
  [mosaicSelection, datasetSchema],
  ([$mosaicSelection, $datasetSchema], set) => {
    if ($mosaicSelection && $datasetSchema) {
      $mosaicSelection.addEventListener("value", async () => {
        let v = await databaseConnection.getCount(
          $datasetSchema.name,
          $mosaicSelection,
        );
        set(v);
      });
      let v = databaseConnection
        .getCount($datasetSchema.name, $mosaicSelection)
        .then((v) => set(v));
    } else {
      set(undefined);
    }
  },
);

export const filteredIndices: Readable<number[]> = derived(
  [mosaicSelection, datasetSchema],
  ([$mosaicSelection, $datasetSchema], set) => {
    if ($mosaicSelection && $datasetSchema) {
      $mosaicSelection.addEventListener("value", async () => {
        databaseConnection
          .getIndex(
            $datasetSchema.name,
            $mosaicSelection,
            $datasetSchema.primary_key.name,
          )
          .then((v) => set(v));
      });
      databaseConnection
        .getIndex(
          $datasetSchema.name,
          $mosaicSelection,
          $datasetSchema.primary_key.name,
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
