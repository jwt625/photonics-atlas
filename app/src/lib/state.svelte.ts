import { staticUrl } from './paths';
import type { Org, OrgEvent, Registry } from './types';

export const store = $state<{ reg: Registry | null; byId: Map<string, Org>; evById: Map<string, OrgEvent>; loading: boolean; error: string }>({
	reg: null,
	byId: new Map(),
	evById: new Map(),
	loading: true,
	error: ''
});
export const ui = $state<{ theme: 'dark' | 'light' }>({ theme: 'dark' });

let started = false;

export async function loadRegistry(): Promise<void> {
	if (started) return;
	started = true;
	try {
		const res = await fetch(staticUrl('data/registry.json'));
		if (!res.ok) throw new Error(`registry.json: HTTP ${res.status}`);
		const r = (await res.json()) as Registry;
		store.byId = new Map(r.orgs.map((o) => [o.id, o]));
		store.evById = new Map(r.events.map((e) => [e.id, e]));
		store.reg = r;
	} catch (e) {
		store.error = e instanceof Error ? e.message : String(e);
	} finally {
		store.loading = false;
	}
}

export function setTheme(t: 'dark' | 'light'): void {
	ui.theme = t;
	document.documentElement.setAttribute('data-theme', t);
	try {
		localStorage.setItem('pa-atlas-theme', t);
	} catch {
		/* storage unavailable */
	}
}
