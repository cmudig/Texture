import {
  type Writable,
  type Readable,
  writable,
  derived,
  get,
} from "svelte/store";
import type { FilterWrapper, SelectionMap } from "./shared/types";
import { TextProfileClient, DefaultService } from "./backendapi";
import { DatabaseConnection } from "./database/db";

// CLIENT INIT
// This needs to match API url
const API_URL = "http://localhost:8000/api";
const backendService: DefaultService = new TextProfileClient({
  BASE: API_URL,
}).default;

// This isnt gonna update so not a store
export const databaseConnection = new DatabaseConnection(backendService);

// ~~~~~~~~~~~~~~~ App wide stores ~~~~~~~~~~~~~~~
export const compareSimilarID: Writable<number | undefined> = writable();

export const filters: Writable<FilterWrapper> = writable({
  brush: undefined, // vg.Selection crossfilter
  datasetName: "",
  joinDatasetName: undefined,
});

export const showBackgroundDist: Writable<boolean> = writable(true);

let initialSM: SelectionMap = {};

export const selectionDisplay = derived(
  filters,
  ($filters, set) => {
    if ($filters.brush) {
      $filters.brush.addEventListener("value", () => {
        let v = updateSelectionMap($filters.brush);
        set(v);
      });
      // event listener not triggered on initial set so call manually
      let v = updateSelectionMap($filters.brush);
      set(v);
    } else {
      set({});
    }
  },
  initialSM,
);

export const filteredCount: Readable<number | undefined> = derived(
  filters,
  ($filters, set) => {
    if ($filters.brush && $filters.datasetName) {
      $filters.brush.addEventListener("value", async () => {
        let v = await databaseConnection.getCount(
          $filters.datasetName,
          $filters.joinDatasetInfo,
          $filters.brush,
        );
        set(v);
      });
      // event listener not triggered on initial set so call manually
      let v = databaseConnection
        .getCount(
          $filters.datasetName,
          $filters.joinDatasetInfo,
          $filters.brush,
        )
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

export function deleteFilter(col: string) {
  const brush = get(filters).brush;

  let contains = brush.clauses.filter((clause) =>
    clause.predicate.columns.includes(col),
  );

  contains.forEach((clause) => {
    // removes filter but does not update originating chart -- how to trigger this?
    let r = brush.update({
      ...clause,
      value: null,
      predicate: null,
    });

    if (typeof clause.source?.reset === "function") {
      console.log("clause has reset");
      clause.source.reset();
    } else {
      console.log("Clause has no reset fuction: ", clause);
      // TODO reset the filter manually if not interval?
    }

    // this updates but forces all plots to re-render
    // maybe will work if I fix the re-rendering issue for charts?
    // $filters = { ...$filters, brush: r };
  });
}
