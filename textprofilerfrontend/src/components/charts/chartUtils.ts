import * as vg from "@uwdata/vgplot";

/**
 * Use instead of vg.plot to get the plot back instead of the element
 * @param directives
 * @returns vg.Plot()
 */
export function getPlot(...directives) {
  const p = new vg.Plot();
  directives.flat().forEach((dir) => dir(p));
  p.marks.forEach((mark) => vg.coordinator().connect(mark));
  return p;
}