import type { SelectionMap, SelectionRange } from "./types";
import { Toggle, Interval1D, Interval2D } from "@uwdata/mosaic-plot";

export function updateSelectionMap(mosaicSelection: any): SelectionMap {
  if (mosaicSelection?.clauses) {
    let r = mosaicSelection.clauses.reduce((d: SelectionMap, clause: any) => {
      try {
        if (clause.source instanceof Interval2D) {
          let p = parseInterval2D(clause);
          p.forEach((m) => {
            d[m.colName] = m.value;
          });
        } else if (clause.source instanceof Interval1D) {
          let p = parseInterval1D(clause);
          d[p.colName] = p.value;
        } else if (clause.source instanceof Toggle) {
          let p = parseToggle(clause);

          if (p.colName in d) {
            // @ts-ignore
            d[p.colName] = [...d[p.colName], ...p.value];
          } else {
            d[p.colName] = p.value;
          }
        } else {
          let p = parseUnknown(clause);
          p.forEach((m) => {
            if (m.colName in d) {
              // @ts-ignore
              d[m.colName] = [...d[m.colName], ...m.value];
            } else {
              d[m.colName] = m.value;
            }
          });
        }
      } catch (error) {
        console.error(error);
      }

      return d;
    }, {});

    return r;
  }

  return {};
}

function parseInterval2D(clause): ValueMap[] {
  let cols = clause?.predicate?.columns; // [x, y]
  let v = clause.value; // [[x1, x2], [y1, y2]]

  return [
    { colName: cols[0], value: v[0] },
    { colName: cols[1], value: v[1] },
  ];
}

function parseInterval1D(clause): ValueMap {
  let colName = clause?.predicate?.columns[0];
  let v = clause.value;
  let value = Array.isArray(v) ? v.flat() : [v];

  return { colName, value };
}

function parseToggle(clause): ValueMap {
  let colName = clause?.predicate?.columns[0];
  let v = clause.value;
  let value = Array.isArray(v) ? v.flat() : [v];

  return { colName, value };
}

function parseUnknown(clause): ValueMap[] {
  let colNames = clause.predicate.columns;
  let v = clause.value;
  let val = Array.isArray(v) ? v.flat() : [v];

  // if we dont know what type of selection, we assign all the values to each column name
  return colNames.map((c) => ({ colName: c, value: val }));
}

type ValueMap = {
  colName: string;
  value: SelectionRange;
};
