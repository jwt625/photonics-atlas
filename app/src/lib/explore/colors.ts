// Categorical slots follow the validated default palette order (dataviz skill, palette.md), the same hexes as the
// sibling atlases. The first six slots pass the adjacent-pair CVD and normal-vision gates in both modes
// (validate_palette.js, 2026-10-20; light mode warns on contrast vs surface, relieved by the legend and hover card).
// Colour follows the platform family, never its rank; unknown / other platforms fold into one neutral group.

export type Theme = 'dark' | 'light';

const DARK = ['#3987e5', '#d95926', '#199e70', '#c98500', '#d55181', '#008300', '#9085e9'];
const LIGHT = ['#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#e87ba4', '#008300', '#4a3aa7'];
const OTHER = '#898781';

export const OTHER_GROUP = 'other';

/** Platform families (colour slots in this order) and the platform enum values (components.schema.yaml) they hold. */
export const FAMILIES: { key: string; label: string; short: string; platforms: string[] }[] = [
	{ key: 'soi', label: 'SOI', short: 'SOI', platforms: ['soi', 'soi_strip', 'soi_rib', 'soi_slot', 'si_sin_multilayer'] },
	{ key: 'sin', label: 'SiN / SiON', short: 'SiN', platforms: ['sin', 'sion'] },
	{
		key: 'ln',
		label: 'TFLN / LN',
		short: 'LN',
		platforms: ['lnoi_rib', 'lnoi_strip', 'lnoi_loaded_sin', 'lnoi_loaded_si', 'lnoi_loaded_oxide', 'suspended_lnoi', 'lnos_rib']
	},
	{ key: 'eo', label: 'Other EO (LT, BTO)', short: 'LT / BTO', platforms: ['ltoi_rib', 'ltoi_loaded_sin', 'bto_on_si', 'bto_on_sin', 'bto_on_oxide_substrate'] },
	{
		key: 'iii_v',
		label: 'III-V (InP, GaAs, GaP)',
		short: 'III-V',
		platforms: ['inp', 'inp_membrane', 'gaas', 'suspended_gaas', 'algaas', 'gap_on_insulator', 'iii_v_on_si_epi']
	},
	{ key: 'glass', label: 'Glass / silica / polymer', short: 'Glass / polymer', platforms: ['glass', 'silica', 'ge_silica', 'polymer'] }
];

const FAMILY_OF = new Map<string, string>();
for (const f of FAMILIES) for (const p of f.platforms) FAMILY_OF.set(p, f.key);

/** Platform enum value -> family key; empty, `other`, `plasmonic_mim`, `al2o3` and unknown values -> OTHER_GROUP. */
export function platformFamily(platform: string | undefined | null): string {
	return (platform && FAMILY_OF.get(platform)) || OTHER_GROUP;
}

export const GROUP_ORDER: string[] = [...FAMILIES.map((f) => f.key), OTHER_GROUP];

export function familyLabel(key: string): string {
	return FAMILIES.find((f) => f.key === key)?.label ?? 'Other / unspecified';
}

export function familyShort(key: string): string {
	return FAMILIES.find((f) => f.key === key)?.short ?? 'Other';
}

export function groupColor(group: string, theme: Theme): string {
	const i = FAMILIES.findIndex((f) => f.key === group);
	if (i < 0) return OTHER;
	return (theme === 'dark' ? DARK : LIGHT)[i];
}

/**
 * Class families with their own colour in the class x year stack (panel j). Fixed list (the seven largest families on
 * 2026-10-20), so a filter never repaints a family; the remaining families fold into one neutral group.
 */
export const CLASS_SLOTS = ['fiber_chip_coupler', 'waveguide_platform', 'laser', 'resonator', 'photodetector', 'splitter', 'phase_shifter'] as const;

export function classColor(family: string, theme: Theme): string {
	const i = (CLASS_SLOTS as readonly string[]).indexOf(family);
	if (i < 0) return OTHER;
	return (theme === 'dark' ? DARK : LIGHT)[i];
}

export interface PlotTheme {
	surface: string;
	ink: string;
	ink2: string;
	muted: string;
	grid: string;
	line: string;
	accent: string;
}

export function plotTheme(t: Theme): PlotTheme {
	return t === 'dark'
		? { surface: '#1a1a19', ink: '#f2f1ec', ink2: '#c3c2b7', muted: '#898781', grid: '#2c2c2a', line: '#383835', accent: '#3987e5' }
		: { surface: '#fcfcfb', ink: '#0b0b0b', ink2: '#52514e', muted: '#6f6d68', grid: '#e1e0d9', line: '#c3c2b7', accent: '#2a78d6' };
}

/** Categorical slot colour (palette order above) for identity series outside the platform / class mappings (supply
 *  vendors, people corpora; DevLog-010 D194, D196); slot < 0 or beyond the palette -> neutral OTHER grey. */
export function slotColor(slot: number, theme: Theme): string {
	const p = theme === 'dark' ? DARK : LIGHT;
	return slot >= 0 && slot < p.length ? p[slot] : OTHER;
}
