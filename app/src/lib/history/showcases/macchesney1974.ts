// MCVD preform process (macchesney1974; DevLog-017 pilot). Scene module: contract in ../showcase/types.ts.
//
// Sources (spec data/history/showcases/macchesney1974.yaml): MacChesney, O'Connor, Presby, Proc. IEEE 62(9) 1974 and
// US 4,217,027 (same inventors, public domain). Orientation as in patent FIG. 1 / FIG. 3: tube axis = x, gas flows +x
// (left to right), burner below (-y), hot zone traverses with the gas and returns fast; soot zone 35 downstream of hot
// zone 32, particle-free fusion region 36 upstream.
// Stated geometry used: tube 14 mm O.D. x 12 mm I.D., 18 in (457.2 mm) long, traversed over its full length (the
// traverse extends beyond both ends into the input / exhaust sections, col. 8:01-03); hot zone ~2 cm with heat 4 cm
// either side; 16 barrier passes; 10 graded core layers in equal radius steps (0.1 a); preform rod 18 in long, 8 mm
// (top of the stated 4-8 mm range); core / OD 0.35 (paper core ~35 um with the patent's ~100 um fiber OD, derived).
// Visual only (spec: assumed / withheld): lathe, chucks, burner block, carriage, pipes, flasks, input / exhaust
// sections (neutral stand-ins, no invented detail), layer thicknesses (barrier : core about 1 : 3 by area in both tube
// and preform), core pass count (5 shown), draw neck shape and draw orientation, collapse shown as two slow traverses
// for the two stated stages ("with reactants flowing", then "flow stopped", col. 7:27-35).
//
// Everything is a pure function of p (and the stored explode k): burner x, glow, deposit, particles (seeded), collapse.
import type * as T from 'three';
import type { Chapter, PartLook, ShowcaseContext3D, ShowcaseHandle, ShowcaseModule, Theme } from '../showcase/types';
import { clamp01, ease, lerp, seg } from '../showcase/progress';

// ------------------------------------------------------------------------------------------------ geometry (mm)
const HALF = 228.6; // 18 in tube, stated
const RO = 7; // 14 mm O.D., stated
const RI = 6; // 12 mm I.D., stated
const SEC = 36; // input / exhaust section length beyond each tube end (stated to exist, length not stated: visual)
const END = HALF + SEC; // drawn glass extent
const XS = -HALF - 12; // traverse start: the traverse 'extends beyond the tube at both ends' (col. 8:01-03)
const XE = HALF + 12; // traverse end
const XC = HALF; // preform = the 18 in tube (col. 3:32); input / exhaust sections removed
const W0 = HALF + 2; // deposit / collapse window: full inside the tube, fading out over the sections
const W1 = HALF + 16;
const CH = END - 8; // chuck centre (holds the input / exhaust sections)
const NCV = 5; // core passes shown (visual; the sources give no pass count)
const TBP = 0.03; // barrier thickness per pass (visual; barrier : core about 1 : 3 by area, as in the preform)
const NB = 16; // barrier passes, stated (Example 1)
const TC = 1.8; // core thickness (visual)
const TPW = 0.18; // porous (soot) deposit ahead of the hot zone, current pass (visual)
const XSL = -40; // cross-section plane of the layer chapter
const PO = 4.0; // preform radius: 8 mm, the upper end of the stated 4-8 mm range
const P1 = 1.62; // preform: silica / borosilicate boundary (visual; barrier : core area 1 : 3, same as the tube view)
const P2 = 1.4; // preform: core radius = 0.35 x PO (paper core ~35 um with the patent's ~100 um fiber OD; ratio derived)
const NG = 10; // graded layers, stated
const NECK = 26; // draw neck length (visual)
const DEG = Math.PI / 180;

const smooth = (a: number, b: number, x: number) => {
	const t = clamp01((x - a) / (b - a));
	return t * t * (3 - 2 * t);
};
const fract = (x: number) => x - Math.floor(x);
/** wrap an angle to (-pi, pi] */
const wrapPi = (a: number) => a - 2 * Math.PI * Math.floor((a + Math.PI) / (2 * Math.PI));
/** deterministic PRNG (mulberry32) */
function rng(seed: number) {
	let a = seed >>> 0;
	return () => {
		a = (a + 0x6d2b79f5) >>> 0;
		let t = a;
		t = Math.imul(t ^ (t >>> 15), t | 1);
		t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
		return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
	};
}

// ------------------------------------------------------------------------------------------------ process state of p
interface St {
	xb: number; // hot zone x
	lit: number; // burner flame 0..1
	glow: number; // hot-zone glow intensity
	hot: number; // 0 deposition (1430-1460 C) .. 1 collapse (~1900 C)
	nb: number; // barrier passes completed
	cur: number; // 1 / 2 while a barrier / core pass goes forward (sinters behind the zone, porous band ahead)
	cd: number; // core passes completed
	c0: number; // collapse state behind / ahead of the collapse front
	c1: number;
	cx: number; // collapse front x (the hot zone during a collapse pass)
	gas: number; // reactant flow 0..1
	cut: number; // cutaway sector 0..1 (front half)
	cw0: number; // cutaway window
	cw1: number;
	stub: number; // tube end stubs 1 (present) .. 0 (cut off)
}

interface PassSeg {
	a: number;
	b: number;
	x0: number;
	x1: number;
	fwd: boolean;
	dep: 'bar' | 'core' | 'col' | null;
	i: number;
}

// GLSL shared by the tube surfaces and the section faces (mirrors bnd() in JS)
const GL_COMMON = /* glsl */ `
uniform float uXb, uNb, uCur, uCd, uC0, uC1, uCx, uCut, uCw0, uCw1, uStub, uGlow, uHot, uGrade, uFade;
uniform vec4 uHi;
uniform vec3 uHiCol, uTubeCol, uBarCol, uCoreCol, uCoreDeep, uPowCol, uSecGlass;
float winX(float x) { return 1.0 - smoothstep(${W0.toFixed(1)}, ${W1.toFixed(1)}, abs(x)); }
float colAt(float x) { return (uC0 + (uC1 - uC0) * smoothstep(0.0, 30.0, uCx - x)) * winX(x); }
// uCur: 1 = barrier pass going forward, 2 = core pass going forward; both sinter behind the zone, porous ahead
float barN(float x) { return (uNb + step(0.5, uCur) * (1.0 - step(1.5, uCur)) * smoothstep(-4.0, 4.0, uXb - x)) * winX(x); }
float coreAt(float x) { return clamp((uCd + step(1.5, uCur) * smoothstep(-4.0, 4.0, uXb - x)) / ${NCV.toFixed(1)}, 0.0, 1.0) * winX(x); }
float powT(float x) { float d = x - uXb; return step(0.5, uCur) * step(0.0, d) * ${TPW.toFixed(3)} * exp(-d / 60.0) * smoothstep(0.0, 6.0, d) * winX(x); }
vec4 bnd(float x, out float bp, out float e) {
	float c = colAt(x); e = c * c * (3.0 - 2.0 * c);
	float b2 = 6.0 - ${TBP.toFixed(3)} * barN(x);
	float b3 = b2 - ${TC.toFixed(3)} * coreAt(x);
	vec4 B = vec4(mix(7.0, 4.0, e), mix(6.0, 1.62, e), mix(b2, 1.40, e), mix(b3, 0.0, e));
	bp = B.w - powT(x) * (1.0 - e);
	return B;
}
float glowAt(float x) { float d = x - uXb; return uGlow * (exp(-d * d / 162.0) + 0.3 * exp(-d * d / 1568.0)); }
vec3 glowCol() { return mix(vec3(1.0, 0.40, 0.09), vec3(1.0, 0.80, 0.52), uHot); }
// angle from +z (the camera side), wrapped to (-pi, pi]; the cut removes |a| < uCut * pi / 2 (uCut 2 = everything)
float angZ(vec2 yz) { float a = atan(yz.y, yz.x) - 1.5707963; return mod(a + 3.14159265, 6.2831853) - 3.14159265; }
bool inSector(vec2 yz) { return abs(angZ(yz)) < uCut * 1.5707963; }
bool cutAway(float x, vec2 yz) {
	if (uCut <= 0.001 || x < uCw0 || x > uCw1) return false;
	return inSector(yz);
}
`;

// section faces: the strip caps on the cut planes and the disc faces (tube ends, cut-window ends)
const SEC_VS = /* glsl */ `
uniform float uMode, uFaceX, uLen, uMid;
varying float vX; varying float vR; varying vec2 vYZ;
void main() {
	vec3 p = position;
	if (uMode < 0.5) { vX = uMid + p.x * uLen; vR = p.y; vYZ = vec2(p.y, 0.0); p.x = vX; }
	else { vX = uFaceX; vR = 0.0; vYZ = p.yz; p.x = uFaceX; }
	gl_Position = projectionMatrix * modelViewMatrix * vec4(p, 1.0);
}`;
const SEC_FS = /* glsl */ `
uniform float uMode, uSector, uAlpha, uFaceX;
varying float vX; varying float vR; varying vec2 vYZ;
${GL_COMMON}
float lineAA(float idx) { float f = abs(fract(idx + 0.5) - 0.5); float w = fwidth(idx) * 0.9; return 1.0 - smoothstep(w * 0.5, w * 1.5, f); }
void main() {
	// disc faces: radius and angle per fragment (an interpolated angle breaks at the disc centre and the seam)
	float r = uMode > 0.5 ? length(vYZ) : vR;
	if (uMode > 0.5) {
		if (uSector > 0.5) { if (!inSector(vYZ)) discard; }
		else if (cutAway(vX, vYZ)) discard;
	}
	float bp; float e; vec4 B = bnd(vX, bp, e);
	if (r > B.x || r < bp) discard;
	vec3 col; float a; float hi = 0.0;
	if (r > B.y) { col = uSecGlass; a = 0.8; hi = max(uHi.x, uHi.w); }
	else if (r > B.z) {
		float n = barN(vX);
		float idx = (B.y - r) / max(B.y - B.z, 1e-4) * n;
		float ln = lineAA(idx) * smoothstep(0.0, 0.6, 1.0 / max(fwidth(idx), 1e-3) - 2.0) * step(0.5, idx) * step(idx, n - 0.5);
		col = uBarCol * (1.0 - 0.22 * ln); a = 0.96; hi = max(uHi.y, uHi.w);
	} else if (r > B.w) {
		float s = (r - B.w) / max(B.z - B.w, 1e-4);
		float f = clamp(1.0 - s, 0.0, 0.9999) * 10.0; // ten layers, equal radius steps (0.1 a)
		float k = floor(f);
		float ln = lineAA(f) * step(0.5, f) * step(f, 9.5) * uGrade;
		col = mix(uCoreCol, mix(uBarCol, uCoreDeep, (k + 1.0) / 10.0), uGrade) * (1.0 - 0.18 * ln);
		a = 0.96; hi = max(uHi.z, uHi.w);
	} else { col = uPowCol; a = 0.97; }
	col += glowCol() * min(glowAt(vX), 1.0) * 0.45;
	col = mix(col, uHiCol, 0.45 * hi);
	float stubA = abs(vX) > ${(XC + 0.5).toFixed(1)} ? uStub : 1.0;
	gl_FragColor = vec4(col, a * uAlpha * stubA * uFade);
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`;

// flame: additive teardrop above the burner nozzle
const FLAME_VS = /* glsl */ `
varying vec3 vP; varying vec3 vN; varying vec3 vV;
void main() {
	vP = position;
	vec4 mv = modelViewMatrix * vec4(position, 1.0);
	vN = normalMatrix * normal; vV = -mv.xyz;
	gl_Position = projectionMatrix * mv;
}`;
const FLAME_FS = /* glsl */ `
uniform float uI; uniform float uFl; uniform float uLight; uniform float uHot;
varying vec3 vP; varying vec3 vN; varying vec3 vV;
void main() {
	float h = clamp(vP.y / 24.0, 0.0, 1.0);
	float c = clamp(abs(dot(normalize(vN), normalize(vV))), 0.0, 1.0);
	vec3 base = vec3(0.35, 0.55, 1.0);
	vec3 tip = mix(vec3(1.0, 0.55, 0.18), vec3(1.0, 0.82, 0.55), uHot);
	vec3 col = mix(base, tip, smoothstep(0.15, 0.85, h));
	float fl = 0.85 + 0.15 * sin(uFl + vP.y * 0.7);
	float a = uI * pow(c, 1.4) * (0.35 + 0.65 * smoothstep(0.0, 0.25, h)) * fl;
	a = clamp(a, 0.0, 1.0);
	gl_FragColor = uLight > 0.5 ? vec4(col * 0.9, a * 0.8) : vec4(col * a, a);
}`;

// ------------------------------------------------------------------------------------------------ module
const mod: ShowcaseModule = {
	renderer: '3d',
	async build(ctx0) {
		const ctx = ctx0 as ShowcaseContext3D;
		const { THREE, scene, camera, spec } = ctx;
		const { RoundedBoxGeometry } = await import('three/examples/jsm/geometries/RoundedBoxGeometry.js');
		let theme: Theme = ctx.theme;
		let w = Math.max(1, ctx.width);
		let h = Math.max(1, ctx.height);
		let k = 0;
		let hi: string[] = [];
		let lastP = 0;
		let tgt: [number, number, number] = [0, 0, 0];

		const disposables: { dispose(): void }[] = [];
		const keep = <X extends { dispose(): void }>(x: X): X => (disposables.push(x), x);
		const root = new THREE.Group();
		scene.add(root);

		// chapters (p ranges from the spec, defaults if a chapter is missing)
		const DEF: Record<string, [number, number]> = {
			tube: [0, 0.1], lathe: [0.1, 0.2], gases: [0.2, 0.3], burner: [0.3, 0.4], soot: [0.4, 0.52],
			layers: [0.52, 0.64], collapse: [0.64, 0.74], preform: [0.74, 0.82], loss: [0.82, 0.92], graded: [0.92, 1]
		};
		const C = (id: string): [number, number] => spec.chapters.find((c: Chapter) => c.id === id)?.p ?? DEF[id];
		const at = (id: string, q: number) => {
			const [a, b] = C(id);
			return a + (b - a) * q;
		};
		const loc = (p: number, id: string, q0 = 0, q1 = 1) => seg(p, at(id, q0), at(id, q1));

		// ------------------------------------------------------------------------ burner schedule (pure lookup)
		const passes: PassSeg[] = [];
		const fwd = (a: number, b: number, dep: PassSeg['dep'], i: number) => passes.push({ a, b, x0: XS, x1: XE, fwd: true, dep, i });
		const ret = (a: number, b: number) => passes.push({ a, b, x0: XE, x1: XS, fwd: false, dep: null, i: -1 });
		fwd(at('burner', 0.5), at('burner', 0.84), 'bar', 0);
		ret(at('burner', 0.86), at('burner', 1));
		fwd(at('soot', 0.04), at('soot', 0.96), 'bar', 1);
		ret(at('layers', 0), at('layers', 0.06));
		{
			const q0 = 0.08;
			const dq = 0.4 / (NB - 2);
			for (let i = 2; i < NB; i++) {
				const a = q0 + (i - 2) * dq;
				fwd(at('layers', a), at('layers', a + 0.72 * dq), 'bar', i);
				ret(at('layers', a + 0.72 * dq), at('layers', a + dq));
			}
		}
		{
			// core: the same moving-zone deposition as the barrier, NCV visual passes (count not stated)
			const dq = 0.4 / NCV;
			for (let i = 0; i < NCV; i++) {
				const a = 0.5 + i * dq;
				fwd(at('layers', a), at('layers', a + 0.72 * dq), 'core', i);
				ret(at('layers', a + 0.72 * dq), at('layers', a + dq));
			}
		}
		// collapse: traverse slowed (col. 7:27-29): each stage takes more scroll than any deposition pass in the wide shots
		fwd(at('collapse', 0.03), at('collapse', 0.56), 'col', 0);
		ret(at('collapse', 0.56), at('collapse', 0.6));
		fwd(at('collapse', 0.61), at('collapse', 0.985), 'col', 1);
		const COL_T = [0.8, 1];

		function state(p: number): St {
			let xb = XS;
			let nb = 0;
			let cur = 0;
			let cd = 0;
			let c0 = 0;
			let c1 = 0;
			let cx = 1e5;
			for (const s of passes) {
				if (p >= s.b) {
					xb = s.x1;
					if (s.dep === 'bar') nb = s.i + 1;
					if (s.dep === 'core') cd = s.i + 1;
					if (s.dep === 'col') c0 = c1 = COL_T[s.i];
				} else if (p >= s.a) {
					const q = (p - s.a) / (s.b - s.a);
					// forward: constant traverse speed with soft ends; return: rapid, eased
					const u = s.fwd ? smooth(0, 1, q) * 0.12 + q * 0.88 : ease(q);
					xb = lerp(s.x0, s.x1, u);
					if (s.dep === 'bar') {
						nb = s.i;
						cur = 1;
					}
					if (s.dep === 'core') {
						cd = s.i;
						cur = 2;
					}
					if (s.dep === 'col') {
						c0 = s.i ? COL_T[s.i - 1] : 0;
						c1 = COL_T[s.i];
						cx = xb;
					}
					break;
				} else break;
			}
			const lit = smooth(at('burner', 0.25), at('burner', 0.42), p) * (1 - smooth(at('preform', 0), at('preform', 0.15), p));
			const hot = smooth(at('collapse', 0), at('collapse', 0.06), p);
			const gas = smooth(at('gases', 0.05), at('gases', 0.4), p) * (1 - smooth(at('collapse', 0.53), at('collapse', 0.58), p));
			// cutaway: front half in a window that follows the hot-zone camera (soot), then the whole tube upstream of the
			// section plane XSL (layers: an end-on cross-section), then the front half along the tube (collapse)
			const xcam = camFollowX(xb);
			const ws = ease(seg(p, at('layers', 0), at('layers', 0.1)));
			const wb = ease(seg(p, at('layers', 0.84), at('layers', 0.95)));
			let cut = ease(seg(p, at('soot', 0), at('soot', 0.16)));
			cut = lerp(cut, 2, ws);
			cut = lerp(cut, 1, wb);
			cut *= 1 - ease(seg(p, at('preform', 0), at('preform', 0.16)));
			let cw0 = lerp(xcam - 110, -330, ws);
			let cw1 = lerp(xcam + 110, XSL, ws);
			cw0 = lerp(cw0, -(HALF - 8), wb);
			cw1 = lerp(cw1, HALF - 8, wb);
			const stub = 1 - smooth(at('preform', 0.04), at('preform', 0.16), p);
			return { xb, lit, glow: lit * (1 + 0.35 * hot), hot, nb, cur, cd, c0, c1, cx, gas, cut, cw0, cw1, stub };
		}
		function camFollowX(xb: number) {
			return 0.78 * xb + 10;
		}

		// JS mirror of the GLSL radial model
		const winX = (x: number) => 1 - smooth(W0, W1, Math.abs(x));
		const colAt = (x: number, s: St) => (s.c0 + (s.c1 - s.c0) * smooth(0, 30, s.cx - x)) * winX(x);
		const barN = (x: number, s: St) => (s.nb + (s.cur === 1 ? smooth(-4, 4, s.xb - x) : 0)) * winX(x);
		const coreAt = (x: number, s: St) => clamp01((s.cd + (s.cur === 2 ? smooth(-4, 4, s.xb - x) : 0)) / NCV) * winX(x);
		function bnd(x: number, s: St) {
			const c = colAt(x, s);
			const e = c * c * (3 - 2 * c);
			const b2 = RI - TBP * barN(x, s);
			const b3 = b2 - TC * coreAt(x, s);
			return { e, B0: lerp(RO, PO, e), B1: lerp(RI, P1, e), B2: lerp(b2, P2, e), B3: lerp(b3, 0, e) };
		}

		// ------------------------------------------------------------------------ materials
		const partLook = (id: string): PartLook => spec.parts.find((q) => q.id === id)?.look ?? {};
		const accent = new THREE.Color();
		const mats = new Map<string, T.MeshStandardMaterial[]>(); // part id -> materials (highlight via emissive)
		const baseOpacity = new Map<T.Material, number>();
		function std(id: string, o: T.MeshStandardMaterialParameters = {}) {
			const l = partLook(id);
			const m = keep(
				new THREE.MeshStandardMaterial({
					color: l.color ?? '#8a9099',
					metalness: l.metal ?? 0,
					roughness: l.rough ?? 0.5,
					transparent: true,
					opacity: l.opacity ?? 1,
					...o
				})
			);
			baseOpacity.set(m, m.opacity);
			if (!mats.has(id)) mats.set(id, []);
			mats.get(id)!.push(m);
			return m;
		}
		/** set a material's opacity as a fraction of its base; hides it (visible false) at 0 */
		function fade(m: T.Material, f: number) {
			m.opacity = (baseOpacity.get(m) ?? 1) * f;
			m.visible = f > 0.002;
			m.depthWrite = f > 0.98 && (baseOpacity.get(m) ?? 1) > 0.98;
		}

		// fresnel rim (glass) and a world-height fade (the preform's upper part during the draw, keeps the keyword clear)
		const FY = { uFy0: { value: 1e5 }, uFy1: { value: 2e5 }, uFl0: { value: -2e5 }, uFl1: { value: -1e5 } };
		function decorate(m: T.MeshStandardMaterial, fres: number, fadeY: boolean, spec = 0) {
			if (spec > 0) m.premultipliedAlpha = true;
			m.onBeforeCompile = (sh) => {
				Object.assign(sh.uniforms, FY);
				sh.vertexShader = sh.vertexShader
					.replace('#include <common>', '#include <common>\nvarying float vWy;')
					.replace('#include <project_vertex>', '#include <project_vertex>\nvWy = (modelMatrix * vec4(transformed, 1.0)).y;');
				sh.fragmentShader = sh.fragmentShader
					.replace('#include <common>', '#include <common>\nuniform float uFy0, uFy1, uFl0, uFl1; varying float vWy;')
					.replace(
						'#include <opaque_fragment>',
						`{ float fr_ = pow(1.0 - clamp(abs(dot(normalize(vViewPosition), normal)), 0.0, 1.0), 2.5);
						  diffuseColor.a = clamp(diffuseColor.a + ${fres.toFixed(2)} * fr_, 0.0, 1.0);
						  outgoingLight += vec3(${(fres * 0.5).toFixed(2)} * fr_); }
						float fyk_ = 1.0;
						${fadeY ? '{ float fy_ = (1.0 - smoothstep(uFy0, uFy1, vWy)) * smoothstep(uFl0, uFl1, vWy); fyk_ = fy_ * fy_; diffuseColor.a *= fyk_; }' : ''}
						#include <opaque_fragment>`
					)
					.replace(
						'#include <premultiplied_alpha_fragment>',
						`#include <premultiplied_alpha_fragment>
						${spec > 0 ? `gl_FragColor.rgb += min(totalSpecular, vec3(1.0)) * ${spec.toFixed(2)} * fyk_;` : ''}`
					);
			};
			m.customProgramCacheKey = () => `mcvd-dec-${fres}-${fadeY}-${spec}`;
			return m;
		}

		// shared uniforms of the tube model
		const U = {
			uXb: { value: XS }, uNb: { value: 0 }, uCur: { value: 0 }, uCd: { value: 0 }, uC0: { value: 0 }, uC1: { value: 0 },
			uCx: { value: 1e5 }, uCut: { value: 0 }, uCw0: { value: -100 }, uCw1: { value: 100 }, uStub: { value: 1 }, uGlow: { value: 0 },
			uHot: { value: 0 }, uGrade: { value: 0 }, uFade: { value: 1 },
			uHi: { value: new THREE.Vector4() }, uHiCol: { value: new THREE.Color('#3987e5') },
			uTubeCol: { value: new THREE.Color() }, uBarCol: { value: new THREE.Color() }, uCoreCol: { value: new THREE.Color() },
			uCoreDeep: { value: new THREE.Color() }, uPowCol: { value: new THREE.Color() }, uSecGlass: { value: new THREE.Color() }
		};

		// ------------------------------------------------------------------------ tube model (radial surfaces)
		const tube = new THREE.Group();
		root.add(tube);
		const cylGeo = keep(new THREE.CylinderGeometry(1, 1, 2 * END, 72, 280, true).rotateZ(-Math.PI / 2));
		/** surface k: 0 outer glass, 1 tube inner face, 2 barrier / core interface, 3 bore (deposit top, powder) */
		function surface(kind: number) {
			const m = keep(
				new THREE.MeshStandardMaterial({ color: '#ffffff', metalness: 0, roughness: kind === 3 ? 0.55 : 0.06, transparent: true, depthWrite: false, side: THREE.DoubleSide, envMapIntensity: kind === 0 ? 2.2 : 0.35 })
			);
			m.onBeforeCompile = (sh) => {
				Object.assign(sh.uniforms, U);
				sh.vertexShader = sh.vertexShader
					.replace('#include <common>', `#include <common>\n${GL_COMMON}\nvarying float vLx; varying vec2 vLyz;`)
					.replace(
						'#include <begin_vertex>',
						`#include <begin_vertex>
						{ float bp; float e; vec4 B = bnd(transformed.x, bp, e);
						  float rr = ${['B.x', 'B.y', 'B.z', 'bp'][kind]};
						  transformed.yz *= rr; vLx = transformed.x; vLyz = transformed.yz; }`
					);
				sh.fragmentShader = sh.fragmentShader
					.replace('#include <common>', `#include <common>\n${GL_COMMON}\nvarying float vLx; varying vec2 vLyz;`)
					.replace(
						'#include <clipping_planes_fragment>',
						`#include <clipping_planes_fragment>
						if (cutAway(vLx, vLyz)) discard;
						float stubA = abs(vLx) > ${(XC + 0.5).toFixed(1)} ? uStub : 1.0;
						if (stubA < 0.01) discard;
						float bp_; float e_; vec4 B_ = bnd(vLx, bp_, e_);
						float g_ = glowAt(vLx);`
					)
					.replace(
						'#include <color_fragment>',
						`#include <color_fragment>
						${
							kind === 0
								? `diffuseColor.rgb = uTubeCol; diffuseColor.a = 0.08 + 0.5 * uHi.x + 0.3 * uHi.w;`
								: kind === 1
									? `diffuseColor.rgb = uTubeCol; diffuseColor.a = 0.04 * (1.0 - e_);`
									: kind === 2
										? `float dp_ = clamp(barN(vLx) / 3.0, 0.0, 1.0); float cf_ = clamp(coreAt(vLx) * 4.0, 0.0, 1.0);
										   diffuseColor.rgb = mix(uBarCol, uCoreCol, cf_ * (1.0 - e_));
										   diffuseColor.a = 0.14 * max(dp_, cf_) + 0.3 * max(uHi.y, uHi.z);`
										: `float dp_ = clamp(barN(vLx) / 2.0, 0.0, 1.0); float cf_ = clamp(coreAt(vLx) * 4.0, 0.0, 1.0);
										   vec3 c_ = mix(uTubeCol, uBarCol, dp_); c_ = mix(c_, uCoreCol, cf_);
										   float a_ = mix(0.03, 0.12, max(dp_, cf_));
										   float pw_ = smoothstep(0.0, 0.03, powT(vLx) * (1.0 - e_));
										   diffuseColor.rgb = mix(c_, uPowCol, pw_); diffuseColor.a = mix(a_, 0.92, pw_) * (1.0 - smoothstep(0.6, 0.98, e_));
										   diffuseColor.a += 0.3 * max(uHi.y, uHi.z);`
						}
						diffuseColor.a = clamp(diffuseColor.a + g_ * ${kind === 0 ? '0.7' : '0.25'}, 0.0, 1.0) * stubA * uFade;`
					)
					.replace(
						'#include <emissivemap_fragment>',
						`#include <emissivemap_fragment>
						totalEmissiveRadiance += glowCol() * g_ * ${kind === 0 ? '2.2' : '1.2'};
						totalEmissiveRadiance += uHiCol * 0.35 * ${kind === 0 || kind === 1 ? 'max(uHi.x, uHi.w)' : 'max(uHi.y, uHi.z)'};`
					)
					.replace(
						'#include <opaque_fragment>',
						kind === 0
							? `{ float fr_ = pow(1.0 - clamp(abs(dot(normalize(vViewPosition), normal)), 0.0, 1.0), 2.5);
							    diffuseColor.a = clamp(diffuseColor.a + 0.5 * fr_ * stubA * uFade, 0.0, 1.0);
							    outgoingLight += vec3(0.22 * fr_); }
							  #include <opaque_fragment>`
							: '#include <opaque_fragment>'
					)
					.replace(
						'#include <premultiplied_alpha_fragment>',
						kind === 0
							? `#include <premultiplied_alpha_fragment>
							   gl_FragColor.rgb += min(totalSpecular, vec3(1.0)) * 1.3 * stubA * uFade;`
							: '#include <premultiplied_alpha_fragment>'
					);
			};
			m.customProgramCacheKey = () => `mcvd-surf-${kind}`;
			if (kind === 0) m.premultipliedAlpha = true;
			const mesh = new THREE.Mesh(cylGeo, m);
			mesh.renderOrder = [8, 6, 5, 4][kind];
			mesh.frustumCulled = false;
			tube.add(mesh);
			return mesh;
		}
		const surfs = [surface(3), surface(2), surface(1), surface(0)];

		// section faces
		const secMats: T.ShaderMaterial[] = [];
		function secMat(mode: number, faceX = 0, sector = 0) {
			const m = keep(
				new THREE.ShaderMaterial({
					uniforms: { ...U, uMode: { value: mode }, uFaceX: { value: faceX }, uLen: { value: 1 }, uMid: { value: 0 }, uSector: { value: sector }, uAlpha: { value: 1 } },
					vertexShader: SEC_VS,
					fragmentShader: SEC_FS,
					transparent: true,
					toneMapped: false,
					side: THREE.DoubleSide
				})
			);
			secMats.push(m);
			return m;
		}
		const stripGeo = keep(new THREE.PlaneGeometry(1, 7.6, 1, 1).translate(0, 3.8, 0));
		const strips = [0, 1].map(() => {
			const pivot = new THREE.Group();
			const m = new THREE.Mesh(stripGeo, secMat(0));
			m.frustumCulled = false;
			m.renderOrder = 3;
			pivot.add(m);
			tube.add(pivot);
			return { pivot, m };
		});
		const discGeo = keep(new THREE.CircleGeometry(7.6, 96).rotateY(Math.PI / 2));
		const disc = (x: number, sector: number) => {
			const m = new THREE.Mesh(discGeo, secMat(1, x, sector));
			m.frustumCulled = false;
			m.renderOrder = 3;
			tube.add(m);
			return m;
		};
		const endDiscs = [disc(-END, 0), disc(END, 0)];
		const cutDiscs = [disc(-XC, 0), disc(XC, 0)]; // ends of the preform after the stubs are cut
		const winDiscs = [disc(0, 1), disc(0, 1)]; // ends of the cutaway window
		// pick proxy for the tube (the drawn surfaces are displaced in the vertex shader)
		const proxyMat = keep(new THREE.MeshBasicMaterial({ visible: false }));
		const tubeProxy = new THREE.Mesh(keep(new THREE.CylinderGeometry(1, 1, 2 * END, 32, 1, false).rotateZ(-Math.PI / 2)), proxyMat);
		tube.add(tubeProxy);

		// ------------------------------------------------------------------------ lathe (neutral stand-ins)
		const lathe = new THREE.Group();
		root.add(lathe);
		const latheMat = std('lathe', { envMapIntensity: 1.5 });
		const latheMat2 = std('lathe', { envMapIntensity: 1.1, roughness: 0.32, metalness: 0.75 });
		const box = (sx: number, sy: number, sz: number, r: number) => keep(new RoundedBoxGeometry(sx, sy, sz, 3, r));
		const head = new THREE.Group();
		const headBody = new THREE.Mesh(box(110, 150, 120, 5), latheMat);
		headBody.position.set(-(CH + 13 + 55), -5, 0);
		const chuckGeo = keep(new THREE.CylinderGeometry(30, 30, 26, 64).rotateZ(Math.PI / 2));
		const headChuck = new THREE.Mesh(chuckGeo, latheMat2);
		headChuck.position.set(-CH, 0, 0);
		head.add(headBody, headChuck);
		const tail = new THREE.Group();
		const tailBody = new THREE.Mesh(box(90, 135, 110, 5), latheMat);
		tailBody.position.set(CH + 13 + 45, -12.5, 0);
		const tailChuck = new THREE.Mesh(chuckGeo, latheMat2);
		tailChuck.position.set(CH, 0, 0);
		tail.add(tailBody, tailChuck);
		const bed = new THREE.Mesh(box(2 * (CH + 13 + 110) + 10, 22, 120, 4), latheMat);
		bed.position.set(0, -91, 0);
		lathe.add(head, tail, bed);
		for (const o of [headBody, headChuck, tailBody, tailChuck, bed]) o.userData.part = 'lathe';

		// rotation arrow (patent FIG. 1 arrow 5a: tube rotation)
		const arrowMat = keep(new THREE.MeshBasicMaterial({ color: '#cfd6de', transparent: true, opacity: 0.8, depthWrite: false }));
		const arrow = new THREE.Group();
		const arc = new THREE.Mesh(keep(new THREE.TorusGeometry(15, 0.55, 8, 72, 1.55 * Math.PI)), arrowMat);
		const tip = new THREE.Mesh(keep(new THREE.ConeGeometry(1.6, 4.5, 16)), arrowMat);
		tip.position.set(15 * Math.cos(1.55 * Math.PI), 15 * Math.sin(1.55 * Math.PI), 0);
		tip.rotation.z = 1.55 * Math.PI;
		arrow.add(arc, tip);
		const arrowPivot = new THREE.Group();
		arrowPivot.add(arrow);
		arrow.rotation.y = Math.PI / 2;
		arrowPivot.position.set(-HALF - 14, 0, 0);
		root.add(arrowPivot);

		// ------------------------------------------------------------------------ burner, carriage, feed screw
		const burner = new THREE.Group();
		root.add(burner);
		const burnMat = std('burner', { envMapIntensity: 1.2 });
		const carriage = new THREE.Mesh(box(56, 14, 96, 3), burnMat);
		carriage.position.set(0, -73, 8);
		const burnBody = new THREE.Mesh(box(36, 30, 36, 4), burnMat);
		burnBody.position.set(0, -51, 0);
		const nozzle = new THREE.Mesh(keep(new THREE.CylinderGeometry(4.5, 6.5, 6, 40)), burnMat);
		nozzle.position.set(0, -33, 0);
		burner.add(carriage, burnBody, nozzle);
		for (const o of [carriage, burnBody, nozzle]) o.userData.part = 'burner';
		const screwMat = std('feed_screw');
		const screw = new THREE.Mesh(keep(new THREE.CylinderGeometry(4, 4, 2 * (CH + 13), 32).rotateZ(Math.PI / 2)), screwMat);
		screw.position.set(0, -73, 42);
		screw.userData.part = 'feed_screw';
		root.add(screw);

		// flame (part "flame" = hot zone) and the glow halo
		const flameMat = keep(
			new THREE.ShaderMaterial({
				uniforms: { uI: { value: 0 }, uFl: { value: 0 }, uLight: { value: 0 }, uHot: U.uHot },
				vertexShader: FLAME_VS,
				fragmentShader: FLAME_FS,
				transparent: true,
				depthWrite: false,
				blending: THREE.AdditiveBlending,
				side: THREE.DoubleSide
			})
		);
		const flamePts: T.Vector2[] = [];
		for (let i = 0; i <= 24; i++) {
			const t = i / 24;
			flamePts.push(new THREE.Vector2(Math.max(0.01, 5.5 * Math.sin(Math.PI * (0.08 + 0.92 * t)) ** 0.6 * (1 - 0.3 * t)), t * 25));
		}
		const flame = new THREE.Mesh(keep(new THREE.LatheGeometry(flamePts, 40)), flameMat);
		flame.position.set(0, -30.5, 0);
		flame.scale.set(1.25, 1, 1);
		flame.renderOrder = 9;
		flame.userData.part = 'burner';
		burner.add(flame);
		const haloTex = (() => {
			const c = document.createElement('canvas');
			c.width = c.height = 128;
			const g = c.getContext('2d')!;
			const gr = g.createRadialGradient(64, 64, 0, 64, 64, 64);
			gr.addColorStop(0, 'rgba(255,255,255,1)');
			gr.addColorStop(0.25, 'rgba(255,255,255,0.45)');
			gr.addColorStop(1, 'rgba(255,255,255,0)');
			g.fillStyle = gr;
			g.fillRect(0, 0, 128, 128);
			return keep(new THREE.CanvasTexture(c));
		})();
		const haloMat = keep(new THREE.SpriteMaterial({ map: haloTex, color: '#ff8a3a', transparent: true, depthWrite: false, blending: THREE.AdditiveBlending }));
		const halo = new THREE.Sprite(haloMat);
		halo.renderOrder = 10;
		root.add(halo);
		const hotLight = new THREE.PointLight('#ff8a3a', 0, 260, 0);
		root.add(hotLight);

		// hot-zone region proxies: soot zone 35 (downstream) and region 36 (upstream); drawn only when highlighted
		const zoneMat35 = keep(new THREE.MeshBasicMaterial({ color: '#3987e5', transparent: true, opacity: 0, depthWrite: false }));
		const zoneMat36 = keep(new THREE.MeshBasicMaterial({ color: '#3987e5', transparent: true, opacity: 0, depthWrite: false }));
		const zoneGeo = keep(new THREE.CylinderGeometry(1, 1, 1, 32, 1, false).rotateZ(-Math.PI / 2));
		const zone35 = new THREE.Mesh(zoneGeo, zoneMat35);
		const zone36 = new THREE.Mesh(zoneGeo, zoneMat36);
		zone35.userData.part = 'soot';
		zone36.userData.part = 'clear_zone';
		zone35.renderOrder = zone36.renderOrder = 7;
		tube.add(zone35, zone36);

		// ------------------------------------------------------------------------ gas supply, inlet, outlet
		const supply = new THREE.Group();
		root.add(supply);
		const glassMat = decorate(std('gas_supply', { roughness: 0.05, depthWrite: false, side: THREE.DoubleSide, envMapIntensity: 1.4 }), 0.35, false, 0.8);
		const liquidMat = std('gas_supply', { color: '#b8d4e2', opacity: 0.55, roughness: 0.2 });
		const pipeMat = std('gas_supply', { color: '#9aa3ab', opacity: 1, metalness: 0.5, roughness: 0.4 });
		const flaskGeo = keep(new THREE.CylinderGeometry(16, 16, 62, 48, 1, true));
		const liqGeo = keep(new THREE.CylinderGeometry(15.2, 15.2, 28, 40));
		const flaskX = [-518, -570];
		for (const fx of flaskX) {
			const f = new THREE.Mesh(flaskGeo, glassMat);
			f.position.set(fx, -71, 0);
			const lq = new THREE.Mesh(liqGeo, liquidMat);
			lq.position.set(fx, -88, 0);
			const bottom = new THREE.Mesh(keep(new THREE.CircleGeometry(16, 48).rotateX(-Math.PI / 2)), glassMat);
			bottom.position.set(fx, -102, 0);
			supply.add(f, lq, bottom);
		}
		const res13 = new THREE.Mesh(keep(new THREE.CylinderGeometry(13, 13, 84, 40)), std('gas_supply', { opacity: 0.6, metalness: 0.3, roughness: 0.3 }));
		res13.position.set(-622, -60, 0);
		supply.add(res13);
		const tubeAlong = (pts: number[][], r: number, mat: T.Material, part: string, grp: T.Object3D) => {
			const curve = new THREE.CatmullRomCurve3(
				pts.map((q) => new THREE.Vector3(q[0], q[1], q[2])),
				false,
				'centripetal'
			);
			const m = new THREE.Mesh(keep(new THREE.TubeGeometry(curve, 96, r, 12, false)), mat);
			m.userData.part = part;
			grp.add(m);
			return { curve, m };
		};
		// O2 into the flasks (dip tubes), flask outlets and reservoir 13 into the manifold
		for (const fx of flaskX) {
			tubeAlong([[fx - 6, -95, 0], [fx - 6, -40, 0], [fx - 6, -28, 0]], 1.3, pipeMat, 'gas_supply', supply);
			tubeAlong([[fx + 6, -40, 0], [fx + 6, -22, 0], [fx + 6, -14, 0]], 1.3, pipeMat, 'gas_supply', supply);
		}
		tubeAlong([[-622, -18, 0], [-622, -14, 0]], 1.3, pipeMat, 'gas_supply', supply);
		tubeAlong([[-680, -14, 0], [-650, -14, 0], [-510, -14, 0], [-490, -14, 0]], 1.6, pipeMat, 'gas_supply', supply);
		for (const o of supply.children) o.userData.part = 'gas_supply';
		const inletGrp = new THREE.Group();
		root.add(inletGrp);
		const inletMat = std('inlet');
		const inlet = tubeAlong([[-490, -14, 0], [-468, -14, 0], [-452, -6, 0], [-440, 0, 0], [-400, 0, 0], [-340, 0, 0], [-END + 4, 0, 0]], 3, inletMat, 'inlet', inletGrp);
		const exhGrp = new THREE.Group();
		root.add(exhGrp);
		const exhMat = std('exhaust');
		const exh = tubeAlong([[END - 4, 0, 0], [340, 0, 0], [420, 0, 0], [470, 0, 0]], 4, exhMat, 'exhaust', exhGrp);

		// ------------------------------------------------------------------------ particles (seeded, pure in p)
		const R = rng(1974);
		const dummy = new THREE.Object3D();
		// soot cloud
		const NS = 640;
		const sootSeed = Array.from({ length: NS }, () => ({ u: R(), r0: R() ** 0.7, th: R() * Math.PI * 2, sp: 0.75 + 0.5 * R(), sz: 0.6 + 0.8 * R() }));
		const sootMat = keep(new THREE.MeshBasicMaterial({ color: '#ffffff', transparent: true, opacity: 0.95, depthWrite: false }));
		const soot = new THREE.InstancedMesh(keep(new THREE.IcosahedronGeometry(0.2, 1)), sootMat, NS);
		soot.instanceColor = new THREE.InstancedBufferAttribute(new Float32Array(NS * 3), 3);
		soot.frustumCulled = false;
		soot.renderOrder = 7;
		soot.userData.part = 'soot';
		tube.add(soot);
		// gas streaks: manifold -> inlet -> bore -> outlet
		const NG2 = 150;
		const gasSeed = Array.from({ length: NG2 }, () => ({ u: R(), r0: Math.sqrt(R()) * 0.85, th: R() * Math.PI * 2, ln: 0.6 + 0.8 * R() }));
		const gasMat = keep(new THREE.MeshBasicMaterial({ color: '#a8d4ff', transparent: true, opacity: 0.55, depthWrite: false, blending: THREE.AdditiveBlending }));
		const gasGeo = keep(new THREE.CylinderGeometry(0.22, 0.22, 7, 6).rotateZ(-Math.PI / 2));
		const gasI = new THREE.InstancedMesh(gasGeo, gasMat, NG2);
		gasI.frustumCulled = false;
		gasI.renderOrder = 7;
		root.add(gasI);
		const inLen = inlet.curve.getLength();
		const exLen = exh.curve.getLength();
		const boreLen = 2 * (END - 4);
		const pathLen = inLen + boreLen + exLen;
		// bubbles in the two flasks
		const NBU = 36;
		const bubSeed = Array.from({ length: NBU }, (_, i) => ({ f: i % 2, u: R(), dx: (R() - 0.5) * 6, dz: (R() - 0.5) * 6, s: 0.8 + 0.8 * R() }));
		const bubMat = keep(new THREE.MeshStandardMaterial({ color: '#ffffff', transparent: true, opacity: 0.7, roughness: 0.1, depthWrite: false }));
		const bubI = new THREE.InstancedMesh(keep(new THREE.SphereGeometry(1, 12, 8)), bubMat, NBU);
		bubI.frustumCulled = false;
		bubI.userData.part = 'gas_supply';
		supply.add(bubI);

		// ------------------------------------------------------------------------ preform (after collapse) and fiber
		const pf = new THREE.Group(); // axis along local x; rotated to vertical for the draw
		root.add(pf);
		const pfLen = 2 * XC;
		const ringR = [PO, P1, P2, ...Array.from({ length: NG - 1 }, (_, i) => P2 * (1 - (i + 1) / NG))]; // core rings: equal radius steps of 0.1 a (paper p.1281)
		const sleeves: { side: T.Mesh; cap: T.Mesh; cap2: T.Mesh; mat: T.MeshStandardMaterial; capMat: T.MeshStandardMaterial; part: string; idx: number }[] = [];
		for (let i = 0; i < ringR.length; i++) {
			const ro = ringR[i];
			const ri = i + 1 < ringR.length ? ringR[i + 1] : 0;
			const part = i === 0 ? 'preform' : i === 1 ? 'barrier_layer' : 'core_layers';
			const mat = std(part === 'preform' ? 'preform' : part, i === 0 ? { depthWrite: false, roughness: 0.05, envMapIntensity: 1.3 } : { roughness: 0.15, depthWrite: false });
			decorate(mat, i === 0 ? 0.35 : 0.12, true, i === 0 ? 0.9 : 0);
			mat.opacity = i === 0 ? 0.14 : i === 1 ? 0.2 : i === 2 ? 0.55 : 0.6;
			baseOpacity.set(mat, mat.opacity);
			const capMat = decorate(keep(new THREE.MeshStandardMaterial({ color: '#ffffff', roughness: 0.35, metalness: 0, transparent: true, side: THREE.DoubleSide })), 0, true);
			mats.get(part)!.push(capMat);
			baseOpacity.set(capMat, 1);
			const side = new THREE.Mesh(keep(new THREE.CylinderGeometry(ro, ro, pfLen, 64, 1, true).rotateZ(-Math.PI / 2)), mat);
			const capGeo = keep(new THREE.RingGeometry(ri, ro, 64, 1).rotateY(-Math.PI / 2));
			const cap = new THREE.Mesh(capGeo, capMat); // top end (local -x)
			cap.position.x = -XC;
			const cap2 = new THREE.Mesh(capGeo, capMat); // bottom end
			cap2.position.x = XC;
			side.renderOrder = 6 - Math.min(i, 3);
			cap.renderOrder = cap2.renderOrder = 3;
			for (const o of [side, cap, cap2]) o.userData.part = part === 'preform' ? 'preform' : part;
			const g = new THREE.Group();
			g.add(side, cap, cap2);
			pf.add(g);
			sleeves.push({ side, cap, cap2, mat, capMat, part, idx: i });
		}
		// draw neck (visual) and fiber line
		const neckPts: T.Vector2[] = [];
		for (let i = 0; i <= 40; i++) {
			const t = i / 40;
			const r = PO * (1 - smooth(0, 1, t) ** 0.8) * (1 - t) ** 0.6 + 0.06;
			neckPts.push(new THREE.Vector2(r, t * NECK));
		}
		const neckMat = std('fiber', { roughness: 0.08, depthWrite: false, emissive: '#ff7a2a', emissiveIntensity: 0 });
		const neck = new THREE.Mesh(keep(new THREE.LatheGeometry(neckPts, 48).rotateZ(-Math.PI / 2)), neckMat);
		neck.position.x = XC;
		neck.userData.part = 'fiber';
		pf.add(neck);
		const fiberGeo = keep(new THREE.BufferGeometry());
		fiberGeo.setAttribute('position', new THREE.Float32BufferAttribute([0, 0, 0, 1, 0, 0, 2, 0, 0], 3));
		// vertex alpha: the drawn fiber fades out along its length (never runs under the plot panel)
		fiberGeo.setAttribute('color', new THREE.Float32BufferAttribute([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], 4));
		const fiberMat = keep(new THREE.LineBasicMaterial({ color: '#e8f4ff', transparent: true, vertexColors: true, depthWrite: false }));
		const fiber = new THREE.Line(fiberGeo, fiberMat);
		fiber.userData.part = 'fiber';
		fiber.frustumCulled = false;
		pf.add(fiber);
		const glintGeo = keep(new THREE.BufferGeometry());
		glintGeo.setAttribute('position', new THREE.Float32BufferAttribute([0, 0, 0, 1, 0, 0], 3));
		const glintMat = keep(new THREE.LineBasicMaterial({ color: '#ffffff', transparent: true, blending: THREE.AdditiveBlending, depthWrite: false }));
		const glint = new THREE.Line(glintGeo, glintMat);
		glint.frustumCulled = false;
		pf.add(glint);

		// ------------------------------------------------------------------------ lights (same rig as the ruby scene)
		const hemi = new THREE.HemisphereLight('#ffffff', '#3a3c44', 0.7);
		const key = new THREE.DirectionalLight('#fff3e6', 2.4);
		key.position.set(60, 120, 95);
		const rim = new THREE.DirectionalLight('#bcd2ff', 1.5);
		rim.position.set(-130, 50, -90);
		const fill = new THREE.DirectionalLight('#ffffff', 0.5);
		fill.position.set(-40, -60, 120);
		// studio light for the opening hero shots (the bare tube catching light); fades out once the lathe is in
		const hero = new THREE.DirectionalLight('#ffffff', 0);
		hero.position.set(-160, 140, 260);
		const heroRim = new THREE.DirectionalLight('#cfe2ff', 0);
		heroRim.position.set(120, 60, -220);
		root.add(hemi, key, rim, fill, hero, heroRim);

		// ------------------------------------------------------------------------ theme
		const sootCol = new THREE.Color();
		const hotCol = new THREE.Color('#ffb070');
		function applyTheme() {
			const light = theme === 'light';
			accent.set(light ? '#2a78d6' : '#3987e5');
			U.uHiCol.value.copy(accent);
			U.uTubeCol.value.set(light ? '#8fa7b6' : (partLook('substrate_tube').color ?? '#dce8ee'));
			U.uSecGlass.value.set(light ? '#a9bcc8' : '#71889a');
			U.uBarCol.value.set(partLook('barrier_layer').color ?? '#bcd6e6');
			U.uCoreCol.value.set(partLook('core_layers').color ?? '#7fb3ff');
			U.uCoreDeep.value.set(light ? '#1f5fc8' : '#3b7cf0');
			U.uPowCol.value.set(light ? '#d9d5cc' : (partLook('soot').color ?? '#f4f4f2'));
			sootCol.set(light ? '#b8b2a6' : '#f4f4f2');
			for (const m of secMats) m.uniforms.uAlpha.value = light ? 1 : 0.92;
			flameMat.uniforms.uLight.value = light ? 1 : 0;
			flameMat.blending = light ? THREE.NormalBlending : THREE.AdditiveBlending;
			haloMat.blending = light ? THREE.NormalBlending : THREE.AdditiveBlending;
			haloMat.color.set(light ? '#ff9a50' : '#ff8a3a');
			gasMat.blending = light ? THREE.NormalBlending : THREE.AdditiveBlending;
			gasMat.color.set(light ? '#4a8ccc' : '#a8d4ff');
			sootMat.blending = THREE.NormalBlending;
			arrowMat.color.set(light ? '#5b6570' : '#cfd6de');
			// lift the lathe in light theme (spec look #3a4048 reads near black on the light page)
			for (const m of mats.get('lathe') ?? []) m.color.set(light ? '#8e969f' : (partLook('lathe').color ?? '#3a4048'));
			fiberMat.color.set(light ? '#2f6fb0' : '#e8f4ff');
			glintMat.blending = light ? THREE.NormalBlending : THREE.AdditiveBlending;
			glintMat.color.set(light ? '#ff8a3a' : '#ffffff');
			bubMat.color.set(light ? '#7f98a8' : '#ffffff');
			for (const m of [flameMat, haloMat, gasMat, glintMat]) m.needsUpdate = true;
		}
		applyTheme();

		// ------------------------------------------------------------------------ camera shots
		interface Shot {
			az: number;
			el: number;
			box: number[]; // x0 x1 y0 y1 z0 z1
			fw: number; // usable width fraction
			fh: number;
			sx: number; // object centre offset, fraction of the view (+ right)
			sy: number; // (+ up)
		}
		const portrait = () => w / h < 0.9;
		const plotShift = (s: Shot): Shot =>
			portrait() ? { ...s, fw: Math.min(s.fw, 0.86), fh: 0.15, sx: 0, sy: 0.18 } : { ...s, fw: Math.min(s.fw, 0.44), fh: Math.min(s.fh, 0.62), sx: -0.25, sy: -0.06 };
		const P = (s: Shot): Shot => (portrait() ? { ...s, fh: s.fh * 0.7, sy: s.sy + 0.06 } : s);
		const sh = {
			intro: (p: number): Shot => {
				// the tube in flight: offset and turned (same motion as frame), endpoints +-(ex, ey, ez)
				const o = 1 - ease(loc(p, 'tube', 0, 0.8));
				const ry = -o * 0.75;
				const rz = o * 0.22;
				const ex = Math.abs(HALF * Math.cos(rz) * Math.cos(ry)) + 8;
				const ey = Math.abs(HALF * Math.sin(rz)) + 8;
				const ez = Math.abs(HALF * Math.cos(rz) * Math.sin(ry)) + 8;
				const box = [230 * o - ex, 230 * o + ex, 60 * o - ey, 60 * o + ey, -170 * o - ez, -170 * o + ez];
				return P({ az: portrait() ? -72 : -46, el: 9, box, fw: 1.02, fh: 0.62, sx: 0.02, sy: -0.1 });
			},
			tube: (): Shot => P({ az: portrait() ? -70 : -44, el: 8, box: [-HALF, HALF, -8, 8, -8, 8], fw: 1.02, fh: 0.62, sx: 0.02, sy: -0.1 }),
			lathe: (): Shot => P({ az: portrait() ? -64 : -27, el: 20, box: [-(CH + 70), CH + 60, -102, 64, -60, 60], fw: 0.97, fh: 0.66, sx: 0, sy: -0.08 }),
			gases: (): Shot => P({ az: portrait() ? -64 : -33, el: 20, box: [-690, 480, -102, 70, -60, 60], fw: 0.9, fh: 0.6, sx: 0, sy: -0.08 }),
			burner: (): Shot => P({ az: portrait() ? -36 : -17, el: portrait() ? 10 : 7, box: [-HALF - 15, HALF + 15, -80, 12, -20, 20], fw: 0.9, fh: 0.56, sx: 0, sy: -0.07 }),
			soot: (p: number): Shot => {
				const xc = camFollowX(state(p).xb);
				return P({ az: portrait() ? -26 : -9, el: 27, box: portrait() ? [xc - 26, xc + 34, -32, 9, -7, 7] : [xc - 50, xc + 50, -34, 9, -7, 7], fw: 0.9, fh: 0.66, sx: 0, sy: -0.07 });
			},
			macro: (): Shot => P({ az: portrait() ? -66 : -60, el: 22, box: [XSL - 0.5, XSL + 0.5, -7.6, 7.6, -7.6, 7.6], fw: 0.8, fh: 0.62, sx: portrait() ? 0 : 0.06, sy: -0.07 }),
			layersWide: (): Shot => P({ az: portrait() ? -40 : -14, el: 15, box: portrait() ? [-80, 80, -9, 9, -7, 7] : [-150, 150, -10, 10, -7, 7], fw: 0.9, fh: 0.6, sx: 0, sy: -0.07 }),
			colFollow: (p: number): Shot => {
				const xc = 0.8 * state(p).xb;
				return P({ az: portrait() ? -30 : -12, el: 14, box: portrait() ? [xc - 32, xc + 40, -34, 10, -8, 8] : [xc - 62, xc + 62, -34, 10, -8, 8], fw: 0.9, fh: 0.62, sx: 0, sy: -0.07 });
			},
			colWide: (): Shot => P({ az: portrait() ? -60 : -14, el: 12, box: portrait() ? [-HALF, HALF, -40, 10, -8, 8] : [-HALF - 10, HALF + 10, -40, 12, -8, 8], fw: 0.9, fh: 0.6, sx: 0, sy: -0.07 }),
			preform: (p: number): Shot => {
				const b = pfBox(p);
				return P({ az: portrait() ? -40 : -22, el: 14, box: b, fw: 0.82, fh: 0.66, sx: 0, sy: -0.06 });
			},
			pfEnd: (p: number): Shot => {
				// the upper end face while the rod turns upright: silica, borosilicate, core rings
				const a = pfAngle(p);
				const ex = -XC * Math.cos(a);
				const ey = -XC * Math.sin(a);
				return P({ az: portrait() ? -38 : -32, el: 34, box: [ex - 10, ex + 10, ey - 22, ey + 5, -6, 6], fw: 0.7, fh: 0.66, sx: portrait() ? 0 : 0.1, sy: -0.08 });
			},
			tip: (): Shot => P({ az: -20, el: 8, box: [-9, 9, -XC - NECK - 70, -XC + 70, -9, 9], fw: 0.6, fh: 0.7, sx: 0, sy: -0.04 }),
			loss: (): Shot => plotShift({ az: -20, el: 8, box: [-9, 9, -XC - NECK - 55, -XC + 45, -9, 9], fw: 0.36, fh: 0.62, sx: -0.25, sy: -0.06 }),
			graded: (): Shot => {
				const top = XC + k * 32;
				return plotShift({ az: -24, el: 52, box: [-PO - 0.3, PO + 0.3, XC - 3, top + 0.5, -PO - 0.3, PO + 0.3], fw: 0.44, fh: 0.62, sx: -0.25, sy: -0.06 });
			}
		};
		/** world box of the preform rod during its rotation to vertical */
		function pfBox(p: number): number[] {
			const a = pfAngle(p);
			const c = Math.cos(a);
			const s = Math.sin(a);
			const ex = Math.abs(c) * XC + PO;
			const ey = Math.abs(s) * XC + PO;
			return [-ex, ex, -ey, ey, -PO, PO];
		}
		const pfAngle = (p: number) => -ease(loc(p, 'preform', 0.3, 0.75)) * Math.PI / 2;
		type Key = [number, (p: number) => Shot];
		const keys: Key[] = [
			[0, sh.intro],
			[at('tube', 0.8), sh.tube],
			[at('lathe', 0.02), sh.tube],
			[at('lathe', 0.5), sh.lathe],
			[at('gases', 0.05), sh.lathe],
			[at('gases', 0.55), sh.gases],
			[at('burner', 0.0), sh.gases],
			[at('burner', 0.35), sh.burner],
			[at('burner', 0.98), sh.burner],
			[at('soot', 0.16), sh.soot],
			[at('soot', 1), sh.soot],
			[at('layers', 0.1), sh.macro],
			[at('layers', 0.82), sh.macro],
			[at('layers', 0.95), sh.layersWide],
			[at('collapse', 0.07), sh.colFollow],
			[at('collapse', 0.5), sh.colFollow],
			[at('collapse', 0.62), sh.colWide],
			[at('collapse', 1), sh.colWide],
			[at('preform', 0.3), sh.preform],
			[at('preform', 0.5), sh.pfEnd],
			[at('preform', 0.78), sh.pfEnd],
			[at('preform', 0.95), sh.tip],
			[at('loss', 0.14), sh.loss],
			[at('loss', 1), sh.loss],
			[at('graded', 0.3), sh.graded],
			[1, sh.graded]
		];
		function shotAt(p: number): Shot {
			let i = 0;
			while (i < keys.length - 1 && p > keys[i + 1][0]) i++;
			const [pa, fa] = keys[i];
			const nx = keys[Math.min(i + 1, keys.length - 1)];
			const A = fa(p);
			if (nx[0] <= pa || p <= pa) return A;
			const B = nx[1](p);
			const t = ease((p - pa) / (nx[0] - pa));
			if (fa === nx[1]) return A;
			const mix = (a: number, b: number) => a + (b - a) * t;
			// boxes: centres blend linearly, half sizes in log so close-ups and wide shots move at a steady visual rate
			const box = [0, 0, 0, 0, 0, 0];
			for (let j = 0; j < 6; j += 2) {
				const ca = (A.box[j] + A.box[j + 1]) / 2;
				const cb = (B.box[j] + B.box[j + 1]) / 2;
				const ha = Math.max(1e-3, (A.box[j + 1] - A.box[j]) / 2);
				const hb = Math.max(1e-3, (B.box[j + 1] - B.box[j]) / 2);
				const hh = Math.exp(Math.log(ha) + (Math.log(hb) - Math.log(ha)) * t);
				box[j] = mix(ca, cb) - hh;
				box[j + 1] = mix(ca, cb) + hh;
			}
			return { az: mix(A.az, B.az), el: mix(A.el, B.el), box, fw: mix(A.fw, B.fw), fh: mix(A.fh, B.fh), sx: mix(A.sx, B.sx), sy: mix(A.sy, B.sy) };
		}
		const vA = new THREE.Vector3();
		const vR = new THREE.Vector3();
		const vU = new THREE.Vector3();
		const vD = new THREE.Vector3();
		function placeCamera(s: Shot) {
			const az = s.az * DEG;
			const el = s.el * DEG;
			vD.set(Math.sin(az) * Math.cos(el), Math.sin(el), Math.cos(az) * Math.cos(el)); // target -> camera
			vR.set(Math.cos(az), 0, -Math.sin(az)); // right
			vU.crossVectors(vD, vR).normalize(); // up
			const [x0, x1, y0, y1, z0, z1] = s.box;
			const cx = (x0 + x1) / 2;
			const cy = (y0 + y1) / 2;
			const cz = (z0 + z1) / 2;
			const tv = Math.tan((camera.fov * DEG) / 2);
			const th = tv * (w / h);
			let d = 1;
			for (const X of [x0, x1])
				for (const Y of [y0, y1])
					for (const Z of [z0, z1]) {
						vA.set(X - cx, Y - cy, Z - cz);
						const xc = vA.dot(vR);
						const yc = vA.dot(vU);
						const zc = vA.dot(vD);
						d = Math.max(d, zc + Math.abs(xc) / (th * s.fw), zc + Math.abs(yc) / (tv * s.fh));
					}
			const px = -s.sx * 2 * d * th;
			const py = -s.sy * 2 * d * tv;
			const tx = cx + vR.x * px + vU.x * py;
			const ty = cy + vR.y * px + vU.y * py;
			const tz = cz + vR.z * px + vU.z * py;
			camera.position.set(tx + vD.x * d, ty + vD.y * d, tz + vD.z * d);
			camera.up.set(0, 1, 0);
			camera.lookAt(tx, ty, tz);
			camera.near = Math.max(0.05, d / 200);
			camera.far = d * 40 + 3000;
			camera.updateProjectionMatrix();
			camera.updateMatrixWorld();
			tgt = [cx, cy, cz];
		}

		// ------------------------------------------------------------------------ frame
		let S: St = state(0);
		const vis: Record<string, number> = {};
		const tmpQ = new THREE.Quaternion();
		const X1 = new THREE.Vector3(1, 0, 0);
		const vP = new THREE.Vector3();
		const vT = new THREE.Vector3();
		function frame(p: number) {
			lastP = p;
			S = state(p);
			const ke = p >= C('tube')[0] && p < at('preform', 0.3) ? k : 0; // lathe explode
			const kp = p >= at('preform', 0.3) ? k : 0; // preform explode

			const heroF = 1 - smooth(at('lathe', 0.3), at('lathe', 0.9), p);
			hero.intensity = 2.6 * heroF;
			heroRim.intensity = 1.8 * heroF;
			// tube flight in (chapter 1)
			const qi = ease(loc(p, 'tube', 0, 0.8));
			tube.position.set((1 - qi) * 230, (1 - qi) * 60, -(1 - qi) * 170);
			tube.rotation.set(0, -(1 - qi) * 0.75, (1 - qi) * 0.22);
			U.uFade.value = 0.35 + 0.65 * smooth(at('tube', 0), at('tube', 0.35), p);
			const swap = p >= at('preform', 0.3);
			tube.visible = !swap;
			pf.visible = swap;

			// tube uniforms
			U.uXb.value = S.xb;
			U.uNb.value = S.nb;
			U.uCur.value = S.cur;
			U.uCd.value = S.cd;
			U.uC0.value = S.c0;
			U.uC1.value = S.c1;
			U.uCx.value = S.cx;
			U.uCut.value = S.cut;
			U.uCw0.value = S.cw0;
			U.uCw1.value = S.cw1;
			U.uStub.value = S.stub;
			U.uGlow.value = S.glow;
			U.uHot.value = S.hot;
			U.uGrade.value = smooth(at('graded', 0.05), at('graded', 0.5), p);
			// section strips sit on the cut planes, the window discs at the window ends
			const half = S.cut * Math.PI / 2;
			const angs = [Math.PI / 2 - half, Math.PI / 2 + half];
			strips.forEach((s, i) => {
				s.pivot.rotation.x = angs[i];
				s.m.material.uniforms.uLen.value = S.cw1 - S.cw0;
				s.m.material.uniforms.uMid.value = (S.cw0 + S.cw1) / 2;
				s.m.visible = S.cut > 0.003 && S.cut < 1.94;
				s.m.material.uniforms.uAlpha.value = (theme === 'light' ? 1 : 0.92) * (1 - smooth(1.6, 1.94, S.cut));
			});
			winDiscs[0].material.uniforms.uFaceX.value = S.cw0;
			winDiscs[1].material.uniforms.uFaceX.value = S.cw1;
			winDiscs[0].visible = S.cut > 0.003 && Math.abs(S.cw0) < END;
			winDiscs[1].visible = S.cut > 0.003 && Math.abs(S.cw1) < END;
			for (const d of endDiscs) d.visible = S.stub > 0.01;
			for (const d of cutDiscs) {
				d.visible = S.stub < 0.99;
				d.material.uniforms.uAlpha.value = (theme === 'light' ? 1 : 0.92) * (1 - S.stub);
			}
			tubeProxy.scale.set(1, bnd(0, S).B0, bnd(0, S).B0);

			// lathe: slides in (chapter 2), retracts (preform)
			const lin = ease(loc(p, 'lathe', 0, 0.55));
			const lout = ease(loc(p, 'preform', 0, 0.3));
			head.position.set(-(1 - lin) * 420 - lout * 260 - ke * 110, 0, 0);
			tail.position.set((1 - lin) * 420 + lout * 260 + ke * 110, 0, 0);
			bed.position.y = -91 - (1 - lin) * 140 - lout * 160 - ke * 60;
			const latheF = smooth(at('lathe', 0), at('lathe', 0.35), p) * (1 - smooth(at('preform', 0.05), at('preform', 0.3), p));
			for (const m of mats.get('lathe') ?? []) fade(m, latheF);
			vis.lathe = latheF;
			// rotation (100 rpm stated; scroll-time is not real time): the arrow turns with p
			const arrowF =
				smooth(at('lathe', 0.55), at('lathe', 0.8), p) *
				(1 - 0.55 * smooth(at('gases', 0.6), at('gases', 0.95), p)) *
				(1 - smooth(at('preform', 0), at('preform', 0.1), p));
			arrowPivot.visible = arrowF > 0.01;
			arrowMat.opacity = 0.85 * arrowF;
			arrowPivot.rotation.x = p * Math.PI * 2 * 14; // same sense as the arrowhead (FIG. 1 arrow 5a)

			// burner: rises (chapter 4), drops away (preform)
			const bin = ease(loc(p, 'burner', 0, 0.3));
			const bout = ease(loc(p, 'preform', 0, 0.25));
			burner.position.set(S.xb, -(1 - bin) * 110 - bout * 140 - ke * 45, 0);
			const burnF = smooth(at('burner', 0), at('burner', 0.2), p) * (1 - smooth(at('preform', 0.05), at('preform', 0.25), p));
			for (const m of mats.get('burner') ?? []) fade(m, burnF);
			screw.position.set(0, -73 - (1 - bin) * 110 - bout * 140 - ke * 70, 42);
			for (const m of mats.get('feed_screw') ?? []) fade(m, burnF);
			vis.burner = burnF;
			vis.feed_screw = burnF;
			// flame + glow
			flame.visible = S.lit > 0.01;
			flameMat.uniforms.uI.value = S.lit * (0.9 + 0.25 * S.hot);
			flameMat.uniforms.uFl.value = p * 900;
			flame.scale.set(1.25 + 0.15 * S.hot, 1 + 0.08 * Math.sin(p * 700), 1.25 + 0.15 * S.hot);
			vis.flame = S.lit;
			const tw = tube.position;
			halo.visible = S.glow > 0.01 && !swap;
			halo.position.set(S.xb + tw.x, -3 + tw.y, 2 + tw.z);
			const hs = (32 + 12 * S.hot) * Math.min(1, S.glow);
			halo.scale.set(hs, hs * 0.75, 1);
			haloMat.opacity = (theme === 'light' ? 0.32 : 0.62) * Math.min(1, S.glow) * (1 - 0.75 * smooth(1.2, 1.9, S.cut));
			hotLight.position.set(S.xb, -14, 18);
			hotLight.intensity = 2.2 * S.glow;
			hotLight.color.set(S.hot > 0.5 ? '#ffc080' : '#ff8a3a');

			// zones 35 / 36 (only drawn when highlighted)
			const bore = bnd(S.xb, S).B3;
			zone35.position.set(S.xb + 4 + 35, 0, 0);
			zone35.scale.set(70, Math.max(0.2, bore * 0.98), Math.max(0.2, bore * 0.98));
			zone36.position.set(S.xb - 4 - 30, 0, 0);
			zone36.scale.set(60, Math.max(0.2, bore * 0.98), Math.max(0.2, bore * 0.98));
			vis.soot = S.lit * S.gas;
			vis.clear_zone = S.lit * S.gas;
			zone35.visible = vis.soot > 0.3;
			zone36.visible = vis.clear_zone > 0.3;
			zoneMat35.opacity = hi.includes('soot') ? 0.16 : 0;
			zoneMat36.opacity = hi.includes('clear_zone') ? 0.16 : 0;

			// gas supply / inlet / outlet: appear with the gases (chapter 3), leave at the preform
			const gin = ease(loc(p, 'gases', 0, 0.35));
			const gF = smooth(at('gases', 0), at('gases', 0.25), p) * (1 - smooth(at('preform', 0.05), at('preform', 0.25), p));
			supply.position.set(-(1 - gin) * 160 - lout * 200 - ke * 90, 0, -ke * 40);
			inletGrp.position.set(-(1 - gin) * 160 - lout * 260 - ke * 70, 0, 0);
			exhGrp.position.set((1 - gin) * 120 + lout * 260 + ke * 110, 0, 0);
			for (const id of ['gas_supply', 'inlet', 'exhaust']) {
				for (const m of mats.get(id) ?? []) fade(m, gF);
				vis[id] = gF;
			}

			// gas streaks (reactants in O2), flow +x
			let emph = lerp(1, 0, smooth(at('soot', 0), at('soot', 0.15), p));
			emph *= 1 - smooth(at('layers', 0), at('layers', 0.06), p) * (1 - smooth(at('layers', 0.9), at('layers', 1), p));
			emph = lerp(emph, 0.35, smooth(at('collapse', 0), at('collapse', 0.1), p));
			const gv = S.gas * gF * emph;
			gasI.visible = gv > 0.01;
			gasMat.opacity = (theme === 'light' ? 0.55 : 0.5) * gv;
			for (let i = 0; i < NG2; i++) {
				const g = gasSeed[i];
				const s = fract(g.u + p * 22) * pathLen;
				let sc = g.ln;
				if (s < inLen) {
					const t = s / inLen;
					inlet.curve.getPointAt(t, vP);
					inlet.curve.getTangentAt(t, vT);
					vP.add(inletGrp.position);
					tmpQ.setFromUnitVectors(X1, vT);
					sc *= 0.5;
				} else if (s < inLen + boreLen) {
					const x = s - inLen - (END - 4);
					const b = bnd(x, S).B3;
					const r = g.r0 * Math.max(0, b - 0.6);
					vP.set(x, r * Math.cos(g.th), r * Math.sin(g.th)).add(tube.position);
					tmpQ.identity();
					if (b < 0.8) sc = 0;
				} else {
					const t = (s - inLen - boreLen) / exLen;
					exh.curve.getPointAt(t, vP);
					exh.curve.getTangentAt(t, vT);
					vP.add(exhGrp.position);
					tmpQ.setFromUnitVectors(X1, vT);
					sc *= 0.8;
				}
				dummy.position.copy(vP);
				dummy.quaternion.copy(tmpQ);
				dummy.scale.set(sc, 1, 1);
				dummy.updateMatrix();
				gasI.setMatrixAt(i, dummy.matrix);
			}
			gasI.instanceMatrix.needsUpdate = true;

			// bubbles in the flasks (O2 bubbled through the liquids)
			bubI.visible = S.gas * gF > 0.01;
			bubMat.opacity = 0.7 * S.gas * gF;
			for (let i = 0; i < NBU; i++) {
				const b = bubSeed[i];
				const a = fract(b.u + p * 30);
				dummy.position.set(flaskX[b.f] - 6 + b.dx * a, -98 + a * 24, b.dz * a);
				dummy.quaternion.identity();
				const s = b.s * (0.6 + 0.6 * a) * (a < 0.95 ? 1 : 0);
				dummy.scale.set(s, s, s);
				dummy.updateMatrix();
				bubI.setMatrixAt(i, dummy.matrix);
			}
			bubI.instanceMatrix.needsUpdate = true;

			// soot cloud: forms in the hot zone, drifts downstream (+x) and out to the wall where it settles
			const sv = S.lit * S.gas * (1 - S.hot * 0.4);
			soot.visible = sv > 0.01 && !swap;
			sootMat.opacity = 0.95 * Math.min(1, sv);
			const col = new THREE.Color();
			for (let i = 0; i < NS; i++) {
				const q = sootSeed[i];
				const a = fract(q.u + p * 46 * q.sp);
				const x = S.xb + 1 + a * 66;
				const b = bnd(x, S).B3;
				const rr = lerp(q.r0 * b * 0.7, b * 0.97, a ** 1.6);
				const th = q.th + a * 0.6;
				dummy.position.set(x, rr * Math.cos(th), rr * Math.sin(th));
				dummy.quaternion.identity();
				const removed = S.cut > 0.003 && x > S.cw0 && x < S.cw1 && Math.abs(wrapPi(th - Math.PI / 2)) < (S.cut * Math.PI) / 2;
				const s = q.sz * smooth(0, 0.06, a) * (1 - smooth(0.82, 1, a)) * (b > 0.6 && !removed ? 1 : 0);
				dummy.scale.set(s, s, s);
				dummy.updateMatrix();
				soot.setMatrixAt(i, dummy.matrix);
				col.copy(hotCol).lerp(sootCol, smooth(0, 0.35, a));
				soot.setColorAt(i, col);
			}
			soot.instanceMatrix.needsUpdate = true;
			if (soot.instanceColor) soot.instanceColor.needsUpdate = true;

			// preform: rotates to vertical, neck forms at the lower end, fiber is drawn
			pf.rotation.set(0, 0, pfAngle(p));
			const grade = U.uGrade.value;
			const barC = U.uBarCol.value;
			const coreC = U.uCoreCol.value;
			const deep = U.uCoreDeep.value;
			for (const s of sleeves) {
				let off = 0;
				if (s.idx === 1) off = -kp * 5;
				if (s.idx >= 2) off = -kp * (9 + 2.4 * (s.idx - 2));
				s.side.parent!.position.x = off;
				if (s.idx === 0) s.capMat.color.copy(U.uTubeCol.value);
				else if (s.idx === 1) s.capMat.color.copy(barC);
				else s.capMat.color.copy(coreC).lerp(col.copy(barC).lerp(deep, (s.idx - 1) / NG), grade);
				s.capMat.opacity = s.idx === 0 ? 0.7 : 0.97;
				if (s.idx >= 2) s.mat.color.copy(s.capMat.color);
				// inner core ring sides only show when the rings are pulled apart
				if (s.idx >= 3) fade(s.mat, smooth(0, 0.12, kp));
			}
			const fadeOn = smooth(at('loss', 0), at('loss', 0.15), p) * (1 - smooth(at('graded', 0), at('graded', 0.4), p));
			FY.uFy0.value = lerp(XC + 80, -XC + 12, fadeOn);
			FY.uFy1.value = FY.uFy0.value + 70;
			// graded: the rod below the end face fades out (keeps the face alone beside the plot)
			const fadeLo = smooth(at('graded', 0.15), at('graded', 0.45), p);
			FY.uFl0.value = lerp(-XC - 400, XC - (portrait() ? 62 : 70), fadeLo);
			FY.uFl1.value = FY.uFl0.value + 55;
			const nk = smooth(at('preform', 0.72), at('loss', 0.4), p);
			neck.visible = nk > 0.01;
			neck.scale.set(Math.max(0.02, nk), 1, 1);
			neckMat.emissiveIntensity = 0.55 * nk * (1 - 0.6 * smooth(at('graded', 0), at('graded', 0.4), p));
			sleeves.forEach((s) => (s.cap2.visible = nk < 0.02));
			const flMax = portrait() ? 45 : 150;
			const fl = flMax * smooth(at('preform', 0.86), at('loss', 0.3), p);
			const fx0 = XC + NECK * nk;
			const fp = fiberGeo.attributes.position as T.BufferAttribute;
			fp.setXYZ(0, fx0, 0, 0);
			fp.setXYZ(1, fx0 + Math.max(0.01, fl * 0.45), 0, 0);
			fp.setXYZ(2, fx0 + Math.max(0.02, fl), 0, 0);
			fp.needsUpdate = true;
			fiber.visible = fl > 0.5;
			vis.fiber = nk > 0.01 ? 1 : 0;
			const gl = fract(p * 120);
			const gp = glintGeo.attributes.position as T.BufferAttribute;
			gp.setXYZ(0, fx0 + gl * fl, 0, 0);
			gp.setXYZ(1, fx0 + Math.min(fl, gl * fl + 14), 0, 0);
			gp.needsUpdate = true;
			glint.visible = fl > 20;
			glintMat.opacity = 0.9 * (1 - gl);
			vis.preform = swap ? 1 : smooth(0.6, 0.95, (S.c0 + S.c1) / 2);
			vis.substrate_tube = swap ? 0 : U.uFade.value;
			vis.barrier_layer = swap ? 1 : S.nb > 0 ? 1 : 0;
			vis.core_layers = swap ? 1 : S.cd > 0 || S.cur === 2 ? 1 : 0;

			// camera
			placeCamera(shotAt(p));
			applyHi();
		}

		// ------------------------------------------------------------------------ highlight / pick / anchors
		function applyHi() {
			const on = (id: string) => (hi.includes(id) ? 1 : 0);
			U.uHi.value.set(on('substrate_tube'), on('barrier_layer'), on('core_layers'), on('preform'));
			for (const [id, list] of mats) for (const m of list) m.emissive?.set(on(id) ? accent : '#000000').multiplyScalar(on(id) ? 0.45 : 1);
			neckMat.emissive.set(on('fiber') ? accent : '#ff7a2a');
			fiberMat.color.set(on('fiber') ? accent : theme === 'light' ? '#2f6fb0' : '#e8f4ff');
			flameMat.uniforms.uI.value = S.lit * (0.9 + 0.25 * S.hot) * (on('flame') ? 1.6 : 1);
			arrowMat.color.set(theme === 'light' ? '#5b6570' : '#cfd6de');
		}

		const ray = new THREE.Raycaster();
		ray.params.Line = { threshold: 1.5 };
		const ndc = new THREE.Vector2();
		const lp = new THREE.Vector3();
		function pick(x: number, y: number): string | null {
			ndc.set((x / w) * 2 - 1, 1 - (y / h) * 2);
			ray.setFromCamera(ndc, camera);
			const cands: T.Object3D[] = [];
			const add = (o: T.Object3D, id: string) => {
				if ((vis[id] ?? 1) > 0.3) cands.push(o);
			};
			if (tube.visible) {
				add(tubeProxy, 'substrate_tube');
				for (const s of strips) if (s.m.visible) cands.push(s.m);
				for (const d of [...winDiscs, ...endDiscs, ...cutDiscs]) if (d.visible) cands.push(d);
				if (zone35.visible) cands.push(zone35);
				if (zone36.visible) cands.push(zone36);
			}
			lathe.traverse((o) => (o as T.Mesh).isMesh && add(o, 'lathe'));
			burner.traverse((o) => (o as T.Mesh).isMesh && add(o, 'burner'));
			add(screw, 'feed_screw');
			supply.traverse((o) => (o as T.Mesh).isMesh && add(o, 'gas_supply'));
			inletGrp.traverse((o) => (o as T.Mesh).isMesh && add(o, 'inlet'));
			exhGrp.traverse((o) => (o as T.Mesh).isMesh && add(o, 'exhaust'));
			if (pf.visible) pf.traverse((o) => ((o as T.Mesh).isMesh || (o as T.Line).isLine) && o.visible && o !== glint && cands.push(o));
			const hits = ray.intersectObjects(cands, false);
			const secObjs: T.Object3D[] = [...strips.map((s) => s.m), ...winDiscs, ...endDiscs, ...cutDiscs];
			for (const hit of hits) {
				const o = hit.object;
				if (o === tubeProxy || secObjs.includes(o)) {
					tube.worldToLocal(lp.copy(hit.point));
					const r = Math.hypot(lp.y, lp.z);
					const az = wrapPi(Math.atan2(lp.z, lp.y) - Math.PI / 2);
					const inCut = S.cut > 0.003 && lp.x > S.cw0 && lp.x < S.cw1 && Math.abs(az) < (S.cut * Math.PI) / 2;
					if (o === tubeProxy) {
						if (inCut) continue;
						if (S.glow > 0.3 && Math.abs(lp.x - S.xb) < 14) return 'flame'; // the glowing band = hot zone 32
						return colAt(lp.x, S) > 0.85 ? 'preform' : 'substrate_tube';
					}
					const b = bnd(lp.x, S);
					if (r > b.B0 + 0.05 || r < b.B3 - 0.05) continue;
					if (b.e > 0.85) return r > b.B1 ? 'preform' : r > b.B2 ? 'barrier_layer' : 'core_layers';
					return r > b.B1 ? 'substrate_tube' : r > b.B2 ? 'barrier_layer' : 'core_layers';
				}
				if (o === zone35) return 'soot';
				if (o === zone36) return 'clear_zone';
				const id = o.userData.part as string | undefined;
				if (id) return id;
			}
			return null;
		}

		const va = new THREE.Vector3();
		function anchor(id: string): [number, number] | null {
			if ((vis[id] ?? 0) < 0.5) return null;
			const swap = lastP >= at('preform', 0.3);
			switch (id) {
				case 'substrate_tube':
					if (swap || colAt(0, S) > 0.5) return null;
					va.set(110, RO + 2, 0);
					tube.localToWorld(va);
					break;
				case 'burner':
					va.set(20, -40, 18);
					burner.localToWorld(va);
					break;
				case 'soot':
					if (S.cut < 0.5) return null;
					va.set(S.xb + 24, RO + 3, 0);
					tube.localToWorld(va);
					break;
				case 'preform':
					if (!swap) {
						if (colAt(-60, S) < 0.95) return null;
						va.set(-60, PO + 1, 0);
						tube.localToWorld(va);
					} else {
						va.set(-60, PO + 1, 0);
						pf.localToWorld(va);
					}
					break;
				default:
					return null;
			}
			va.project(camera);
			if (va.z > 1) return null;
			const ax = ((va.x + 1) / 2) * w;
			const ay = ((1 - va.y) / 2) * h;
			// the label reads to the right of the point: keep it inside the pane
			if (ax < 4 || ax > w - 170 || ay < 8 || ay > h - 12) return null;
			return [ax, ay];
		}

		return {
			assembledAt: C('lathe')[1],
			frame,
			highlight(ids) {
				hi = [...ids];
				applyHi();
			},
			pick,
			resize(nw, nh) {
				w = Math.max(1, nw);
				h = Math.max(1, nh);
			},
			explode(nk) {
				k = clamp01(nk);
			},
			anchor,
			target: () => tgt,
			theme(t) {
				theme = t;
				applyTheme();
				frame(lastP);
			},
			dispose() {
				scene.remove(root);
				for (const d of disposables) d.dispose();
				soot.dispose();
				gasI.dispose();
				bubI.dispose();
			}
		} satisfies ShowcaseHandle;
	}
};

export default mod;
