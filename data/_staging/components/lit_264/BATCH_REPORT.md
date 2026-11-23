# lit_264 batch report

Date: 2026-11-23. Papers: lit:benedikovic2016, lit:chen2020b, lit:wang2017b, lit:zou2015 (all fiber-chip grating couplers).
Page-1 titles match the source rows; no garbled text layers. Validation: `merge_component_staging.py data/_staging/components/lit_264 --dry-run`:
+27 components, +133 metrics, 0 errors.

| paper | components | metric rows | fab org |
|---|---|---|---|
| benedikovic2016 | 12 (9 fabricated, 3 design) | 55 | empty |
| chen2020b | 3 (2 fabricated, 1 design) | 14 | empty |
| wang2017b | 4 (2 fabricated, 2 design) | 36 | org_applied_nanotools |
| zou2015 | 8 (all design) | 28 | empty (theory paper) |

## benedikovic2016 (single-etch SWG GCs, 220 nm SOI, O-band)

- Rows: 3 grating designs (uniform, two-step apodized, continuously apodized) x 3 layouts (linear grating + 500 um adiabatic
  taper, focusing + 40 um non-adiabatic taper, focusing + 17 um free-propagation region) = 9 fabricated rows (rule 9: a
  focusing grating with curved trenches is a different physical design); 3 backside-metal-mirror design rows (FDTD only, Sec. 4).
- Measured: per-row ripple-averaged peak loss read off Figs. 6(a) / 7(a) / 8(a) (`extracted_from_figure`, +/-0.15 dB,
  loopback_half, method loopback); back-reflection estimates from the fringe magnitude (~6 % linear, ~3 % curved, p.10)
  converted to dB (`derived`, approx).
- Simulated nominal 2D values (F-EEM / FDTD: -2.4 / -1.78 / -1.61 dB, back reflections 5 / 2.5 / 1.4 %) and the nominal
  geometry (Table 1 / 2, p.6) are on the three linear-taper rows only.
- Not entered:
  - Headline -2.7 dB (54 %) uniform and -2.5 dB (56 %) apodized (p.9, abstract, conclusion): stated over all three
    layouts and, for -2.5 dB, over both apodization designs; not tied to one row (D159). Kept in every row's notes. The
    figure reads agree (uniform FPR row about -2.65 dB, two-step linear row about -2.5 dB).
  - Percent forms of printed dB values (converted pairs, one form only, zhang2014 precedent).
  - Directionality 78 % / 45 % (Fig. 2), field overlap 78 / 91 / 93 %: no parameter. CD 120 / 150 nm variants (< 0.4 dB
    change, Fig. 5): notes only. Fig. 9 bias-corrected simulations: notes only. Ripple 0.2-0.6 dB: no parameter.
  - Measured peak wavelength: not printed; the reads (about 1330-1343 nm, +/-5 nm) are in the notes only.
- Fab / facility: passive "The structures were fabricated on an SOI wafer" (p.8); no org named; authors at four orgs.
  SEM data bars print "NRC" (Figs. 6-8), not a fabrication statement. No facility acknowledged. Nothing missing from the registry.

## chen2020b (2D GC, crossed-ellipse holes, Au mirror, substrate-side fiber, 1310 nm)

- `2dgc_au_mirror` (fabricated): measured -2.37 dB at 1310 nm (best, loopback_half, measured per D452: back-to-back pair
  in Fig. 6(a), halving not printed), 1-dB BW 29 nm, PDL < 0.2 dB over 78 nm; simulated -1.73 dB, 1-dB BW 29 nm
  (1298-1327 nm), PDL < 0.2 dB over 63 nm; geometry (P 496 nm, 70 nm etch, 220 nm Si, 2 um BOX, 0.6 um cladding, 10 deg).
- `2dgc_no_mirror` (fabricated): 4.07 dB `derived` = 2.37 + the stated 1.7 dB mirror reduction (p.7); wavelength 1310 nm
  inferred (the reduction is stated without a wavelength).
- `2dgc_conventional_design` (design): simulated -2.87 dB, S-polarized only (p.4).
- Not entered: simulated reflection "in the order of 10^-5" (order of magnitude only); tolerance PDLs (< 0.25 dB, < 0.34 dB,
  Figs. 3(b), 5); hole radii R_S 98.8 nm / R_L 225 nm and lattice slant 3.3 deg (no parameter, in core_material);
  Table 1 rows of other works (cited, rule 3).
- Fab / facility: passive "Test structures ... were fabricated" (p.5), no org, no facility; authors at SCNU, SYSU, ZJU.

## wang2017b (single-etch focusing SWG GCs, O-band, high-efficiency and broadband)

- Two fabricated rows: measured peak CE -3.8 / -4.3 dB, 3-dB BW 41 / 71 nm, 1-dB BW 21 / 38 nm (Fig. 6 device), spreads
  over 11 copies each (-4.3..-3.8 / -4.5..-4.2 dB; 41-45 / 65-71 nm; n counted on the Fig. 7 Device-ID axis), back
  reflection about 20 dB (1280-1360 nm) and 15.5 dB (1260-1280 nm) `derived` from the ripple ER; simulated -2.9 / -3.3 dB,
  BW 41 / 75 nm (3 dB), 24 / 46 nm (1 dB); design geometry (Table 1 / 2), footprint < 1080 um2 (`derived`, 45 x 24 um).
  Scope loopback_half with the fiber-array loss included (p.7).
- Two bottom-mirror design rows (2D FDTD): -1.0 / -1.3 dB, 3-dB BW 46 / 86 nm.
- Not entered: directionality 0.61, substrate penetration loss 1.6 / 2.4 dB, l_sub 80 nm, SWG fill factors 0.46 / 0.17
  and SWG counts 3 / 2 (no parameter, notes); Fig. 8 sensitivity curves; headline "below -15 dB" (covered by the two
  band rows).
- Fab: "fabricated using electron beam lithography at Applied Nanotools Inc." (p.7) -> `org_applied_nanotools`. CMC
  Microsystems acknowledged only for simulation / CAD tool access (p.9): neither fab nor facility.

## zou2015 (Si3N4 GC with bottom Si grating reflector; theory only)

- 7 design GC rows following the paper's design steps: uniform without substrate (-5.80 dB, 1-dB BW 70 nm), uniform on
  Si substrate (-3.51 dB), apodized on Si substrate (-3.13 dB), uniform + Si GR (-1.47 dB), apodized + Si GR P_GR 870 nm
  (-1.01 dB), apodized + Si GR P_GR 890 nm (-0.88 dB, headline), CD 150 nm variant (-0.90 dB, back reflectivity 2 % ->
  17.0 dB simulated). One `reflector.other` design row for the Si grating reflector (> 92 % over the C band, P 870 nm,
  tooth fraction 0.46).
- Loss values: wavelength 1550 nm `wavelength_inferred` (design peak wavelength stated on p.4; the losses are printed
  without one; Figs. 2(b) / 4(b) peak near 1550 nm).
- Not entered: back reflectivity 3 % of the CD 100 nm GC (the 870 nm and 890 nm reflector rows share that Si3N4 grating;
  D159, notes on both); separation layer H 1.68 um / H_SiO2 1.62 um (no parameter: see registry gaps); tolerances
  (0.04 dB per 20 nm H, 4 / 7 nm shift per 20 nm groove change, BOX 1 / 3 um); comparison DBR (110 / 270 nm); values
  cited in the introduction (refs. [3]-[17]).
- Fab: none (design only; Sec. 3 is a proposed process).

## Judgment calls for the auditor

1. benedikovic2016: 9 layout x grating rows with figure reads, headline -2.7 / -2.5 dB only in notes (D159 / D552
   per-device reads). Alternative: 3 rows per grating design with layouts as conditions, which would carry the uniform
   -2.7 dB as `best` (the apodized -2.5 dB stays ambiguous either way; its 0.9 dB penalty over simulation matches the
   continuously apodized -1.61 dB, not the two-step -1.78 dB).
2. benedikovic2016: the fringe-based back-reflection estimates entered on every row of the group the sentence names
   (6 % on 3 linear rows, ~3 % on 6 curved rows), not on one representative (D254 forbids only the latter). Could be
   notes only instead.
3. benedikovic2016: simulated nominal values and design geometry only on the linear-taper rows (the 2D model describes
   straight trenches).
4. chen2020b: loopback_half + measured although the paper never prints the halving (D452); polarization `both` because
   the P- and S-curves coincide; no-mirror 4.07 dB derived from the stated 1.7 dB difference.
5. wang2017b: the simulated -2.9 / -3.3 dB are not labelled 2D or 3D (condition says so); abstract 3-dB BW 40 nm vs body
   41 nm (41 entered).
6. zou2015: Si grating reflector as its own `reflector.other` design row (D396 split; it is optimized standalone, Fig. 3),
   whereas zhang2014 kept its DBR in notes. Fig. 3(b) y axis is mislabelled "Loss (dB)" for a linear reflectivity.
7. zou2015: intermediate design steps (no substrate, Si substrate) kept as design rows; fiber angle 8 deg entered as
   printed ("between the fiber and the GC surface").

## Registry gaps (skipped values, proposed definitions)

- `gap_nm` widened to fiber_chip_coupler (vertical spacing between the grating layer and a bottom reflector / substrate):
  zou2015 H 1.68 um (p.6), H_SiO2 1.62 um (p.4). Today `box_thickness_um` cannot hold it without confusing the drawing.
- `directionality_pct` (fiber_chip_coupler, simulated upward fraction): benedikovic2016 78 % at 33 deg vs 45 % at 10 deg
  (p.5 Fig. 2), 75 % for CD variants (p.8); wang2017b 0.61 (p.4).
- `field_overlap_pct` (fiber_chip_coupler, overlap of the diffracted field with the fiber mode): benedikovic2016 78 / 91 / 93 %
  (p.6-8).
- SWG gap / segment length for SWG gratings (`subwavelength_gap_nm`): benedikovic2016 W_G 166 nm (p.6), 102-185 nm
  (Tables 1-2); wang2017b l_sub 80 nm (p.4 Table 1).
- Substrate penetration (leakage) loss of a GC, dB: wang2017b 1.6 / 2.4 dB (p.6, simulated).

## Missing orgs

None. No fab or facility org printed in benedikovic2016, chen2020b or zou2015; Applied Nanotools is in the registry.
