import * as vg from "@uwdata/vgplot";
import { Plot } from "@uwdata/mosaic-plot";

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


const lightModeStyles: Record<string, string> = {
  primaryColor: "#4768B5",
  secondaryColor: "#F3752B",
};

export const categoricalLayout: Record<string, any> = {
    width: 420,
    marginLeft: 80,
    marginRight: 40,
    marginTop: 10,
    marginBottom: 30,
    axisLineWidth: 7, //7 for 80 marginLeft
    textLineWidth: 3, //3 for 40 marginRight
    barHeight: 15, //thin bars:
    inset: 0,
    color: lightModeStyles.primaryColor,
}

export const dateLayout: Record<string, any> = {
  width: 420,
  height: 150,
  marginLeft: 55,
  marginRight: 40,
  axisLineWidth: 4, //7 for 80 marginLeft
  textLineWidth: 3, //3 for 40 marginRight
  inset: 0.5,
  color: lightModeStyles.secondaryColor,
}

export const histogramLayout: Record<string, any> = {
  width: 420,
  height: 150,
  marginLeft: 55,
  marginRight: 40,
  axisLineWidth: 4, //7 for 80 marginLeft
  textLineWidth: 3, //3 for 40 marginRight
  inset: 0.5,
  steps: 50, //thin bars: bin(thresholds) default=25 in bin.js
  color: lightModeStyles.secondaryColor,
}

export const projectionLayout: Record<string, any> = {
  width: 420,
  height: 280,
  marginLeft: 55,
  marginRight: 40,
  axisLineWidth: 4, //7 for 80 marginLeft
  textLineWidth: 3, //3 for 40 marginRight
  inset: 0.5,
  color: lightModeStyles.primaryColor,
}