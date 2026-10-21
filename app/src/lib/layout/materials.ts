// Layer materials for the layout viewer, parsed from the component's platform code and its core_material / cladding
// text (DevLog-005 D103). Materials are qualitative: no number is ever read from the text.
import type { Component } from '../components.svelte';

export const MATERIALS: Record<string, string> = {
	si: 'Si',
	sin: 'SiN',
	sion: 'SiON',
	ln: 'LN (LiNbO3)',
	lt: 'LT (LiTaO3)',
	sio2: 'SiO2',
	glass: 'glass',
	inp: 'InP / III-V',
	active: 'III-V active layer',
	gaas: 'GaAs / AlGaAs',
	ge: 'Ge',
	metal: 'metal',
	polymer: 'polymer',
	bto: 'BTO (BaTiO3)',
	other: 'other',
	unknown: 'not stated'
};

const TOKENS: [RegExp, string][] = [
	[/LiNbO3|\bTFLN\b|\bLNOI\b|\bLN\b|[Ll]ithium niobate/g, 'ln'],
	[/LiTaO3|\bTFLT\b|\bLTOI\b|\bLT\b|[Ll]ithium tantalate/g, 'lt'],
	[/Si3N4|SiNx|\bSiN\b|[Ss]ilicon nitride|\bSi-rich\b/g, 'sin'],
	[/\bSiON\b|SiOxNy|[Oo]xynitride/g, 'sion'],
	[/SiO2|\b[Ss]ilica\b|\b[Oo]xide\b|\bTEOS\b|\bHSQ\b/g, 'sio2'],
	[/\b[Gg]lass\b|\b[Bb]orosilicate\b/g, 'glass'],
	[/\bInP\b|InGaAsP|InGaAs|InAlGaAs|\bInAs\b|\bIII-V\b/g, 'inp'],
	[/\bGaAs\b|AlGaAs/g, 'gaas'],
	[/\bGe\b|\bGeSi\b|\bSiGe\b|[Gg]ermanium/g, 'ge'],
	[/\b(?:a-|poly-)?Si\b(?!-rich)|\b[Ss]ilicon\b(?! nitride| oxide| dioxide)|\bSOI\b/g, 'si'],
	[/\bSU-?8\b|\bBCB\b|[Pp]olymer|\bPMMA\b|\b[Rr]esin\b|\b[Ee]poxy\b|\bOrmo\w*/g, 'polymer'],
	[/\bBTO\b|BaTiO3/g, 'bto'],
	[/\bTiN\b|\bNiCr\b|\bAu\b|\bAl\b|\bPt\b|\bTi\b|\bW\b|\bCr\b|[Mm]etal|\bITO\b/g, 'metal'],
	[/Ta2O5|\bAlN\b|Al2O3|\bTiO2\b|\bSiC\b|[Dd]iamond|\bGaN\b|[Cc]halcogenide|As2S3|[Ss]apphire/g, 'other']
];

/** Material ids in order of first appearance in the text, each with the matched token. */
export function scanMaterials(text: string | undefined): { mat: string; token: string }[] {
	if (!text) return [];
	const hits: { i: number; mat: string; token: string }[] = [];
	for (const [re, mat] of TOKENS) {
		re.lastIndex = 0;
		let m: RegExpExecArray | null;
		while ((m = re.exec(text))) hits.push({ i: m.index, mat, token: m[0] });
	}
	hits.sort((a, b) => a.i - b.i);
	const out: { mat: string; token: string }[] = [];
	for (const h of hits) if (!out.some((o) => o.mat === h.mat)) out.push({ mat: h.mat, token: h.token });
	return out;
}

export interface Stack {
	core: string;
	layer2: string;
	box: string; // 'none' when the core sits on its substrate, 'air' when suspended
	substrate: string;
	cladding: string; // 'air' when uncladded
	overlay: string;
	absorber: string;
	heater: string;
	/** Short provenance strings for hover: which text or platform code set each material. */
	why: Record<string, string>;
}

const PLATFORM: Record<string, [string, string?]> = {
	soi: ['si'], soi_rib: ['si'], soi_strip: ['si'], soi_slot: ['si'],
	sin: ['sin'], sion: ['sion'], si_sin_multilayer: ['si', 'sin'],
	lnoi_rib: ['ln'], lnoi_strip: ['ln'], suspended_lnoi: ['ln'], lnos_rib: ['ln'], lnoi_loaded_oxide: ['ln', 'sio2'],
	lnoi_loaded_sin: ['ln', 'sin'], lnoi_loaded_si: ['si', 'ln'],
	ltoi_rib: ['lt'], ltoi_loaded_sin: ['lt', 'sin'],
	bto_on_si: ['si', 'bto'], bto_on_sin: ['sin', 'bto'], bto_on_oxide_substrate: ['bto'],
	inp: ['inp'], inp_membrane: ['inp'], gaas: ['gaas'], suspended_gaas: ['gaas'], algaas: ['gaas'],
	polymer: ['polymer'], glass: ['glass'], silica: ['glass'], ge_silica: ['glass'], al2o3: ['other'], plasmonic_mim: ['metal']
};

/** Layer materials of a component: platform code first, text order for bilayers, text for cladding / overlay. */
export function stackOf(c: Component): Stack {
	const p = c.platform ?? '';
	const text = scanMaterials(c.core_material);
	const why: Record<string, string> = {};
	let [core, layer2] = PLATFORM[p] ?? [text[0]?.mat ?? 'unknown', text[1]?.mat];
	why.core = PLATFORM[p] ? `platform ${p}` : text[0] ? `core_material text "${text[0].token}"` : 'not stated';
	if (PLATFORM[p]?.[1] && text.length >= 2) {
		// Bilayer platforms: the first-mentioned of the two platform materials is drawn as the lower (core) layer.
		const pair = PLATFORM[p] as [string, string];
		const ia = text.findIndex((t) => t.mat === pair[0]), ib = text.findIndex((t) => t.mat === pair[1]);
		if (ia >= 0 && ib >= 0 && ib < ia) [core, layer2] = [pair[1], pair[0]];
		why.core = `platform ${p}; layer order from core_material text`;
	}
	let ovlForced: string | undefined;
	if (c.class === 'fiber_chip_coupler.edge' && text.length >= 2 && text[0].mat !== core && text.some((t) => t.mat === core)) {
		// Spot-size converter described as "<taper material> ... under a <platform material> overlay": the taper is the
		// first-mentioned material, the platform material is the overlay.
		why.overlay = `platform ${p} (overlay); taper material from core_material text`;
		why.core = `core_material text "${text[0].token}"`;
		ovlForced = core;
		core = text[0].mat;
	}
	if (!layer2) layer2 = text.find((t) => t.mat !== core && t.mat !== 'sio2' && t.mat !== 'metal')?.mat ?? 'unknown';
	why.layer2 = PLATFORM[p]?.[1] ? `platform ${p}` : layer2 === 'unknown' ? 'not stated' : 'core_material text';

	let box = 'sio2', substrate = 'si';
	if (p === 'inp' || p === 'gaas' || p === 'algaas') [box, substrate] = ['none', p === 'inp' ? 'inp' : 'gaas'];
	else if (p.startsWith('suspended')) [box, substrate] = ['air', p === 'suspended_gaas' ? 'gaas' : 'si'];
	else if (p === 'glass' || p === 'silica') [box, substrate] = ['glass', 'glass'];
	else if (p === 'lnos_rib') [box, substrate] = ['none', 'other'];
	else if (p === 'polymer') [box, substrate] = ['polymer', 'other'];
	why.box = box === 'sio2' ? 'assumed SiO2 lower cladding' : `platform ${p}`;
	why.substrate = substrate === 'si' && !p.startsWith('suspended') ? 'assumed Si substrate' : `platform ${p}`;

	const cl = c.cladding ?? '';
	const first = cl.split(/[;,(]/)[0];
	const cladding = /\b(air|none|removed|uncladded|unclad)\b/i.test(first) ? 'air' : (scanMaterials(cl)[0]?.mat ?? (cl ? 'other' : 'unknown'));
	why.cladding = cl ? `cladding text "${cl.slice(0, 60)}"` : 'not stated';

	const overlay = ovlForced ?? text.find((t) => t.mat !== core && ['sion', 'polymer', 'sin', 'sio2'].includes(t.mat))?.mat ?? 'unknown';
	why.overlay ??= overlay === 'unknown' ? 'not stated' : 'core_material text';
	const all = scanMaterials((c.core_material ?? '') + ' ' + c.label + ' ' + (c.notes ?? ''));
	const absorber = c.class === 'photodetector.ge_waveguide' ? 'ge' : (all.find((t) => t.mat === 'ge' || t.mat === 'inp')?.mat ?? 'unknown');
	why.absorber = c.class === 'photodetector.ge_waveguide' ? 'class ge_waveguide' : absorber === 'unknown' ? 'not stated' : 'text';
	const heaterTok = all.find((t) => t.mat === 'metal')?.token;
	why.heater = heaterTok ? `text "${heaterTok}"` : 'heater (material not stated)';
	return { core, layer2, box, substrate, cladding, overlay, absorber, heater: 'metal', why };
}
