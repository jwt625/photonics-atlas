# lit_294 batch report

Distilled 2026-11-26 (verified_on 2026-11-26). Contract: pic-component-distill SKILL.md (hard rules, Contracts v4-v7), DevLog-002 D30-D84, DevLog-007 D150-D780.
Validation: `uv run --offline python scripts/merge_component_staging.py data/_staging/components/lit_294 --dry-run` -> +8 components, +73 metrics, 0 errors (the 2 warnings name merged rows of other papers).

Page-1 title check: all four cached texts match their `sources.csv` rows (soref2006 JSTQE 2006, sacher2015 JLT 2015, snyder2013 TCPMT 2013, bakir2010 PTL 2010). No correction / erratum, no garbled text layer.

| paper | components | metrics |
|---|---|---|
| soref2006 | 0 | 0 |
| sacher2015 | 6 | 49 |
| snyder2013 | 1 | 9 |
| bakir2010 | 1 | 15 |

## soref2006 (perspective / review): 0 rows

- The paper sets the stage for a JSTQE special issue ("reviewing the history, the present status, and the future prospects", p.1 Sec. I). Every device value is credited to other groups (Luxtera, BAE, Stanford QCSE modulator, MIT, Cornell, A. Poon, ...) with reference numbers, or reproduced from other papers' figures (Figs. 2-4 "reprinted"); rules 1 and 3, D259.
- The author's own content is proposals with no result: the Group IV microring laser diode (Fig. 5; ring diameter 3-5 um and ~300 nm bus gap as design ideas, p.6) and the N x N microring cross-connect / permutation switches (Figs. 6-7, "devices that have not yet been built", p.6). The 2 x 2 switch finding (complete switching at delta n ~2e-3) is from the author's earlier refs. [64]-[67] (D259). No component rows.

## sacher2015 (invited paper: review plus new results): 6 components / 49 metrics

Rows (all FEOL stack, fab `org_astar_ime`, process_name empty):
- `cmp_lit_sacher2015_feol_sin_wg` (waveguide_platform.straight, sin): LPCVD Si3N4 900 x 400 nm, 1.3 / 0.4 / 0.34 dB/cm at 1550 / 1580 / 1270 nm (TE, cutback) + geometry.
- `cmp_lit_sacher2015_feol_si_wg` (waveguide_platform.straight, soi_strip): Si 500 x 150 nm, ~2.9 dB/cm (C band, inferred from the paragraph) and ~6 dB/cm (O band) + geometry.
- `cmp_lit_sacher2015_trans_scl` (waveguide_platform.transition, si_sin_multilayer): Si tip 180 / Si3N4 tip 200 nm, Lc 15 um, < 0.07 dB over 1480-1600 nm (measured, cutback); simulated < 0.09 dB for Lc > 10 um; geometry.
- `cmp_lit_sacher2015_trans_oband`: Si tip 140 / Si3N4 tip 200 nm, Lc 15 um, < 0.09 dB over the O band; geometry.
- `cmp_lit_sacher2015_crossing` (crossing.mmi, sin): < 0.07 +/- 0.01 dB per crossing 1480-1600 nm (cutback), crosstalk > 48 dB measured, > 70 dB simulated; Fig. 5(a) labelled dimensions (23 um x 3.5 um MMI, 6 um tapers) as extracted_from_figure.
- `cmp_lit_sacher2015_uniform_gc` (fiber_chip_coupler.grating, si_sin_multilayer): uniform bi-level GC, -2.3 dB peak (loopback_half, derived from the stated square root), 1-dB bandwidth 110 nm, peak ~1540 nm read off Fig. 7; 21 deg design fiber, period 1.4 um, stack.

Values not entered and why:
- BEOL stack (PECVD SixNy 600 nm waveguides 3.5 / 0.8 / 0.24 dB/cm, 220 nm Si waveguides, BEOL transitions < 0.2 dB, BEOL tips 200 / 300 nm SEMs): "first reported in [20]" (Fig. 3 / Fig. 4 captions, p.5) = the authors' lit:huang2014; D259.
- Apodized bi-level GC (simulated -1.0 dB / 82 nm, measured -1.3 dB at 1536 nm / 80 nm, focusing layout and two-stage taper, Fig. 6 parameters), -16 dB reflectivity bound, +/-50 nm / +/-100 nm interlayer-misalignment simulations: credited to [21] (= lit:sacher2014b, merged); D259.
- Uniform GC simulated design values (-1.8 dB, 114 nm, 1536 nm, 80 % directionality, p.6-7): same values as the merged lit:sacher2014b uniform design row (cmp_lit_sacher2014b_uniform_gc_design, p.5-6 there); D259. Tooth widths 750 / 400 nm and offset 250 nm not entered as width_nm (sacher2014b precedent).
- 1-dB fiber alignment sensitivity ~2 um (p.7): "the grating coupler" not tied to the uniform or apodized design, and the same value is merged on lit:sacher2014b (D159 / D259).
- PRS (crosstalk < -19 dB, IL < 1.5 dB, PDL < 1.0 dB) and polarization controller (IL < 4.5 dB with its budget: PRS ~3 dB for two, transitions ~0.07 dB, MMIs ~0.1-0.2 dB each, waveguide ~0.3 dB): "These figures are taken from [22]" (= lit:sacher2014a, merged with the same 4.5 / 1.5 / 1.0 dB values); D259.
- Simulated transition misalignment excess loss (< 0.03 dB perpendicular / < 0.001 dB along, +/-50 nm offsets, p.4): no registry parameter (D250 rejected tolerance parameters for transitions); not proposed again.
- Comparison values of other works (0.1 dB/m, 0.3 dB/m, 4.2 dB/m, Si crossing 0.04-0.1 dB / -35 dB, Si GCs -0.64 to -1.6 dB, 67 nm Si3N4 GC, -4.2 dB, 1 dB per transition of wafer-bonded platforms): cited (rule 3).
- Raw transition loss per transition < 0.06 / < 0.07 dB and the uncertainties (< 0.01 / < 0.02 dB): in the transition component notes, not as separate rows (the printed headline bounds already include them).

Judgment calls for the auditor:
1. Fab `org_astar_ime`: Sec. III is titled "SiN-on-SOI fabrication at IME", the text says "At the Institute of Microelectronics, we have developed" the FEOL / BEOL flows and the reported devices "were fabricated in a BEOL and a FEOL process" (p.2). Contract v4 says "we developed" alone is not enough; here the org is named with the process, as on the merged lit:sacher2014b / sacher2014a rows. Kept; please rule.
2. FEOL LPCVD Si3N4 losses: the paper says the FEOL waveguide losses are presented for the first time (p.3), but 1.3 dB/cm at 1550 nm and 0.4 dB/cm at 1580 nm equal the 400 nm LPCVD entries of lit:huang2014 Table 1 ("from our earlier runs"; that table gives 0.32 dB/cm at 1270 nm vs 0.34 here). Entered as this paper's own result with a note; the alternative is D259 removal of the two matching values.
3. Uniform GC geometry (period 1.4 um, 21 deg, stack) entered on the new fabricated row although the same design numbers appear in sacher2014b's uniform design row; only the performance values of that design were withheld (D259).
4. Si 150 nm waveguide: "about 2.9 dB/cm" and "about 6 dB/cm" are printed for the 150 nm and 220 nm Si guides together; entered only on the FEOL 150 nm row (the 220 nm guides are BEOL / ref. [20]). The 2.9 dB/cm row gets c_band inferred from its paragraph.
5. Transition SCL span 1480-1600 nm and the simulated row use the Fig. 4(d) axis span for "SCL-bands" (wavelength_inferred); the O-band row uses `band: o_band` as printed.

Missing orgs: none (`org_astar_ime` in the registry). Registry gaps: none new.

## snyder2013: 1 component / 9 metrics

- `cmp_lit_snyder2013_gc_angle_polished` (fiber_chip_coupler.grating, soi; li2015 angle-polished packaging precedent), fab `org_imec` (acknowledgment "for fabrication of the test devices", p.5; D448).
- Metrics: 9 dB peak fiber-to-fiber after epoxy (measured; includes the 4 mm waveguide), 4.5 dB per coupler (loopback_half, derived: authors' halving), 4.3 dB theoretical maximum per grating (author_estimate, origin not stated, C band inferred), measured 1-dB lateral tolerance X 2.75 / Y 2.6 um and simulated X 2.8 / Y 2.6 um (half-widths of the printed 5.5 / 5.2 / 5.6 / 5.2 um windows), simulated 1-dB working distance <= 13.5 um (tol_1db_longitudinal_um), 10 deg design angle.

Values not entered and why:
- Fig. 1(a)-(b) grating geometry (12 x 20 um area, 70 nm etch in 220 nm Si): introduced as an SEM of "one of these gratings" of refs. [1]-[9] (p.1); not tied to the packaged first-generation grating (D159); in the component notes.
- Roll tolerance (simulated +/- 2.5 deg; measured < 1 dB excess over > 5 deg, p.3-4), epoxy-induced efficiency rise (simulated 2.95 dB, measured nearly 3 dB), peak shifts (14 nm blue with epoxy on a flat-cleaved fiber, 6.25 nm per degree red with fiber pitch, net 10 nm red): no registry parameter (see gaps).
- Earlier-work values (76 % / -1.2 dB GC of ref. [8], 20-30 nm blue shift and ~9 nm/deg of refs. [2], [3], [15]): cited (rule 3).
- Expected < 2.8 dB fiber-to-fiber and < 1.4 dB per coupler with improved gratings: projections, not results.
- Packaged ring resonator filter (Fig. 6, provided by imec / Ghent University): spectrum only, no printed value; Fig. 3(b) measured working-distance scan: no printed 1-dB value; initial working distance 2-3 um is a fit-derived setup value.

Judgment calls for the auditor:
1. Fab: only `org_imec`. The packaging (polish, V-grooves, capillary epoxy, cure) is the authors' process at Tyndall National Institute (registry `org_tyndall_national_institute`), but the paper states it in passive voice and "our current packaging activity" (p.4); Tyndall not entered as fab (D450-style assembly with no first-person statement). Please rule whether Tyndall should be co-fab for the packaged interface.
2. Tolerances stored as half-widths of the printed full windows (registry definition), basis derived (measured) / simulated (D83f), assuming windows centred on the optimum.
3. Peak wavelength ~1541 nm for the 9 / 4.5 dB rows read off Fig. 5(c) (wavelength_inferred true, +/- 3 nm); polarization not stated.

Missing orgs: none. Registry gaps (proposed, with skipped values):
- `tol_1db_roll_deg` (deg, fiber_chip_coupler / fiber_interface): fiber roll misalignment about its axis for 1 dB excess loss (+/- value). Skipped: simulated +/- 2.5 deg (p.3 Sec. II-B, Fig. 2(c)); measured < 1 dB over > 5 deg (p.4, Fig. 3(c)).
- `angle_tuning_nm_per_deg` (nm/deg, fiber_chip_coupler): shift of the peak coupling wavelength per degree of incidence angle (sign as printed). Skipped: 6.25 nm/deg red shift for steeper incidence (p.5, Fig. 5(b)).
- (lower priority) cladding / index-matching induced peak shift and efficiency change of a GC: 14 nm blue shift, net 10 nm red shift, ~3 dB rise (p.5); definition varies with the packaging step, not proposed as a parameter.

## bakir2010: 1 component / 15 metrics

- `cmp_lit_bakir2010_siox_ssc` (fiber_chip_coupler.edge, platform other): Si nano-tip (500 -> 80 nm, 220 nm Si) under a n~1.6 SiOx rib injector (3.5 um, 1.5 um etch), 1 um silica encapsulation, lensed fiber MFD 3 um.
- Metrics: per-coupler loss < 1 dB 1520-1600 nm, < 3 dB 1300-1600 nm (both polarizations), < 0.25 dB at 1550 nm (all loopback_half, derived: stated halving assuming identical couplers); 1-dB bandwidth ~100 nm, 3-dB bandwidth > 300 nm (both polarizations, derived from the per-coupler spectrum); simulated < 1 dB over 1550-1600 nm (BPM, TE); mfd_fiber_um 3 (specification); geometry (500 nm, 220 nm, 80 nm tip, taper 200-300 um range, SiOx 3.5 um, etch 1.5 um derived, slab 2.0 um derived, 1 um cladding).

Values not entered and why:
- Wafer-level spread: three additional samples, variation < 0.2 dB over 1500-1600 nm, ~0.6 dB at 1400 nm, ~1 dB at 1300 nm (p.3): no registry parameter for coupler-to-coupler / across-wafer loss spread (gap below); in the component notes.
- PDL: not printed; Fig. 4(a) traces for 0-90 deg polarizer angles not read into a PDL value.
- Fig. 3(a) simulated coupling efficiency vs taper length (~0.8 at 300 um by eye): only the printed "< 1 dB over 1550-1600 nm" entered.
- 2-D grating coupler ~20 % and other intro values: cited (rule 3). Cleaved SMF MFD ~10 um: future work.

Judgment calls for the auditor:
1. Fab empty: "fabricated on a 200-mm wafer with the standard CMOS technology" names no org; six of seven authors at CEA-Leti (`org_cea_leti`), one at INSA Lyon (D80b / D154). Contract v7 forbids filling fab from affiliation.
2. Platform `other`: the fiber-facing layer is silicon-rich oxide (SiOx, n ~1.6); `sion` or `silica` would assert a composition the paper does not state (D82f, D71).
3. The < 0.25 dB at 1550 nm row has polarization unspecified (the sentence does not tie it to TE / TM); the 1520-1600 / 1300-1600 rows and the bandwidths use `both` (title, abstract and p.3 "for both TE/TM polarization states").
4. taper_length_um entered as the printed 200-300 um design range; the measured coupler's length is not stated.

Missing orgs: none. Registry gap (proposed): `il_spread_db` (dB, fiber_chip_coupler; or widen `il_nonuniformity_db` to fiber_chip_coupler with "max - min loss across samples / wafer sites, sample count in condition"). Skipped: < 0.2 dB over 1500-1600 nm across four samples of the 200 mm wafer, ~0.6 dB at 1400 nm, ~1 dB at 1300 nm (p.3 Sec. III).
