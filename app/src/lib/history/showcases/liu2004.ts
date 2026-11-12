// Scene module: MOS-capacitor silicon modulator, Liu et al., Nature 2004 (DevLog-017, D1014).
// Spec: data/history/showcases/liu2004.yaml. Contract: ../showcase/types.ts.
//
// Two scales (spec header, report section 4):
// - Cross-section (world x across the rib, world y up, Fig. 1 axes) in um from the spec: substrate (drawn truncated),
//   buried oxide 0.375, n-Si 1.4, gate oxide (12 nm, drawn 0.04 um), p-poly rib 2.5 x 0.9, oxide blocks and the wide
//   polysilicon layer as drawn in Fig. 1 (vertical basis figure), 10.5 um polysilicon read as the total width (D1014),
//   contacts and contact regions at assumed lateral sizes (Fig. 1 is not to scale across).
// - Along the light path (world z) the plan is schematic and shortened: MM drawn units per mm (about 60 times shorter
//   than the device), lengths in proportion (10 mm MZI arms, 8 mm single shifter of Fig. 2, 2.5 mm shifter of Fig. 4).
//   Y junctions, passive guides and chip ends are plain stand-ins (plan layout withheld).
// Withheld and not drawn: optical mode spot (D1014), oxide cover, n-side metal, process order (the cross-section is
// assembled layer by layer, no process steps), charge density numbers.
// Animated quantities follow the plot pen (D1006): the drive voltage is the plotted point of Fig. 2 (8 mm, measured) or
// Fig. 3b; the frequency the plotted point of Fig. 4b; never beyond the measured range.
//
// The model is drawn inside a window (x0, x1, y0, z0, z1): the whole chip in the wide shots, a block cut from the driven
// arm's phase shifter (face at z = ZC, seen from +z as Fig. 1 is) in the cross-section chapters. Every layer is a unit
// box scaled to the window, so the block grows into the chip as the camera pulls back. Pure function of p and explode k.
import type * as T from 'three';
import { penAt } from '../showcase/plot';
import { clamp01, ease, easeOut, lerp, seg } from '../showcase/progress';
import type { PickInfo, ShowcaseContext, ShowcaseHandle, ShowcaseModule, Theme } from '../showcase/types';

type Geo = Record<string, unknown>;
type Win = [number, number, number, number, number]; // x0 x1 y0 z0 z1
type P2 = [number, number]; // (x, z)

const DEG = Math.PI / 180;
const TAU = Math.PI * 2;
const num = (v: unknown, d: number): number => (typeof v === 'number' && Number.isFinite(v) ? v : d);
const pair = (v: unknown, d: [number, number]): [number, number] =>
	Array.isArray(v) && v.length === 2 && v.every((x) => typeof x === 'number') ? [v[0] as number, v[1] as number] : d;

// ------------------------------------------------------------------------------------------------ schematic plan (assumed)
const XA = 10; // arm centre |x| (driven arm A at +XA, arm B at -XA); arm spacing not given (plan withheld)
const MM = 16; // drawn units per mm along the light path (10 mm = 160, about 60 times shorter than the device)
const HL = 5 * MM; // half length of the 10 mm phase shifters of the Fig. 3 MZI
const H8 = 4 * MM; // half length of the 8 mm shifter of Fig. 2
const H25 = 1.25 * MM; // half length of the 2.5 mm shifter of Fig. 4
const LB = 55; // Y-junction bend length (schematic)
const LS = 25; // straight input / output guide (schematic)
const Z0 = -HL - LB - LS;
const Z1 = HL + LB + LS;
const CHIP_X = 21;
const BEAM = 70; // drawn beam length outside the chip
const ZC = HL - 8; // cross-section face (near the output end of arm A's shifter)
const DZ = 7; // depth of the cross-section block
const T_OX = 0.04; // drawn gate oxide (120 A = 0.012 um, exaggerated)
const T_Q = 0.06; // drawn charge sheets (10 nm effective thickness, exaggerated)
const CREST = 10; // drawn crest spacing of the light (illustrative, not 1.55 um)
const BAND1 = 40; // drawn modulation band spacing at 1 GHz (illustrative; spacing proportional to 1 / f)
const V_FB = 1.25; // flat-band voltage (simulation), Liu et al. p.616
const V_BIAS = 3; // d.c. bias of the high-frequency test, p.617

// ------------------------------------------------------------------------------------------------ shaders
const RIB_VS = /* glsl */ `
attribute vec3 aN; attribute float aSide;
uniform float uW;
varying float vZ; varying float vU;
void main() {
	vec3 p = position + aN * aSide * uW * 0.5;
	vZ = position.z; vU = aSide;
	gl_Position = projectionMatrix * modelViewMatrix * vec4(p, 1.0);
}`;
// light along a waveguide path: front, window clip, beam ends, output modulation bands, crests with the phase picked up
// across the shifter, reference crests (zero drive) after it
const RIB_FS = /* glsl */ `
uniform vec3 uColor; uniform float uI; uniform float uLight; uniform float uK;
uniform float uFront; uniform float uWz0; uniform float uWz1;
uniform float uModA; uniform float uModK; uniform float uModZ;
uniform float uZa; uniform float uZb;
uniform float uCrA; uniform float uCrK; uniform float uPhS; uniform float uPhE; uniform float uPhi; uniform float uGh;
varying float vZ; varying float vU;
void main() {
	if (vZ < uWz0 || vZ > uWz1) discard;
	float u2 = vU * vU;
	float across = 0.55 * exp(-u2 * 2.5) + 0.45 * exp(-u2 * 14.0);
	float a = uI;
	a *= clamp(1.0 + uModA * cos(uModK * (vZ - uModZ)), 0.0, 2.0);
	float fr = clamp((vZ - uPhS) / max(1e-3, uPhE - uPhS), 0.0, 1.0);
	float cr = 0.5 + 0.5 * cos(uCrK * vZ - uPhi * fr);
	a *= mix(1.0, 0.18 + 1.1 * cr * cr, uCrA);
	a *= across;
	a *= 1.0 - smoothstep(uFront - 30.0, uFront, vZ);
	float ends = smoothstep(uZa, uZa + 40.0, vZ) * (1.0 - smoothstep(uZb - 30.0, uZb, vZ));
	a = clamp(a * ends * uK, 0.0, 1.0);
	float g = uGh * step(uPhE, vZ) * smoothstep(0.95, 0.995, cos(uCrK * vZ)) * ends;
	vec3 gc = vec3(uLight);
	gl_FragColor = vec4(mix(uColor, gc, clamp(g / max(1e-3, a + g), 0.0, 1.0)), max(a, g * 0.9));
}`;

// ------------------------------------------------------------------------------------------------ module
const mod: ShowcaseModule = {
	renderer: '3d',
	build(ctx: ShowcaseContext): ShowcaseHandle {
		if (ctx.kind !== '3d') throw new Error('liu2004 is a 3D scene');
		const { THREE, scene, camera, spec } = ctx;
		let w = Math.max(1, ctx.width);
		let h = Math.max(1, ctx.height);
		let k = 0;
		let theme: Theme = ctx.theme;
		let hi: string[] = [];
		let lastP = 0;

		const partOf = (id: string) => spec.parts.find((q) => q.id === id);
		const geo = (id: string): Geo => (partOf(id)?.geometry ?? {}) as Geo;
		const look = (id: string) => partOf(id)?.look ?? {};
		const fallback: Record<string, [number, number]> = {
			intro: [0, 0.07], soi: [0.07, 0.15], gate: [0.15, 0.22], rib: [0.22, 0.31], contacts: [0.31, 0.39], charge: [0.39, 0.49],
			mzi: [0.49, 0.59], phase: [0.59, 0.72], transfer: [0.72, 0.85], response: [0.85, 1]
		};
		const CH = Object.fromEntries(
			Object.keys(fallback).map((id) => [id, (spec.chapters.find((c) => c.id === id)?.p ?? fallback[id]) as [number, number]])
		) as Record<string, [number, number]>;
		const cq = (id: string, p: number) => seg(p, CH[id][0], CH[id][1]);
		const at = (id: string, q: number) => lerp(CH[id][0], CH[id][1], q);
		const inCh = (id: string, p: number) => p >= CH[id][0] && p < CH[id][1];

		// ---------------------------------------------------------------------------- cross-section from the spec (um)
		const [siY0, siY1] = pair(geo('si_substrate').y, [-3.775, -1.775]);
		const [boxY0, boxY1] = pair(geo('buried_oxide').y, [-1.775, -1.4]);
		const [nY0, nY1] = pair(geo('n_si').y, [-1.4, 0]);
		const XS = Math.abs(pair(geo('n_si').x, [-7.83, 7.83])[1]); // slab half width (assumed)
		const ncG = geo('n_contact_regions');
		const ncIn = num(ncG.x_inner, 6.25);
		const ncY0 = pair(ncG.y, [-0.2, 0])[0];
		const RW = Math.abs(pair(geo('gate_oxide').x, [-1.25, 1.25])[1]); // rib half width
		const oxTop = pair(geo('oxide_regions').y, [0, 0.69])[1];
		const ribTop = pair(geo('poly_rib').y, [0.012, 0.9])[1];
		const ptG = geo('poly_top');
		const PT = Math.abs(pair(ptG.x, [-5.25, 5.25])[1]); // half of the 10.5 um layer (read as total width)
		const dopIn = pair((ptG.doped_surface as Geo | undefined)?.x_abs, [0.89, 5.25])[0];
		const mcG = geo('metal_contacts');
		const mcIn = num(mcG.x_inner, 1.73);
		const mcOut = num(mcG.x_outer, 3.93);
		const mcTop = pair(mcG.y, [0.9, 1.175])[1];
		const VD_X = -(mcIn + mcOut) / 2; // V_D lead on the left contact (Fig. 1)
		const VD_TOP = mcTop + 1.3;

		// ---------------------------------------------------------------------------- digitized curves
		const plotOf = (id: string) => spec.plots?.find((x) => x.id === id);
		const ptsOf = (id: string, si: number) =>
			((plotOf(id)?.series?.[si]?.points ?? []) as [number, number][])
				.filter((q) => Array.isArray(q) && Number.isFinite(q[0]) && Number.isFinite(q[1]))
				.sort((a, b) => a[0] - b[0]);
		const PH_SI = Math.max(0, plotOf('phase')?.series?.findIndex((s) => /8\.0 mm, measured/.test(s.name)) ?? 1);
		/** chapter whose progress q the pens take (an alternate assembles in its main plot's chapter) */
		const PEN_CH: Record<string, string> = { phase: 'phase', transfer: 'transfer', response: 'response', rms: 'response' };
		/** point under the plot pen of series si at chapter progress q (runtime penAt: same reveal as the plot); the pen sits
		 *  on the first point before its series starts and holds at the last point once it is drawn */
		function pen(plotId: string, si: number, q: number): [number, number] | null {
			const pts = ptsOf(plotId, si);
			if (!pts.length) return null;
			const pe = penAt(spec, plotId, at(PEN_CH[plotId] ?? plotId, q))[si];
			return pe ? [pe.x, pe.y] : [pts[0][0], pts[0][1]];
		}
		const phasePen = (q: number): [number, number] => pen('phase', PH_SI, q) ?? [1, 0];
		const transferPen = (q: number): [number, number] => pen('transfer', 0, q) ?? [1, -15];
		let plotSel: string | null = null; // plot on screen (runtime hook): Fig. 4b or its alternate Fig. 4a
		const respPts = ptsOf('response', 0);
		/** Fig. 4b response (dB) at f, interpolated in log f between the printed vertices */
		function respAt(f: number): number {
			if (!respPts.length) return 0;
			if (f <= respPts[0][0]) return respPts[0][1];
			for (let i = 1; i < respPts.length; i++)
				if (f <= respPts[i][0]) {
					const [x0, y0] = respPts[i - 1];
					const [x1, y1] = respPts[i];
					return lerp(y0, y1, Math.log(f / x0) / Math.max(1e-9, Math.log(x1 / x0)));
				}
			return respPts[respPts.length - 1][1];
		}
		/** [frequency, response dB] at chapter progress q: the pen of the plot on screen (Fig. 4b, or the on-chip voltage
		 *  trace of Fig. 4a when the viewer switched to it; the response then comes from Fig. 4b at that frequency) */
		const responsePen = (q: number): [number, number] => {
			if (plotSel === 'rms') {
				const f = pen('rms', 0, q)?.[0] ?? 0.1;
				return [f, respAt(f)];
			}
			return pen('response', 0, q) ?? [0.1, 0];
		};
		const V_TOP = 10; // top of the Fig. 2 range: the charge chapter ramps 0 .. 10 V
		/** charge density relative to its value at the top of the Fig. 2 range (Eq. 1: linear in V_D - V_FB, zero below) */
		const charge = (v: number) => clamp01((v - V_FB) / (V_TOP - V_FB));

		// ---------------------------------------------------------------------------- materials, bodies
		const disposables: { dispose(): void }[] = [];
		const keep = <X extends { dispose(): void }>(x: X): X => (disposables.push(x), x);
		const G = <X extends T.BufferGeometry>(g: X): X => keep(g);
		const root = new THREE.Group();
		scene.add(root);
		const model = new THREE.Group();
		root.add(model);

		// studio environment for the metal and the glassy oxides (soft boxes in a dark room)
		const studio = (() => {
			const S = 256;
			const face = (base: [string, string, string], boxes: [number, number, number, number, number][]) => {
				const cv = document.createElement('canvas');
				cv.width = cv.height = S;
				const g = cv.getContext('2d')!;
				const gr = g.createLinearGradient(0, 0, 0, S);
				gr.addColorStop(0, base[0]);
				gr.addColorStop(0.5, base[1]);
				gr.addColorStop(1, base[2]);
				g.fillStyle = gr;
				g.fillRect(0, 0, S, S);
				for (const [x, y, bw, bh, a] of boxes) {
					const cx = (x + bw / 2) * S;
					const cy = (y + bh / 2) * S;
					const rg = g.createRadialGradient(cx, cy, 0, cx, cy, (Math.max(bw, bh) * S) / 2);
					rg.addColorStop(0, `rgba(255,255,255,${a})`);
					rg.addColorStop(0.55, `rgba(255,255,255,${a * 0.75})`);
					rg.addColorStop(1, 'rgba(255,255,255,0)');
					g.fillStyle = rg;
					g.fillRect(x * S, y * S, bw * S, bh * S);
				}
				return cv;
			};
			const side: [string, string, string] = ['#9a9da2', '#3e4044', '#0e0f10'];
			const t = new THREE.CubeTexture([
				face(side, [[0.12, 0.1, 0.76, 0.6, 1]]),
				face(side, [[0.12, 0.1, 0.76, 0.6, 1]]),
				face(['#6a6d72', '#6a6d72', '#6a6d72'], [[0.18, 0.18, 0.64, 0.64, 1]]),
				face(['#0b0b0c', '#0b0b0c', '#0b0b0c'], []),
				face(side, [[0.06, 0.08, 0.88, 0.16, 0.95]]),
				face(side, [[0.14, 0.14, 0.18, 0.6, 0.55], [0.68, 0.14, 0.18, 0.6, 0.55]])
			]);
			t.colorSpace = THREE.SRGBColorSpace;
			t.needsUpdate = true;
			return keep(t);
		})();

		interface Body {
			key: string;
			part: string;
			obj: T.Object3D;
			mats: { m: T.MeshPhysicalMaterial; base: number; trans: boolean }[];
			picks: T.Mesh[];
			o: number;
		}
		const bodies: Body[] = [];
		function body(key: string, part: string, obj: T.Object3D): Body {
			const b: Body = { key, part, obj, mats: [], picks: [], o: 1 };
			obj.traverse((n) => {
				const mesh = n as T.Mesh;
				const m = mesh.material as T.MeshPhysicalMaterial | undefined;
				if (mesh.isMesh && m && 'emissive' in m && !b.mats.some((x) => x.m === m)) b.mats.push({ m, base: m.opacity, trans: m.transparent });
				if (mesh.isMesh) {
					n.userData.part = part;
					b.picks.push(mesh);
				}
			});
			model.add(obj);
			bodies.push(b);
			return b;
		}
		const std = (id: string, extra: Partial<T.MeshPhysicalMaterialParameters> = {}) => {
			const lk = look(id);
			const op = num(lk.opacity, 1);
			return keep(
				new THREE.MeshPhysicalMaterial({
					color: lk.color || '#888888',
					metalness: num(lk.metal, 0),
					roughness: num(lk.rough, 0.5),
					transparent: op < 1,
					opacity: op,
					envMap: studio,
					envMapIntensity: 0.35,
					...extra
				})
			);
		};
		const unitBox = G(new THREE.BoxGeometry(1, 1, 1).translate(0.5, 0.5, 0.5)); // [0,1]^3
		/** scale a unit-box mesh to [x0,x1] x [y0,y1] x [z0,z1]; hidden when empty */
		function fit(o: T.Object3D, x0: number, x1: number, y0: number, y1: number, z0: number, z1: number): boolean {
			const ok = x1 - x0 > 1e-4 && y1 - y0 > 1e-5 && z1 - z0 > 1e-4;
			o.visible = ok;
			if (!ok) return false;
			o.position.set(x0, y0, z0);
			o.scale.set(x1 - x0, y1 - y0, z1 - z0);
			return true;
		}
		const dielectric = { roughness: 0.4, clearcoat: 0.25, clearcoatRoughness: 0.35 };
		const glassy = { roughness: 0.18, clearcoat: 0.6, clearcoatRoughness: 0.15, envMapIntensity: 0.55, depthWrite: false };

		/** a layer of a phase shifter: pieces [x0, x1] (relative to the arm centre) over a y range, at explode level lv */
		interface Piece {
			mesh: T.Mesh;
			x: [number, number];
		}
		interface Layer {
			b: Body;
			pieces: Piece[];
			y: [number, number];
			lv: number;
		}
		function layer(key: string, part: string, mat: T.Material, xs: [number, number][], y: [number, number], lv: number): Layer {
			const g = new THREE.Group();
			const pieces = xs.map((x) => {
				const mesh = new THREE.Mesh(unitBox, mat);
				g.add(mesh);
				return { mesh, x };
			});
			return { b: body(key, part, g), pieces, y, lv };
		}
		const sym = (a: number, b: number): [number, number][] => [
			[-b, -a],
			[a, b]
		];

		// substrate and buried oxide (whole window)
		const si = body('si', 'si_substrate', new THREE.Mesh(unitBox, std('si_substrate', { envMapIntensity: 0.3 })));
		const boxL = body('box', 'buried_oxide', new THREE.Mesh(unitBox, std('buried_oxide', glassy)));

		// one phase shifter cross-section per arm (own materials: opacity is set per body)
		const mats = () => ({
			nsi: std('n_si', dielectric),
			ncon: std('n_contact_regions', dielectric),
			gox: std('gate_oxide', { ...dielectric, roughness: 0.25 }),
			oxb: std('oxide_regions', glassy),
			rib: std('poly_rib', dielectric),
			top: std('poly_top', dielectric),
			al: std('metal_contacts', { envMapIntensity: 1.9, roughness: 0.28, clearcoat: 0.1 })
		});
		type Mats = ReturnType<typeof mats>;
		const solid = (M: Mats): Mats => {
			for (const m of [M.nsi, M.ncon, M.rib, M.top, M.gox]) {
				m.transparent = false;
				m.opacity = 1;
			}
			return M;
		};
		const MA = solid(mats());
		const MB = solid(mats());
		const colRib = new THREE.Color(look('poly_rib').color || '#7ac7e2');
		const colTop = new THREE.Color(look('poly_top').color || '#0097ab');
		const colNsi = new THREE.Color(look('n_si').color || '#9aa3ad');
		const colNcon = new THREE.Color(look('n_contact_regions').color || '#6b7078');
		const shifter = (tag: string, M: Mats) => [
			layer(`nsiLo${tag}`, 'n_si', M.nsi, [[-XS, XS]], [nY0, ncY0], 2),
			layer(`nsiUp${tag}`, 'n_si', M.nsi, [[-ncIn, ncIn]], [ncY0, nY1], 2),
			layer(`ncon${tag}`, 'n_contact_regions', M.ncon, sym(ncIn, XS), [ncY0, nY1], 2),
			layer(`gox${tag}`, 'gate_oxide', M.gox, [[-RW, RW]], [nY1, nY1 + T_OX], 3),
			layer(`oxb${tag}`, 'oxide_regions', M.oxb, sym(RW, XS), [nY1, oxTop], 3),
			layer(`ribC${tag}`, 'poly_rib', M.rib, [[-dopIn, dopIn]], [nY1 + T_OX, ribTop], 4),
			layer(`ribS${tag}`, 'poly_rib', M.rib, sym(dopIn, RW), [nY1 + T_OX, oxTop], 4),
			layer(`top${tag}`, 'poly_top', M.top, sym(dopIn, PT), [oxTop, ribTop], 4),
			layer(`al${tag}`, 'metal_contacts', M.al, sym(mcIn, mcOut), [ribTop, mcTop], 5)
		];
		const SA = shifter('A', MA);
		const SB = shifter('B', MB);
		const LAYER_KEYS = ['nsiLo', 'nsiUp', 'ncon', 'gox', 'oxb', 'ribC', 'ribS', 'top', 'al'] as const;
		const lay = (S: Layer[], key: (typeof LAYER_KEYS)[number]) => S[LAYER_KEYS.indexOf(key)];

		// accumulated charge (arm A only, the driven shifter): hole sheet in the polysilicon above the oxide, electron
		// sheet in the n-type silicon below it; drawn as flat colour (not light), thickness exaggerated
		const qMat = keep(
			new THREE.MeshBasicMaterial({ color: look('accumulation').color || '#f7962c', transparent: true, opacity: 0, depthWrite: false })
		);
		const qHoles = new THREE.Mesh(unitBox, qMat);
		const qElec = new THREE.Mesh(unitBox, qMat);
		const qG = new THREE.Group();
		qG.add(qHoles, qElec);
		qG.traverse((n) => {
			n.userData.part = 'accumulation';
			(n as T.Mesh).renderOrder = 9;
		});
		model.add(qG);

		// passive guides and Y junctions: plain rib stand-ins (cross-section not described)
		const pvMat = std('passive_waveguide', { ...dielectric, side: THREE.DoubleSide });
		const yjMat = std('y_junctions', { ...dielectric, side: THREE.DoubleSide });
		for (const m of [pvMat, yjMat]) {
			m.transparent = false;
			m.opacity = 1;
		}
		const bend = (xa: number, za: number, xb: number, zb: number, n = 40): P2[] =>
			Array.from({ length: n + 1 }, (_, i) => {
				const t = i / n;
				return [xa + ((xb - xa) * (1 - Math.cos(Math.PI * t))) / 2, za + (zb - za) * t];
			});
		function frames(path: P2[]): { x: number; z: number; nx: number; nz: number }[] {
			return path.map(([x, z], i) => {
				const a = path[Math.max(0, i - 1)];
				const b = path[Math.min(path.length - 1, i + 1)];
				const tx = b[0] - a[0];
				const tz = b[1] - a[1];
				const l = Math.hypot(tx, tz) || 1;
				return { x, z, nx: tz / l, nz: -tx / l };
			});
		}
		const SB_Y0 = nY0; // stand-in from the buried oxide to the rib top
		function sweep(path: P2[]): T.BufferGeometry {
			const prof: [number, number][] = [
				[-RW, SB_Y0],
				[-RW, ribTop],
				[RW, ribTop],
				[RW, SB_Y0]
			];
			const F = frames(path);
			const pos: number[] = [];
			for (const f of F) for (const [u, y] of prof) pos.push(f.x + f.nx * u, y, f.z + f.nz * u);
			const idx: number[] = [];
			for (let i = 0; i < F.length - 1; i++)
				for (let j = 0; j < prof.length - 1; j++) {
					const a = i * 4 + j;
					const b = (i + 1) * 4 + j;
					idx.push(a, a + 1, b, a + 1, b + 1, b);
				}
			const g = new THREE.BufferGeometry();
			g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
			g.setIndex(idx);
			g.computeVertexNormals();
			return G(g);
		}
		const pSplA = bend(0, Z0 + LS, XA, -HL);
		const pSplB = bend(0, Z0 + LS, -XA, -HL);
		const pCombA = bend(XA, HL, 0, Z1 - LS);
		const pCombB = bend(-XA, HL, 0, Z1 - LS);
		const yjG = new THREE.Group();
		for (const pth of [pSplA, pSplB, pCombA, pCombB]) yjG.add(new THREE.Mesh(sweep(pth), yjMat));
		const yj = body('yj', 'y_junctions', yjG);
		// straight passive pieces: input stem, output stem, arm A outside its shifter (two), arm B outside its shifter
		const pvMeshes = [0, 1, 2, 3, 4].map(() => new THREE.Mesh(unitBox, pvMat));
		const pvG = new THREE.Group();
		pvG.add(...pvMeshes);
		const pv = body('pv', 'passive_waveguide', pvG);

		// drive and ground markers at the block face (neutral; probes and pads are not described)
		const tmMat = std('terminals', { envMapIntensity: 0.6 });
		const tmG = new THREE.Group();
		const post = new THREE.Mesh(G(new THREE.CylinderGeometry(0.07, 0.07, 1, 12).translate(0, 0.5, 0)), tmMat);
		const dot = new THREE.Mesh(G(new THREE.SphereGeometry(0.17, 16, 12)), tmMat);
		const gLead = new THREE.Mesh(G(new THREE.CylinderGeometry(0.06, 0.06, 1, 10).rotateZ(Math.PI / 2).translate(-0.5, 0, 0)), tmMat);
		const gBars = [0, 1, 2].map((i) => new THREE.Mesh(G(new THREE.BoxGeometry(0.06, 0.62 - i * 0.2, 0.06)), tmMat));
		tmG.add(post, dot, gLead, ...gBars);
		const tm = body('tm', 'terminals', tmG);

		const order: [Body, number][] = [[si, 1], [boxL, 3], [yj, 2], [pv, 2], [tm, 2]];
		for (const S of [SA, SB])
			for (const L of S) {
				const r = L.b.part === 'oxide_regions' ? 6 : 2;
				L.b.obj.traverse((n) => ((n as T.Mesh).renderOrder = r));
			}
		for (const [b, r] of order) b.obj.traverse((n) => ((n as T.Mesh).renderOrder = r));

		// ---------------------------------------------------------------------------- light (ribbons)
		type Rib = { m: T.ShaderMaterial; mesh: T.Mesh; part: string; kind: string };
		const ribbons: Rib[] = [];
		const RIB_Y = nY1 + T_OX / 2; // the light path is drawn at the gate oxide plane (mode profile not printed)
		function ribbonGeo(path: P2[], y = RIB_Y): T.BufferGeometry {
			const F = frames(path);
			const pos: number[] = [];
			const nrm: number[] = [];
			const side: number[] = [];
			for (const f of F)
				for (const s of [-1, 1]) {
					pos.push(f.x, y, f.z);
					nrm.push(f.nx, 0, f.nz);
					side.push(s);
				}
			const idx: number[] = [];
			for (let i = 0; i < F.length - 1; i++) idx.push(2 * i, 2 * i + 2, 2 * i + 1, 2 * i + 1, 2 * i + 2, 2 * i + 3);
			const g = new THREE.BufferGeometry();
			g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
			g.setAttribute('aN', new THREE.Float32BufferAttribute(nrm, 3));
			g.setAttribute('aSide', new THREE.Float32BufferAttribute(side, 1));
			g.setIndex(idx);
			return G(g);
		}
		const lightGroup = new THREE.Group();
		root.add(lightGroup);
		const ribbon = (path: P2[], part: string, kind: string): Rib => {
			const m = keep(
				new THREE.ShaderMaterial({
					uniforms: {
						uColor: { value: new THREE.Color('#ff3a28') },
						uI: { value: 0 },
						uLight: { value: 0 },
						uK: { value: 1 },
						uW: { value: 1 },
						uFront: { value: 1e6 },
						uWz0: { value: -1e6 },
						uWz1: { value: 1e6 },
						uModA: { value: 0 },
						uModK: { value: 0 },
						uModZ: { value: 0 },
						uZa: { value: -1e6 },
						uZb: { value: 1e6 },
						uCrA: { value: 0 },
						uCrK: { value: TAU / CREST },
						uPhS: { value: 0 },
						uPhE: { value: 1 },
						uPhi: { value: 0 },
						uGh: { value: 0 }
					},
					vertexShader: RIB_VS,
					fragmentShader: RIB_FS,
					transparent: true,
					depthWrite: false,
					depthTest: false,
					side: THREE.DoubleSide,
					blending: THREE.NormalBlending,
					toneMapped: false
				})
			);
			const mesh = new THREE.Mesh(ribbonGeo(path), m);
			mesh.renderOrder = 12;
			mesh.frustumCulled = false;
			lightGroup.add(mesh);
			const r: Rib = { m, mesh, part, kind };
			ribbons.push(r);
			return r;
		};
		ribbon([[0, Z0 - BEAM], [0, Z0]], 'light_in', 'in');
		ribbon([[0, Z0], [0, Z0 + LS]], 'passive_waveguide', 'chip');
		ribbon(pSplA, 'y_junctions', 'chip');
		ribbon(pSplB, 'y_junctions', 'chip');
		ribbon([[XA, -HL], [XA, HL]], 'phase_shifter', 'armA');
		ribbon([[-XA, -HL], [-XA, HL]], 'phase_shifter', 'armB');
		ribbon(pCombA, 'y_junctions', 'comb');
		ribbon(pCombB, 'y_junctions', 'comb');
		ribbon([[0, Z1 - LS], [0, Z1]], 'passive_waveguide', 'outStem');
		ribbon([[0, Z1], [0, Z1 + BEAM]], 'light_out', 'out');
		ribbon([[XA, -H8 - BEAM], [XA, -H8]], 'light_in', 'phIn');
		ribbon([[XA, H8], [XA, H8 + BEAM]], 'light_out', 'phOut');

		// pick proxies for the thin light paths in the wide shots (invisible, 7 units wide)
		const proxyMat = keep(new THREE.MeshBasicMaterial({ visible: false, side: THREE.DoubleSide }));
		const proxies: { m: T.Mesh; r: Rib }[] = [];
		for (const r of ribbons) {
			const g = (r.mesh.geometry as T.BufferGeometry).clone();
			keep(g);
			const pos = g.getAttribute('position');
			const nrm = g.getAttribute('aN');
			const sd = g.getAttribute('aSide');
			for (let i = 0; i < pos.count; i++) pos.setXYZ(i, pos.getX(i) + nrm.getX(i) * sd.getX(i) * 3.5, ribTop, pos.getZ(i) + nrm.getZ(i) * sd.getX(i) * 3.5);
			g.computeBoundingSphere();
			const m = new THREE.Mesh(g, proxyMat);
			lightGroup.add(m);
			proxies.push({ m, r });
		}

		// output facet glow (brightness of the light leaving the chip)
		const spotTex = (() => {
			const cv = document.createElement('canvas');
			cv.width = cv.height = 128;
			const g = cv.getContext('2d')!;
			const gr = g.createRadialGradient(64, 64, 0, 64, 64, 64);
			gr.addColorStop(0, 'rgba(255,255,255,1)');
			gr.addColorStop(0.25, 'rgba(255,220,210,0.95)');
			gr.addColorStop(0.55, 'rgba(255,90,60,0.5)');
			gr.addColorStop(1, 'rgba(255,40,20,0)');
			g.fillStyle = gr;
			g.fillRect(0, 0, 128, 128);
			const t = new THREE.CanvasTexture(cv);
			t.colorSpace = THREE.SRGBColorSpace;
			return keep(t);
		})();
		const flareMat = keep(new THREE.SpriteMaterial({ map: spotTex, color: '#ff6a50', transparent: true, depthWrite: false, depthTest: false, toneMapped: false, blending: THREE.AdditiveBlending, opacity: 0 }));
		const flare = new THREE.Sprite(flareMat);
		flare.renderOrder = 16;
		lightGroup.add(flare);

		// ---------------------------------------------------------------------------- lights
		const hemi = new THREE.HemisphereLight('#ffffff', '#3a3c44', 0.95);
		const key = new THREE.DirectionalLight('#fff3e6', 2.0);
		key.position.set(-60, 140, 110);
		const rim = new THREE.DirectionalLight('#bcd2ff', 0.9);
		rim.position.set(130, 60, -120);
		const fill = new THREE.DirectionalLight('#ffffff', 0.7);
		fill.position.set(-90, 20, 140);
		root.add(hemi, key, rim, fill);

		// ---------------------------------------------------------------------------- theme
		const accent = new THREE.Color();
		const black = new THREE.Color(0, 0, 0);
		function applyTheme() {
			const light = theme === 'light';
			accent.set(light ? '#2a78d6' : '#3987e5');
			for (const r of ribbons) {
				r.m.uniforms.uLight.value = light ? 0.22 : 0.8; // grey of the zero-drive crest ticks
				r.m.uniforms.uK.value = light ? 0.95 : 1;
			}
			flareMat.blending = light ? THREE.NormalBlending : THREE.AdditiveBlending;
			flareMat.color.set(light ? '#e0301c' : '#ff6a50');
			flareMat.needsUpdate = true;
			qMat.color.set(light ? '#d9730f' : look('accumulation').color || '#f7962c');
			hemi.intensity = light ? 1.05 : 0.95;
		}
		applyTheme();

		// ---------------------------------------------------------------------------- shots: window + camera
		interface Shot {
			az: number;
			el: number;
			win: Win;
			box: number[]; // camera framing box x0 x1 y0 y1 z0 z1
			fw: number;
			fh: number;
			sx: number;
			sy: number;
		}
		const portrait = () => w / h < 0.9;
		const P = (s: Shot): Shot => (portrait() ? { ...s, fw: Math.min(0.96, s.fw * 1.1), fh: s.fh * 0.62, sy: s.sy + 0.02 } : s);
		const plotShift = (s: Shot): Shot => (portrait() ? { ...s, fw: 0.9, fh: 0.22, sx: 0, sy: 0.24 } : { ...s, fw: Math.min(s.fw, 0.44), fh: Math.min(s.fh, 0.6), sx: -0.25, sy: -0.04 });
		let kEff = 0;
		const explodeGap = () => 5 * ease(clamp01(kEff));
		const FULL: Win = [-CHIP_X, CHIP_X, siY0, Z0, Z1];
		const W = {
			block: [XA - XS - 0.8, XA + XS + 0.8, siY0, ZC - DZ, ZC] as Win,
			gate: [XA - 2.1, XA + 2.1, -0.9, ZC - 2.6, ZC] as Win,
			charge: [XA - 4.4, XA + 4.4, -1.25, ZC - 3.6, ZC] as Win,
			extr: [XA - XS - 0.8, XA + XS + 0.8, siY0, -HL, ZC] as Win,
			single: [XA - XS - 0.8, XA + XS + 0.8, siY0, -H8, H8] as Win
		};
		const boxOf = (v: Win, top: number): number[] => [v[0], v[1], v[2], top, v[3], v[4]];
		const chipBox = (): number[] => [-CHIP_X, CHIP_X, siY0, mcTop + 5 * explodeGap(), Z0 - 24, Z1 + 30];
		const dr = (id: string, p: number, a: number, b: number) => lerp(a, b, cq(id, p));
		const sh = {
			intro: (p: number): Shot => P({ az: dr('intro', p, -116, -104), el: 34, win: FULL, box: chipBox(), fw: 0.9, fh: 0.5, sx: 0, sy: -0.08 }),
			soi: (p: number): Shot => P({ az: dr('soi', p, -30, -24), el: 18, win: W.block, box: boxOf(W.block, mcTop + 0.3), fw: 0.7, fh: 0.6, sx: 0.02, sy: -0.1 }),
			gate: (p: number): Shot => P({ az: dr('gate', p, -26, -20), el: 20, win: W.gate, box: boxOf(W.gate, 0.35), fw: 0.62, fh: 0.5, sx: 0.02, sy: -0.1 }),
			rib: (p: number): Shot => P({ az: dr('rib', p, -24, -18), el: 19, win: W.block, box: boxOf(W.block, mcTop + 0.3), fw: 0.72, fh: 0.6, sx: 0.02, sy: -0.1 }),
			contacts: (p: number): Shot => P({ az: dr('contacts', p, -20, -16), el: 19, win: W.block, box: boxOf(W.block, VD_TOP + 0.2), fw: 0.72, fh: 0.62, sx: 0.02, sy: -0.1 }),
			charge: (p: number): Shot => P({ az: dr('charge', p, -14, -10), el: 13, win: W.charge, box: boxOf(W.charge, 1.4), fw: 0.7, fh: 0.56, sx: 0.02, sy: -0.1 }),
			extr: (): Shot => P({ az: -40, el: 24, win: W.extr, box: boxOf(W.extr, mcTop + 1), fw: 0.86, fh: 0.56, sx: 0, sy: -0.08 }),
			chip: (p: number): Shot => P({ az: dr('mzi', p, -112, -106), el: 34, win: FULL, box: chipBox(), fw: 0.9, fh: 0.5, sx: 0, sy: -0.08 }),
			phase: (p: number): Shot => plotShift({ az: dr('phase', p, -108, -102), el: 24, win: W.single, box: [XA - XS, XA + XS, siY0, mcTop + 5 * explodeGap(), -H8 - 12, H8 + 12], fw: 0.44, fh: 0.6, sx: -0.25, sy: -0.04 }),
			transfer: (p: number): Shot => plotShift({ az: dr('transfer', p, -106, -102), el: 38, win: FULL, box: chipBox(), fw: 0.44, fh: 0.6, sx: -0.25, sy: -0.04 }),
			response: (p: number): Shot => plotShift({ az: dr('response', p, -102, -98), el: 40, win: FULL, box: chipBox(), fw: 0.44, fh: 0.6, sx: -0.25, sy: -0.04 })
		};
		type Key = [number, (p: number) => Shot];
		const keys: Key[] = [
			[0, sh.intro],
			[at('intro', 1), sh.intro],
			[at('soi', 0.4), sh.soi],
			[at('soi', 1), sh.soi],
			[at('gate', 0.14), sh.gate],
			[at('gate', 0.7), sh.gate],
			[at('gate', 0.96), sh.rib],
			[at('rib', 1), sh.rib],
			[at('contacts', 0.1), sh.contacts],
			[at('contacts', 1), sh.contacts],
			[at('charge', 0.12), sh.charge],
			[at('charge', 1), sh.charge],
			[at('mzi', 0.3), sh.extr],
			[at('mzi', 0.36), sh.extr],
			[at('mzi', 0.62), sh.chip],
			[at('mzi', 1), sh.chip],
			[at('phase', 0.12), sh.phase],
			[at('phase', 1), sh.phase],
			[at('transfer', 0.12), sh.transfer],
			[at('transfer', 1), sh.transfer],
			[at('response', 0.1), sh.response],
			[1, sh.response]
		];
		/** blend two [lo, hi] spans: half size in log, centre following the size change (a pull-back keeps the subject) */
		function blendSpan(a0: number, a1: number, b0: number, b1: number, t: number): [number, number] {
			const ha = Math.max(1e-4, (a1 - a0) / 2);
			const hb = Math.max(1e-4, (b1 - b0) / 2);
			const hh = Math.exp(Math.log(ha) + (Math.log(hb) - Math.log(ha)) * t);
			const wc = Math.abs(hb - ha) > 1e-3 * Math.max(ha, hb) ? clamp01((hh - ha) / (hb - ha)) : t;
			const c = (a0 + a1) / 2 + ((b0 + b1) / 2 - (a0 + a1) / 2) * wc;
			return [c - hh, c + hh];
		}
		function shotAt(p: number): Shot {
			let i = 0;
			while (i < keys.length - 1 && p > keys[i + 1][0]) i++;
			const [pa, fa] = keys[i];
			const nx = keys[Math.min(i + 1, keys.length - 1)];
			const A = fa(p);
			if (nx[0] <= pa || p <= pa || fa === nx[1]) return A;
			const B = nx[1](p);
			const t = ease((p - pa) / (nx[0] - pa));
			const mix = (a: number, b: number) => a + (b - a) * t;
			const box = [0, 0, 0, 0, 0, 0];
			for (let j = 0; j < 6; j += 2) [box[j], box[j + 1]] = blendSpan(A.box[j], A.box[j + 1], B.box[j], B.box[j + 1], t);
			const [wx0, wx1] = blendSpan(A.win[0], A.win[1], B.win[0], B.win[1], t);
			const [wz0, wz1] = blendSpan(A.win[3], A.win[4], B.win[3], B.win[4], t);
			return {
				az: mix(A.az, B.az),
				el: mix(A.el, B.el),
				win: [wx0, wx1, mix(A.win[2], B.win[2]), wz0, wz1],
				box,
				fw: mix(A.fw, B.fw),
				fh: mix(A.fh, B.fh),
				sx: mix(A.sx, B.sx),
				sy: mix(A.sy, B.sy)
			};
		}
		const vA = new THREE.Vector3();
		const vR = new THREE.Vector3();
		const vU = new THREE.Vector3();
		const vD = new THREE.Vector3();
		let tgt: [number, number, number] = [0, 0, 0];
		let camD = 1;
		function placeCamera(s: Shot) {
			const az = s.az * DEG;
			const el = s.el * DEG;
			vD.set(Math.sin(az) * Math.cos(el), Math.sin(el), Math.cos(az) * Math.cos(el)); // target -> camera
			vR.set(Math.cos(az), 0, -Math.sin(az));
			vU.crossVectors(vD, vR).normalize();
			const [x0, x1, y0, y1, z0, z1] = s.box;
			const cx = (x0 + x1) / 2;
			const cy = (y0 + y1) / 2;
			const cz = (z0 + z1) / 2;
			const tv = Math.tan((camera.fov * DEG) / 2);
			const th = tv * (w / h);
			let d = 1e-3;
			for (const X of [x0, x1])
				for (const Y of [y0, y1])
					for (const Z of [z0, z1]) {
						vA.set(X - cx, Y - cy, Z - cz);
						const xc = vA.dot(vR);
						const yc = vA.dot(vU);
						const zc = vA.dot(vD);
						d = Math.max(d, zc + Math.abs(xc) / (th * s.fw), zc + Math.abs(yc) / (tv * s.fh));
					}
			camera.position.set(cx + vD.x * d, cy + vD.y * d, cz + vD.z * d);
			camera.up.set(0, 1, 0);
			camera.lookAt(cx, cy, cz);
			camera.setViewOffset(w, h, -s.sx * w, s.sy * h, w, h);
			camera.near = Math.max(0.005, d / 500);
			camera.far = d * 30 + 4000;
			camera.updateProjectionMatrix();
			camera.updateMatrixWorld();
			tgt = [cx, cy, cz];
			camD = d;
		}

		// ---------------------------------------------------------------------------- state helpers
		const SHIFTER_PARTS = new Set(['n_si', 'n_contact_regions', 'gate_oxide', 'oxide_regions', 'poly_rib', 'poly_top', 'metal_contacts', 'accumulation']);
		const MZI_PARTS = new Set([...SHIFTER_PARTS, 'phase_shifter', 'passive_waveguide', 'y_junctions']);
		const lit = (part: string) => hi.includes(part) || (hi.includes('phase_shifter') && SHIFTER_PARTS.has(part)) || (hi.includes('mzi') && MZI_PARTS.has(part));
		function setOpacity(b: Body, o: number) {
			const eff = lit(b.part) && o > 0.02 && o < 0.3 ? 0.3 : o;
			b.o = o;
			b.obj.visible = eff > 0.004;
			for (const x of b.mats) {
				const op = x.base * eff;
				const trans = x.trans || op < 0.999;
				if (x.m.transparent !== trans) {
					x.m.transparent = trans;
					x.m.needsUpdate = true;
				}
				x.m.opacity = op;
			}
		}
		function tint(b: Body) {
			const on = lit(b.part);
			for (const x of b.mats) {
				x.m.emissive.copy(on ? accent : black);
				x.m.emissiveIntensity = on ? 0.3 : 1;
			}
		}

		/** drive voltage on arm A's shifter (V) at p: the charge chapter ramps 0 .. 10 V (top of the Fig. 2 range); the
		 *  plot chapters take the plotted point (Fig. 2, 8 mm measured; Fig. 3b); the high-frequency test sits at its 3 V
		 *  bias; 0 elsewhere */
		function driveV(p: number): number {
			if (inCh('charge', p)) return V_TOP * seg(cq('charge', p), 0.1, 0.82);
			if (inCh('phase', p)) return phasePen(cq('phase', p))[0];
			if (inCh('transfer', p)) return transferPen(cq('transfer', p))[0];
			if (p >= CH.response[0]) return V_BIAS;
			return 0;
		}
		/** share of the phase chapter's single-shifter set-up (0: chip, 1: one 8 mm shifter alone) */
		function single(p: number): number {
			if (inCh('phase', p)) return ease(seg(cq('phase', p), 0, 0.12));
			if (inCh('transfer', p)) return 1 - ease(seg(cq('transfer', p), 0, 0.12));
			return 0;
		}
		/** arm A shifter half length (drawn) */
		function halfA(p: number): number {
			if (inCh('phase', p)) return lerp(HL, H8, ease(seg(cq('phase', p), 0, 0.12)));
			if (inCh('transfer', p)) return lerp(H8, HL, ease(seg(cq('transfer', p), 0, 0.12)));
			if (p >= CH.response[0]) return lerp(HL, H25, ease(seg(cq('response', p), 0, 0.12)));
			return HL;
		}

		interface Light {
			on: number;
			front: number;
			out: number;
			modA: number;
			modK: number;
			modZ: number;
			crA: number;
			phi: number;
		}
		/** output level when the paper gives none (zero drive, Fig. 4 bias point): half brightness, illustrative */
		const OUT_NA = 0.5;
		const bandK = (f: number) => TAU / (BAND1 / Math.max(0.05, f));
		function lightAt(p: number): Light {
			const L: Light = { on: 0, front: 1e6, out: OUT_NA, modA: 0, modK: 0, modZ: 0, crA: 0, phi: 0 };
			if (p < CH.soi[0]) L.on = easeOut(seg(cq('intro', p), 0.05, 0.5));
			else if (p < CH.mzi[0]) L.on = inCh('soi', p) ? 1 - seg(cq('soi', p), 0, 0.14) : 0;
			else if (p < CH.phase[0]) {
				const q = cq('mzi', p);
				L.on = seg(q, 0.6, 0.66);
				L.front = lerp(Z0 - BEAM, Z1 + BEAM + 40, seg(q, 0.62, 0.95));
			} else if (p < CH.transfer[0]) {
				const q = cq('phase', p);
				L.on = 1;
				L.crA = ease(seg(q, 0.08, 0.2));
				L.phi = Math.PI * phasePen(q)[1];
			} else if (p < CH.response[0]) {
				const q = cq('transfer', p);
				L.on = 1;
				L.crA = 1 - ease(seg(q, 0, 0.1));
				L.phi = Math.PI * phasePen(1)[1] * L.crA;
				L.out = Math.pow(10, transferPen(q)[1] / 10);
			} else {
				const q = cq('response', p);
				const [f, y] = responsePen(q);
				L.on = 1;
				L.modA = Math.min(0.95, 0.85 * Math.pow(10, y / 10)) * ease(seg(q, 0.02, 0.1));
				L.modK = bandK(f);
				L.modZ = Z1 - LS + 260 * q;
			}
			return L;
		}

		// ---------------------------------------------------------------------------- frame
		let win: Win = FULL;
		const vP = new THREE.Vector3();
		/** longest beam from (x, z0) along +z whose end stays inside the free part of the pane */
		function beamClip(x: number, z0: number, len: number, ok: (sx: number, sy: number) => boolean): number {
			const s = (l: number): [number, number] => {
				vP.set(x, RIB_Y + 3 * explodeGap(), z0 + l).applyMatrix4(root.matrixWorld).project(camera);
				return [((vP.x + 1) / 2) * w, ((1 - vP.y) / 2) * h];
			};
			if (ok(...s(len))) return len;
			if (!ok(...s(0))) return 0;
			let lo = 0;
			let hi2 = len;
			for (let i = 0; i < 14; i++) {
				const m = (lo + hi2) / 2;
				if (ok(...s(m))) lo = m;
				else hi2 = m;
			}
			return lo;
		}
		const zCov = (a: number, b: number) => clamp01((Math.min(win[4], b) - Math.max(win[3], a)) / (b - a));
		const xIn = (a: number, b: number) => (a >= win[0] - 1e-6 && b <= win[1] + 1e-6 ? 1 : 0);

		function frame(p: number) {
			lastP = p;
			kEff = p >= CH.phase[0] ? k : 0;
			const g = explodeGap();
			const fl = 1 - ease(seg(cq('intro', p), 0, 0.9));
			root.rotation.set(-0.05 * fl, 0.14 * fl, 0.03 * fl);
			root.updateMatrixWorld(true);
			const s = shotAt(p);
			win = s.win;
			placeCamera(s);
			const [x0, x1, y0w, zA, zB] = win;

			// ---- build: the finished chip dissolves to the substrate, then the cross-section is assembled layer by layer
			const inBuild = p >= CH.soi[0] && p < CH.mzi[0];
			const qS = cq('soi', p);
			const leaving = inCh('soi', p) && qS < 0.32;
			const gone = leaving ? ease(seg(qS, 0.03, 0.28)) : 0;
			/** [opacity, drop] of a layer arriving in chapter c over local [a, b] */
			const arrive = (c: string, a: number, b: number, drop: number): [number, number] => {
				if (!inBuild) return [1, 0];
				if (leaving) return [1 - gone, 3 * gone];
				if (p < CH[c][0]) return [0, drop];
				const t = ease(seg(cq(c, p), a, b));
				return [t, drop * (1 - t)];
			};
			const stBox = arrive('soi', 0.34, 0.58, 2.2);
			const stNsi = arrive('soi', 0.5, 0.78, 2.2);
			const stGox = arrive('gate', 0.22, 0.6, 0.5);
			const stOxb = arrive('rib', 0.06, 0.42, 1.6);
			const stPoly = arrive('rib', 0.4, 0.8, 1.8);
			const stAl = arrive('contacts', 0.3, 0.64, 1.4);
			const stTm = inBuild && !leaving ? (p < CH.contacts[0] ? 0 : ease(seg(cq('contacts', p), 0.62, 0.9))) : 0;
			// colours: contact regions shade in at the slab ends; the outer polysilicon shades to the doped colour
			const ncShade = inBuild && !leaving ? (p < CH.soi[0] ? 0 : ease(seg(qS, 0.78, 0.96))) : 1;
			const dopShade = inBuild && !leaving ? (p < CH.contacts[0] ? 0 : ease(seg(cq('contacts', p), 0.04, 0.34))) : 1;
			for (const M of [MA, MB]) {
				M.ncon.color.copy(colNsi).lerp(colNcon, ncShade);
				M.top.color.copy(colRib).lerp(colTop, dopShade);
			}

			// chip-level presence: second shifter, passive guides, Y junctions
			const qM = cq('mzi', p);
			const sgl = single(p);
			let chipO = 1;
			if (leaving) chipO = 1 - gone;
			else if (inBuild) chipO = 0;
			else if (inCh('mzi', p)) chipO = ease(seg(qM, 0.42, 0.68));
			chipO *= 1 - sgl;
			let shiftB = chipO;
			if (p >= CH.response[0]) shiftB = 1 - ease(seg(cq('response', p), 0, 0.12));
			const pvB = p >= CH.response[0] ? 1 - shiftB : 0;

			// substrate and buried oxide to the window
			fit(si.obj, x0, x1, Math.max(y0w, siY0), siY1, zA, zB);
			setOpacity(si, si.obj.visible ? 1 : 0);
			if (fit(boxL.obj, x0, x1, Math.max(y0w, boxY0), boxY1, zA, zB)) boxL.obj.position.y += g + stBox[1];
			setOpacity(boxL, boxL.obj.visible ? stBox[0] : 0);

			// shifters
			const hA = halfA(p);
			const stOf = (key: string): [number, number] =>
				key.startsWith('nsi') || key.startsWith('ncon') ? stNsi : key.startsWith('gox') ? stGox : key.startsWith('oxb') ? stOxb : key.startsWith('al') ? stAl : stPoly;
			const place = (S: Layer[], cx: number, z0: number, z1: number, oMul: number) => {
				const za = Math.max(zA, z0);
				const zb = Math.min(zB, z1);
				for (const L of S) {
					const st = stOf(L.b.key);
					let any = false;
					for (const pc of L.pieces) {
						const ok = fit(pc.mesh, Math.max(x0, cx + pc.x[0]), Math.min(x1, cx + pc.x[1]), Math.max(y0w, L.y[0]), L.y[1], za, zb);
						if (ok) pc.mesh.position.y += L.lv * g + st[1];
						any ||= ok;
					}
					setOpacity(L.b, any ? st[0] * oMul : 0);
				}
			};
			place(SA, XA, -hA, hA, 1);
			place(SB, -XA, -HL, HL, shiftB);

			// accumulated charge on arm A: density from the drive (Eq. 1), drawn only above flat band
			{
				const f = charge(driveV(p));
				// proud of the cut faces by a hair so the sheets show on them
				const e = 0.002 * Math.max(1, zB - zA);
				const za = Math.max(zA, -hA) - e;
				const zb = Math.min(zB, hA) + e;
				const okH = fit(qHoles, Math.max(x0, XA - RW + 0.004), Math.min(x1, XA + RW - 0.004), nY1 + T_OX, nY1 + T_OX + T_Q, za, zb);
				if (okH) qHoles.position.y += 4 * g + stPoly[1];
				const okE = fit(qElec, Math.max(x0, XA - RW + 0.004), Math.min(x1, XA + RW - 0.004), nY1 - T_Q, nY1, za, zb);
				if (okE) qElec.position.y += 2 * g + stNsi[1];
				const o = f > 0 ? 0.25 + 0.75 * Math.sqrt(f) : 0;
				qMat.opacity = o * (lit('accumulation') ? 1 : 0.95);
				qMat.color.set(lit('accumulation') ? (theme === 'light' ? '#2a78d6' : '#7fb3ff') : theme === 'light' ? '#d9730f' : look('accumulation').color || '#f7962c');
				// a few nanometres of charge: shown on the cut face in the close shots only
				const wppQ = (2 * camD * Math.tan((camera.fov * DEG) / 2)) / h;
				qG.visible = o > 0.004 && stPoly[0] > 0.5 && stNsi[0] > 0.5 && wppQ < 0.12;
			}

			// passive guides and Y junctions (only when the window holds the chip)
			{
				const full = xIn(-XA - 1, XA + 1);
				const cov = (a: number, b: number) => full * seg(zCov(a, b), 0.97, 1);
				const yO = chipO * cov(Z0, Z1);
				yj.obj.position.y = 2 * g;
				setOpacity(yj, yO);
				const segs: [number, number, number][] = [
					[0, Z0, Z0 + LS],
					[0, Z1 - LS, Z1],
					[XA, -HL, -hA],
					[XA, hA, HL],
					[-XA, -HL, HL]
				];
				pvMeshes.forEach((m, i) => {
					const [cx, a, b] = segs[i];
					const ok = fit(m, cx - RW, cx + RW, SB_Y0, ribTop, Math.max(zA, a), Math.min(zB, b));
					m.visible = ok && (i < 4 || pvB > 0.004);
				});
				pv.obj.position.y = 2 * g;
				setOpacity(pv, Math.max(yO, pvB * cov(Z0, Z1)));
			}

			// drive and ground markers at the block face (Fig. 1)
			{
				const o = inBuild ? stTm : inCh('mzi', p) ? 1 - seg(qM, 0, 0.18) : 0;
				const zf = ZC - 0.5;
				post.position.set(XA + VD_X, mcTop, zf);
				post.scale.set(1, VD_TOP - mcTop, 1);
				dot.position.set(XA + VD_X, VD_TOP, zf);
				const gx = XA - XS;
				gLead.position.set(gx, nY1 - 0.06, zf);
				gLead.scale.set(0.55, 1, 1);
				gBars.forEach((b, i) => b.position.set(gx - 0.55 - i * 0.11, nY1 - 0.06, zf));
				tm.obj.position.y = 4 * g;
				post.visible = dot.visible = !!xIn(XA + VD_X - 0.2, XA + VD_X + 0.2);
				const gIn2 = !!xIn(gx - 0.8, gx);
				gLead.visible = gIn2;
				for (const b of gBars) b.visible = gIn2;
				setOpacity(tm, o);
			}
			for (const b of bodies) tint(b);

			// ---- light
			const L = lightAt(p);
			const wpp = (2 * camD * Math.tan((camera.fov * DEG) / 2)) / h; // world units per pixel at the target
			const rw = Math.min(4.6, Math.max(0.5, 6 * wpp));
			lightGroup.position.y = 3 * g;
			const light = theme === 'light';
			const red = light ? '#e0281a' : '#ff3324';
			const plotCh = p >= CH.phase[0];
			const wide = w >= 700;
			const free = (sx: number, sy: number) => sx <= w - 24 && sx >= 0 && (!plotCh ? true : wide ? sx <= 0.5 * w - 28 : sy <= 0.44 * h - 12);
			const fullX = xIn(-XA - 1, XA + 1);
			const outLen = fullX ? beamClip(0, Z1, BEAM, free) : 0;
			const phOutLen = beamClip(XA, H8, BEAM, free);
			for (const r of ribbons) {
				const u = r.m.uniforms;
				u.uW.value = rw * (r.kind === 'in' || r.kind === 'out' || r.kind === 'phIn' || r.kind === 'phOut' ? 1.4 : 1);
				u.uFront.value = L.front;
				u.uWz0.value = r.kind === 'in' || r.kind === 'phIn' ? -1e6 : zA;
				u.uWz1.value = r.kind === 'out' || r.kind === 'phOut' ? 1e6 : zB;
				const outStem = r.kind === 'outStem' || r.kind === 'out';
				u.uModA.value = outStem ? L.modA : 0;
				u.uModK.value = L.modK;
				u.uModZ.value = L.modZ;
				const crest = r.kind === 'armA' || r.kind === 'phIn' || r.kind === 'phOut';
				u.uCrA.value = crest ? L.crA : 0;
				u.uPhS.value = -hA;
				u.uPhE.value = hA;
				u.uPhi.value = L.phi;
				u.uGh.value = r.kind === 'phOut' ? L.crA : 0;
				let I = 0.8;
				if (r.kind === 'in' || r.kind === 'chip' || r.kind === 'phIn') I = 1;
				else if (outStem) I = Math.min(1, L.out * 1.1);
				// whole-chip light vs the single shifter of Fig. 2
				let pres = 1;
				if (r.kind === 'phIn' || r.kind === 'phOut') pres = sgl;
				else if (r.kind !== 'armA') pres = (1 - sgl) * fullX;
				u.uI.value = I * L.on * pres;
				u.uZa.value = r.kind === 'in' ? Z0 - BEAM : r.kind === 'phIn' ? -H8 - BEAM : -1e6;
				u.uZb.value = r.kind === 'out' ? Z1 + Math.max(1, outLen) : r.kind === 'phOut' ? H8 + Math.max(1, phOutLen) : 1e6;
				const on = lit(r.part) || (r.kind === 'armA' && lit('phase_shifter'));
				u.uColor.value.set(on ? (light ? '#2a78d6' : '#7fb3ff') : red);
				if (on && pres > 0.5 && u.uI.value < 0.35 && L.on > 0.5) u.uI.value = 0.35;
				r.mesh.visible = u.uI.value > 0.002;
			}
			for (const { m, r } of proxies) m.visible = wpp > 0.12 && r.mesh.visible && (r.m.uniforms.uI.value as number) > 0.2;
			{
				const reached = seg(L.front, Z1, Z1 + 40);
				const mod = clamp01(1 + L.modA * Math.cos(L.modK * (Z1 - L.modZ)));
				const fI = fullX && zB >= Z1 - 1 ? L.on * reached * Math.min(1, L.out * 1.1) * mod * (1 - sgl) : 0;
				flare.visible = fI > 0.01 && wpp > 0.12 && outLen > 1;
				flare.position.set(0, RIB_Y, Z1 + 1);
				flare.scale.setScalar(26 * wpp * (0.6 + 0.4 * Math.min(1, fI)));
				flareMat.opacity = Math.min(1, fI * 1.1);
			}
		}

		// ---------------------------------------------------------------------------- pick / anchor
		const raycaster = new THREE.Raycaster();
		const v2 = new THREE.Vector2();
		const vq = new THREE.Vector3();
		const vc = new THREE.Vector3();
		function screen(x: number, y: number, z: number): [number, number] | null {
			vq.set(x, y, z).applyMatrix4(root.matrixWorld);
			vc.copy(vq).applyMatrix4(camera.matrixWorldInverse);
			if (vc.z > -camera.near) return null;
			vq.project(camera);
			return [((vq.x + 1) / 2) * w, ((1 - vq.y) / 2) * h];
		}
		const f1 = (v: number) => v.toFixed(1);
		const f2 = (v: number) => v.toFixed(2);
		function phaseInfo(p: number): PickInfo {
			const q = cq('phase', p);
			const [v, ph] = phasePen(q);
			return {
				id: 'phase_light',
				label: 'Light through one 8 mm phase shifter',
				detail: [
					`V_{D} ${f1(v)} V, phase shift ${f2(ph)} π (Fig. 2, 8 mm, measured; the plotted point)`,
					'Crests drawn far apart (illustrative spacing); beyond the shifter they move by the phase shift, ticks = zero drive',
					'Measured in a free-space interferometer at 1.55 µm, not in the MZI'
				]
			};
		}
		function outInfo(p: number): PickInfo | null {
			if (inCh('transfer', p)) {
				const [v, db] = transferPen(cq('transfer', p));
				return {
					id: 'light_out',
					label: 'Modulated light out',
					detail: [
						`V_{D} ${f1(v)} V on one 10 mm shifter (the plotted point)`,
						`Relative transmission ${f1(db)} dB (Fig. 3b, digitized); brightness = that power ratio, linear`,
						'1.54 µm; the other shifter undriven'
					]
				};
			}
			if (p >= CH.response[0]) {
				const [f, y] = responsePen(cq('response', p));
				return {
					id: 'light_out',
					label: 'Modulated light out',
					detail: [
						`Drive ${f2(f)} GHz on one 2.5 mm shifter, 3 V bias (the plotted point${plotSel === 'rms' ? ' of Fig. 4a' : ''})`,
						`Optical response ${f2(y)} dB (Fig. 4b${plotSel === 'rms' ? ' at that frequency' : ''}); band contrast scaled by that ratio, linear`,
						'Band spacing drawn proportional to 1 / f (illustrative); mean level not given, drawn at half brightness'
					]
				};
			}
			if (p < CH.phase[0])
				return {
					id: 'light_out',
					label: 'Light out',
					detail: ['No drive; the output level at zero drive is not given (drawn at half brightness)']
				};
			return null;
		}
		function chargeInfo(p: number): PickInfo {
			const v = driveV(p);
			const src = inCh('charge', p) ? 'ramp to 10 V, the top of the Fig. 2 range' : inCh('phase', p) ? 'the plotted point of Fig. 2' : inCh('transfer', p) ? 'the plotted point of Fig. 3b' : 'the 3 V bias of the high-frequency test';
			return {
				id: 'accumulation',
				label: 'Accumulated charge',
				detail: [
					`V_{D} ${f1(v)} V (${src})`,
					v > V_FB ? 'Density grows with V_{D} − 1.25 V (Eq. 1); colour strength grows with it, no density value (permittivity not printed)' : 'Below the 1.25 V flat-band voltage: no accumulation'
				]
			};
		}
		const SHIFTER_LAYERS = new Set(['n_si', 'n_contact_regions', 'gate_oxide', 'oxide_regions', 'poly_rib', 'poly_top', 'metal_contacts']);
		function pick(x: number, y: number): string | PickInfo | null {
			const p = lastP;
			v2.set((x / w) * 2 - 1, 1 - (y / h) * 2);
			raycaster.setFromCamera(v2, camera);
			const wpp = (2 * camD * Math.tan((camera.fov * DEG) / 2)) / h;
			// light first in the wide shots (it is drawn over the chip)
			const lc: T.Object3D[] = [];
			for (const { m } of proxies) if (m.visible) lc.push(m);
			if (flare.visible) lc.push(flare);
			const lh = raycaster.intersectObjects(lc, false)[0];
			if (lh) {
				if (lh.object === flare) return outInfo(p) ?? 'light_out';
				const r = proxies.find((q) => q.m === lh.object)?.r;
				if (r) {
					if (inCh('phase', p) && (r.kind === 'armA' || r.kind === 'phIn' || r.kind === 'phOut')) return phaseInfo(p);
					if ((r.kind === 'out' || r.kind === 'outStem') && p >= CH.phase[0]) return outInfo(p) ?? r.part;
					return r.part;
				}
			}
			const cands: T.Object3D[] = [];
			for (const b of bodies) if (b.obj.visible && b.o > 0.2) cands.push(...b.picks.filter((m) => m.visible));
			if (qG.visible) cands.push(qHoles, qElec);
			const hit = raycaster.intersectObjects(cands, false)[0];
			if (!hit) return null;
			const part = (hit.object.userData.part as string | undefined) ?? null;
			if (part === 'accumulation') return chargeInfo(p);
			// far away a layer is a few pixels thick: the whole phase shifter is the useful pick
			if (part && wpp > 0.12 && SHIFTER_LAYERS.has(part)) return 'phase_shifter';
			return part;
		}
		function anchor(id: string): [number, number] | null {
			const p = lastP;
			let s: [number, number] | null = null;
			if (id === 'n_si') {
				if (!inCh('soi', p) || cq('soi', p) < 0.6) return null;
				s = screen(XA - 4.2, (nY0 + nY1) / 2 + 2.2 * (1 - ease(seg(cq('soi', p), 0.5, 0.78))), win[4]);
			} else if (id === 'gate_oxide') {
				if (!inCh('gate', p) || cq('gate', p) < 0.6 || cq('gate', p) > 0.92) return null;
				s = screen(XA + 0.7, nY1 + T_OX, win[4]);
			} else if (id === 'poly_rib') {
				if (!inCh('rib', p) || cq('rib', p) < 0.82) return null;
				s = screen(XA + 0.4, (oxTop + ribTop) / 2, win[4]);
			} else return null;
			if (!s) return null;
			if (s[0] < 4 || s[0] > w - 4 || s[1] < 8 || s[1] > h - 12) return null;
			return s;
		}

		return {
			assembledAt: CH.phase[0],
			orbit: { polar: [6, 80] },
			frame,
			plot(id) {
				plotSel = id;
			},
			highlight(ids) {
				hi = [...ids];
			},
			pick,
			anchor,
			target: () => tgt,
			resize(nw, nh) {
				w = Math.max(1, nw);
				h = Math.max(1, nh);
			},
			explode(nk) {
				k = clamp01(nk);
			},
			theme(t) {
				theme = t;
				applyTheme();
			},
			dispose() {
				scene.remove(root);
				camera.clearViewOffset();
				for (const d of disposables) d.dispose();
			}
		};
	}
};
export default mod;
