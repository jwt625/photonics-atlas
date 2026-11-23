# lit_258 batch report

Papers: lit:prost2019 (IEEE Photonics J. 2019), lit:malik2014 (Optics Express 2014), lit:steckler2024 (IEEE PTL
2024), lit:lischke2019 (IEDM 2019), lit:yan2018 (IEEE PTL 2018). Page-1 titles match the source rows; no garbled
text layers; no correction / erratum. verified_on 2026-11-23. Dry run: +26 components, +129 metrics, 0 errors (the
only warning is the pre-existing ni2025b duplicate, not in this batch). No existing rows for these sources. Only
values each paper reports itself are entered; comparison tables of other works (steckler2024 Table I columns
Runge / Lischke / Liu / Steckler [7]; lischke2019 Table 1 columns [7], [5], [4]; yan2018 Table I rows [12], [15],
[20]) are not entered.

## Components / metric rows

| paper | component | class | metrics |
|---|---|---|---|
| prost2019 | cmp_lit_prost2019_ge_strip_wg | waveguide_platform.straight | 4 (1.6 dB/cm mean over 4.55-4.60 um, spiral cutback; 2 x 2 um; 50 um bend radius) |
| prost2019 | cmp_lit_prost2019_trench_heater | phase_shifter.thermo_optic | 6 (P_pi 52 mW derived from 104 +/- 14 mW per 2 pi; 53 mW simulated; 1 mm x 4 um x 200 nm Ti/Au; 3 um lateral gap) |
| prost2019 | cmp_lit_prost2019_heater_no_trench_design | phase_shifter.thermo_optic (design) | 1 (P_pi about 490 mW simulated, no trenches) |
| prost2019 | cmp_lit_prost2019_sinx_ge_grating_emitter | free_space_emitter.grating_emitter | 5 (45 deg simulated; period 1.6 um; 1.5 mm; duty cycle 0.81 -> 0.5; 2 um wire) |
| prost2019 | cmp_lit_prost2019_opa_12ch | free_space_emitter.other | 10 (divergence 3.07 x 0.18 deg measured, 3.2 / 0.15 deg expected; steering up to 12.7 deg lateral by phase, up to 12 deg longitudinal by wavelength, +/-22.5 deg unambiguous calculated; 0.069 deg/nm; 12 channels; 6 um pitch) |
| malik2014 | cmp_lit_malik2014_ge_si_heater_700um | phase_shifter.thermo_optic | 8 (P_pi 350 mW measured-derived and simulated; 700 um; 2 um x 100 nm metal; 2 um gap; 2.2 x 2 um waveguide) |
| malik2014 | cmp_lit_malik2014_ge_si_fib_undercut_heater_210um | phase_shifter.thermo_optic | 2 (P_pi 40 mW from 80 mW per 2 pi; 210 um) |
| malik2014 | cmp_lit_malik2014_ge_soi_heater_210um | phase_shifter.thermo_optic | 3 (P_pi 52.5 mW from the abstract 105 mW; about 60 mW simulated, Fig. 11; 210 um) |
| malik2014 | cmp_lit_malik2014_ge_soi_undercut_heater_210um | phase_shifter.thermo_optic | 3 (P_pi 10 mW simulated and confirmed by measurement; 210 um) |
| malik2014 | cmp_lit_malik2014_ge_soi_undercut_heater_280um | phase_shifter.thermo_optic | 2 (P_pi 8 mW from 16 mW per 2 pi; 280 um) |
| malik2014 | cmp_lit_malik2014_ge_soi_wg | waveguide_platform.straight | 3 (7 dB/cm TM at 5.25-5.35 um; 2.2 um; 2 um Ge) |
| malik2014 | cmp_lit_malik2014_amzi_test | wdm.cascaded_mzi | 4 (typical IL 0.5 dB, ER 19 dB; FSR 25 nm; 260 um path difference) |
| steckler2024 | cmp_lit_steckler2024_ge250_20 | photodetector.ge_waveguide | 13 (internal R 0.62 / 0.71 A/W at -2 / -4 V, 1620 nm; 0.72 at -4 V, 1610 nm from Fig. 3; 0.52-0.55 at 0 V; BW > 110 GHz at -2 V and at 1.5 mA, -4 V; dark ~200 / ~500 nA, 2500 / 6250 mA/cm2; 0.25 x 20 um, ~400 nm) |
| steckler2024 | cmp_lit_steckler2024_ge400_20 | photodetector.ge_waveguide | 12 (R 0.76 / 0.9 at 1620 nm; 0.91 at 1610 nm Fig. 3; 0.52-0.55 at 0 V; 85 GHz at -4 V; dark as above; 0.4 x 20 um) |
| steckler2024 | cmp_lit_steckler2024_ge550_20 | photodetector.ge_waveguide | 13 (R 0.74 / 0.97 at 1620 nm; 0.96 at 1610 nm Fig. 3; 0.52-0.55 at 0 V; 65 GHz at -4 V; about 10 GHz above 1 mA; dark as above; 0.55 x 20 um) |
| steckler2024 | cmp_lit_steckler2024_gc_1d | fiber_chip_coupler.grating | 1 (about 3.5 dB per grating at 1610 nm, estimate) |
| lischke2019 | cmp_lit_lischke2019_sin_ge_pd_bulk_si | photodetector.ge_waveguide | 8 (BW > 67 GHz at -2 V, ~40 GHz at 0 V; internal R 0.29 A/W at 1310 nm; per-diode dark <= 400 nA at -2 V (~96 %) and <= 60 nA at -1 V (~98 %) from 57-site array maps; single-diode 15-40 nA at -2 V and 11-12.5 fF at -2 V from figures; 20 um) |
| lischke2019 | cmp_lit_lischke2019_soi_ge_pd_reference | photodetector.ge_waveguide | 2 (7-8 fF and ~30 nA at -2 V, figure reads of the reference measured here) |
| lischke2019 | cmp_lit_lischke2019_sin_gc | fiber_chip_coupler.grating | 2 (6-6.5 dB loopback half at 1310 nm, 9 sites; peak about 1325 nm) |
| lischke2019 | cmp_lit_lischke2019_sin_gc_followup | fiber_chip_coupler.grating | 1 (mean about 5 dB per coupler at 1310 nm, 57 sites) |
| lischke2019 | cmp_lit_lischke2019_sin_wg | waveguide_platform.straight | 3 (about 2.3 dB/cm at 1310 nm; 1300 x 500 nm) |
| yan2018 | cmp_lit_yan2018_nicr_heater_10um | phase_shifter.thermo_optic | 9 (P_pi 9 mW from 18 mW per 2 pi; 215 / 132 pm/mW with / without slow light; rise 2.4 / fall 2.0 us; ~2.5 us simulated; 10 x 2 um; 6.5 um edge-to-PhCW-centre) |
| yan2018 | cmp_lit_yan2018_nicr_heater_20um | phase_shifter.thermo_optic | 6 (about 123 / 79 pm/mW from Fig. 5(b); rise 5 / fall 6.5 us; 20 x 2 um) |
| yan2018 | cmp_lit_yan2018_phcw_slow_light | waveguide_platform.slow_light | 4 (ng about 35 at 1540-1545 nm; 3 dB PhC IL from the loss budget; 220 nm; 2 um BOX) |
| yan2018 | cmp_lit_yan2018_phcw_mzi | wdm.cascaded_mzi | 3 (FSR 3.6 nm; 15 dB fiber-to-fiber; 145.64 um path difference) |
| yan2018 | cmp_lit_yan2018_gc | fiber_chip_coupler.grating | 1 (6 dB per coupler, origin not stated) |

Per paper (components / metrics): prost2019 5 / 26, malik2014 7 / 25, steckler2024 4 / 39, lischke2019 5 / 16,
yan2018 5 / 23. Total 26 / 129.

## Values not entered and why

prost2019
- 1x2 MMI (35.5 x 9 um, 4.8 um output pitch, 2 -> 3 um tapers over 50 um) and the 1x16 MMI tree: geometry only, no
  performance value (no row).
- Test asymmetric MZI FSR "approximately 23 nm" at 4.6 um (225 um path difference): no fsr parameter for
  phase_shifter and no other MZI performance value; in the phase-shifter notes.
- Simulated thermal crosstalk at 200 um pitch (25 % without trenches, < 0.1 % with): no phase_shifter crosstalk
  parameter. Trench design (> 200 um deep, 20 um wide, 5 um from the waveguide) and the fabricated 200 um trench depth:
  notes only (etch_depth_nm would misdescribe a substrate isolation trench).
- Fig. 4(a) waveguide-crosstalk simulation (10 % only after 1 cm for pitch > 3.2 um): array design study, no parameter.
- n_eff,TM 3.89 (simulated mode, Fig. 1(c)): no effective-index parameter.
- Setup values (QCL 200 mW, 180 nm tuning, NA 0.64 / 0.22 lenses, 0.038 deg/px, +/-13 deg acceptance): rule 13.
- Conclusion "uniform propagation constant over a 2-mm length" conflicts with the 1.5 mm design; not entered.

malik2014
- Fig. 11 / Fig. 13 length series (70-700 um, measured and simulated tuning power per 2 pi): only the text-anchored
  lengths are entered (210 / 280 / 700 um); the remaining sibling lengths would need about 30 figure reads and new
  rows each. Plateau statements (about 100 mW for long Ge-on-SOI heaters; about 110 mW at 700 um for the collapsed
  free-standing heaters) in notes.
- Simulated total phase shifts in Fig. 3(b) (1.98 pi at 700 mW), Fig. 5(b) (2.1 pi at 80 mW), Fig. 10(b)
  (2.0291 pi at 100 mW), Fig. 12(b) (2.0569 pi at 20 mW): not converted (the 700 / 20 mW per 2 pi statements are
  entered as printed).
- Fig. 6 simulated buried-oxide absorption vs Si thickness (no value printed); FIB trench depth 15 um (simulation
  window label only).
- Ge-on-Si waveguide loss (ref. [7], cited): not entered.

steckler2024
- Responsivity "improvement of > 35 %" over the authors' earlier devices: relative value, no parameter.
- Fig. 3 (1610 nm) responsivities at 0 / -1 / -2 / -3 V and Fig. 4 at -1 / -3 V: only text / table values plus the
  -4 V points at 1610 nm (used by the conclusion) are entered.
- Fig. 6 inset bandwidths of Ge400_20 / Ge550_20 at 0.3-1.5 mA beyond the printed "about 10 GHz above 1 mA": curves
  only.
- Self-heating responsivity increase with optical power (Fig. 7-8, up to 1.3 mW): curves only.
- Franz-Keldysh parameter Ep = 26.3 eV: model input, no parameter.
- Si waveguide locally thinned from 220 nm to 50 nm under the Ge (Fig. 1-2): no parameter for the Si thickness under
  an absorber (core_material text).

lischke2019
- Table 1 columns for refs. [7], [5], [4] (cited): not entered. The SOI reference PD's bandwidth and responsivity
  (cited from [7]) not entered.
- -1 V frequency response (Fig. 5) has no printed 3-dB value; forward current at +0.2 V (Fig. 13, about 0.24 uA per
  diode): no parameter. Yield: 3 of 57 edge arrays failed (statement only).
- SiN feed taper 1.3 um -> 600 nm over 30 um at the PD: taper_length_um not allowed for photodetector (core_material).
- Fig. 11 / 12 histogram centres (about 40 nA at -1 V, about 250 nA at -2 V): the arrows are not defined as mean or
  median; the cumulative-plot statements (98 % / 96 %) are entered instead.

yan2018
- Operating bandwidth about 10 nm of the slow-light heater (p.4): no phase_shifter bandwidth parameter.
- Average response time 2.2 us (intro) and Table I "2 us": summaries of the measured rise / fall; not separate rows.
- PhCW lattice constant 400 nm, hole radius 101 nm, row shifts 37 / 9 nm: period_nm not allowed for
  waveguide_platform; core_material text.
- Calculated group-index curve (3-D PWE, Fig. 1(d)) and FEM thermal map (40 K below the heater at the PhCW centre):
  curves / model, not entered.

## Missing fab / facility orgs

None. prost2019: org_university_of_california_davis (fab), org_center_for_nano_micro_manufacturing and
org_marvell_nanofabrication_laboratory (facility, p.9 acknowledgment) exist. steckler2024 / lischke2019:
org_ihp_leibniz_institute_for_high_performance_microelectronics exists. malik2014 and yan2018 have no fab statement
naming an org and no facility acknowledgment.

## Judgment calls for the auditor

1. steckler2024 / lischke2019 fab IHP (borderline): first-person process statements ("we had to apply a CoSi2 based
   process", "we introduced a CMP step") with authors mostly at IHP plus TU Berlin / IHP Solutions; lischke2019 also
   thanks IHP's cleanroom staff (D84b). Follows lischke2020 / steckler2025 precedent; no process_name printed.
2. steckler2024 internal responsivities `author_estimate` (grating loss "estimated to be around 3.5 dB per grating at
   1610 nm", origin not stated, also applied at 1620 nm); lischke2019 0.29 A/W `derived` (6.25 dB from the measured
   9-site GC pair spectra, Fig. 9). Precedents are split (lischke2020 derived, lischke2021 author_estimate).
3. steckler2024 shared statements entered on all three variant rows: dark current ~200 / ~500 nA and densities
   ("All PDs exhibit ...", Table I spans all three columns) and the zero-bias range 0.52-0.55 A/W (printed jointly,
   per-variant values not printed). D254 forbids one representative row; here the statement covers each device.
4. steckler2024 text inconsistencies (D417): Ge250_20 0.71 A/W (Table I) vs 0.72 A/W (p.3 text) at 1620 nm, -4 V;
   conclusion "0.71 to 0.97 A/W at -4 V and 1610 nm" vs Table I at 1620 nm. Table values entered at 1620 nm; Fig. 3
   reads added at 1610 nm.
5. malik2014 Ge-on-SOI 105 mW per 2 pi (abstract, no length) tied to the 210 um device via the Fig. 11 measured point
   and Fig. 10(c) (D159 borderline: the 280 um point is about 100 mW).
6. malik2014 undercut Ge-on-SOI 210 um measured P_pi entered as approx 10 mW `derived` from "20 mW ... confirmed by
   the measurements in Fig. 12(c)" (no separate measured number printed).
7. malik2014 AMZI test row: "typical" IL 0.5 dB / ER -19 dB entered on an array-level MZI row (D165) rather than on a
   heater row; platform read as Ge-on-Si (Sec. 2 precedes the Ge-on-SOI section; Fig. 2(b) chip not stated).
   FSR 25 nm author_estimate ("resulted in").
8. malik2014 phase-shifter wavelengths: band mid_ir, wavelength_inferred, from the stated 5 um range (no wavelength
   printed with each P_2pi).
9. prost2019: p.9 says the 12.7 deg phase-tuned steering is longitudinal; abstract and conclusion say lateral; entered
   as lateral. Divergence 3.07 deg (Sec. 3, conclusion) vs abstract 3.08 deg. Unambiguous range +/-22.5 deg stored
   as a 45 deg full span `simulated`.
10. prost2019 fab org_university_of_california_davis from the first-person fabrication section with all authors at
    UC Davis (D72), plus both acknowledged facilities (D448).
11. prost2019 / malik2014 / yan2018 / lischke2019 test-structure and design-study rows: no-trench heater kept as a
    `design` row (P_pi about 490 mW); yan2018 PhCW-MZI kept as `wdm.cascaded_mzi` (FSR, fiber-to-fiber IL);
    prost2019 test MZI not given a row (FSR only, origin not stated).
12. yan2018 PhC insertion loss 3 dB `author_estimate` (15 dB minus 2 x 6 dB, GC loss of unstated origin); group
    index ~35 `derived` (extraction method only cited from ref. [15]); lischke2019 reference SOI PD row from figure
    reads of measurements made in this paper (Fig. 6 / 7), not from ref. [7].
13. lischke2019 dark currents per diode from 500-diode arrays stored with qualifier `le` and the percentile in the
    condition (Table 1 "< 400 nA"); single-diode figure reads (Fig. 7) kept as a separate range row.
14. Platforms: Ge-on-Si / Ge-on-SOI rows `other` (gallacher2018 precedent); lischke2019 SiN-fed PD `sin` (ahn2007
    precedent).

## Registry gaps (skipped value + locator + proposed definition)

- phase_shifter thermal crosstalk: prost2019 25 % -> < 0.1 % at 200 um pitch (simulated, p.5-6). Proposed
  `thermal_crosstalk_pct` (phase_shifter, switch_fabric): fraction of the phase / temperature change induced in a
  neighbouring channel at the stated pitch.
- phase_shifter operating bandwidth: yan2018 about 10 nm (p.4). Proposed `operating_bw_nm` (phase_shifter): span over
  which the stated efficiency holds (criterion in condition).
- fsr_nm for phase_shifter test interferometers: prost2019 about 23 nm (p.7); malik2014 25 nm is on the AMZI row.
  Alternative: keep MZI test rows as `wdm.cascaded_mzi`.
- layer2_thickness_nm for free_space_emitter: prost2019 160 nm SiNx grating overlayer (p.4, p.6).
- period_nm / hole radius for waveguide_platform.slow_light: yan2018 a = 400 nm, r = 101 nm (p.2). Proposed: allow
  period_nm on waveguide_platform and add `hole_radius_nm` (waveguide_platform, reflector, resonator).
- taper_length_um for photodetector feed tapers: lischke2019 30 um (1.3 um -> 600 nm SiN, p.2).
- Si thickness under an absorber: steckler2024 50 nm (220 nm SOI locally thinned, Fig. 2). Proposed
  `under_absorber_thickness_nm` (photodetector).
