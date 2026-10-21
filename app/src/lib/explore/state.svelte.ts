import { defaultExFilters, type ExFilters } from './logic';

/** Explore filters (page-local; kept across navigation within the session). */
export const exFilters = $state<ExFilters>(defaultExFilters());

export function resetExFilters(): void {
	Object.assign(exFilters, defaultExFilters());
}
