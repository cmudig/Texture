import * as vg from "@uwdata/vgplot";
import { Plot } from "@uwdata/mosaic-plot";
import { type Readable, derived } from "svelte/store";
import { databaseConnection } from "../../stores";

/**
 * Use instead of vg.plot to get the plot back instead of the element
 * @param directives
 * @returns vg.Plot()
 */
export function getPlot(...directives) {
  const p = new Plot();
  directives.flat().forEach((dir) => dir(p));
  p.marks.forEach((mark) => vg.coordinator().connect(mark));
  return p;
}

export function getColCountStore(
  plotTableNamePromise: Promise<string>,
  columnName: string,
  showBackground: boolean,
  selectionStore: Readable<any>,
): Readable<number> {
  const colCountStore: Readable<number> = derived(
    selectionStore,
    ($selectionStore: any, set) => {
      if ($selectionStore) {
        $selectionStore.addEventListener("value", async () => {
          calcCount(
            plotTableNamePromise,
            columnName,
            showBackground,
            $selectionStore,
          ).then((v) => {
            set(v);
          });
        });
        // event listener not triggered on initial set so call manually
        calcCount(
          plotTableNamePromise,
          columnName,
          showBackground,
          $selectionStore,
        ).then((v) => {
          set(v);
        });
      } else {
        set(0);
      }
    },
  );

  return colCountStore;
}

async function calcCount(
  table: Promise<string>,
  col,
  showBG,
  sel,
): Promise<number> {
  let tableName = await table;

  return databaseConnection.getColCount(
    tableName,
    col,
    showBG ? undefined : sel, // only apply filters if not showing background
  );
}
