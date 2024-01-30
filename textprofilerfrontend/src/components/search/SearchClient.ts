import * as vg from "@uwdata/vgplot";
import { isSelection } from "@uwdata/mosaic-core";
import {
  regexp_matches,
  contains,
  prefix,
  suffix,
  literal,
  or,
} from "@uwdata/mosaic-sql";
import { writable, type Writable } from "svelte/store";

export type SearchMatchType = "contains" | "prefix" | "suffix" | "regexp";

const FUNCTIONS = { contains, prefix, suffix, regexp: regexp_matches };

export type SearchProps = {
  selection: any; // mosaic selection
  columns: string[];
  from: any;
  filterBy?: any;
  type?: SearchMatchType;
};

export class SearchClient extends vg.MosaicClient {
  public selection: any;
  public columns: string[];
  public filterBy: any;
  public from: any;
  public currentQuery: Writable<string>;
  public type: SearchMatchType;

  constructor({
    selection,
    columns,
    filterBy,
    from,
    type = "contains",
  }: SearchProps) {
    super(filterBy);

    console.log("SearchClient constructor called: ");

    this.selection = selection;
    this.columns = columns;
    this.filterBy = filterBy;
    this.from = from;
    this.currentQuery = writable();
    this.type = type;

    if (this.selection) {
      this.currentQuery.subscribe((value) => {
        console.log("this.currentQuery.subscribe new value: ", value);
        this.publish(value);
      });

      // if (!isSelection(this.selection)) {
      //   console.warn(
      //     "SearchClient: selection is not a selection, listening for value changes",
      //   );
      //   this.selection.addEventListener("value", (value) => {
      //     if (value !== get(this.currentQuery)) {
      //       this.currentQuery.set(value);
      //     }
      //   });
      // }
    }
  }

  reset() {
    console.log("SearchClient reset called");
    this.currentQuery.set("");
  }

  publish(value: string | undefined) {
    const { selection, columns, type } = this;
    if (isSelection(selection)) {
      // adds predicates to provided selection; if a cross filter then these will be OR'd

      let pred = null;

      if (value) {
        pred =
          columns.length > 1
            ? or(columns.map((col) => FUNCTIONS[type](col, literal(value))))
            : FUNCTIONS[type](columns[0], literal(value));
      }

      let updateInfo = {
        source: this,
        schema: { type },
        value,
        predicate: pred,
      };

      console.log("Updating selection with: ", updateInfo);
      console.log("....pred: ", updateInfo.predicate?.toString());

      selection.update(updateInfo);
    }
  }

  /**
   * Return a query to coordinator specifying the data needed by this client.
   */
  query(filter = []) {
    console.log("SearchClient query called");
    // TODO dont think need this becuase not saving to list

    const { from, columns } = this;
    if (!from) return null;
    return vg.Query.from(from)
      .select({ list: columns })
      .distinct()
      .where(filter)
      .limit(1);
  }

  /**
   * Called by the coordinator to return a query result.
   */
  queryResult(newData: any) {
    console.log("SearchClient queryResult called: ", [...newData]);
    // console.table([...newData]);
    // TODO dont think need ths becuase not saving to list
    // this.data = newData;
    return this;
  }

  /**
   * Called by coordinator to request client update.
   */
  update() {
    console.log("SearchClient update called");

    // no update
    return this;
  }
}
