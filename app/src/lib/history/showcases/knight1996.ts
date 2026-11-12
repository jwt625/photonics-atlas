// Photonic crystal fiber, three-stage stack-and-draw (knight1996). Scene module: contract in ../showcase/types.ts.
//
// Source (spec data/history/showcases/knight1996.yaml): Knight, Birks, Russell, Atkin, Opt. Lett. 21, 1547 (1996).
// Stated: 30 mm silica rod, 16 mm hole down its length, six flats milled to a regular hexagon, drawn on a fiber drawing
// tower (~2000 C, first draw) to 0.8 mm hexagonal cane, cut and stacked with one solid cane at the center, the stack
// drawn again (canes fused, pitch ~50 um), a piece drawn down again to fiber (pitch 2.3 um, 38 um flat-to-flat, core
// 4.6 um); test: four lasers, objective, 1 m fiber, index-matching fluid, vidicon with a 60x objective (near field
// Fig. 2(a), 632.8 nm), sheet of paper several centimeters away (far field: central spot plus six spots).
// Figure + derived: 9 rings (271 canes) counted from Fig. 1; outer flats parallel to the rows of holes. Ref: hole
// d / pitch about 0.15 (Birks et al. 1997). Assumed (labelled where shown): hexagon at the 26.0 mm bound, rod length,
// vertical downward draw, neck shapes, furnace stand-in size, fluid position, bench boxes and distances, the hole
// proportion kept through the first two draws (shrinks only in the final draw, as the paper describes).
// Withheld and not drawn: loss, tower construction, draw temperatures (the glow encodes none), cane and stack lengths
// (pieces fade out along their length or run out of frame), far-field angular scale (spots at one schematic size).
//
// Everything is a pure function of p (and the stored explode k).
import type * as T from 'three';
import type { Chapter, PartLook, PickInfo, ShowcaseContext3D, ShowcaseHandle, ShowcaseModule, Theme } from '../showcase/types';
import { clamp01, ease, lerp, seg } from '../showcase/progress';
import { revealAt } from '../showcase/plot';

const DEG = Math.PI / 180;
const S3 = Math.sqrt(3);
const smooth = (a: number, b: number, x: number) => {
	const t = clamp01((x - a) / (b - a));
	return t * t * (3 - 2 * t);
};

// ------------------------------------------------------------------------------------------------ geometry (mm)
const ROD_R = 15; // 30 mm rod, stated
const HOLE_R = 8; // 16 mm hole, stated
const HEX_F = 30 * Math.cos(30 * DEG); // 25.98 mm: upper bound of the milled hexagon (assumed, drawn at the bound)
const ROD_L = 100; // rod length not stated (visual)
const YR = 40; // rod bottom in the first two chapters
const HOLE_RATIO = (2 * HOLE_R) / HEX_F; // 0.62, kept in the first draw (assumed)
const CANE_F = 0.8; // stated (0.8 mm, as printed)
const RINGS = 9; // counted from Fig. 1 (figure + derived)
const STACK_F = 16.5 * CANE_F; // 13.2 mm across the flats (derived)
const FUSED_F = 0.8; // about 0.8 mm (derived estimate: 16.5 x 50 um)
const FIB_F = 0.038; // 38 um, stated
const PITCH_UM = 2.3; // stated
const HOLE_UM = 0.35; // d / pitch about 0.15 (ref)
const FIB_F_UM = 38;
const LC = 70; // drawn cane length in the stack (fades out from LC_F0 back: no cane end is drawn)
const LC_F0 = 22;
// furnace stand-in (visual), drawn cut away toward the camera
const FUR_RI = 24;
const FUR_RO = 31;
const FUR_H = 44;
const HOT_Y = -4; // hot zone centre (visual)
// stack set (beside the tower), bench output end (the fiber end face)
const S0: [number, number, number] = [0, 75, 90];
const BO: [number, number, number] = [0, -30, 0];
// bench (visual stand-ins, distances not stated)
const Z_IN = -170; // fiber input end
const Z_BRK = -86; // drawn break (1 m fiber shortened)
const Z_FL0 = -150; // index-matching fluid (position assumed)
const Z_FL1 = -126;
const Z_OBJ = -186; // launch objective centre
const Z_LAS = -240; // laser box centre
const Z_VID = 48; // vidicon box centre
const Z_PAPER = 45; // sheet of paper (several centimeters, not stated exactly)
// light cone to the paper: half-angle 20.7 deg (sin 0.35), inside the largest printed output NA (0.36 at 1550 nm)
const FF_CONE_R = 17;

// laser lines (stated), drawn colours; 850 / 1550 nm are infrared: neutral greys as false colour (no visible hue)
const LINES = [
	{ nm: 457.9, name: 'argon-ion', col: '#4f7dff', ir: false },
	{ nm: 632.8, name: 'He-Ne', col: '#ff3a2a', ir: false },
	{ nm: 850, name: 'Ti:sapphire', col: '#c9c2bb', ir: true },
	{ nm: 1550, name: 'diode', col: '#8f969d', ir: true }
];

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

/** triangular lattice sites up to `rings` (pitch units), rows along x; ring = hexagonal distance from the centre */
function latticeSites(rings: number) {
	const out: { x: number; y: number; ring: number; ang: number }[] = [];
	for (let i = -rings; i <= rings; i++)
		for (let j = -rings; j <= rings; j++) {
			const ring = (Math.abs(i) + Math.abs(j) + Math.abs(i + j)) / 2;
			if (ring > rings) continue;
			const x = i + j / 2;
			const y = (j * S3) / 2;
			out.push({ x, y, ring, ang: Math.atan2(y, x) });
		}
	out.sort((a, b) => a.ring - b.ring || a.ang - b.ang);
	return out;
}
const SITES = latticeSites(RINGS); // 271

/** point on a hexagon perimeter (flat-to-flat F, first vertex at angle rot), u in [0, 1) */
function hexAt(u: number, F: number, rot: number): [number, number] {
	const R = F / S3;
	const f = (((u % 1) + 1) % 1) * 6;
	const s = Math.floor(f);
	const t = f - s;
	const a0 = rot + s * 60 * DEG;
	const a1 = a0 + 60 * DEG;
	return [R * lerp(Math.cos(a0), Math.cos(a1), t), R * lerp(Math.sin(a0), Math.sin(a1), t)];
}

const mod: ShowcaseModule = {
	renderer: '3d',
	build(ctx0) {
		const ctx = ctx0 as ShowcaseContext3D;
		const { THREE, scene, camera, spec } = ctx;
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

		// chapters
		const DEF: Record<string, [number, number]> = {
			rod: [0, 0.08], flats: [0.08, 0.16], cane: [0.16, 0.27], stack: [0.27, 0.39], fuse: [0.39, 0.49],
			fiber: [0.49, 0.59], lattice: [0.59, 0.7], launch: [0.7, 0.79], near_field: [0.79, 0.89], single_mode: [0.89, 1]
		};
		const C = (id: string): [number, number] => spec.chapters.find((c: Chapter) => c.id === id)?.p ?? DEF[id];
		const at = (id: string, q: number) => {
			const [a, b] = C(id);
			return a + (b - a) * q;
		};
		const loc = (p: number, id: string, q0 = 0, q1 = 1) => seg(p, at(id, q0), at(id, q1));
		const after = (p: number, id: string) => p >= C(id)[0];

		// ------------------------------------------------------------------------ materials
		const partLook = (id: string): PartLook => spec.parts.find((q) => q.id === id)?.look ?? {};
		const accent = new THREE.Color('#3987e5');
		const mats = new Map<string, T.Material[]>();
		const baseOpacity = new Map<T.Material, number>();
		const reg = <M extends T.Material>(id: string, m: M): M => {
			keep(m);
			baseOpacity.set(m, m.opacity);
			if (!mats.has(id)) mats.set(id, []);
			mats.get(id)!.push(m);
			return m;
		};
		function fade(m: T.Material, f: number) {
			m.opacity = (baseOpacity.get(m) ?? 1) * f;
			m.visible = f > 0.002;
		}
		// shared hot-zone glow (world y), physical light only
		const G = { uGlow: { value: 0 }, uHy: { value: HOT_Y }, uHs: { value: 11 }, uGlowCol: { value: new THREE.Color('#ff7a2a') } };
		interface GlassU {
			uAx: { value: T.Vector3 };
			uF0: { value: number };
			uF1: { value: number };
			uN0: { value: number };
			uN1: { value: number };
			uNk: { value: number };
			uFres: { value: number };
		}
		const glassU = new Map<T.Material, GlassU>();
		/** glass: fresnel rim, axial fade (geometry-local axis: alpha falls from uF0 to uF1), near-face fade, hot-zone glow */
		function glass(id: string, o: T.MeshStandardMaterialParameters = {}, fres = 0.45) {
			const l = partLook(id);
			const m = new THREE.MeshStandardMaterial({
				color: l.color ?? '#dfe9ee', metalness: 0, roughness: l.rough ?? 0.1, transparent: true,
				opacity: l.opacity ?? 0.5, depthWrite: false, side: THREE.DoubleSide, envMapIntensity: 1.4, ...o
			});
			const u: GlassU = {
				uAx: { value: new THREE.Vector3(0, 0, -1) }, uF0: { value: 1e5 }, uF1: { value: 2e5 },
				uN0: { value: -1 }, uN1: { value: 0 }, uNk: { value: 0 }, uFres: { value: fres }
			};
			glassU.set(m, u);
			m.onBeforeCompile = (sh) => {
				Object.assign(sh.uniforms, G, u);
				sh.vertexShader = sh.vertexShader
					.replace('#include <common>', '#include <common>\nuniform vec3 uAx; varying float vS; varying float vWy;')
					.replace(
						'#include <project_vertex>',
						`#include <project_vertex>
						{ vec4 wp_ = vec4(transformed, 1.0);
						#ifdef USE_INSTANCING
						wp_ = instanceMatrix * wp_;
						#endif
						vS = dot(wp_.xyz, uAx);
						vWy = (modelMatrix * wp_).y; }`
					);
				sh.fragmentShader = sh.fragmentShader
					.replace(
						'#include <common>',
						'#include <common>\nuniform float uF0, uF1, uN0, uN1, uNk, uFres, uGlow, uHy, uHs; uniform vec3 uGlowCol; varying float vS; varying float vWy;'
					)
					.replace(
						'#include <opaque_fragment>',
						`{ float fr_ = pow(1.0 - clamp(abs(dot(normalize(vViewPosition), normal)), 0.0, 1.0), 2.5);
						  diffuseColor.a = clamp(diffuseColor.a + uFres * fr_, 0.0, 1.0);
						  outgoingLight += vec3(uFres * 0.4 * fr_);
						  float f_ = clamp((vS - uF0) / (uF1 - uF0), 0.0, 1.0);
						  float n_ = clamp((vS - uN0) / (uN1 - uN0), 0.0, 1.0);
						  float k_ = (1.0 - f_ * f_ * (3.0 - 2.0 * f_)) * mix(1.0, n_ * n_ * (3.0 - 2.0 * n_), uNk);
						  float d_ = (vWy - uHy) / uHs; float g_ = uGlow * exp(-0.5 * d_ * d_);
						  outgoingLight += uGlowCol * g_ * 1.6; diffuseColor.a = clamp(diffuseColor.a + 0.5 * g_, 0.0, 1.0) * k_; }
						#include <opaque_fragment>`
					);
			};
			// one program for every glass material (fresnel strength is a uniform): fewer first-use compiles
			m.customProgramCacheKey = () => 'pcf-glass';
			return reg(id, m);
		}
		function std(id: string, o: T.MeshStandardMaterialParameters = {}) {
			const l = partLook(id);
			return reg(
				id,
				new THREE.MeshStandardMaterial({ color: l.color ?? '#8a9099', metalness: l.metal ?? 0, roughness: l.rough ?? 0.5, transparent: true, opacity: l.opacity ?? 1, ...o })
			);
		}
		const setFade = (m: T.Material, f0: number, f1: number, ax?: [number, number, number]) => {
			const u = glassU.get(m)!;
			u.uF0.value = f0;
			u.uF1.value = f1;
			if (ax) u.uAx.value.set(...ax);
		};
		const tag = <O extends T.Object3D>(o: O, part: string, info?: () => PickInfo): O => {
			o.userData.part = part;
			if (info) o.userData.info = info;
			return o;
		};

		// ------------------------------------------------------------------------ shapes
		function hexShape(F: number, rot: number, holeR = 0) {
			const s = new THREE.Shape();
			const R = F / S3;
			for (let i = 0; i < 6; i++) {
				const a = rot + i * 60 * DEG;
				if (i === 0) s.moveTo(R * Math.cos(a), R * Math.sin(a));
				else s.lineTo(R * Math.cos(a), R * Math.sin(a));
			}
			s.closePath();
			if (holeR > 0) {
				const hp = new THREE.Path();
				hp.absarc(0, 0, holeR, 0, Math.PI * 2, true);
				s.holes.push(hp);
			}
			return s;
		}
		/** prism along +z from 0 to L of a shape, then oriented: 'up' = y in [0, L]; 'down' = y in [0, -L]; 'back' = z in [-L, 0] */
		function prism(shape: T.Shape, L: number, dir: 'up' | 'down' | 'back', seg = 32) {
			const g = new THREE.ExtrudeGeometry(shape, { depth: L, bevelEnabled: false, curveSegments: seg });
			if (dir === 'up') g.rotateX(-Math.PI / 2);
			else if (dir === 'down') g.rotateX(Math.PI / 2);
			else g.translate(0, 0, -L);
			return keep(g);
		}

		// ------------------------------------------------------------------------ chapters 1-3: rod, flats, first draw
		const rodG = new THREE.Group();
		root.add(rodG);
		const rodMat = glass('rod');
		const rodRound = tag(new THREE.Mesh(keep(new THREE.BufferGeometry()), rodMat), 'rod', () => rodInfo());
		rodG.add(rodRound);
		let boreKey = -1;
		function setBore(D: number) {
			const key = Math.round(D * 10);
			if (key === boreKey) return;
			boreKey = key;
			const d = Math.max(0.01, D);
			const pts = [
				new THREE.Vector2(0.001, 0), new THREE.Vector2(ROD_R, 0), new THREE.Vector2(ROD_R, ROD_L), new THREE.Vector2(HOLE_R, ROD_L),
				new THREE.Vector2(HOLE_R, ROD_L - d), new THREE.Vector2(0.001, ROD_L - d)
			];
			const g = new THREE.LatheGeometry(pts, 72);
			rodRound.geometry.dispose();
			rodRound.geometry = g;
		}
		setBore(0);
		const hexRot = 30 * DEG; // preform and cane: vertices at 30, 90, ... deg (flats face the lattice neighbours later)
		const rodHex = tag(new THREE.Mesh(prism(hexShape(HEX_F, hexRot, HOLE_R), ROD_L, 'up', 48), rodMat), 'rod', () => rodInfo());
		rodG.add(rodHex);
		// six circular segments between the circle and the flats (corners on the 30 mm surface)
		const slabMat = glass('rod');
		const slabs: T.Mesh[] = [];
		for (let i = 0; i < 6; i++) {
			const phi = hexRot + 30 * DEG + i * 60 * DEG; // flat normal (between two vertices)
			const s = new THREE.Shape();
			const a0 = phi - 30 * DEG;
			s.moveTo(ROD_R * Math.cos(a0), ROD_R * Math.sin(a0));
			s.absarc(0, 0, ROD_R, a0, phi + 30 * DEG, false);
			s.closePath();
			const m = tag(new THREE.Mesh(prism(s, ROD_L, 'up', 16), slabMat), 'rod', () => ({
				id: 'milled_flat',
				label: 'milled-off segment',
				detail: [
					'Six flats milled on the outside, forming a regular hexagon (stated, Knight et al., Opt. Lett. 1996, p.1547)',
					'Flat-to-flat drawn at the 26.0 mm upper bound, corners on the 30 mm surface: assumed, not stated',
					'Drawn as one piece for clarity; milling removes it as chips'
				]
			}));
			m.userData.phi = phi;
			slabs.push(m);
			rodG.add(m);
		}
		const rodInfo = (): PickInfo => ({
			id: 'rod',
			label: 'silica rod',
			detail: lastP >= C('flats')[0]
				? ['30 mm rod, 16 mm hole, six flats (stated)', 'Hexagon drawn at the 26.0 mm upper bound: assumed', 'Rod length not stated: visual']
				: ['30 mm diameter, 16 mm hole down its length (stated)', 'Rod length not stated: visual']
		});

		// furnace stand-in: a ring drawn cut away toward the camera, glowing hot zone inside
		const furG = new THREE.Group();
		root.add(furG);
		const furMat = std('tower', { side: THREE.DoubleSide });
		const CUT = 140 * DEG; // open sector
		const furTheta = Math.PI * 2 - CUT;
		const furOut = tag(new THREE.Mesh(keep(new THREE.CylinderGeometry(FUR_RO, FUR_RO, FUR_H, 64, 1, true, CUT / 2, furTheta)), furMat), 'tower', () => towerInfo());
		const furIn = tag(new THREE.Mesh(keep(new THREE.CylinderGeometry(FUR_RI, FUR_RI, FUR_H, 64, 1, true, CUT / 2, furTheta)), furMat), 'tower', () => towerInfo());
		const ringGeo = keep(new THREE.RingGeometry(FUR_RI, FUR_RO, 64, 1, CUT / 2 - Math.PI / 2, furTheta));
		const capT = tag(new THREE.Mesh(ringGeo, furMat), 'tower', () => towerInfo());
		capT.rotation.x = -Math.PI / 2;
		capT.position.y = FUR_H / 2;
		const capB = tag(new THREE.Mesh(ringGeo, furMat), 'tower', () => towerInfo());
		capB.rotation.x = -Math.PI / 2;
		capB.position.y = -FUR_H / 2;
		// glowing lining (physical light): inner face just inside the bore
		const hzMat = keep(new THREE.MeshBasicMaterial({ color: '#ff7a2a', transparent: true, opacity: 0, side: THREE.BackSide, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false }));
		const hzCanvas = document.createElement('canvas');
		hzCanvas.width = 4;
		hzCanvas.height = 128;
		{
			const c2 = hzCanvas.getContext('2d')!;
			const gr = c2.createLinearGradient(0, 0, 0, 128);
			gr.addColorStop(0, '#000');
			gr.addColorStop(0.5 - HOT_Y / FUR_H, '#fff');
			gr.addColorStop(1, '#000');
			c2.fillStyle = gr;
			c2.fillRect(0, 0, 4, 128);
		}
		const hzTex = keep(new THREE.CanvasTexture(hzCanvas));
		hzMat.alphaMap = hzTex;
		const hz = tag(new THREE.Mesh(keep(new THREE.CylinderGeometry(FUR_RI - 0.3, FUR_RI - 0.3, FUR_H, 64, 1, true, CUT / 2, furTheta)), hzMat), 'hot_zone', () => hotInfo());
		furG.add(furOut, furIn, capT, capB, hz);
		const towerInfo = (): PickInfo => ({
			id: 'tower',
			label: 'fiber drawing tower (stand-in)',
			detail: [
				'The paper names the tower for the first two draws; the final draw is "drawn down again" (furnace stated)',
				'Plain furnace ring, drawn cut away; size visual',
				'Vertical, downward draw: assumed (feed and draw directions not stated)',
				'Tower construction, furnace type, speeds and tension not stated'
			]
		});
		const hotInfo = (): PickInfo => ({
			id: 'hot_zone',
			label: 'furnace hot zone (stand-in)',
			detail: [
				'About 2000 °C for the first draw (stated, p.1547); temperatures of the second and third draws not stated',
				'The glow shows heat, not a temperature',
				'Vertical, downward draw: assumed (feed and draw directions not stated)'
			]
		});

		// generic neck: tapered hexagon (optionally with a round bore), rebuilt in place from p
		class Neck {
			geo = keep(new THREE.BufferGeometry());
			mesh: T.Mesh;
			NJ = 28;
			M = 48;
			constructor(public Fin: number, public Fout: number, public H: number, public rot: number, public holeRatio: number, mat: T.Material) {
				const nv = (this.NJ + 1) * (this.M + 1) * (holeRatio > 0 ? 2 : 1);
				this.geo.setAttribute('position', new THREE.Float32BufferAttribute(new Float32Array(nv * 3), 3));
				const idx: number[] = [];
				const surf = holeRatio > 0 ? 2 : 1;
				for (let s = 0; s < surf; s++) {
					const o = s * (this.NJ + 1) * (this.M + 1);
					for (let j = 0; j < this.NJ; j++)
						for (let i = 0; i < this.M; i++) {
							const a = o + j * (this.M + 1) + i;
							const b = a + this.M + 1;
							if (s === 0) idx.push(a, b, a + 1, a + 1, b, b + 1);
							else idx.push(a, a + 1, b, a + 1, b + 1, b);
						}
				}
				this.geo.setIndex(idx);
				this.mesh = new THREE.Mesh(this.geo, mat);
				this.mesh.frustumCulled = false;
			}
			/** neck from y0 downward; d in [0, 1] = development (0: blunt end, 1: full neck to Fout); returns the bottom y */
			update(y0: number, d: number): number {
				const ed = ease(d);
				const Hd = this.H * (0.08 + 0.92 * ed);
				const Fo = lerp(this.Fin, this.Fout, ed);
				const pos = this.geo.getAttribute('position') as T.BufferAttribute;
				const arr = pos.array as Float32Array;
				let n = 0;
				const surf = this.holeRatio > 0 ? 2 : 1;
				for (let s = 0; s < surf; s++)
					for (let j = 0; j <= this.NJ; j++) {
						const t = j / this.NJ;
						// log-space blend: the taper reads smooth from 26 mm to 0.8 mm (and 0.8 mm to 38 um)
						const g = 0.5 * (1 + Math.cos(Math.PI * t));
						const F = Math.exp(Math.log(Fo) + (Math.log(this.Fin) - Math.log(Fo)) * g);
						const y = y0 - t * Hd;
						for (let i = 0; i <= this.M; i++) {
							const u = i / this.M;
							let a: number;
							let b: number;
							if (s === 0) [a, b] = hexAt(u, F, this.rot);
							else {
								const r = (this.holeRatio * F) / 2;
								a = r * Math.cos(u * Math.PI * 2 + this.rot);
								b = r * Math.sin(u * Math.PI * 2 + this.rot);
							}
							arr[n++] = a;
							arr[n++] = y;
							arr[n++] = -b;
						}
					}
				pos.needsUpdate = true;
				this.geo.computeVertexNormals();
				return y0 - Hd;
			}
		}
		const neckInfo = (extra: string[] = []): PickInfo => ({
			id: 'neck',
			label: 'neck-down in the hot zone',
			detail: ['Neck shape and length: visual (not stated)', ...extra]
		});
		// draw 1: preform -> cane
		const neck1Mat = glass('rod');
		const neck1 = new Neck(HEX_F, CANE_F, 34, hexRot, HOLE_RATIO, neck1Mat);
		tag(neck1.mesh, 'neck', () => neckInfo(['Hole kept at the preform proportion in this draw: assumed']));
		root.add(neck1.mesh);
		const caneMat = glass('cane');
		const caneGeo = prism(hexShape(CANE_F, hexRot, (HOLE_RATIO * CANE_F) / 2), 1, 'down', 20);
		const caneInfo = (): PickInfo => ({
			id: 'cane',
			label: 'hexagonal cane, cut to length',
			detail: ['0.8 mm "diameter" as printed; the paper does not say flat-to-flat or corner-to-corner: drawn across the flats (assumed)', 'Hole drawn at the preform proportion: assumed', 'Cut length not stated: the piece runs out of frame']
		});
		const caneOut = tag(new THREE.Mesh(caneGeo, caneMat), 'cane', caneInfo);
		const canePiece = tag(new THREE.Mesh(caneGeo, caneMat), 'cane', caneInfo);
		root.add(caneOut, canePiece);

		// ------------------------------------------------------------------------ chapter 4-5: stack, second draw
		const stackG = new THREE.Group();
		root.add(stackG);
		const stackMat = glass('stack', { opacity: Math.min(0.5, partLook('stack').opacity ?? 0.5) }, 0.35);
		const stackGeo = prism(hexShape(CANE_F * 0.985, hexRot, (HOLE_RATIO * CANE_F) / 2), LC, 'back', 16);
		const hollow = SITES.filter((s) => s.ring > 0);
		const stackInfo = (): PickInfo => ({
			id: 'stack',
			label: 'stack',
			detail: [
				'9 rings, 271 canes (270 hollow, 1 solid): counted from Fig. 1 and checked against the printed widths; the paper gives no count (figure + derived)',
				'Outer flats parallel to the rows of canes (Fig. 1)',
				'Cane length not stated: the canes fade out along their length',
				'Built end-on and stood upright for the second draw: assumed (not stated)'
			]
		});
		const canes = tag(new THREE.InstancedMesh(stackGeo, stackMat, hollow.length), 'stack', stackInfo);
		canes.frustumCulled = false;
		stackG.add(canes);
		const solidMat = glass('solid_cane', {}, 0.35);
		const solid = tag(new THREE.Mesh(prism(hexShape(CANE_F * 0.985, hexRot), LC, 'back', 6), solidMat), 'solid_cane', () => ({
			id: 'solid_cane',
			label: 'solid cane',
			detail: ['One hollow cane replaced by a similar cane without a hole, at the center (stated, p.1547)']
		}));
		stackG.add(solid);
		const flyR = rng(1996);
		const fly = hollow.map(() => ({ jit: flyR() * 0.35, dz: 1.5 + flyR() * 3 }));
		const mI = new THREE.Matrix4();
		// draw 2: stack -> fused stack (flat-top outline: outer flats parallel to the rows)
		const neck2Mat = glass('fused_stack');
		const neck2 = new Neck(STACK_F, FUSED_F, 26, 0, 0, neck2Mat);
		tag(neck2.mesh, 'neck', () => neckInfo(['The canes fuse together; pitch drawn down to about 50 µm (stated)']));
		root.add(neck2.mesh);
		const fusedMat = glass('fused_stack');
		const fusedGeo = prism(hexShape(FUSED_F, 0), 1, 'down', 6);
		const fusedOut = tag(new THREE.Mesh(fusedGeo, fusedMat), 'fused_stack');
		const fusedPiece = tag(new THREE.Mesh(fusedGeo, fusedMat), 'fused_stack');
		root.add(fusedOut, fusedPiece);

		// end-face textures (lattice drawn from the counted rings; flat-top outline; centre site solid)
		function faceTexture(px: number, span: number, F: number, pitch: number, holeD: number, holesOnly = false) {
			const cv = document.createElement('canvas');
			cv.width = cv.height = px;
			const c2 = cv.getContext('2d')!;
			const s = px / span;
			c2.translate(px / 2, px / 2);
			c2.scale(s, -s);
			if (!holesOnly) {
				c2.beginPath();
				for (let i = 0; i < 6; i++) {
					const [a, b] = hexAt(i / 6, F, 0);
					if (i === 0) c2.moveTo(a, b);
					else c2.lineTo(a, b);
				}
				c2.closePath();
				c2.fillStyle = '#d9e5eb';
				c2.fill();
				c2.lineWidth = Math.max(1.5 / s, F * 0.006);
				c2.strokeStyle = '#7d93a1';
				c2.stroke();
			}
			c2.fillStyle = holesOnly ? '#ffffff' : '#0d1216';
			for (const st of SITES) {
				if (st.ring === 0) continue;
				c2.beginPath();
				c2.arc(st.x * pitch, st.y * pitch, Math.max(holeD / 2, 0.9 / s), 0, Math.PI * 2);
				c2.fill();
			}
			const t = keep(new THREE.CanvasTexture(cv));
			t.colorSpace = THREE.SRGBColorSpace;
			t.anisotropy = 4;
			return t;
		}
		const FUSED_PITCH = FUSED_F / 16.5;
		const fusedFaceMat = reg('fused_stack', new THREE.MeshBasicMaterial({ map: faceTexture(1024, FUSED_F * 1.2, FUSED_F, FUSED_PITCH, HOLE_RATIO * FUSED_PITCH), transparent: true, depthWrite: false, side: THREE.DoubleSide }));
		const fusedFace = tag(new THREE.Mesh(keep(new THREE.PlaneGeometry(FUSED_F * 1.2, FUSED_F * 1.2)), fusedFaceMat), 'fused_stack', () => ({
			id: 'fused_stack',
			label: 'fused stack, cut face',
			detail: [
				'Canes fused, pitch about 50 µm (stated, p.1547)',
				'Outer size about 0.8 mm across the flats: derived estimate (16.5 × 50 µm)',
				'Hole proportion drawn as in the cane: assumed (the paper reports shrinkage in the final drawing stages)'
			]
		}));
		fusedFace.rotation.x = -Math.PI / 2;
		fusedFace.renderOrder = 3;
		root.add(fusedFace);
		// draw 3: fused piece -> fiber
		const feedMat = glass('fused_stack');
		const feed3 = tag(new THREE.Mesh(prism(hexShape(FUSED_F, 0), 60, 'up', 6), feedMat), 'fused_stack');
		root.add(feed3);
		const neck3Mat = glass('fiber');
		const neck3 = new Neck(FUSED_F, FIB_F, 3.6, 0, 0, neck3Mat);
		tag(neck3.mesh, 'neck', () => neckInfo(['Relative hole size shrinks in the final drawing stages (surface tension, p.1548)']));
		root.add(neck3.mesh);
		const fibMat = glass('fiber', { opacity: 0.9 });
		const fibOut = tag(new THREE.Mesh(prism(hexShape(FIB_F, 0), 1, 'down', 6), fibMat), 'fiber', () => ({
			id: 'fiber',
			label: 'photonic crystal fiber',
			detail: ['38 µm across the flats, many meters long (stated)', 'Relative hole size shrinks in this draw (surface tension, p.1548)']
		}));
		root.add(fibOut);

		// ------------------------------------------------------------------------ chapter 7: the fiber end face (um units)
		const um = new THREE.Group();
		um.scale.setScalar(0.001);
		um.position.set(...BO);
		root.add(um);
		const LF = 150; // drawn piece length, um (fades out: the 1 m length is not drawn here)
		const faceSpan = FIB_F_UM * 1.2;
		const faceMat = reg('fiber', new THREE.MeshBasicMaterial({ map: faceTexture(2048, faceSpan, FIB_F_UM, PITCH_UM, HOLE_UM), transparent: true, depthWrite: false }));
		const face = tag(new THREE.Mesh(keep(new THREE.PlaneGeometry(faceSpan, faceSpan)), faceMat), 'fiber');
		face.renderOrder = 4;
		um.add(face);
		const holeHiMat = keep(new THREE.MeshBasicMaterial({ map: faceTexture(1024, faceSpan, FIB_F_UM, PITCH_UM, HOLE_UM * 1.6, true), transparent: true, depthWrite: false, color: '#3987e5', opacity: 0 }));
		const holeHi = new THREE.Mesh(face.geometry, holeHiMat);
		holeHi.position.z = 0.02;
		holeHi.renderOrder = 6;
		um.add(holeHi);
		const bodyMat = glass('fiber', { opacity: 0.32 }, 0.5);
		setFade(bodyMat, 30, LF, [0, 0, -1]);
		const body = tag(new THREE.Mesh(prism(hexShape(FIB_F_UM, 0), LF, 'back', 6), bodyMat), 'fiber');
		body.position.z = -0.05;
		um.add(body);
		const holeMat = glass('air_holes', { opacity: 0.4, roughness: 0.6, side: THREE.FrontSide, envMapIntensity: 0.2 }, 0.1);
		setFade(holeMat, 20, LF * 0.85, [0, 0, -1]);
		const holeGeo = keep(new THREE.CylinderGeometry(HOLE_UM / 2, HOLE_UM / 2, 1, 10, 1, true).rotateX(Math.PI / 2).translate(0, 0, -0.5));
		const holeMeshes = tag(new THREE.InstancedMesh(holeGeo, holeMat, hollow.length), 'air_holes');
		holeMeshes.frustumCulled = false;
		um.add(holeMeshes);
		const coreRing = new THREE.LineLoop(
			keep(new THREE.BufferGeometry().setFromPoints(Array.from({ length: 64 }, (_, i) => new THREE.Vector3(2.3 * Math.cos((i / 64) * Math.PI * 2), 2.3 * Math.sin((i / 64) * Math.PI * 2), 0.05)))),
			keep(new THREE.LineBasicMaterial({ color: '#3987e5', transparent: true, opacity: 0 }))
		);
		um.add(coreRing);

		// near-field glow: one layer per digitized contour (outermost first), shape from the plot series
		const nf = spec.plots?.find((q) => q.id === 'near_field');
		const contours = (nf?.series ?? []).slice(1); // [outermost, third, second, innermost]
		const NF_SPAN = 9.6;
		const glowLayers = contours.map((s, i) => {
			const cv = document.createElement('canvas');
			cv.width = cv.height = 512;
			const c2 = cv.getContext('2d')!;
			const sc = 512 / NF_SPAN;
			c2.translate(256, 256);
			c2.shadowColor = 'rgba(255,255,255,0.9)';
			c2.shadowBlur = 8;
			c2.fillStyle = 'rgba(255,255,255,0.58)';
			c2.beginPath();
			s.points.forEach(([x, y], j) => (j ? c2.lineTo(x * sc, -y * sc) : c2.moveTo(x * sc, -y * sc)));
			c2.closePath();
			c2.fill();
			const t = keep(new THREE.CanvasTexture(cv));
			t.colorSpace = THREE.SRGBColorSpace;
			const m = reg('guided_mode', new THREE.MeshBasicMaterial({ map: t, color: '#ff3a2a', transparent: true, depthWrite: false, toneMapped: false }));
			const mesh = tag(new THREE.Mesh(keep(new THREE.PlaneGeometry(NF_SPAN, NF_SPAN)), m), 'guided_mode');
			mesh.position.z = 0.03 + i * 0.01;
			mesh.renderOrder = 5 + i;
			um.add(mesh);
			return { mesh, m, si: i + 1 };
		});
		const nfInfo = (): PickInfo => ({
			id: 'guided_mode',
			label: 'guided mode, near field at 632.8 nm',
			detail: ['Glow shaped by the four digitized contours of Fig. 2(a) (p.1548)', 'Innermost / outermost contour: factor 25 (caption); other levels not printed', 'Brightness steps illustrative; only the 25:1 ratio is printed']
		});
		for (const g of glowLayers) g.mesh.userData.info = nfInfo;

		// ------------------------------------------------------------------------ chapters 8-10: test bench (stand-ins)
		const bench = new THREE.Group();
		bench.position.set(BO[0], BO[1], 0);
		root.add(bench);
		const benchInfo = (id: string, label: string, extra: string[]) => (): PickInfo => ({ id, label, detail: [...extra, 'Neutral stand-in: shape, size and position not stated'] });
		const laserMat = std('lasers');
		const laser = tag(new THREE.Mesh(keep(new THREE.BoxGeometry(22, 22, 70)), laserMat), 'lasers', benchInfo('lasers', 'lasers (one box for four lasers)', ['Argon-ion 457.9 nm, He-Ne 632.8 nm, Ti:sapphire 850 nm, diode 1550 nm (stated)']));
		const objMat = std('launch_lens');
		const objGeo = keep(new THREE.CylinderGeometry(7, 7, 18, 40).rotateX(Math.PI / 2));
		const noseGeo = keep(new THREE.CylinderGeometry(3.2, 4.5, 5, 32).rotateX(Math.PI / 2));
		const objG = new THREE.Group();
		objG.add(tag(new THREE.Mesh(objGeo, objMat), 'launch_lens', benchInfo('launch_lens', 'objective lens', ['More than 50 % coupling into the guided mode (stated)'])));
		const nose = tag(new THREE.Mesh(noseGeo, objMat), 'launch_lens', benchInfo('launch_lens', 'objective lens', ['More than 50 % coupling into the guided mode (stated)']));
		nose.position.z = 11.5;
		objG.add(nose);
		const fluidMat = glass('index_fluid', { opacity: partLook('index_fluid').opacity ?? 0.35 }, 0.3);
		const fluid = tag(new THREE.Mesh(keep(new THREE.CylinderGeometry(2.6, 2.6, Z_FL1 - Z_FL0, 32).rotateX(Math.PI / 2)), fluidMat), 'index_fluid', () => ({
			id: 'index_fluid',
			label: 'index-matching fluid',
			detail: ['Strips light from cladding modes (stated, p.1548)', 'Position and length along the fiber: assumed (not stated)']
		}));
		fluid.position.z = (Z_FL0 + Z_FL1) / 2;
		const fibLineMat = reg('fiber', new THREE.LineBasicMaterial({ color: '#cfdde6', transparent: true }));
		const benchFiberInfo = (): PickInfo => ({ id: 'fiber', label: 'photonic crystal fiber, 1 m', detail: ['1 m length (stated, p.1548), drawn shortened with a break'] });
		const fibA = tag(new THREE.Line(keep(new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(0, 0, Z_IN), new THREE.Vector3(0, 0, Z_BRK - 3)])), fibLineMat), 'fiber', benchFiberInfo);
		const fibB = tag(new THREE.Line(keep(new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(0, 0, Z_BRK + 3), new THREE.Vector3(0, 0, -0.16)])), fibLineMat), 'fiber', benchFiberInfo);
		const vidMat = std('vidicon');
		const vidG = new THREE.Group();
		const vidInfo = benchInfo('vidicon', 'vidicon camera with a 60× objective', ['Images the output end (near field, Fig. 2(a)); working distance drawn visual']);
		vidG.add(tag(new THREE.Mesh(keep(new THREE.BoxGeometry(30, 30, 46)), vidMat), 'vidicon', vidInfo));
		const vidObj = tag(new THREE.Mesh(keep(new THREE.CylinderGeometry(5, 6, 16, 32).rotateX(Math.PI / 2)), vidMat), 'vidicon', vidInfo);
		vidObj.position.z = -31;
		vidG.add(vidObj);
		const paperMat = std('screen', { side: THREE.DoubleSide });
		const paper = tag(new THREE.Mesh(keep(new THREE.PlaneGeometry(80, 80)), paperMat), 'screen', () => ({
			id: 'screen',
			label: 'sheet of paper',
			detail: ['Several centimeters from the far end (stated); drawn distance visual', 'Output NA about 0.13 at 457.9 nm, 0.36 at 1550 nm (p.1548)']
		}));
		bench.add(laser, objG, fluid, fibA, fibB, vidG, paper);

		// light (physical: glows allowed)
		const lightMats: T.MeshBasicMaterial[] = [];
		const lm = (o: number) => {
			const m = keep(new THREE.MeshBasicMaterial({ color: '#ff3a2a', transparent: true, opacity: o, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false }));
			baseOpacity.set(m, o);
			lightMats.push(m);
			return m;
		};
		const beamInfo = (): PickInfo => {
			const L = LINES[lineIdx];
			return {
				id: 'beam',
				label: `laser light, ${L.nm} nm (${L.name})`,
				detail: [
					L.ir ? 'Infrared: grey is a false colour' : 'Visible line',
					'Beam and core light drawn wider than the fiber',
					lastP < C('single_mode')[0] ? 'Drawn at 632.8 nm; the paper launched each laser in turn' : 'Each laser launched in turn (stated)'
				]
			};
		};
		const beamMat = lm(0.85);
		const beam = tag(new THREE.Mesh(keep(new THREE.CylinderGeometry(0.7, 0.7, 1, 16, 1, true).rotateX(Math.PI / 2).translate(0, 0, 0.5)), beamMat), 'beam', beamInfo);
		const focusMat = lm(0.55);
		const focus = tag(new THREE.Mesh(keep(new THREE.ConeGeometry(3, 1, 32, 1, true).rotateX(Math.PI / 2).translate(0, 0, 0.5)), focusMat), 'beam', beamInfo);
		const coreLitMat = lm(0.9);
		const coreLit = tag(new THREE.Mesh(keep(new THREE.CylinderGeometry(0.42, 0.42, 1, 12, 1, true).rotateX(Math.PI / 2).translate(0, 0, 0.5)), coreLitMat), 'beam', beamInfo);
		const cladMat = lm(0.3);
		const clad = tag(new THREE.Mesh(keep(new THREE.CylinderGeometry(1.3, 1.3, 1, 16, 1, true).rotateX(Math.PI / 2).translate(0, 0, 0.5)), cladMat), 'clad_light', () => ({
			id: 'clad_light',
			label: 'light in cladding modes',
			detail: ['Stripped off by the index-matching fluid (stated, p.1548)', 'Drawn schematically']
		}));
		const coneMat = lm(0.07);
		coneMat.side = THREE.DoubleSide;
		const cone = tag(new THREE.Mesh(keep(new THREE.ConeGeometry(FF_CONE_R, Z_PAPER, 48, 1, true).rotateX(-Math.PI / 2).translate(0, 0, Z_PAPER / 2)), coneMat), 'far_field', () => ffInfo());
		bench.add(beam, focus, coreLit, clad, cone);
		// gap in the lit core at the break
		const coreLit2 = tag(new THREE.Mesh(coreLit.geometry, coreLitMat), 'beam', beamInfo);
		bench.add(coreLit2);
		// output end glow (wide shots) and the far-field pattern (schematic)
		function radialTex(spots: [number, number, number][], span: number) {
			const cv = document.createElement('canvas');
			cv.width = cv.height = 512;
			const c2 = cv.getContext('2d')!;
			const s = 512 / span;
			for (const [x, y, r] of spots) {
				const g = c2.createRadialGradient(256 + x * s, 256 - y * s, 0, 256 + x * s, 256 - y * s, r * s);
				g.addColorStop(0, 'rgba(255,255,255,1)');
				g.addColorStop(0.45, 'rgba(255,255,255,0.75)');
				g.addColorStop(1, 'rgba(255,255,255,0)');
				c2.fillStyle = g;
				c2.fillRect(0, 0, 512, 512);
			}
			const t = keep(new THREE.CanvasTexture(cv));
			t.colorSpace = THREE.SRGBColorSpace;
			return t;
		}
		const endGlowMat = keep(new THREE.SpriteMaterial({ map: radialTex([[0, 0, 1]], 2), color: '#ff3a2a', transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false, opacity: 0 }));
		const endGlow = new THREE.Sprite(endGlowMat);
		endGlow.scale.setScalar(7);
		bench.add(endGlow);
		const FF_SPAN = 64;
		// proportions from Fig. 3(a) (p.1549): centre half-max radius about 0.5 of the spot-ring radius, satellites
		// about 0.15 of it and 0.15-0.3 of the centre brightness; one schematic size (no angular scale printed)
		const FF_RING = 12.5;
		const HALF = 0.633; // half-max point of radialTex as a fraction of its outer radius
		const outerSpots: [number, number, number][] = Array.from({ length: 6 }, (_, i) => {
			const a = (30 + 60 * i) * DEG; // six spots at 30, 90, ... deg with the rows of holes horizontal (Fig. 2(b) relative to 2(a))
			return [FF_RING * Math.cos(a), FF_RING * Math.sin(a), (0.15 * FF_RING) / HALF];
		});
		const spotMatC = keep(new THREE.MeshBasicMaterial({ map: radialTex([[0, 0, (0.5 * FF_RING) / HALF]], FF_SPAN), color: '#ff3a2a', side: THREE.DoubleSide, transparent: true, depthWrite: false, toneMapped: false, opacity: 0 }));
		const spotMatO = keep(new THREE.MeshBasicMaterial({ map: radialTex(outerSpots, FF_SPAN), color: '#ff3a2a', side: THREE.DoubleSide, transparent: true, depthWrite: false, toneMapped: false, opacity: 0 }));
		const ffGeo = keep(new THREE.PlaneGeometry(FF_SPAN, FF_SPAN));
		const ffC = tag(new THREE.Mesh(ffGeo, spotMatC), 'far_field', () => ffInfo());
		const ffO = tag(new THREE.Mesh(ffGeo, spotMatO), 'far_field', () => ffInfo());
		ffC.renderOrder = 7;
		ffO.renderOrder = 8;
		bench.add(ffC, ffO);
		const ffInfo = (): PickInfo => {
			const L = LINES[lineIdx];
			return {
				id: 'far_field',
				label: `far-field pattern (schematic), ${L.nm} nm${L.ir ? ' in false colour' : ''}`,
				detail: [
					'Central spot and six spots (Fig. 3, p.1549); orientation from the calculated Fig. 2(b)',
					'Spot proportions from Fig. 3(a); no angular scale printed',
					'The real pattern widens with wavelength: output NA about 0.13 at 457.9 nm to about 0.36 at 1550 nm (Knight et al., Opt. Lett. 1996, p.1548); only these two values are printed, so it is drawn at one size for all four lasers',
					'Light cone drawn inside NA 0.36',
					"Outer spots weaker at longer wavelengths (stated); the paper's 'outer spots' may mean the higher-order spots of Fig. 3(b); dimming drawn on the six spots, illustrative",
					...(L.ir ? ['Infrared: grey is a false colour'] : [])
				]
			};
		};

		// ------------------------------------------------------------------------ lights
		const hemi = new THREE.HemisphereLight('#ffffff', '#3a3c44', 0.8);
		const key = new THREE.DirectionalLight('#fff3e6', 2.2);
		key.position.set(60, 120, 95);
		const rim = new THREE.DirectionalLight('#bcd2ff', 1.4);
		rim.position.set(-130, 50, -90);
		const fill = new THREE.DirectionalLight('#ffffff', 0.5);
		fill.position.set(-40, -60, 120);
		// soft light from the far side of the bench: the sheet of paper faces the fiber, away from the key light
		const back = new THREE.DirectionalLight('#ffffff', 1.1);
		back.position.set(-60, 90, -200);
		root.add(back);
		const furLight = new THREE.PointLight('#ff8a3a', 0, 140, 1.4);
		furLight.position.set(0, HOT_Y, 0);
		root.add(hemi, key, rim, fill, furLight);

		// ------------------------------------------------------------------------ theme
		const glassMats = [rodMat, slabMat, neck1Mat, caneMat, stackMat, neck2Mat, fusedMat, feedMat, neck3Mat, fibMat, bodyMat];
		function applyTheme() {
			const light = theme === 'light';
			accent.set(light ? '#2a78d6' : '#3987e5');
			for (const m of glassMats) m.color.set(light ? '#7f9aac' : (partLook('rod').color ?? '#dfe9ee'));
			solidMat.color.set(light ? '#9fb6c4' : (partLook('solid_cane').color ?? '#f0f4f6'));
			fluidMat.color.set(light ? '#5f9cbf' : (partLook('index_fluid').color ?? '#b8d8e8'));
			for (const m of [laserMat, vidMat]) m.color.set(light ? '#8e969f' : (partLook('lasers').color ?? '#2a2e33'));
			furMat.color.set(light ? '#8e969f' : (partLook('tower').color ?? '#3a4048'));
			paperMat.color.set(light ? '#f4f2ea' : (partLook('screen').color ?? '#ecebe4'));
			fibLineMat.color.set(light ? '#6d8494' : '#cfdde6');
			holeMat.color.set(light ? '#2a3238' : '#0a0e12');
			const add = light ? THREE.NormalBlending : THREE.AdditiveBlending;
			for (const m of [...lightMats, hzMat, endGlowMat]) {
				m.blending = add;
				m.needsUpdate = true;
			}
			(coreRing.material as T.LineBasicMaterial).color.copy(accent);
			holeHiMat.color.copy(accent);
		}
		applyTheme();

		// ------------------------------------------------------------------------ camera shots (same framing rule as the MCVD scene)
		interface Shot {
			az: number;
			el: number;
			box: number[];
			fw: number;
			fh: number;
			sx: number;
			sy: number;
		}
		const portrait = () => w / h < 0.9;
		const P = (s: Shot): Shot => (portrait() ? { ...s, fh: s.fh * 0.72, sy: s.sy + 0.05 } : s);
		// vertical draws on phones: smaller and lower, so feed and fiber stay clear of the chapter text
		const PD = (s: Shot): Shot => (portrait() ? { ...s, fh: s.fh * 0.55, sy: s.sy - 0.16 } : s);
		const plotShift = (s: Shot): Shot =>
			portrait() ? { ...s, fw: Math.min(s.fw, 0.8), fh: 0.2, sx: 0, sy: 0.2 } : { ...s, fw: Math.min(s.fw, 0.42), fh: Math.min(s.fh, 0.6), sx: -0.25, sy: -0.06 };
		const box3 = (c: [number, number, number], hx: number, hy: number, hz: number) => [c[0] - hx, c[0] + hx, c[1] - hy, c[1] + hy, c[2] - hz, c[2] + hz];
		const umB = (x: number, y: number, z: number): [number, number, number] => [BO[0] + x * 0.001, BO[1] + y * 0.001, BO[2] + z * 0.001];
		const sh = {
			rodIn: (): Shot => P({ az: -24, el: 16, box: [-ROD_R, ROD_R, YR - 36, YR + ROD_L - 30, -ROD_R, ROD_R], fw: 0.7, fh: 0.62, sx: 0.04, sy: -0.1 }),
			rod: (): Shot => P({ az: -24, el: 24, box: [-ROD_R, ROD_R, YR, YR + ROD_L, -ROD_R, ROD_R], fw: 0.7, fh: 0.66, sx: 0.04, sy: -0.1 }),
			rodTop: (): Shot => P({ az: -18, el: 34, box: [-ROD_R - 4, ROD_R + 4, YR + 40, YR + ROD_L, -ROD_R - 4, ROD_R + 4], fw: 0.72, fh: 0.66, sx: 0.04, sy: -0.1 }),
			draw1: (): Shot => P({ az: -28, el: 12, box: [-FUR_RO, FUR_RO, -112, 66, -FUR_RO, FUR_RO], fw: 0.8, fh: 0.7, sx: 0.04, sy: -0.08 }),
			stackFace: (): Shot => P({ az: -10, el: 9, box: box3(S0, STACK_F * 0.62, STACK_F * 0.62, 2), fw: 0.66, fh: 0.62, sx: 0.04, sy: -0.08 }),
			stackSide: (): Shot => P({ az: -30, el: 18, box: box3(S0, STACK_F * 0.6, STACK_F * 0.6, 14), fw: 0.66, fh: 0.62, sx: 0.04, sy: -0.08 }),
			draw2: (): Shot => PD({ az: -28, el: 12, box: [-FUR_RO, FUR_RO, -96, 74, -FUR_RO, FUR_RO], fw: 0.8, fh: 0.7, sx: 0.04, sy: -0.08 }),
			cutFace: (): Shot => PD({ az: -22, el: 46, box: box3([0, CUT2_Y - 2.2, 0], 0.62, 0.5, 0.62), fw: 0.6, fh: 0.56, sx: 0.04, sy: -0.08 }),
			draw3: (): Shot => PD({ az: -28, el: 10, box: [-FUR_RO, FUR_RO, -60, 46, -FUR_RO, FUR_RO], fw: 0.8, fh: 0.7, sx: 0.04, sy: -0.08 }),
			neck3: (): Shot => PD({ az: -28, el: 8, box: [-2.4, 2.4, NECK3_Y - 4.6, NECK3_Y + 1.6, -1, 1], fw: 0.6, fh: 0.66, sx: 0.04, sy: -0.08 }),
			fibDown: (): Shot => PD({ az: -28, el: 8, box: [-2.4, 2.4, -24, -18, -1, 1], fw: 0.6, fh: 0.66, sx: 0.04, sy: -0.08 }),
			face: (): Shot => P({ az: 0, el: 0, box: box3(umB(0, 0, 0), 0.023, 0.023, 0.0005), fw: 0.62, fh: 0.62, sx: 0.04, sy: -0.08 }),
			faceDepth: (): Shot => P({ az: -38, el: 20, box: [BO[0] - 0.022, BO[0] + 0.022, BO[1] - 0.022, BO[1] + 0.022, BO[2] - 0.06, BO[2]], fw: 0.66, fh: 0.62, sx: 0.06, sy: -0.08 }),
			benchWide: (): Shot => P({ az: portrait() ? -102 : -116, el: 16, box: [-14, 14, BO[1] - 14, BO[1] + 14, Z_LAS - 38, Z_PAPER + 8], fw: 0.94, fh: 0.6, sx: 0, sy: -0.1 }),
			outEnd: (): Shot => P({ az: -124, el: 14, box: [-16, 16, BO[1] - 16, BO[1] + 16, -40, Z_VID + 26], fw: 0.8, fh: 0.6, sx: 0.02, sy: -0.1 }),
			nfFace: (): Shot => plotShift({ az: 0, el: 0, box: box3(umB(0, 0, 0), 0.0195, 0.0195, 0.0003), fw: 0.44, fh: 0.6, sx: -0.25, sy: -0.06 }),
			ffWide: (): Shot => P({ az: portrait() ? -106 : -122, el: 15, box: [-40, 40, BO[1] - 40, BO[1] + 40, Z_LAS - 38, Z_PAPER + 4], fw: 0.94, fh: 0.62, sx: 0, sy: -0.1 })
		};
		const CUT2_Y = -60;
		const NECK3_Y = 4;
		type Key = [number, (p: number) => Shot];
		const keys: Key[] = [
			[0, sh.rodIn],
			[at('rod', 0.5), sh.rod],
			[at('rod', 0.75), sh.rodTop],
			[at('rod', 1), sh.rodTop],
			[at('flats', 0.18), sh.rod],
			[at('flats', 1), sh.rod],
			[at('cane', 0.32), sh.draw1],
			[at('cane', 1), sh.draw1],
			[at('stack', 0.16), sh.stackFace],
			[at('stack', 0.86), sh.stackFace],
			[at('stack', 1), sh.stackSide],
			[at('fuse', 0.34), sh.draw2],
			[at('fuse', 0.78), sh.draw2],
			[at('fuse', 0.95), sh.cutFace],
			[at('fuse', 1), sh.cutFace],
			[at('fiber', 0.2), sh.draw3],
			[at('fiber', 0.3), sh.draw3],
			[at('fiber', 0.48), sh.neck3],
			[at('fiber', 0.62), sh.neck3],
			[at('fiber', 0.92), sh.fibDown],
			[at('fiber', 1), sh.fibDown],
			[at('lattice', 0.34), sh.face],
			[at('lattice', 0.52), sh.face],
			[at('lattice', 0.86), sh.faceDepth],
			[at('lattice', 1), sh.faceDepth],
			[at('launch', 0.32), sh.benchWide],
			[at('launch', 1), sh.benchWide],
			[at('near_field', 0.1), sh.outEnd],
			[at('near_field', 0.24), sh.nfFace],
			[at('near_field', 1), sh.nfFace],
			[at('single_mode', 0.24), sh.ffWide],
			[1, sh.ffWide]
		];
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
			// centres blend linearly, half sizes in log (the story spans 30 mm to 0.35 um)
			const box = [0, 0, 0, 0, 0, 0];
			for (let j = 0; j < 6; j += 2) {
				const ca = (A.box[j] + A.box[j + 1]) / 2;
				const cb = (B.box[j] + B.box[j + 1]) / 2;
				const ha = Math.max(1e-6, (A.box[j + 1] - A.box[j]) / 2);
				const hb = Math.max(1e-6, (B.box[j + 1] - B.box[j]) / 2);
				const hh = Math.exp(Math.log(ha) + (Math.log(hb) - Math.log(ha)) * t);
				// zooming far in: hold the centre near the target end so the dive does not drift off the subject
				const tc = hb < ha * 0.05 ? Math.min(1, t * 1.6) : ha < hb * 0.05 ? Math.max(0, 1.6 * t - 0.6) : t;
				const c = ca + (cb - ca) * tc;
				box[j] = c - hh;
				box[j + 1] = c + hh;
			}
			return { az: mix(A.az, B.az), el: mix(A.el, B.el), box, fw: mix(A.fw, B.fw), fh: mix(A.fh, B.fh), sx: mix(A.sx, B.sx), sy: mix(A.sy, B.sy) };
		}
		const vA = new THREE.Vector3();
		const vR = new THREE.Vector3();
		const vU = new THREE.Vector3();
		const vD = new THREE.Vector3();
		let camD = 100;
		function placeCamera(s: Shot) {
			const az = s.az * DEG;
			const el = s.el * DEG;
			vD.set(Math.sin(az) * Math.cos(el), Math.sin(el), Math.cos(az) * Math.cos(el));
			vR.set(Math.cos(az), 0, -Math.sin(az));
			vU.crossVectors(vD, vR).normalize();
			const [x0, x1, y0, y1, z0, z1] = s.box;
			const cx = (x0 + x1) / 2;
			const cy = (y0 + y1) / 2;
			const cz = (z0 + z1) / 2;
			const tv = Math.tan((camera.fov * DEG) / 2);
			const th = tv * (w / h);
			let d = 1e-6;
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
			camera.near = Math.max(1e-5, d / 300);
			camera.far = d * 60 + 600;
			camera.updateProjectionMatrix();
			camera.updateMatrixWorld();
			camD = d;
			tgt = [cx, cy, cz];
		}

		// ------------------------------------------------------------------------ frame
		const vis: Record<string, number> = {};
		let stackFadeMid = 7; // canes are drawn (alpha > 1/2) up to this distance behind the face
		let lineIdx = 1;
		const colTmp = new THREE.Color();
		const lineCols = LINES.map((L) => new THREE.Color(L.col));
		function lineColour(p: number) {
			// launch / near field: 632.8 nm; single mode: blue, red, 850, 1550 in turn (stated lines; IR in false colour)
			if (!after(p, 'single_mode')) {
				lineIdx = 1;
				return colTmp.set(LINES[1].col);
			}
			const q = loc(p, 'single_mode');
			const edges = [0.32, 0.54, 0.76];
			let i = 0;
			while (i < 3 && q >= edges[i]) i++;
			lineIdx = i;
			colTmp.set(LINES[i].col);
			// short blend into each new line (no flash)
			if (i > 0) {
				const b = smooth(edges[i - 1], edges[i - 1] + 0.025, q);
				colTmp.lerpColors(lineCols[i - 1], lineCols[i], b);
			}
			return colTmp;
		}

		function frame(p: number) {
			lastP = p;
			placeCamera(shotAt(p));
			const kb = after(p, 'single_mode') ? k : 0;
			const all: T.Material[] = [];
			const show = (m: T.Material, f: number) => {
				fade(m, f);
				all.push(m);
			};

			// ---- rod, drill, flats, first draw
			const rodIn = ease(loc(p, 'rod', 0, 0.45));
			const drill = ease(loc(p, 'rod', 0.4, 0.95));
			setBore(drill * ROD_L);
			const desc = ease(loc(p, 'cane', 0.04, 0.3));
			const rodY = lerp(YR - 40 * (1 - rodIn), 6, desc);
			rodG.position.set(0, rodY, 0);
			rodG.rotation.y = -(1 - rodIn) * Math.PI * 0.5;
			const hexOn = after(p, 'flats');
			rodRound.visible = !hexOn;
			rodHex.visible = hexOn;
			const rodF = rodIn * (1 - smooth(at('stack', 0), at('stack', 0.12), p));
			show(rodMat, rodF);
			vis.rod = rodF;
			slabs.forEach((s, i) => {
				const q = loc(p, 'flats', 0.12 + i * 0.12, 0.12 + i * 0.12 + 0.2);
				const phi = s.userData.phi as number;
				const out = ease(q) * 14;
				s.position.set(Math.cos(phi) * out, -ease(q) * ease(q) * 40, -Math.sin(phi) * out);
				s.visible = hexOn && q < 0.999;
			});
			show(slabMat, hexOn ? rodIn * (1 - smooth(at('flats', 0.7), at('flats', 0.95), p)) : 0);
			// furnace
			// furnace: in for the draws, out while the canes are stacked beside it
			const furF =
				smooth(at('cane', 0), at('cane', 0.16), p) *
				(1 - smooth(at('stack', 0), at('stack', 0.1), p) + smooth(at('fuse', 0.12), at('fuse', 0.3), p)) *
				(1 - smooth(at('lattice', 0.02), at('lattice', 0.2), p));
			const zoomK = smooth(25, 140, camD); // camera close to the neck: walls and lining step back
			show(furMat, furF * zoomK);
			furG.visible = furF > 0.002;
			vis.tower = furF;
			// hot zone: on while drawing (no temperature is encoded)
			const glowOn =
				Math.max(
					smooth(at('cane', 0.15), at('cane', 0.32), p) * (1 - smooth(at('stack', 0), at('stack', 0.1), p)),
					smooth(at('fuse', 0.25), at('fuse', 0.4), p) * (1 - smooth(at('fiber', 0.02), at('fiber', 0.1), p)),
					smooth(at('fiber', 0.18), at('fiber', 0.32), p)
				) * furF;
			G.uGlow.value = glowOn * 0.85;
			hzMat.opacity = glowOn * 0.55 * lerp(0.12, 1, zoomK);
			hzMat.visible = glowOn > 0.01;
			furLight.intensity = glowOn * 2.5e3 * zoomK;
			vis.hot_zone = glowOn;
			// neck 1 and cane
			const d1 = loc(p, 'cane', 0.3, 0.5);
			const y1 = neck1.update(6 + (rodY - 6), d1);
			const n1F = d1 > 0 ? 1 - smooth(at('stack', 0), at('stack', 0.12), p) : 0;
			show(neck1Mat, n1F);
			neck1.mesh.visible = n1F > 0.002 && d1 > 0;
			const caneLen = ease(loc(p, 'cane', 0.45, 0.85)) * 260;
			const cutQ = loc(p, 'cane', 0.86, 0.97);
			const yCut = -76;
			caneOut.position.y = y1;
			caneOut.scale.y = Math.max(1e-3, cutQ > 0 ? Math.min(caneLen, y1 - yCut - 0.6 * ease(cutQ)) : caneLen);
			caneOut.visible = caneLen > 0.1;
			canePiece.visible = cutQ > 0;
			canePiece.position.y = yCut - ease(cutQ) * 18 - 0.4;
			canePiece.scale.y = 200;
			show(caneMat, n1F);
			vis.cane = caneLen > 1 ? n1F : 0;

			// ---- stack: solid cane first at the centre, then rings 1-9 slide in
			const stF = smooth(at('stack', 0.02), at('stack', 0.14), p) * (1 - smooth(at('fiber', 0.02), at('fiber', 0.14), p));
			const rotK = ease(loc(p, 'fuse', 0, 0.26));
			const movK = ease(loc(p, 'fuse', 0.04, 0.3));
			const dropK = ease(loc(p, 'fuse', 0.3, 0.42));
			const fuseY = lerp(30, 6, dropK);
			stackG.rotation.x = rotK * Math.PI * 0.5;
			stackG.position.set(lerp(S0[0], 0, movK), lerp(S0[1], fuseY, movK), lerp(S0[2], 0, movK));
			const solidQ = ease(loc(p, 'stack', 0.08, 0.2));
			solid.position.z = (1 - solidQ) * 10;
			solid.visible = solidQ > 0;
			hollow.forEach((s, i) => {
				const r0 = 0.16 + ((s.ring - 1) / RINGS) * 0.62;
				const q = ease(loc(p, 'stack', r0 + fly[i].jit * 0.06, r0 + 0.14 + fly[i].jit * 0.06));
				const out = (1 - q) * (2.2 + s.ring * 0.25);
				const a = s.ang;
				mI.makeTranslation(s.x * CANE_F + Math.cos(a) * out, s.y * CANE_F + Math.sin(a) * out, (1 - q) * fly[i].dz);
				if (q <= 0) mI.makeScale(0, 0, 0);
				canes.setMatrixAt(i, mI);
			});
			canes.instanceMatrix.needsUpdate = true;
			canes.boundingSphere = null; // raycast bounds follow the instances
			stackFadeMid = lerp(7, portrait() ? 17 : 46, rotK);
			for (const m of [stackMat, solidMat]) {
				// short drawn length end-on (no cane end drawn); longer once upright on the tower
				setFade(m, lerp(2.5, portrait() ? 8 : LC_F0, rotK), lerp(12, portrait() ? 26 : LC, rotK), [0, 0, -1]);
				const u = glassU.get(m)!;
				// in the furnace the cane boundaries vanish: the canes near the hot face fade into the neck
				u.uN0.value = 0;
				u.uN1.value = 5;
				u.uNk.value = smooth(at('fuse', 0.38), at('fuse', 0.5), p);
			}
			const cutZoom = portrait() ? smooth(at('fuse', 0.8), at('fuse', 0.92), p) : 0;
			show(stackMat, stF * (1 - cutZoom));
			show(solidMat, stF * (1 - cutZoom));
			vis.stack = stF;
			vis.solid_cane = solidQ > 0.5 ? stF : 0;
			// neck 2, fused output, cut
			const d2 = loc(p, 'fuse', 0.4, 0.55);
			const y2 = neck2.update(fuseY, d2);
			const n2F = d2 > 0 ? 1 - smooth(at('fiber', 0.02), at('fiber', 0.14), p) : 0;
			neck2.mesh.visible = n2F > 0.002 && d2 > 0;
			show(neck2Mat, n2F * (1 - cutZoom));
			const fLen = ease(loc(p, 'fuse', 0.5, 0.74)) * 220;
			const cut2 = loc(p, 'fuse', 0.75, 0.84);
			fusedOut.position.y = y2;
			fusedOut.scale.y = Math.max(1e-3, cut2 > 0 ? Math.min(fLen, y2 - CUT2_Y - 0.4 * ease(cut2)) : fLen);
			fusedOut.visible = fLen > 0.1;
			fusedPiece.visible = cut2 > 0;
			fusedPiece.position.y = CUT2_Y - ease(cut2) * 2.2;
			fusedPiece.scale.y = 160;
			fusedFace.visible = cut2 > 0;
			fusedFace.position.set(0, CUT2_Y - ease(cut2) * 2.2 + 0.002, 0);
			show(fusedMat, n2F);
			fusedOut.visible = fusedOut.visible && cutZoom < 0.98;
			show(fusedFaceMat, n2F * smooth(0.2, 0.6, cut2));
			vis.fused_stack = Math.max(fLen > 1 ? n2F : 0, 0);
			// draw 3: fused piece fed in, fiber out
			const f3In = smooth(at('fiber', 0.04), at('fiber', 0.18), p);
			const f3F = f3In * (1 - smooth(at('lattice', 0.02), at('lattice', 0.2), p));
			const feedY = lerp(26, NECK3_Y, ease(loc(p, 'fiber', 0.08, 0.3)));
			feed3.position.y = feedY;
			setFade(feedMat, portrait() ? 1.2 : 6, portrait() ? 4 : 26, [0, 1, 0]);
			show(feedMat, f3F);
			feed3.visible = f3F > 0.002;
			if (after(p, 'fiber')) vis.fused_stack = Math.max(vis.fused_stack, f3F);
			const d3 = loc(p, 'fiber', 0.3, 0.46);
			const y3 = neck3.update(feedY, d3);
			neck3.mesh.visible = f3F > 0.002 && d3 > 0;
			show(neck3Mat, f3F);
			const fbLen = ease(loc(p, 'fiber', 0.44, 0.88)) * 240;
			fibOut.position.y = y3;
			fibOut.scale.y = Math.max(1e-3, fbLen);
			{
				// phone: while the camera follows the fiber down, its upper part fades out above the frame (keeps the
				// chapter text clear); geometry-local axis runs 0 -> 1 down the fiber
				const u = glassU.get(fibMat)!;
				const L = Math.max(1e-3, fbLen);
				u.uAx.value.set(0, -1, 0);
				u.uN0.value = (y3 + 17) / L;
				u.uN1.value = (y3 + 18.6) / L;
				u.uNk.value = portrait() ? smooth(at('fiber', 0.64), at('fiber', 0.86), p) * (1 - smooth(at('lattice', 0), at('lattice', 0.1), p)) : 0;
			}
			fibOut.visible = fbLen > 0.01 && f3F > 0.002;
			show(fibMat, f3F);

			// ---- end face (um)
			const umF = smooth(at('lattice', 0.04), at('lattice', 0.22), p);
			const benchIn = smooth(at('launch', 0.06), at('launch', 0.3), p);
			um.visible = umF > 0.002;
			show(faceMat, umF);
			const bodyK = 1 - smooth(at('near_field', 0.06), at('near_field', 0.18), p); // fiber body ends before the plot
			show(bodyMat, umF * bodyK);
			const ext = ease(loc(p, 'lattice', 0.5, 0.86));
			hollow.forEach((s, i) => {
				if (ext <= 0) mI.makeScale(0, 0, 0);
				else mI.makeScale(1, 1, Math.max(1e-3, ext * LF)).setPosition(s.x * PITCH_UM, s.y * PITCH_UM, -0.02);
				holeMeshes.setMatrixAt(i, mI);
			});
			holeMeshes.instanceMatrix.needsUpdate = true;
			holeMeshes.boundingSphere = null;
			show(holeMat, umF * bodyK * smooth(0, 0.1, ext));
			vis.fiber = Math.max(umF, f3F);
			vis.air_holes = umF;
			vis.core = umF;
			const col = lineColour(p);
			// near-field glow: each layer follows its contour in the plot (outermost first); full mode outside that chapter
			const nfOn = after(p, 'near_field');
			const lit = smooth(at('launch', 0.76), at('launch', 0.86), p);
			const rev = revealAt(spec, 'near_field', p); // reveal fraction per plot series (runtime helper, same pen)
			glowLayers.forEach((g) => {
				const kk = nfOn && p < C('single_mode')[0] ? (rev[g.si] ?? 0) : lit;
				g.m.color.copy(col);
				fade(g.m, kk * umF * (theme === 'light' ? 0.85 : 1));
				g.mesh.visible = kk > 0.002 && umF > 0.002;
			});
			vis.guided_mode = Math.max(...glowLayers.map((g) => (g.mesh.visible ? g.m.opacity : 0)), 0);

			// ---- bench
			bench.visible = benchIn > 0.002;
			const bF = benchIn;
			// stand-ins step back while the camera is at the end face (they would sit at the vanishing point)
			const farK = smooth(0.6, 4, camD);
			show(laserMat, bF * farK);
			show(objMat, bF * farK);
			show(fluidMat, bF * farK);
			show(fibLineMat, bF * farK);
			laser.position.z = Z_LAS - kb * 50;
			objG.position.z = Z_OBJ - kb * 25;
			fluid.position.y = kb * 14;
			vis.lasers = vis.launch_lens = vis.index_fluid = bF;
			const vidIn = ease(loc(p, 'near_field', 0, 0.14)) * (1 - ease(loc(p, 'single_mode', 0, 0.16)));
			vidG.position.z = Z_VID + (1 - vidIn) * 90;
			show(vidMat, vidIn * farK);
			vidG.visible = vidIn > 0.002;
			vis.vidicon = vidIn;
			const papIn = ease(loc(p, 'single_mode', 0.1, 0.26));
			paper.position.set(0, (1 - papIn) * 70, Z_PAPER + kb * 40);
			paper.rotation.y = Math.PI;
			show(paperMat, papIn * farK);
			paper.visible = papIn > 0.002;
			vis.screen = papIn;
			// launch: beam out of the laser, focus into the core, core light to the output end; cladding light ends at the fluid
			const bq = loc(p, 'launch', 0.36, 0.46);
			const lz0 = Z_LAS - kb * 50 + 35;
			const lz1 = Z_OBJ - kb * 25 - 9;
			beam.position.z = lz0;
			beam.scale.z = Math.max(1e-3, (lz1 - lz0) * bq);
			const fq = loc(p, 'launch', 0.46, 0.5);
			const fz0 = Z_OBJ - kb * 25 + 14;
			focus.position.z = fz0;
			focus.scale.z = Math.max(1e-3, (Z_IN - fz0) * fq);
			const cq = ease(loc(p, 'launch', 0.5, 0.8));
			const zFront = lerp(Z_IN, 0, cq);
			coreLit.position.z = Z_IN;
			coreLit.scale.z = Math.max(1e-3, Math.min(zFront, Z_BRK - 3) - Z_IN);
			coreLit2.position.z = Z_BRK + 3;
			coreLit2.scale.z = Math.max(1e-3, zFront - (Z_BRK + 3));
			coreLit2.visible = zFront > Z_BRK + 3;
			const clq = ease(loc(p, 'launch', 0.5, 0.62));
			clad.position.z = Z_IN;
			clad.scale.z = Math.max(1e-3, (Z_FL0 + 10 - Z_IN) * clq);
			const lightOn = after(p, 'launch') ? bF * farK : 0;
			for (const m of lightMats) m.color.copy(col);
			show(beamMat, lightOn * (bq > 0 ? 1 : 0));
			show(focusMat, lightOn * (fq > 0 ? 1 : 0));
			show(coreLitMat, lightOn * (cq > 0 ? 1 : 0));
			// cladding light dies out inside the fluid (shader-free: whole segment fades once it reaches the sleeve)
			show(cladMat, lightOn * (clq > 0 ? 1 : 0));
			clad.visible = clq > 0 && lightOn > 0;
			// far field
			const ffQ = ease(loc(p, 'single_mode', 0.22, 0.34));
			cone.position.z = 0;
			cone.scale.set(1, 1, (Z_PAPER + kb * 40) / Z_PAPER);
			show(coneMat, ffQ * papIn);
			ffC.position.set(0, 0, Z_PAPER + kb * 40 - 0.3);
			ffO.position.copy(ffC.position);
			ffC.rotation.y = ffO.rotation.y = Math.PI;
			// on the light paper the grey false colours are darkened to stay visible
			const ir = LINES[lineIdx].ir;
			spotMatC.color.copy(col).multiplyScalar(ir ? 0.62 : 1);
			spotMatO.color.copy(spotMatC.color);
			const outerW = [1, 1, 0.85, 0.72][lineIdx]; // weaker toward long wavelengths (stated qualitatively; illustrative)
			fade(spotMatC, ffQ * 0.95);
			fade(spotMatO, ffQ * 0.95 * 0.3 * outerW); // 0.3 of the centre (Fig. 3(a): 0.15-0.3)
			vis.far_field = ffQ;
			// output-end glow for the wide shots (fades as the camera dives in)
			endGlow.position.set(0, 0, 0.5);
			endGlowMat.color.copy(col);
			endGlowMat.opacity = lit * bF * clamp01((camD - 3) / 20) * 0.9;
			endGlow.visible = endGlowMat.opacity > 0.002;
			vis.beam = lightOn;
			vis.clad_light = clad.visible ? 1 : 0;

			applyHi();
		}

		// cladding light fades along its length into the sleeve: per-vertex alpha would need a shader; use a short gradient map
		{
			const cv = document.createElement('canvas');
			cv.width = 4;
			cv.height = 64;
			const c2 = cv.getContext('2d')!;
			const g = c2.createLinearGradient(0, 0, 0, 64);
			// canvas top = far end (v = 1): dark there, so the light dies out inside the fluid
			g.addColorStop(0, '#000');
			g.addColorStop(0.3, '#999');
			g.addColorStop(1, '#fff');
			c2.fillStyle = g;
			c2.fillRect(0, 0, 4, 64);
			const t = keep(new THREE.CanvasTexture(cv));
			cladMat.alphaMap = t;
			cladMat.needsUpdate = true;
		}

		// ------------------------------------------------------------------------ highlight / pick / anchors
		function applyHi() {
			const on = (id: string) => hi.includes(id);
			for (const [id, list] of mats)
				for (const m of list) {
					const sm = m as T.MeshStandardMaterial;
					if (sm.emissive) sm.emissive.copy(accent).multiplyScalar(on(id) ? 0.45 : 0);
				}
			faceMat.color.set(on('fiber') ? '#9cc0ea' : theme === 'light' ? '#ffffff' : '#a9b7bf');
			fusedFaceMat.color.set(on('fused_stack') ? '#bcd6f5' : '#ffffff');
			holeHiMat.opacity = on('air_holes') ? 0.9 * faceMat.opacity : 0;
			holeHi.visible = holeHiMat.opacity > 0;
			const cr = coreRing.material as T.LineBasicMaterial;
			cr.opacity = on('core') ? faceMat.opacity : 0;
			coreRing.visible = cr.opacity > 0;
			if (on('guided_mode')) for (const g of glowLayers) g.m.opacity = Math.min(1, g.m.opacity * 1.5);
			hzMat.color.set(on('hot_zone') ? '#ffb070' : '#ff7a2a');
			for (const m of [spotMatC, spotMatO]) if (on('far_field')) m.color.lerp(accent, 0.3);
		}

		const ray = new THREE.Raycaster();
		const ndc = new THREE.Vector2();
		const lp = new THREE.Vector3();
		function pick(x: number, y: number): string | PickInfo | null {
			ndc.set((x / w) * 2 - 1, 1 - (y / h) * 2);
			ray.setFromCamera(ndc, camera);
			ray.params.Line = { threshold: Math.max(0.05, camD * 0.004) };
			const cands: T.Object3D[] = [];
			root.traverseVisible((o) => {
				const id = o.userData.part as string | undefined;
				if (!id) return;
				const m = (o as T.Mesh).material as T.Material | undefined;
				if (m && (m.opacity ?? 1) < 0.08 && !(m as T.MeshBasicMaterial).map) return;
				if ((vis[id] ?? 1) < 0.3) return;
				cands.push(o);
			});
			const hits = ray.intersectObjects(cands, false);
			for (const hit of hits) {
				const o = hit.object;
				if (o === face) {
					um.worldToLocal(lp.copy(hit.point));
					const r = Math.hypot(lp.x, lp.y);
					// inside the hexagon?
					let inside = true;
					for (let i = 0; i < 6; i++) {
						const a = (30 + i * 60) * DEG;
						if (lp.x * Math.cos(a) + lp.y * Math.sin(a) > FIB_F_UM / 2) inside = false;
					}
					if (!inside) continue;
					const tol = Math.max(HOLE_UM * 0.8, 4 * camD);
					for (const s of hollow) if (Math.hypot(lp.x - s.x * PITCH_UM, lp.y - s.y * PITCH_UM) < tol) return 'air_holes';
					if (r < 2.3) return vis.guided_mode > 0.2 ? nfInfo() : 'core';
					return {
						id: 'fiber',
						label: 'photonic crystal fiber, end face',
						detail: [
							'Pitch 2.3 µm, 38 µm across the flats, core nominally 4.6 µm (stated)',
							'Nine rings of holes as counted from Fig. 1',
							'Holes about 0.35 µm: d/Λ ≈ 0.15 from Birks et al., Opt. Lett. 1997 (p.962)'
						]
					};
				}
				if (o === fusedFace) {
					const l = fusedFace.worldToLocal(lp.copy(hit.point));
					let inside = true;
					for (let i = 0; i < 6; i++) {
						const a = (30 + i * 60) * DEG;
						if (l.x * Math.cos(a) + l.y * Math.sin(a) > FUSED_F / 2) inside = false;
					}
					if (!inside) continue;
				}
				if (o === canes || o === solid) {
					stackG.worldToLocal(lp.copy(hit.point));
					if (-lp.z > stackFadeMid) continue; // faded-out length is not pickable
				}
				if (glowLayers.some((g) => g.mesh === o)) {
					um.worldToLocal(lp.copy(hit.point));
					if (Math.hypot(lp.x, lp.y) > 2.7) continue;
				}
				const info = o.userData.info as (() => PickInfo) | undefined;
				if (info) return info();
				const id = o.userData.part as string | undefined;
				if (id) return id;
			}
			return null;
		}

		const va = new THREE.Vector3();
		function anchor(id: string): [number, number] | null {
			if ((vis[id] ?? 0) < 0.5) return null;
			switch (id) {
				case 'rod':
					if (lastP > C('flats')[0]) return null;
					va.set(ROD_R * 0.7, ROD_L - 6, ROD_R * 0.7);
					rodG.localToWorld(va);
					break;
				case 'cane':
					if (caneOut.scale.y < 90) return null;
					va.set(CANE_F, caneOut.position.y - 66, 0);
					break;
				case 'solid_cane':
					va.set(0, 0, 0.1);
					stackG.localToWorld(va);
					break;
				case 'fiber':
					if (lastP < at('lattice', 0.3)) return null;
					va.set(PITCH_UM, 0, 0);
					um.localToWorld(va);
					break;
				default:
					return null;
			}
			va.project(camera);
			if (va.z > 1) return null;
			const ax = ((va.x + 1) / 2) * w;
			const ay = ((1 - va.y) / 2) * h;
			if (ax < 2 || ax > w - 2 || ay < 2 || ay > h - 2) return null;
			return [ax, ay];
		}

		return {
			frame,
			highlight(ids) {
				hi = [...ids];
				frame(lastP);
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
				rodRound.geometry.dispose();
				for (const d of disposables) d.dispose();
				canes.dispose();
				holeMeshes.dispose();
			}
		} satisfies ShowcaseHandle;
	}
};

export default mod;
