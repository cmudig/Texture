import { desc } from "@uwdata/mosaic-sql";
import * as vg from "@uwdata/vgplot";
import { type Writable, writable, get } from "svelte/store";
import type { Column } from "../../backendapi";

export type TableProps = {
  filterBy?: any;
  from: string;
  idColumn: Column;
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
  public idColumn: Column;
  public mainColumns: Column[];
  public otherColumns: Column[];
  public filterBy: any;
  public from: string; // N.B. don't change this property name bc used in mosaic
  public data: Writable<any[]>; // apache-arrow.Table
  public arrayColData: Writable<Map<string, any[]>>;
  public limit: number;
  public loaded: Writable<boolean>;
  public offset: number;
  public pending: boolean;
  public prevScrollTop: number;
  public schema: Writable<FieldInfo[]>;
  public sortColumn: Writable<string>;
  public sortDesc: Writable<boolean>;
  public sortHeader: any;

  constructor({
    filterBy,
    from,
    idColumn,
    mainColumns,
    otherColumns,
  }: TableProps) {
    super(filterBy);

    this.idColumn = idColumn;
    this.mainColumns = mainColumns;
    this.otherColumns = otherColumns;
    this.filterBy = filterBy;
    this.from = from;
    this.data = writable();
    this.arrayColData = writable(new Map());
    this.limit = 50;
    this.loaded = writable(false);
    this.offset = 0;
    this.pending = false;
    this.prevScrollTop = -1;
    this.schema = writable([]);
    this.sortColumn = writable(this.idColumn.name);
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
    const base = this.mainColumns.map((col) => vg.column(this.from, col.name));
    base.push(vg.column(this.from, this.idColumn.name));
    return base;
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
  query(filter = [], columns?: string[]) {
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

    const columnNames =
      columns != undefined ? columns : schema.map((s) => s.column);

    let q = vg.Query.from({ source: from })
      .select(columnNames)
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
      this.arrayColData.set(new Map());
    }

    if (newData) {
      let thisData = [...newData];

      this.data.update((oldItems) => {
        if (oldItems != undefined) return [...oldItems, ...thisData];
        return [...thisData];
      });

      this.getOtherTableData().then((newResult) => {
        this.arrayColData.update((oldMap) => {
          for (let [key, value] of newResult.entries()) {
            let oldArray = oldMap.get(key);
            if (oldArray) {
              oldMap.set(key, [...oldArray, ...value]);
            } else {
              oldMap.set(key, [...value]);
            }
          }

          return oldMap;
        });
      });

      if (thisData.length < this.limit) {
        // data table has been fully loaded
        this.loaded.set(true);
      }
    }

    return this;
  }

  async getOtherTableData() {
    const idName = vg.column(this.idColumn.name);

    const baseQuery = this.query(this.filterBy?.predicate(this), [
      this.idColumn.name,
    ]);

    const queries = this.otherColumns.map((col) => {
      const table = vg.column(col.derivedSchema?.table_name);
      const q = vg.sql`SELECT ${table}.* FROM ${table} JOIN (${baseQuery}) AS main_table ON ${table}.${idName} = main_table.${idName}`;
      return vg.coordinator().query(q);
    });

    const results = await Promise.all(queries);
    const resultMap = new Map();
    results.forEach((result, i) => {
      const colName = this.otherColumns[i].name;
      resultMap.set(colName, result);
    });

    return resultMap;
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
