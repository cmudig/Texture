import { desc } from "@uwdata/mosaic-sql";
import * as vg from "@uwdata/vgplot";
import { type Writable, writable, get } from "svelte/store";
import type { Column } from "../../backendapi";

export type TableProps = {
  filterBy?: any;
  from: string;
  mainColumns: Column[];
  otherColumns: Column[];
};

export type FieldInfo = {
  table: any;
  column: string;
  sqlType: string;
  type: string; // ["string" | "number" | "date"] but maybe more
  nullable: boolean;
};

export class TableClient extends vg.MosaicClient {
  public mainColumns: Column[];
  public otherColumns: Column[];
  public filterBy: any;
  public from: string; // N.B. don't change this property name bc used in mosaic
  public data: Writable<any[]>;
  public limit: number;
  public loaded: Writable<boolean>;
  public offset: number;
  public pending: boolean;
  public prevScrollTop: number;
  public schema: Writable<FieldInfo[]>;
  public sortColumn: Writable<string | undefined>;
  public sortDesc: Writable<boolean>;
  public sortHeader: any;

  constructor({ filterBy, from, mainColumns, otherColumns }: TableProps) {
    super(filterBy);

    this.mainColumns = mainColumns;
    this.otherColumns = otherColumns;
    this.filterBy = filterBy;
    this.from = from;
    this.data = writable();
    this.limit = 50;
    this.loaded = writable(false);
    this.offset = 0;
    this.pending = false;
    this.prevScrollTop = -1;
    this.schema = writable([]);
    this.sortColumn = writable(undefined);
    this.sortDesc = writable(false);
    this.sortHeader = null;

    // subsribe to updates
    // NOTE: this fires on subscription so request data has to manually check if schema is initialized
    this.sortColumn.subscribe((newValue) => this.requestData());
    this.sortDesc.subscribe((newValue) => this.requestData());
  }

  requestData(offset = 0) {
    let schema = get(this.schema);

    // only do this if schema initialized
    if (schema?.length) {
      this.offset = offset;

      // request next data batch
      const query = this.query(this.filterBy?.predicate(this));
      this.requestQuery(query);

      // prefetch subsequent data batch
      vg.coordinator().prefetch(query.clone().offset(offset + this.limit));
    }
  }

  /**
   * Return an array of fields queried by this client.
   */
  fields() {
    return this.mainColumns.map((col) => vg.column(this.from, col.name));
  }

  /**
   * Called by the coordinator to set the field info for this client.
   */
  fieldInfo(info: FieldInfo[]) {
    this.schema.set(info);
    return this;
  }

  /**
   * Return a query to coordinator specifying the data needed by this client.
   */
  query(filter = []) {
    // console.log(
    //   "Filters in tableClient::",
    //   filter.map((f: any) => f.toString()),
    // );

    // if not explicitly requested, reset offset because data will change
    if (!this.pending) {
      this.offset = 0;
    }

    const { from, limit, offset } = this;
    let sortColumn = get(this.sortColumn);
    let schema = get(this.schema);
    let sortDesc = get(this.sortDesc);

    let q = vg.Query.from({ source: from })
      .select(schema.map((s) => s.column))
      .where(filter)
      .orderby(sortColumn ? (sortDesc ? desc(sortColumn) : sortColumn) : [])
      .limit(limit)
      .offset(offset);

    return q;
  }

  /**
   * Called by the coordinator to return a query result.
   */
  queryResult(newData: any) {
    if (!this.pending) {
      // data is not from an internal request, so reset table
      this.loaded.set(false);
      this.data.set([]);
    }

    if (newData) {
      let thisData = [...newData];

      const otherData = this.getOtherTableData(thisData);

      this.data.update((oldItems) => [...oldItems, ...thisData]);
      // TODO: make store for other table data

      if (thisData.length < this.limit) {
        // data table has been fully loaded
        this.loaded.set(true);
      }
    }

    return this;
  }

  getOtherTableData(newMainData) {
    // query the tables in otherColumns to get the new data and update...
  }

  /**
   * Called by coordinator to request client update.
   */
  update() {
    this.pending = false;
    return this;
  }

  scroll(event: any) {
    const { scrollHeight, scrollTop, clientHeight } = event.target;

    const back = scrollTop < this.prevScrollTop;
    this.prevScrollTop = scrollTop;
    if (back || this.pending || get(this.loaded)) {
      return;
    }

    if (scrollHeight - scrollTop < 2 * clientHeight) {
      this.loadMoreData();
    }
  }

  loadMoreData() {
    this.pending = true;
    this.requestData(this.offset + this.limit);
  }
}
