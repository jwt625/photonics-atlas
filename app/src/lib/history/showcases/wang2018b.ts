// Scene module: thin-film lithium niobate Mach-Zehnder modulator, Wang et al., Nature 2018 (DevLog-017).
// Spec: data/history/showcases/wang2018b.yaml. Contract: ../showcase/types.ts.
//
// Two scales (spec header, report section 8):
// - Cross-section (world x = crystal z across the gaps, world y = film normal) in um and to scale: Si (drawn truncated),
//   buried SiO2 4.7, LN film 0.6 (slab 0.3, ridge 0.3), ridge top 0.8 / bottom 1.0 (digitized), gold 1.1 on the slab
//   (2018 value), cladding 0.8 (flat top, profile assumed). Drawn electrode widths are render values (assumed): centre body
//   33.5, outer bodies 150; the 2018 gap (4.5, digitized) and widths live in the part details as 2018 values only.
// - Along the propagation (world z) the device is schematic and compressed: the 20 mm electrodes are drawn EL long, the
//   Y-junction bends and the chip ends are plain stand-ins (plan layout withheld). Nothing implies a scale along z.
// Electrodes (owner decision, pass 3): drawn as a later differential T-rail design, not the 2018 plain G-S-G line:
// three strips S-bar / S / S-bar on the slab (no ground between the signals, Aimone et al., OFC 2026), rows of T segments
// along every gap edge with Kharel et al. (Optica 2021) sizes (g, h, s, t, r, c) = (5, 6, 2, 6, 45, 5) um, period 50 um,
// facing rows mirror-aligned. Close-ups are true size; the whole-chip view shows an illustrative count (20 periods on the
// shortened 20 mm line). Driver pads S-bar S S S-bar at the light-input end; four loads at the far end (one per outer
// strip, two on the centre strip, Aimone et al. Fig. 1a). The 2018 stack, ridges and arm positions as drawn are kept;
// every plot is the 2018 device.
// Microwave scale (pass 4): in the true-size close-ups the field is drawn at an illustrative 34 GHz with its true 4 mm
// wavelength (about 80 segment periods), so it is nearly uniform over the view and oscillates with p; the travelling
// wave with the light tracer is shown only in the whole-chip view, where the wavelength is shortened like the plan.
// Velocity matching shown is the 2018 plain line's; it is not claimed for the drawn T-rail line on the 2018 stack.
// Field arrows, the mode spot and the light tracer are illustrative.
//
// The model is drawn inside a window (x0, x1, y0, z0, z1): the whole chip in the wide shots, a small block cut from the
// electrode section (near face at z = ZC) in the cross-section chapters. Every layer is a unit body scaled to the window,
// so the block grows into the chip as the camera pulls back. Everything is a pure function of p (and explode k).
import type * as T from 'three';
import { AXES_END, staggerK } from '../showcase/plot';
import { clamp01, ease, easeOut, lerp, seg } from '../showcase/progress';
import type { PickInfo, ShowcaseContext, ShowcaseHandle, ShowcaseModule, Theme } from '../showcase/types';

type V3 = [number, number, number];
type Geo = Record<string, unknown>;
type Win = [number, number, number, number, number]; // x0 x1 y0 z0 z1

const DEG = Math.PI / 180;
const TAU = Math.PI * 2;
const num = (v: unknown, d: number): number => (typeof v === 'number' && Number.isFinite(v) ? v : d);
const pair = (v: unknown, d: [number, number]): [number, number] =>
	Array.isArray(v) && v.length === 2 && v.every((x) => typeof x === 'number') ? [v[0] as number, v[1] as number] : d;

// ------------------------------------------------------------------------------------------------ schematic plan (assumed)
const EL = 1000; // drawn electrode length (stands for 20 mm)
const LB = 170; // Y-junction bend length
const LS = 70; // straight input / output waveguide to the facet
const CHIP_X = 200; // chip half width (um, beyond the ground strips)
const Z0 = -EL / 2 - LB - LS; // input facet
const Z1 = EL / 2 + LB + LS; // output facet
const ZC = -EL / 2 + 260; // section cut through the electrode section (near face of the cross-section block)
const BEAM = 150; // drawn beam length outside the chip
const F_CLOSE = 34; // GHz: illustrative drive frequency in the true-size close-ups (wavelength c / (2.2 f) = 4 mm there)
const NG = 2.2; // microwave and optical group index, "both approximately 2.2" (Methods)
const MM = EL / 20; // drawn units per mm along the device (20 mm electrodes)
const ARROW_DZ = 9; // spacing of the field arrows along each gap
const LINE_L = 600; // length of the block in the fields chapter

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
// light along a waveguide path: front (light entering), window clip, tracer packet, output modulation, beam end fades
const RIB_FS = /* glsl */ `
uniform vec3 uColor; uniform float uI; uniform float uLight; uniform float uK;
uniform float uFront; uniform float uWz0; uniform float uWz1;
uniform float uPk; uniform float uPkI; uniform float uPkW;
uniform float uModA; uniform float uModK; uniform float uModZ;
uniform float uZa; uniform float uZb;
varying float vZ; varying float vU;
void main() {
	if (vZ < uWz0 || vZ > uWz1) discard;
	float u2 = vU * vU;
	float across = 0.55 * exp(-u2 * 2.5) + 0.45 * exp(-u2 * 14.0);
	float a = uI;
	a *= clamp(1.0 + uModA * cos(uModK * (vZ - uModZ)), 0.0, 2.0);
	float pk = uPkI * exp(-pow((vZ - uPk) / uPkW, 2.0));
	a += pk;
	a *= across;
	a *= 1.0 - smoothstep(uFront - 30.0, uFront, vZ);
	a *= smoothstep(uZa, uZa + 60.0, vZ) * (1.0 - smoothstep(uZb - 50.0, uZb, vZ));
	a = clamp(a * uK, 0.0, 1.0);
	vec3 col = mix(uColor, uLight > 0.5 ? vec3(0.75, 0.1, 0.05) : vec3(1.0, 0.9, 0.85), clamp(pk * 0.7, 0.0, 0.8));
	gl_FragColor = uLight > 0.5 ? vec4(col, a) : vec4(col * a, a);
}`;
// microwave voltage on a strip: glow ~ |V(z)|, V = sign (U + W cos(k (z - z0))); amber positive, blue negative; unit plane
// scaled to the strip in the window
const WAVE_VS = /* glsl */ `
varying vec3 vL;
void main() { vL = position; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`;
const WAVE_FS = /* glsl */ `
uniform vec3 uColor; uniform float uA; uniform float uU; uniform float uWv; uniform float uKw; uniform float uZw;
uniform float uLight; uniform vec4 uMap; // local -> strip coords: x = uMap.x + local.x * uMap.y, z = uMap.z + local.z * uMap.w
uniform float uE0; uniform float uE1; uniform float uSign; uniform vec3 uColorN; uniform float uSq;
varying vec3 vL;
void main() {
	float x = uMap.x + vL.x * uMap.y;
	float z = uMap.z + vL.z * uMap.w;
	float v0 = uU + uWv * cos(uKw * (z - uZw));
	if (uSq > 0.0) v0 = tanh(uSq * v0) / tanh(uSq);
	float v = uSign * v0;
	float e = abs(v);
	// weight: even floor across the strip, brighter toward its gap-facing edge(s)
	float d = min(abs(x - uE0), abs(x - uE1));
	float a = clamp(uA * pow(e, 1.4) * (0.55 + 0.45 * exp(-d / 12.0)), 0.0, 1.0);
	vec3 col = v >= 0.0 ? uColor : uColorN;
	gl_FragColor = uLight > 0.5 ? vec4(col, a * 0.8) : vec4(col * a, a);
}`;

// ------------------------------------------------------------------------------------------------ module
const mod: ShowcaseModule = {
	renderer: '3d',
	build(ctx: ShowcaseContext): ShowcaseHandle {
		if (ctx.kind !== '3d') throw new Error('wang2018b is a 3D scene');
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
			intro: [0, 0.07], stack: [0.07, 0.17], ridge: [0.17, 0.27], electrodes: [0.27, 0.37], cladding: [0.37, 0.44],
			mzi: [0.44, 0.55], fields: [0.55, 0.69], vpi: [0.69, 0.79], bandwidth: [0.79, 0.89], fom: [0.89, 1]
		};
		const CH = Object.fromEntries(
			Object.keys(fallback).map((id) => [id, (spec.chapters.find((c) => c.id === id)?.p ?? fallback[id]) as [number, number]])
		) as Record<string, [number, number]>;
		/** local progress inside a chapter */
		const cq = (id: string, p: number) => seg(p, CH[id][0], CH[id][1]);
		/** p at local progress q of a chapter */
		const at = (id: string, q: number) => lerp(CH[id][0], CH[id][1], q);
		const inCh = (id: string, p: number) => p >= CH[id][0] && p < CH[id][1];

		// ---------------------------------------------------------------------------- cross-section from the spec (um)
		const siD = num(geo('si_substrate').drawn_depth, 8);
		const [boxY0, boxY1] = pair(geo('buried_oxide').y, [-4.7, 0]);
		const [slabY0, slabY1] = pair(geo('ln_slab').y, [0, 0.3]);
		const rG = geo('ln_ridge');
		const [ridY0, ridY1] = pair(rG.y, [0.3, 0.6]);
		const ridTop = num(rG.top_width, 0.8);
		const ridBot = num(rG.bottom_width, 1.0);
		const RX = Math.abs(pair(rG.centers_z, [-27.25, 27.25])[1]); // arm centre |x|
		const sG = geo('signal_line');
		const [elY0, elY1] = pair(sG.y, [0.3, 1.4]);
		const sigHalf = Math.abs(pair(sG.z, [-25, 25])[1]);
		const gG = geo('ground_lines');
		const gIn = num(gG.z_inner, 29.5);
		const gW = num(gG.width, 150);
		const cladT = num(geo('cladding').thickness, 0.8);
		const siY0 = boxY0 - siD;
		// T-rail segments (Kharel et al. geometry, part t_rail): gap g between facing caps, stem h x t, cap s x r, slit c
		const tG = geo('t_rail');
		const tg = num(tG.gap_g, 5);
		const thh = num(tG.stem_h, 6);
		const ts = num(tG.cap_s, 2);
		const tt = num(tG.stem_t, 6);
		const tr = num(tG.cap_r, 45);
		const tc = num(tG.slit_c, 5);
		const tP = num(tG.period, tr + tc);
		const gapMid = RX; // ridge centred in the gap between facing caps
		const topY = elY1 + cladT;

		// ---------------------------------------------------------------------------- transfer curve (Fig. 1c, digitized)
		const tPts = ((spec.plots?.find((q) => q.id === 'transfer')?.series?.[0]?.points ?? []) as [number, number][])
			.filter((q) => Array.isArray(q) && Number.isFinite(q[0]) && Number.isFinite(q[1]))
			.sort((a, b) => a[0] - b[0]);
		const vMax = tPts.length ? tPts[tPts.length - 1][0] : 2.8;
		function transfer(v: number): number {
			if (!tPts.length) return 0.5;
			if (v <= tPts[0][0]) return tPts[0][1];
			for (let i = 1; i < tPts.length; i++)
				if (v <= tPts[i][0]) {
					const [x0, y0] = tPts[i - 1];
					const [x1, y1] = tPts[i];
					return clamp01(y0 + ((y1 - y0) * (v - x0)) / Math.max(1e-9, x1 - x0));
				}
			return clamp01(tPts[tPts.length - 1][1]);
		}

		// ---------------------------------------------------------------------------- materials, bodies
		const disposables: { dispose(): void }[] = [];
		const keep = <X extends { dispose(): void }>(x: X): X => (disposables.push(x), x);
		const G = <X extends T.BufferGeometry>(g: X): X => keep(g);
		const root = new THREE.Group();
		scene.add(root);
		const model = new THREE.Group();
		root.add(model);

		// studio environment for the metals (soft boxes on a dark room): clean long highlights on the gold
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
		const bodies = new Map<string, Body>();
		function body(key: string, part: string, obj: T.Object3D): Body {
			const b: Body = { key, part, obj, mats: [], picks: [], o: 1 };
			obj.traverse((n) => {
				const mesh = n as T.Mesh;
				const m = mesh.material as T.MeshPhysicalMaterial | undefined;
				if (mesh.isMesh && m && 'emissive' in m && !b.mats.some((x) => x.m === m)) b.mats.push({ m, base: m.opacity, trans: m.transparent });
				if (mesh.isMesh && !n.userData.nopick) {
					n.userData.part = part;
					b.picks.push(mesh);
				}
			});
			model.add(obj);
			bodies.set(key, b);
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
					// own environment on every body: the look does not depend on whether the shared room map is set yet
					envMap: studio,
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
		const dielectric = { roughness: 0.42, clearcoat: 0.25, clearcoatRoughness: 0.35, envMapIntensity: 0.35 };

		const si = body('si', 'si_substrate', new THREE.Mesh(unitBox, std('si_substrate', { envMapIntensity: 0.3 })));
		const boxL = body('box', 'buried_oxide', new THREE.Mesh(unitBox, std('buried_oxide', { ...dielectric, roughness: 0.25 })));
		const slab = body('slab', 'ln_slab', new THREE.Mesh(unitBox, std('ln_slab', dielectric)));
		// the upper half of the film before the etch: one box per field between the ridges, lowered by the etch
		const etchMat = std('ln_ridge', dielectric);
		const etchMeshes = [0, 1, 2].map(() => new THREE.Mesh(unitBox, etchMat));
		const etchG = new THREE.Group();
		etchG.add(...etchMeshes);
		const etch = body('etch', 'ln_slab', etchG);

		// ridges: trapezoid prisms of unit length along z (to scale in x, y)
		const trapShape = (cx: number) =>
			new THREE.Shape([
				new THREE.Vector2(cx - ridBot / 2, ridY0),
				new THREE.Vector2(cx + ridBot / 2, ridY0),
				new THREE.Vector2(cx + ridTop / 2, ridY1),
				new THREE.Vector2(cx - ridTop / 2, ridY1)
			]);
		const ridgeMat = std('ln_ridge', { ...dielectric, roughness: 0.3 });
		const armMeshes = [-RX, RX].map((cx) => new THREE.Mesh(G(new THREE.ExtrudeGeometry(trapShape(cx), { depth: 1, bevelEnabled: false })), ridgeMat));
		const armG = new THREE.Group();
		armG.add(...armMeshes);
		const ridges = body('ridge', 'ln_ridge', armG);

		// Y-junction routing (schematic): the trapezoid swept along a path in the x-z plane
		type P2 = [number, number]; // (x, z)
		const bend = (xa: number, za: number, xb: number, zb: number, n = 48): P2[] =>
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
		function sweep(path: P2[]): T.BufferGeometry {
			const prof: [number, number][] = [
				[-ridBot / 2, ridY0],
				[-ridTop / 2, ridY1],
				[ridTop / 2, ridY1],
				[ridBot / 2, ridY0]
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
		const pStem: P2[] = [[0, Z0], [0, Z0 + LS]];
		const pSplitU = bend(0, Z0 + LS, RX, -EL / 2);
		const pSplitD = bend(0, Z0 + LS, -RX, -EL / 2);
		const pArmU: P2[] = [[RX, -EL / 2], [RX, EL / 2]];
		const pArmD: P2[] = [[-RX, -EL / 2], [-RX, EL / 2]];
		const pCombU = bend(RX, EL / 2, 0, Z1 - LS);
		const pCombD = bend(-RX, EL / 2, 0, Z1 - LS);
		const pOut: P2[] = [[0, Z1 - LS], [0, Z1]];
		const routeMat = (id: string) => std(id, { ...dielectric, roughness: 0.3, side: THREE.DoubleSide });
		const routeG = (paths: P2[][], m: T.Material) => {
			const g = new THREE.Group();
			for (const pth of paths) g.add(new THREE.Mesh(sweep(pth), m));
			return g;
		};
		const split = body('split', 'y_splitter', routeG([pStem, pSplitU, pSplitD], routeMat('y_splitter')));
		const comb = body('comb', 'y_combiner', routeG([pCombU, pCombD, pOut], routeMat('y_combiner')));

		// electrodes on the slab: G (x < 0), S, G (x > 0); widths are render values (assumed)
		const goldMat = () => std('signal_line', { envMap: studio, envMapIntensity: 1.15, clearcoat: 0.15 });
		const sig = body('sig', 'signal_line', new THREE.Mesh(unitBox, goldMat()));
		const gndL = body('gndL', 'ground_lines', new THREE.Mesh(unitBox, goldMat()));
		const gndR = body('gndR', 'ground_lines', new THREE.Mesh(unitBox, goldMat()));
		// driver pads S-bar S S S-bar at the input end (Aimone et al. Fig. 1a: the two inner pads on the centre strip) and one
		// load per conductor at the far end: neutral markers, no geometry in the sources
		const outC = gIn + gW / 2; // centre of an outer strip
		const PADS: [number, number][] = [[-outC - 8, -outC + 8], [-sigHalf + 2, -2], [2, sigHalf - 2], [outC - 8, outC + 8]];
		const LOADS: [number, number][] = [[-outC - 12, -outC + 12], [-sigHalf + 2, -2], [2, sigHalf - 2], [outC - 12, outC + 12]];
		const markerG = (n: number, id: string) => {
			const m = std(id, { envMap: studio, envMapIntensity: 0.6 });
			const g = new THREE.Group();
			for (let i = 0; i < n; i++) g.add(new THREE.Mesh(unitBox, m));
			return g;
		};
		const rfIn = body('rf_input', 'rf_input', markerG(PADS.length, 'rf_input'));
		const rfTerm = body('rf_termination', 'rf_termination', markerG(LOADS.length, 'rf_termination'));
		const MK = 24; // marker length along z

		// T segments: instanced caps and stems in 4 rows (both edges of both gaps), period tP along the electrodes
		const NSEG = Math.floor((EL - tc) / tP + 1e-6) + 1;
		const trailMat = goldMat();
		const caps = new THREE.InstancedMesh(unitBox, trailMat, 4 * NSEG);
		const stems = new THREE.InstancedMesh(unitBox, trailMat, 4 * NSEG);
		caps.frustumCulled = stems.frustumCulled = false;
		const trailG = new THREE.Group();
		trailG.add(caps, stems);
		const trail = body('trail', 't_rail', trailG);
		/** z start of cap k (slits c midway between caps; the first cap starts c / 2 after the electrode start) */
		const capZ = (k: number) => -EL / 2 + tc / 2 + tP * k;

		// cladding: flat-topped translucent layer as every source schematic draws it (Fig. 1d inset, Extended Data Fig. 5a):
		// from the slab to 0.8 um (stated thickness) above the electrode tops; top height and profile assumed
		const cladMat = std('cladding', { roughness: 0.1, clearcoat: 0.8, clearcoatRoughness: 0.1, envMap: studio, envMapIntensity: 0.6, depthWrite: false });
		cladMat.transparent = true;
		const cladMesh = new THREE.Mesh(unitBox, cladMat);
		const cladG = new THREE.Group();
		cladG.add(cladMesh);
		cladG.traverse((n) => ((n as T.Mesh).renderOrder = 20));
		const clad = body('clad', 'cladding', cladG);
		for (const x of clad.mats) x.base = 1; // opacity set per frame
		// the LN film bodies are drawn solid (look opacity 0.9-0.95 would let the light oxide show through, depending on
		// the draw order); fades still go through setOpacity. Translucent layers get a fixed order from the bottom up.
		for (const b of [slab, etch, ridges, split, comb])
			for (const x of b.mats) {
				x.base = 1;
				x.trans = false;
				x.m.transparent = false;
				x.m.opacity = 1;
			}
		const order: [Body, number][] = [[si, 1], [boxL, 2], [slab, 3], [etch, 4], [ridges, 4], [split, 4], [comb, 4], [sig, 5], [gndL, 5], [gndR, 5], [trail, 5], [rfIn, 6], [rfTerm, 6]];
		for (const [b, r] of order) b.obj.traverse((n) => ((n as T.Mesh).renderOrder = r));
		const cladBase = num(look('cladding').opacity, 0.18);

		// ---------------------------------------------------------------------------- light (ribbons), microwave, mode
		type Rib = { m: T.ShaderMaterial; mesh: T.Mesh; part: string };
		const ribbons: Rib[] = [];
		const RIB_Y = ridY1 + 0.02;
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
		const ribbon = (path: P2[], part: string): Rib => {
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
						uPk: { value: -1e6 },
						uPkI: { value: 0 },
						uPkW: { value: 12 },
						uModA: { value: 0 },
						uModK: { value: 0 },
						uModZ: { value: 0 },
						uZa: { value: -1e6 },
						uZb: { value: 1e6 }
					},
					vertexShader: RIB_VS,
					fragmentShader: RIB_FS,
					transparent: true,
					depthWrite: false,
					side: THREE.DoubleSide,
					blending: THREE.AdditiveBlending,
					toneMapped: false
				})
			);
			const mesh = new THREE.Mesh(ribbonGeo(path), m);
			mesh.renderOrder = 12;
			mesh.frustumCulled = false;
			lightGroup.add(mesh);
			const r: Rib = { m, mesh, part };
			ribbons.push(r);
			return r;
		};
		const ribIn = ribbon([[0, Z0 - BEAM], [0, Z0]], 'light_in');
		const ribStem = ribbon(pStem, 'y_splitter');
		ribbon(pSplitU, 'y_splitter');
		ribbon(pSplitD, 'y_splitter');
		ribbon(pArmU, 'ln_ridge');
		ribbon(pArmD, 'ln_ridge');
		ribbon(pCombU, 'y_combiner');
		ribbon(pCombD, 'y_combiner');
		const ribOutStem = ribbon(pOut, 'y_combiner');
		const ribOut = ribbon([[0, Z1], [0, Z1 + BEAM]], 'light_out');

		// pick proxies for the thin waveguides and beams in the wide shots (invisible, 9 um wide)
		const proxyMat = keep(new THREE.MeshBasicMaterial({ visible: false, side: THREE.DoubleSide }));
		const proxies: T.Mesh[] = [];
		const proxy = (path: P2[], part: string) => {
			const g = ribbonGeo(path, ridY1);
			const pos = g.getAttribute('position');
			const nrm = g.getAttribute('aN');
			const sd = g.getAttribute('aSide');
			for (let i = 0; i < pos.count; i++) pos.setXYZ(i, pos.getX(i) + nrm.getX(i) * sd.getX(i) * 4.5, pos.getY(i), pos.getZ(i) + nrm.getZ(i) * sd.getX(i) * 4.5);
			g.computeBoundingSphere();
			const m = new THREE.Mesh(g, proxyMat);
			m.userData.part = part;
			lightGroup.add(m);
			proxies.push(m);
		};
		for (const pth of [pArmU, pArmD]) proxy(pth, 'ln_ridge');
		for (const pth of [pStem, pSplitU, pSplitD]) proxy(pth, 'y_splitter');
		for (const pth of [pCombU, pCombD, pOut]) proxy(pth, 'y_combiner');
		proxy([[0, Z0 - BEAM], [0, Z0]], 'light_in');
		proxy([[0, Z1], [0, Z1 + BEAM]], 'light_out');

		// microwave on the three strips: the centre strip (S) and the two outer strips (S-bar) in antiphase
		const fieldCol = look('microwave_field').color || '#f7962c';
		const negCol = '#5cc2ff';
		const waveGeo = G(new THREE.PlaneGeometry(1, 1).rotateX(-Math.PI / 2).translate(0.5, 0, 0.5));
		const waveGroup = new THREE.Group();
		root.add(waveGroup);
		// strip x range, sign, gap-facing edges
		const STRIPS: [number, number, number, number, number][] = [
			[-gIn - gW, -gIn, -1, -gIn, -gIn],
			[-sigHalf, sigHalf, 1, -sigHalf, sigHalf],
			[gIn, gIn + gW, -1, gIn, gIn]
		];
		const waves = STRIPS.map(([xa, xb, sg, e0, e1]) => {
			const m = keep(
				new THREE.ShaderMaterial({
					uniforms: {
						uColor: { value: new THREE.Color(fieldCol) },
						uColorN: { value: new THREE.Color(negCol) },
						uA: { value: 0 },
						uU: { value: 0 },
						uWv: { value: 0 },
						uKw: { value: 0 },
						uZw: { value: 0 },
						uLight: { value: 0 },
						uMap: { value: new THREE.Vector4(0, 1, 0, 1) },
						uSq: { value: 0 },
						uE0: { value: e0 },
						uE1: { value: e1 },
						uSign: { value: sg }
					},
					vertexShader: WAVE_VS,
					fragmentShader: WAVE_FS,
					transparent: true,
					depthWrite: false,
					blending: THREE.AdditiveBlending,
					toneMapped: false
				})
			);
			const mesh = new THREE.Mesh(waveGeo, m);
			mesh.renderOrder = 13;
			waveGroup.add(mesh);
			return { m, mesh, xa, xb };
		});

		// field arrows across both gaps (instanced; illustrative): shaft + head along +x, scaled by E(z) and sign
		const NA = Math.floor(LINE_L / ARROW_DZ) + 2;
		const arrowMat = keep(new THREE.MeshBasicMaterial({ color: fieldCol, transparent: true, depthWrite: false, toneMapped: false }));
		const gapW = tg; // arrows span the gap between facing caps
		const shaftL = gapW * 0.62;
		const headL = gapW * 0.2;
		const shaftGeo = G(new THREE.CylinderGeometry(1, 1, 1, 10).rotateZ(-Math.PI / 2).translate(0.5, 0, 0));
		const headGeo = G(new THREE.ConeGeometry(1, 1, 14).rotateZ(-Math.PI / 2).translate(0.5, 0, 0));
		const shafts = new THREE.InstancedMesh(shaftGeo, arrowMat, 2 * NA);
		const heads = new THREE.InstancedMesh(headGeo, arrowMat, 2 * NA);
		shafts.renderOrder = heads.renderOrder = 14;
		shafts.frustumCulled = heads.frustumCulled = false;
		shafts.userData.part = heads.userData.part = 'microwave_field';
		const arrowGroup = new THREE.Group();
		arrowGroup.add(shafts, heads);
		root.add(arrowGroup);
		const ARROW_Y = (ridY1 + elY1) / 2 + 0.1;

		// optical mode on the block face: soft spot centred under each ridge (extent as drawn in Extended Data Fig. 5d)
		const modeExt = pair(geo('optical_mode').extent_um, [1.06, 0.55]);
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
		const spotMat = keep(new THREE.MeshBasicMaterial({ map: spotTex, color: '#ff5a40', transparent: true, depthWrite: false, toneMapped: false, blending: THREE.AdditiveBlending, opacity: 0 }));
		const spotGeo = G(new THREE.PlaneGeometry(modeExt[0] * 1.5, modeExt[1] * 1.7).rotateY(Math.PI));
		const spots = [-RX, RX].map((x) => {
			const s = new THREE.Mesh(spotGeo, spotMat);
			s.position.set(x, slabY1 + 0.02, 0);
			s.renderOrder = 15;
			s.userData.part = 'optical_mode';
			return s;
		});
		const spotGroup = new THREE.Group();
		spotGroup.add(...spots);
		root.add(spotGroup);

		// output facet glow: brightness of the modulated light leaving the chip
		const flareMat = keep(new THREE.SpriteMaterial({ map: spotTex, color: '#ff6a50', transparent: true, depthWrite: false, depthTest: false, toneMapped: false, blending: THREE.AdditiveBlending, opacity: 0 }));
		const flare = new THREE.Sprite(flareMat);
		flare.renderOrder = 16;
		flare.userData.part = 'light_out';
		lightGroup.add(flare);

		// ---------------------------------------------------------------------------- lights
		const hemi = new THREE.HemisphereLight('#ffffff', '#3a3c44', 0.9);
		const key = new THREE.DirectionalLight('#fff3e6', 2.0);
		key.position.set(-50, 140, -110);
		const rim = new THREE.DirectionalLight('#bcd2ff', 1.0);
		rim.position.set(130, 60, 120);
		const fill = new THREE.DirectionalLight('#ffffff', 0.7);
		fill.position.set(90, 20, -140);
		root.add(hemi, key, rim, fill);

		// ---------------------------------------------------------------------------- theme
		const accent = new THREE.Color();
		const black = new THREE.Color(0, 0, 0);
		function applyTheme() {
			const light = theme === 'light';
			accent.set(light ? '#2a78d6' : '#3987e5');
			for (const r of ribbons) {
				r.m.uniforms.uLight.value = light ? 1 : 0;
				r.m.blending = light ? THREE.NormalBlending : THREE.AdditiveBlending;
				r.m.uniforms.uK.value = light ? 0.9 : 1;
				r.m.needsUpdate = true;
			}
			for (const wv of waves) {
				wv.m.uniforms.uLight.value = light ? 1 : 0;
				wv.m.blending = light ? THREE.NormalBlending : THREE.AdditiveBlending;
				wv.m.uniforms.uColor.value.set(light ? '#d9730f' : fieldCol);
				wv.m.uniforms.uColorN.value.set(light ? '#1f6fb8' : negCol);
				wv.m.needsUpdate = true;
			}
			spotMat.blending = light ? THREE.NormalBlending : THREE.AdditiveBlending;
			flareMat.blending = light ? THREE.NormalBlending : THREE.AdditiveBlending;
			flareMat.color.set(light ? '#e0301c' : '#ff6a50');
			for (const m of [arrowMat, spotMat, flareMat]) m.needsUpdate = true;
			hemi.intensity = light ? 1.05 : 0.9;
		}
		applyTheme();

		// ---------------------------------------------------------------------------- shots: window + camera
		interface Shot {
			az: number;
			el: number;
			win: Win; // drawn window
			box: number[]; // camera framing box x0 x1 y0 y1 z0 z1
			fw: number;
			fh: number;
			sx: number;
			sy: number;
		}
		const portrait = () => w / h < 0.9;
		const P = (s: Shot): Shot => (portrait() ? { ...s, fw: Math.min(0.98, s.fw * 1.08), fh: s.fh * 0.6, sy: s.sy + 0.02 } : s);
		const plotShift = (s: Shot): Shot =>
			portrait() ? { ...s, fw: 0.9, fh: 0.2, sx: 0, sy: 0.22 } : { ...s, fw: Math.min(s.fw, 0.44), fh: Math.min(s.fh, 0.62), sx: -0.25, sy: -0.06 };
		const gapX = RX; // the gap framed in the macro shots (x > 0 sits on the left of the screen from the input side)
		let kEff = 0;
		const explodeGap = () => 70 * ease(clamp01(kEff));
		const FULL: Win = [-CHIP_X, CHIP_X, siY0, Z0, Z1];
		const W = {
			stack: [gapX - 8, gapX + 8, siY0, ZC, ZC + 11] as Win,
			ridgeM: [gapX - 3, gapX + 3, -1.5, ZC, ZC + 4.5] as Win,
			ridgeW: [-RX - 6, RX + 6, -2.4, ZC, ZC + 26] as Win,
			elec: [-gIn - 9, gIn + 9, -2.6, ZC, ZC + 28] as Win,
			gap: [gapX - 12, gapX + 12, -1.6, ZC, ZC + 60] as Win,
			tclose: [gapX - 14, gapX + 14, -1.6, ZC, ZC + 110] as Win,
			line: [-gIn - 8, gIn + 8, -2.6, ZC, ZC + LINE_L] as Win,
			face: [-gIn - 8, gIn + 8, -2.6, ZC, ZC + 46] as Win
		};
		/** framing box of a window: its extent with the drawn top */
		const boxOf = (v: Win, top = topY + 0.2, zMax = Infinity): number[] => [v[0], v[1], v[2], top, v[3], Math.min(v[4], v[3] + zMax)];
		const chipBox = (tight = false): number[] => [-CHIP_X, CHIP_X, siY0, elY1 + 3 + 4 * explodeGap(), Z0 - (tight ? 20 : BEAM * 0.4), Z1 + (tight ? 50 : BEAM * 0.4)];
		const dr = (id: string, p: number, a: number, b: number) => lerp(a, b, cq(id, p));
		const sh = {
			intro: (p: number): Shot => P({ az: dr('intro', p, -120, -108), el: 36, win: FULL, box: chipBox(), fw: 0.92, fh: 0.58, sx: 0, sy: -0.1 }),
			stack: (p: number): Shot =>
				P({ az: dr('stack', p, -160, -152), el: 17, win: W.stack, box: boxOf(W.stack, ridY1 + 0.3), fw: 0.74, fh: 0.64, sx: 0.04, sy: -0.12 }),
			ridgeM: (p: number): Shot => P({ az: dr('ridge', p, -156, -148), el: 21, win: W.ridgeM, box: boxOf(W.ridgeM, ridY1 + 0.3), fw: 0.66, fh: 0.5, sx: 0.04, sy: -0.12 }),
			ridgeW: (): Shot => P({ az: -156, el: 19, win: W.ridgeW, box: boxOf(W.ridgeW, ridY1 + 0.3), fw: 0.78, fh: 0.56, sx: 0, sy: -0.12 }),
			elec: (p: number): Shot => P({ az: dr('electrodes', p, -158, -152), el: 20, win: W.elec, box: boxOf(W.elec), fw: 0.8, fh: 0.56, sx: 0, sy: -0.12 }),
			gap: (p: number): Shot =>
				P({ az: dr('cladding', p, -152, -146), el: 24, win: W.gap, box: boxOf(W.gap, topY + 0.2, 14), fw: 0.7, fh: 0.54, sx: 0.04, sy: -0.12 }),
			tclose: (p: number): Shot =>
				P({ az: dr('electrodes', p, -104, -98), el: 52, win: W.tclose, box: boxOf(W.tclose), fw: 0.88, fh: 0.62, sx: 0, sy: -0.1 }),
			chip: (p: number): Shot => P({ az: dr('mzi', p, -110, -104), el: 36, win: FULL, box: chipBox(), fw: 0.92, fh: 0.58, sx: 0, sy: -0.1 }),
			endOn: (p: number): Shot =>
				P({ az: dr('fields', p, -164, -160), el: 24, win: W.face, box: boxOf(W.face, topY + 0.2, 16), fw: 0.84, fh: 0.5, sx: 0, sy: -0.16 }),
			line: (p: number): Shot => P({ az: dr('fields', p, -170, -166), el: 14, win: W.line, box: boxOf(W.line, topY + 0.2, 60), fw: 0.9, fh: 0.6, sx: 0, sy: -0.15 }),
			vpi: (p: number): Shot => plotShift({ az: dr('vpi', p, -106, -102), el: 40, win: FULL, box: chipBox(true), fw: 0.44, fh: 0.62, sx: -0.25, sy: -0.06 }),
			bw: (p: number): Shot => plotShift({ az: dr('bandwidth', p, -102, -98), el: 44, win: FULL, box: chipBox(true), fw: 0.44, fh: 0.62, sx: -0.25, sy: -0.06 }),
			fom: (p: number): Shot => plotShift({ az: dr('fom', p, -106, -114), el: 36, win: FULL, box: chipBox(true), fw: 0.44, fh: 0.62, sx: -0.25, sy: -0.06 })
		};
		type Key = [number, (p: number) => Shot];
		const keys: Key[] = [
			[0, sh.intro],
			[at('intro', 1), sh.intro],
			[at('stack', 0.42), sh.stack],
			[at('stack', 1), sh.stack],
			[at('ridge', 0.12), sh.ridgeM],
			[at('ridge', 0.68), sh.ridgeM],
			[at('ridge', 0.96), sh.ridgeW],
			[at('electrodes', 0.12), sh.elec],
			[at('electrodes', 0.46), sh.elec],
			[at('electrodes', 0.64), sh.tclose],
			[at('electrodes', 1), sh.tclose],
			[at('cladding', 0.3), sh.gap],
			[at('cladding', 1), sh.gap],
			[at('mzi', 0.55), sh.chip],
			[at('mzi', 1), sh.chip],
			[at('fields', 0.14), sh.endOn],
			[at('fields', 0.46), sh.endOn],
			[at('fields', 0.66), sh.line],
			[at('fields', 0.86), sh.line],
			[CH.vpi[0], sh.vpi],
			[at('vpi', 1), sh.vpi],
			[at('bandwidth', 0.1), sh.bw],
			[at('bandwidth', 1), sh.bw],
			[at('fom', 0.1), sh.fom],
			[1, sh.fom]
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
		let tgt: V3 = [0, 0, 0];
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
			// the subject sits off centre (sx, sy) through a view offset, so an orbit pivots on the subject and keeps it there
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
		function setOpacity(b: Body, o: number) {
			const on = lit(b.part);
			const eff = on && o > 0.02 && o < 0.3 ? 0.3 : o;
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
		const MZM = new Set((geo('mzm').members as string[] | undefined) ?? ['ln_ridge', 'y_splitter', 'y_combiner', 'signal_line', 'ground_lines']);
		const lit = (part: string) => hi.includes(part) || (hi.includes('mzm') && MZM.has(part));
		function tint(b: Body) {
			const on = lit(b.part);
			for (const x of b.mats) {
				if (x.m === etchMat) continue;
				x.m.emissive.copy(on ? accent : black);
				x.m.emissiveIntensity = on ? (b.part === 'cladding' ? 0.6 : 0.3) : 1;
			}
		}

		/** field along the line: E(z) = U + Wv cos(Kw (z - Zw)); arrow amplitude A, strip glow Ov */
		interface Field {
			A: number;
			Ov: number;
			U: number;
			Wv: number;
			Kw: number;
			Zw: number;
			/** shaping of the drive: 0 = sinusoid, > 0 = rounded square wave tanh(Sq E) / tanh(Sq) */
			Sq: number;
		}
		interface Light {
			on: number;
			front: number; // light front z
			out: number; // output brightness (fraction of the maximum)
			modA: number;
			modK: number;
			modZ: number;
			pk: number; // tracer z
			pkI: number;
		}
		/** point of series 0 of a plot under the plot pen at chapter progress q: the runtime assembles a plot over the first
		 *  90 % of its chapter (rr), draws the axes first and reveals the series staggered (plot.ts); the pen holds at the last
		 *  point once the series is drawn */
		function pen(plotId: string, q: number): [number, number] | null {
			const pl = spec.plots?.find((x) => x.id === plotId);
			const pts = (pl?.series?.[0]?.points ?? []) as [number, number][];
			const N = pts.length;
			if (!N) return null;
			const kk = staggerK(seg(q, 0, 0.9), AXES_END, 1, 0, pl?.series?.length ?? 1);
			const t = Math.max(0, Math.min(N - 1, kk * N - 1));
			const i = Math.floor(t);
			const j = Math.min(N - 1, i + 1);
			return [lerp(pts[i][0], pts[j][0], t - i), lerp(pts[i][1], pts[j][1], t - i)];
		}
		/** vpi chapter drive (V): the voltage under the pen of the Fig. 1c curve */
		const vpiV = (q: number) => pen('transfer', q)?.[0] ?? vMax * seg(q, 0, 0.9);
		/** bandwidth chapter drive: frequency (GHz) and S21 (dB) under the pen of the 20 mm trace (Fig. 2a), held at its end */
		const bwPen = (q: number): [number, number] => pen('eo_20mm', q) ?? [1, 0];
		/** output modulation depth at S21 (dB): electro-optic S21 is a power ratio at the photodiode, so amplitude 10^(S21/20) */
		const depth = (s21: number) => 0.7 * Math.pow(10, s21 / 20);
		/** drawn microwave wavelength at f GHz: c / (n f) in mm, times the drawn units per mm */
		const lamD = (f: number) => (300 / (NG * f)) * MM;
		function fieldAt(p: number): Field {
			const f: Field = { A: 0, Ov: 0, U: 0, Wv: 0, Kw: 0, Zw: 0, Sq: 0 };
			if (inCh('fields', p)) {
				const q = cq('fields', p);
				// true-size close-up: the 4 mm wavelength (in um, the close-up units) is far longer than the view, so the field
				// is nearly uniform over it and flips in time with p (three drive cycles); both gaps opposite, flipping together.
				// It fades before the camera pulls back to the whole chip (no true-scale wave on the shortened plan).
				// The drive swings like a data signal (rounded square wave: most of the time at full swing, quick sign changes).
				const lamT = (300 / (NG * F_CLOSE)) * 1000;
				const ph = TAU * 2 * seg(q, 0.14, 0.94);
				f.A = easeOut(seg(q, 0.08, 0.22)) * (1 - seg(q, 0.86, 0.96));
				f.Ov = f.A * 0.5;
				// E(z) = U + W cos(K (z - Zw)): the near-uniform true-scale wave, shaped by the square-wave drive at the face
				f.U = 0;
				f.Wv = 1;
				f.Kw = TAU / lamT;
				f.Zw = ZC + (ph / TAU) * lamT;
				f.Sq = 2.5;
			} else if (inCh('vpi', p)) {
				f.Ov = 0.55 * (vpiV(cq('vpi', p)) / vMax);
				f.U = 1;
			} else if (inCh('bandwidth', p)) {
				const q = cq('bandwidth', p);
				f.Ov = 0.5 * easeOut(seg(q, 0, 0.08));
				f.Wv = 1;
				f.Kw = TAU / lamD(Math.max(1, bwPen(q)[0]));
				f.Zw = -EL / 2 + EL * seg(q, 0.02, 0.98);
			} else if (p >= CH.fom[0]) {
				const q = cq('fom', p);
				// the last state of the bandwidth chapter (end of the measured 20 mm trace), drifting slowly
				f.Ov = 0.36;
				f.Wv = 1;
				f.Kw = TAU / lamD(Math.max(1, bwPen(1)[0]));
				f.Zw = -EL / 2 + EL * 0.5 * q;
			}
			return f;
		}
		const T0 = transfer(0);
		function lightAt(p: number): Light {
			const L: Light = { on: 0, front: 1e6, out: T0, modA: 0, modK: 0, modZ: 0, pk: -1e6, pkI: 0 };
			if (p < CH.stack[0]) L.on = easeOut(seg(cq('intro', p), 0.05, 0.5));
			else if (p < CH.mzi[0]) L.on = 1 - seg(cq('stack', p), 0, 0.14);
			else if (p < CH.fields[0]) {
				const q = cq('mzi', p);
				L.on = seg(q, 0.3, 0.36);
				L.front = lerp(Z0 - BEAM, Z1 + BEAM + 40, seg(q, 0.32, 0.86));
			} else if (p < CH.vpi[0]) {
				// steady light; the co-moving tracer belongs to the whole-chip travelling wave (bandwidth chapter)
				L.on = 1;
				L.out = 0.5;
			} else if (p < CH.bandwidth[0]) {
				L.on = 1;
				L.out = transfer(vpiV(cq('vpi', p)));
			} else {
				const f = fieldAt(p);
				const bw = p < CH.fom[0];
				const q = bw ? cq('bandwidth', p) : cq('fom', p);
				L.on = 1;
				L.out = 0.5;
				L.modA = depth(bwPen(bw ? q : 1)[1]) * (bw ? seg(q, 0, 0.08) : 1);
				L.modK = f.Kw;
				L.modZ = f.Zw;
				L.pk = f.Zw;
				L.pkI = bw ? 1.2 * seg(q, 0.02, 0.1) * (1 - seg(q, 0.94, 0.99)) : 0;
			}
			return L;
		}

		// ---------------------------------------------------------------------------- frame
		const dummy = new THREE.Object3D();
		const vP = new THREE.Vector3();
		const plasma = new THREE.Color('#8a6cff');
		let win: Win = FULL;
		/** longest output beam (from the output facet) whose end stays left of pane x `xmax` */
		function beamClip(xmax: number): number {
			const sx = (len: number) => {
				vP.set(0, RIB_Y + 2 * explodeGap(), Z1 + len).applyMatrix4(root.matrixWorld).project(camera);
				return ((vP.x + 1) / 2) * w;
			};
			if (sx(BEAM) <= xmax) return BEAM;
			if (sx(0) > xmax) return 0;
			let lo = 0;
			let hi2 = BEAM;
			for (let i = 0; i < 14; i++) {
				const m = (lo + hi2) / 2;
				if (sx(m) <= xmax) lo = m;
				else hi2 = m;
			}
			return lo;
		}
		/** coverage in [0, 1] of the z range [a, b] by the window */
		const zCov = (a: number, b: number) => clamp01((Math.min(win[4], b) - Math.max(win[3], a)) / (b - a));
		/** 1 when [a, b] in x lies inside the window */
		const xIn = (a: number, b: number) => (a >= win[0] - 1e-6 && b <= win[1] + 1e-6 ? 1 : 0);

		function frame(p: number) {
			lastP = p;
			kEff = p >= CH.vpi[0] ? k : 0;
			const g = explodeGap();
			// intro float: the chip settles from a tilt (pure in p)
			const fl = 1 - ease(seg(cq('intro', p), 0, 0.9));
			root.rotation.set(-0.06 * fl, 0.16 * fl, 0.03 * fl);
			root.updateMatrixWorld(true);
			const s = shotAt(p);
			win = s.win;
			placeCamera(s);
			const [x0, x1, y0w, zA, zB] = win;

			const qS = cq('stack', p);
			const qR = cq('ridge', p);
			const qE = cq('electrodes', p);
			const qC = cq('cladding', p);
			const qM = cq('mzi', p);
			const qF = cq('fields', p);

			// build: in the stack chapter the finished layers leave (fade, lift), then the stack is rebuilt
			const inBuild = p >= CH.stack[0] && p < CH.mzi[0];
			const leaving = inBuild && p < CH.ridge[0] && qS < 0.34;
			const gone = leaving ? ease(seg(qS, 0.04, 0.3)) : 0;
			const leaveO = 1 - gone;
			const leaveY = 5 * gone;
			const boxIn = inBuild ? (leaving ? leaveO : ease(seg(qS, 0.36, 0.62))) : 1;
			const filmIn = inBuild ? (leaving ? leaveO : ease(seg(qS, 0.58, 0.86))) : 1;
			const boxDy = leaving ? leaveY * 0.6 : 6 * (1 - boxIn);
			const filmDy = leaving ? leaveY * 0.8 : 3 * (1 - filmIn);
			const etchS = inBuild && !leaving ? 1 - (p >= CH.ridge[0] ? ease(seg(qR, 0.14, 0.62)) : 0) : 0;
			const elT = (a: number, b: number) => (p >= CH.electrodes[0] ? easeOut(seg(qE, a, b)) : 0);
			// one gold lift-off (Methods): the three strips land together
			const sI = inBuild ? (leaving ? leaveO : elT(0.1, 0.44)) : 1;
			// T segments grow from the strip edges once the strips have landed (stem first, then the cap along the line)
			const gT = inBuild && !leaving ? (p >= CH.electrodes[0] ? seg(qE, 0.6, 0.94) : 0) : 1;
			const gR = sI;
			const gL = sI;
			const elDy = (t: number) => (leaving ? leaveY : 8 * (1 - t));

			// substrate, oxide, slab (to the window)
			fit(si.obj, x0, x1, Math.max(y0w, siY0), boxY0, zA, zB);
			setOpacity(si, si.obj.visible ? 1 : 0);
			if (fit(boxL.obj, x0, x1, Math.max(y0w, boxY0), boxY1, zA, zB)) boxL.obj.position.y += g + boxDy;
			setOpacity(boxL, boxL.obj.visible ? boxIn : 0);
			fit(slab.obj, x0, x1, slabY0, slabY1, zA, zB);
			slab.obj.position.y += 2 * g + filmDy;
			setOpacity(slab, filmIn);
			// unetched upper film (while building)
			{
				const iv: [number, number][] = [
					[x0, -RX - ridTop / 2],
					[-RX + ridTop / 2, RX - ridTop / 2],
					[RX + ridTop / 2, x1]
				];
				etchMeshes.forEach((m, i) => {
					fit(m, Math.max(x0, iv[i][0]), Math.min(x1, iv[i][1]), ridY0, ridY0 + Math.max(1e-3, etchS) * (ridY1 - ridY0), zA, zB);
					m.position.y += filmDy;
				});
				setOpacity(etch, inBuild && etchS > 0.002 ? filmIn : 0);
				const etching = inCh('ridge', p) ? Math.sin(Math.PI * seg(qR, 0.12, 0.64)) : 0;
				etchMat.emissive.copy(plasma);
				etchMat.emissiveIntensity = 0.22 * etching;
			}
			// ridges (straight arms inside the window) and routing (only when the window holds it)
			{
				const za = Math.max(zA, -EL / 2);
				const zb = Math.min(zB, EL / 2);
				armMeshes.forEach((m, i) => {
					const cx = i ? RX : -RX;
					m.visible = !!xIn(cx - ridBot / 2, cx + ridBot / 2) && zb > za;
					m.position.set(0, 0, za);
					m.scale.set(1, 1, Math.max(1e-4, zb - za));
				});
				ridges.obj.position.y = 2 * g + filmDy;
				setOpacity(ridges, filmIn);
				const full = xIn(-RX - 1, RX + 1);
				split.obj.position.y = 2 * g;
				setOpacity(split, full * seg(zCov(Z0, -EL / 2), 0.97, 1) * filmIn);
				comb.obj.position.y = 2 * g + filmDy;
				setOpacity(comb, full * seg(zCov(EL / 2, Z1), 0.97, 1) * filmIn);
			}
			// electrodes (clipped to the window)
			{
				const za = Math.max(zA, -EL / 2);
				const zb = Math.min(zB, EL / 2);
				const strip = (b: Body, xa: number, xb: number, t: number) => {
					const ok = fit(b.obj, Math.max(x0, xa), Math.min(x1, xb), elY0, elY1, za, zb);
					b.obj.position.y += 3 * g + elDy(t);
					setOpacity(b, ok ? t : 0);
				};
				strip(sig, -sigHalf, sigHalf, sI);
				strip(gndL, -gIn - gW, -gIn, gL);
				strip(gndR, gIn, gIn + gW, gR);
				// T segments, clipped to the window
				{
					let n = 0;
					const put = (im: T.InstancedMesh, xa: number, xb: number, za2: number, zb2: number) => {
						const a0 = Math.max(x0, xa);
						const a1 = Math.min(x1, xb);
						const b0 = Math.max(zA, za2);
						const b1 = Math.min(zB, zb2);
						if (a1 - a0 < 1e-4 || b1 - b0 < 1e-4) return false;
						dummy.position.set(a0, elY0, b0);
						dummy.rotation.set(0, 0, 0);
						dummy.scale.set(a1 - a0, elY1 - elY0, b1 - b0);
						dummy.updateMatrix();
						im.setMatrixAt(n, dummy.matrix);
						return true;
					};
					let nc = 0;
					let ns = 0;
					const hL = thh * Math.min(1, gT / 0.6);
					const cL = tr * seg(gT, 0.6, 1);
					if (gT > 0.002)
						for (let k = 0; k < NSEG; k++) {
							const z0c = capZ(k);
							const zm = z0c + tr / 2;
							for (const side of [-1, 1])
								for (const inner of [true, false]) {
									// body edge, direction toward the gap centre
									const edge = inner ? sigHalf : gIn;
									const d = inner ? 1 : -1;
									const s0 = edge;
									const s1 = edge + d * hL;
									const c0 = edge + d * thh;
									const c1 = c0 + d * ts;
									const sx = (a: number, b: number): [number, number] => {
										const u = side * a;
										const v = side * b;
										return [Math.min(u, v), Math.max(u, v)];
									};
									const [sa, sb] = sx(s0, s1);
									n = ns;
									if (put(stems, sa, sb, zm - tt / 2, zm + tt / 2)) ns++;
									if (cL > 0.01 && gT >= 0.6) {
										const [ca, cb] = sx(c0, c1);
										n = nc;
										if (put(caps, ca, cb, zm - cL / 2, zm + cL / 2)) nc++;
									}
								}
						}
					caps.count = nc;
					stems.count = ns;
					caps.instanceMatrix.needsUpdate = true;
					stems.instanceMatrix.needsUpdate = true;
					trail.obj.position.y = 3 * g + elDy(sI);
					setOpacity(trail, nc + ns > 0 ? sI : 0);
				}
				// markers on the strip ends: driver pads (S-bar S S S-bar) and one load per conductor
				const mo = inBuild ? 0 : inCh('mzi', p) ? ease(seg(qM, 0.5, 0.7)) : 1;
				const ms = (b: Body, xs: [number, number][], za2: number, zb2: number) => {
					const c = seg(zCov(za2, zb2), 0.98, 1) * xIn(-sigHalf, sigHalf);
					b.obj.children.forEach((m, i) => fit(m, xs[i][0], xs[i][1], elY1, elY1 + 2.4, za2, zb2));
					b.obj.position.y = 3 * g;
					setOpacity(b, c * mo);
				};
				ms(rfIn, PADS, -EL / 2, -EL / 2 + MK);
				ms(rfTerm, LOADS, EL / 2 - MK, EL / 2);
			}
			// cladding: settles in its chapter at full presence, then turns faint
			{
				const rest = cladBase * 0.6;
				let o = rest;
				let y = 0;
				if (leaving) {
					o = rest * leaveO;
					y = leaveY * 1.2;
				} else if (inBuild) {
					const clIn = p >= CH.cladding[0] ? ease(seg(qC, 0.06, 0.5)) : 0;
					const peak = Math.min(0.5, cladBase * 2.6);
					const fade = p >= CH.cladding[0] ? ease(seg(qC, 0.7, 1)) : 0;
					o = clIn * lerp(peak, rest, fade);
					y = 4 * (1 - clIn);
				}
				if (inCh('fields', p)) o = rest * 0.7;
				// faces pushed out a hair so the translucent coat never shares a plane with the faces of the block
				const e = 0.002 * Math.max(x1 - x0, zB - zA, 1);
				fit(cladMesh, x0 - e, x1 + e, slabY1 + e * 0.1, topY, zA - e, zB + e);
				clad.obj.position.y = 4 * g + y;
				setOpacity(clad, lit('cladding') ? Math.max(o, 0.3) : o);
			}
			for (const b of bodies.values()) tint(b);

			// ---- light
			const L = lightAt(p);
			const F = fieldAt(p);
			const wpp = (2 * camD * Math.tan((camera.fov * DEG) / 2)) / h; // world units per pixel at the target
			const rw = Math.min(24, Math.max(0.55, (wpp > 0.3 ? 7.5 : 4.4) * wpp));
			const wide = wpp > 0.3;
			lightGroup.position.y = 2 * g;
			const light = theme === 'light';
			const red = light ? '#e0281a' : '#ff3a28';
			const plotCh = p >= CH.vpi[0];
			const paneClip = beamClip(w - 24);
			const outLen = w >= 700 && plotCh ? Math.min(paneClip, beamClip(0.5 * w - 28)) : paneClip;
			const fullX = xIn(-RX - 1, RX + 1);
			for (const r of ribbons) {
				const u = r.m.uniforms;
				u.uW.value = rw * (r === ribIn || r === ribOut ? 1.5 : 1);
				u.uFront.value = L.front;
				u.uWz0.value = r === ribIn ? (zA <= Z0 + 1 ? -1e6 : 1e6) : zA;
				u.uWz1.value = r === ribOut ? (zB >= Z1 - 1 ? 1e6 : -1e6) : zB;
				u.uPk.value = L.pk;
				u.uPkW.value = Math.max(6, 10 * wpp);
				u.uPkI.value = r.part === 'ln_ridge' ? L.pkI : 0;
				const outStem = r === ribOutStem || r === ribOut;
				u.uModA.value = outStem ? L.modA : 0;
				u.uModK.value = L.modK;
				u.uModZ.value = L.modZ;
				let I = inCh('fields', p) ? 0.9 : 0.75;
				if (r === ribIn || r === ribStem) I = 1;
				else if (outStem) I = Math.min(1, L.out * 1.05);
				u.uI.value = I * L.on * fullX;
				u.uZa.value = r === ribIn ? Z0 - BEAM : -1e6;
				u.uZb.value = r === ribOut ? Z1 + Math.max(1, outLen) : 1e6;
				const on = lit(r.part);
				u.uColor.value.set(on ? (light ? '#2a78d6' : '#7fb3ff') : red);
				if (on && fullX && u.uI.value < 0.35) u.uI.value = 0.35;
				r.m.depthTest = !wide;
				r.mesh.visible = u.uI.value > 0.002 || u.uPkI.value > 0.002;
			}
			for (const m of proxies) m.visible = wpp > 0.25 && L.on > 0.2 && fullX > 0;
			{
				const full = zB >= Z1 - 1 && fullX > 0;
				const reached = seg(L.front, Z1, Z1 + 40);
				const mod = clamp01(1 + L.modA * Math.cos(L.modK * (Z1 - L.modZ)));
				const fI = full ? L.on * reached * Math.min(1, L.out * 1.05) * mod : 0;
				flare.visible = fI > 0.01 && wide;
				flare.position.set(0, RIB_Y, Z1 + 1);
				flare.scale.setScalar(26 * wpp * (0.6 + 0.4 * Math.min(1, fI)));
				flareMat.opacity = Math.min(1, fI * 1.1);
			}

			// ---- microwave: strip glow and field arrows
			waveGroup.position.y = 3 * g;
			for (const wv of waves) {
				const xa = Math.max(x0, wv.xa);
				const xb = Math.min(x1, wv.xb);
				const za = Math.max(zA, -EL / 2);
				const zb = Math.min(zB, EL / 2);
				const ok = F.Ov > 0.002 && sig.o > 0.5 && xb > xa && zb > za;
				wv.mesh.visible = ok;
				if (ok) {
					wv.mesh.position.set(xa, elY1 + 0.03, za);
					wv.mesh.scale.set(xb - xa, 1, zb - za);
					const wu = wv.m.uniforms;
					wu.uA.value = F.Ov;
					wu.uU.value = F.U;
					wu.uWv.value = F.Wv;
					wu.uKw.value = F.Kw;
					wu.uZw.value = F.Zw;
					wu.uSq.value = F.Sq;
					(wu.uMap.value as T.Vector4).set(xa, xb - xa, za, zb - za);
				}
			}
			arrowGroup.position.y = 2 * g;
			const arrowsOn = F.A > 0.002;
			arrowGroup.visible = arrowsOn;
			if (arrowsOn) {
				const rad = Math.min(0.4, Math.max(0.07, 1.9 * wpp));
				let n = 0;
				for (let i = 0; i < NA; i++) {
					const z = zA + 0.6 + i * ARROW_DZ;
					if (z > Math.min(zB, EL / 2)) break;
					const e0 = F.U + F.Wv * Math.cos(F.Kw * (z - F.Zw));
					const e = F.A * (F.Sq > 0 ? Math.tanh(F.Sq * e0) / Math.tanh(F.Sq) : e0);
					for (const side of [-1, 1]) {
						if (!xIn(Math.min(side * (RX - tg / 2), side * (RX + tg / 2)), Math.max(side * (RX - tg / 2), side * (RX + tg / 2)))) continue;
						// differential drive: S at +V, both S-bar at -V: the field points from S outward in both gaps, -x in the x < 0
						// gap and +x in the x > 0 gap (opposite in the two arms, push-pull)
						const dir = Math.sign(e) * side || side;
						const a = Math.abs(e);
						const L0 = shaftL * a;
						const hs = Math.min(1, a * 1.6);
						const Lh = headL * hs;
						const xs = side * gapMid - (dir * (L0 + Lh)) / 2;
						dummy.position.set(xs, ARROW_Y, z);
						dummy.rotation.set(0, dir < 0 ? Math.PI : 0, 0);
						const th = rad * Math.min(1, a * 2);
						dummy.scale.set(Math.max(1e-4, L0), Math.max(1e-4, th), Math.max(1e-4, th));
						dummy.updateMatrix();
						shafts.setMatrixAt(n, dummy.matrix);
						dummy.position.set(xs + dir * L0, ARROW_Y, z);
						dummy.scale.set(Math.max(1e-4, Lh), Math.max(1e-4, 2.8 * rad * hs), Math.max(1e-4, 2.8 * rad * hs));
						dummy.updateMatrix();
						heads.setMatrixAt(n, dummy.matrix);
						n++;
					}
				}
				shafts.count = heads.count = n;
				shafts.instanceMatrix.needsUpdate = true;
				heads.instanceMatrix.needsUpdate = true;
				arrowMat.color.set(lit('microwave_field') ? (light ? '#2a78d6' : '#7fb3ff') : light ? '#d9730f' : fieldCol);
				arrowMat.opacity = Math.min(1, 0.95 * F.A + 0.05);
			}
			// ---- optical mode spots on the block face
			spotGroup.position.set(0, 2 * g, zA - 0.04);
			const spotO = inCh('fields', p) ? easeOut(seg(qF, 0.08, 0.2)) * (1 - 0.5 * seg(qF, 0.5, 0.7)) : 0;
			spotMat.opacity = (light ? 0.85 : 1) * spotO;
			spotMat.color.set(lit('optical_mode') ? (light ? '#2a78d6' : '#7fb3ff') : light ? '#e0301c' : '#ff5a40');
			spots.forEach((m, i) => (m.visible = !!xIn((i ? RX : -RX) - 1, (i ? RX : -RX) + 1)));
			spotGroup.visible = spotO > 0.002;
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
		const tracer = (p: number): PickInfo => ({
			id: 'light_tracer',
			label: 'Light keeps pace with the microwave',
			detail: [
				'Group indices about 2.2: the 2018 plain line (Methods); the drawn T-rail line is not claimed to match',
				`Drive ${bwPen(cq('bandwidth', p))[0].toFixed(1)} GHz, depth from the 20 mm response (Fig. 2a)`,
				'Wavelength drawn about 20x shortened, like the plan',
				'Illustrative tracer on the continuous light, not a pulse'
			]
		});
		function pick(x: number, y: number): string | PickInfo | null {
			const L = lightAt(lastP);
			if (L.pkI > 0.3 && L.on > 0.5) {
				for (const sx of [-RX, RX]) {
					const s = screen(sx, RIB_Y + 2 * explodeGap(), L.pk);
					if (s && Math.hypot(s[0] - x, s[1] - y) < 14) return tracer(lastP);
				}
			}
			v2.set((x / w) * 2 - 1, 1 - (y / h) * 2);
			raycaster.setFromCamera(v2, camera);
			const cands: T.Object3D[] = [];
			// the faint cladding is picked first only in its chapter; otherwise only when nothing else is hit
			const cladFirst = lastP >= CH.cladding[0] && lastP < CH.mzi[0];
			if (trail.obj.visible) {
				caps.computeBoundingSphere();
				stems.computeBoundingSphere();
			}
			for (const b of bodies.values()) if (b.obj.visible && b.o > 0.2 && (b !== clad || cladFirst)) cands.push(...b.picks.filter((m) => m.visible));
			if (arrowGroup.visible) {
				// instance matrices change every frame: refresh the bounds the raycaster tests first
				shafts.computeBoundingSphere();
				heads.computeBoundingSphere();
				cands.push(shafts, heads);
			}
			if (spotGroup.visible) cands.push(...spots.filter((m) => m.visible));
			for (const m of proxies) if (m.visible) cands.push(m);
			if (flare.visible) cands.push(flare);
			const hit = raycaster.intersectObjects(cands, false)[0];
			if (hit) return (hit.object.userData.part as string | undefined) ?? null;
			if (!cladFirst && clad.obj.visible && clad.o > 0.05) {
				const ch = raycaster.intersectObjects(clad.picks.filter((m) => m.visible), false)[0];
				if (ch) return 'cladding';
			}
			return null;
		}
		const isFull = () => win[3] <= Z0 + 1 && win[4] >= Z1 - 1 && win[0] <= -CHIP_X + 1;
		function anchor(id: string): [number, number] | null {
			let s: [number, number] | null = null;
			const p = lastP;
			if (id === 'ln_slab') {
				if (!inCh('stack', p) || cq('stack', p) < 0.8 || slab.o < 0.6) return null;
				s = screen(win[0] + 0.25 * (win[1] - win[0]), slabY1 + slab.obj.position.y, win[3]);
			} else if (id === 't_rail') {
				if (!inCh('electrodes', p) || cq('electrodes', p) < 0.9) return null;
				// an inner cap a few periods into the close-up
				const k = Math.max(0, Math.ceil((win[3] - capZ(0)) / tP) + 1);
				s = screen(RX - tg / 2 - ts / 2, elY1 + trail.obj.position.y, capZ(k) + tr / 2);
			} else if (id === 'signal_line') {
				if (!inCh('mzi', p) || !isFull()) return null;
				s = screen(0, elY1 + 3 * explodeGap(), -EL * 0.18);
			} else if (id === 'mzm') {
				if (!inCh('vpi', p) || !isFull()) return null;
				s = screen(0, elY1 + 3 * explodeGap(), -EL * 0.3);
			} else return null;
			if (!s) return null;
			if (s[0] < 4 || s[0] > w - 4 || s[1] < 8 || s[1] > h - 12) return null;
			return s;
		}

		return {
			assembledAt: CH.vpi[0],
			// keep the flat chip from turning edge-on
			orbit: { polar: [4, 74] },
			frame,
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
				shafts.dispose();
				heads.dispose();
				caps.dispose();
				stems.dispose();
				for (const d of disposables) d.dispose();
			}
		};
	}
};
export default mod;
