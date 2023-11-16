import { type Writable, writable } from "svelte/store";
import type { FilterWrapper } from "./shared/types";

export const filters: Writable<FilterWrapper> = writable({
  brush: undefined,
});
