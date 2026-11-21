# lit_225 batch report

Papers: lit:cheng2023b, lit:serries2001, lit:papatryfonos2014. Page-1 titles match the source rows. verified_on
2026-11-20. Dry run of `merge_component_staging.py`: +6 components, +71 metrics, 0 errors; the one warning names the
merged row cmp_lit_ni2025b_pimmwc, not in this batch.

| paper | components | metric rows |
|---|---|---|
| cheng2023b | 1 | 38 |
| serries2001 | 2 | 21 |
| papatryfonos2014 | 3 | 12 |

All three are discrete III-V lasers (laser class); in scope by the merged VCSEL and broad-area / FP laser precedents
(chaw2025, wu2025b, shi2010, hazan2022, chen2016, babichev2025).

## cheng2023b (40.1 GHz sub-freezing 850 nm VCSEL, Optics Express 2023)

`garbled_text_layer` (page 5): every value checked on the page renders (pages 5, 7, 9); the p.5 figure text layer is
garbled, captions and body text are clean.

Row: `laser.vcsel` `gaas` (one device, 25 C to -50 C as metric conditions):
- Fig. 2(b) (not attributed): 2 mA lasing peaks 846.04 nm (25 C) and 841.64 nm (-50 C), labels, measured; cavity shift
  0.0587 nm/C -> 58.7 pm/K (derived, D256).
- Fig. 3 / Sec. 4.1: fundamental mode ~848.5 nm at 8 mA (25 C) and 16 mA (-50 C), approx, measured.
- Fig. 5(b) (not attributed): f3dB 17.2 GHz at 4.2 mA (4 x Ith), -50 C, measured (PD response de-embedded only,
  fu2020 precedent; no parasitic de-embedding, so D678 `derived` does not apply).
- Table 1 S11 equivalent-circuit fit (measured, D80a; zeng2019 / li2015 model-element precedents), -25 C and -50 C,
  five biases each: Cp (10 rows), Cd (10 rows), Ca 48 fF (1 row per temperature) as `capacitance_ff`; Rm,total
  (DBR mirror resistance, 10 rows) as `series_resistance_ohm`.

Not entered:
- D259a / D408: Fig. 2(a), Fig. 5(a) and Fig. 6 carry "Adapted with permission from Cheng et al., Copyright 2020 IEEE
  [32]" (ref. [32] = the same authors' OECC 2020 paper, title "... 40.1 GHz modulation bandwidth at 223 K"). Out:
  thresholds 0.6 / 0.62 / 0.7 / 1.05 mA at 25 / 0 / -25 / -50 C (Fig. 2(a) caption, p.4 text; restated in the Table 1
  headers and the Table 2 "This Work" row); 4.4 mW peak at 12.7 mA (25 C), 8.4 mW maximum with roll-off at 17.4 mA
  (-50 C) (p.4); maximum f3dB 30.8 / 35 / 40.1 GHz at 25 / -25 / -50 C (Fig. 5(a), abstract, Table 2); the 40.1 GHz
  trace at 14.7 mA in Fig. 5(b) (same trace as Fig. 5(a) -50 C: identical bias, identical 40.1 GHz label); junction
  temperatures 13 / 62 / 78 C at 10 / 14.7 / 16 mA (from Fig. 6). All listed in the component notes.
- No registry parameter: recombination lifetime ~170 -> 113 ps and photon lifetime 5.5 -> 4.1 ps (25 C -> -50 C,
  gamma vs fR^2 fit, Fig. 8; wu2025b precedent); optical aperture ~4.8 um (Helmholtz estimate); 15 um mesa (shi2010
  precedent); 8 nm gain-cavity detuning (design); rms spectral width ~2 nm, transverse-mode split ~7 nm; Table 1 Rp
  (pad resistance) and Rj (junction resistance, a shunt element of the model, not a series resistance).
- Fig. 8 gamma / fR^2 points: no printed values.

Printed conflict: Fig. 5(a) caption names 25, 0 and -50 C; the legend and text name 25, -25 and -50 C (out anyway).

Fab / facility: fab empty (process steps passive, "We developed", D80b; authors at National Taiwan University and
UIUC). Facility missing from the registry (acknowledgment, p.12, "for experimental and semiconductor devices
fabrication support"): "Semiconductor Manufacturing Lab of the Consortia of Key Technologies" and
"Nano-Electro-Mechanical-System Research Center, National Taiwan University" (both facility role, lit:cheng2023b p.12).
Staff thanks for FIB / SEM (NSTC, National Taiwan University) not a facility (D84b).

## serries2001 (2 um GaInAs strained QW lasers on InP, IEEE PTL 2001)

The internal-efficiency / loss sentence on p.3 lost its numbers in the text layer; read from a PyMuPDF render of the
cached PDF page 3 (no `page_03.png` exists; D554 precedent).

Rows: two `laser.other` `inp` index-guided ridge FP lasers, 1750 x 37 um, uncoated (device A ternary GaInAs barriers,
device B quaternary GaInAsP barriers). Per device: highest-temperature emission wavelength (2050 nm at 320 K / 2092 nm
at 330 K, derived from um), wavelength drift 980 / 910 pm/K (derived from nm/K), CW maximum power per facet at each
printed heat-sink temperature (A 55 mW at 300 K, 2.8 mW at 320 K; B >= 120 / 100 / 42 mW at 300 / 310 / 330 K), T0 in
two ranges (A 37 / 21 K, B 45 / 31 K), total power efficiency as `wpe_pct` (A 10.4 / 0.75 %, B 13.4 / 5.5 %), length
and ridge width (design_target).

Not entered: differential quantum efficiency (A 25 -> 5.9 %, B 33 -> 19 %), internal quantum efficiency (72 / 71.5 %)
and internal loss (printed "6.9 %" / "5.8 %", unit as printed): no parameter (registry gap, D678); threshold current
densities (Fig. 4, log axis only); Fig. 2 spectra peaks at other temperatures (no printed values); Fig. 1 calculated
band offsets (values missing from the text layer, design calculation, no parameter).

Printed conflicts kept in conditions / notes: T0 low-temperature range "250 K up to 320 K" (text) vs "250 K-300 K" (Fig. 4
caption); device A high-range T0 printed for 300-330 K although A lases only to 320 K; device B power "up to 40 mW"
(p.1 introduction) vs 42 mW/facet (abstract, p.2, conclusion).

Fab / facility: fab = Fraunhofer IAF by D80b (abstract "We have fabricated and analyzed", all authors at one
institute), but the institute is not in the registry: left empty, note on both rows. Missing org: "Fraunhofer-Institut
fur Angewandte Festkorperphysik" (as printed with umlauts, p.1 footnote; fab role, lit:serries2001 p.1; parent
`org_fraunhofer_gesellschaft` exists). No facility.

## papatryfonos2014 (InAs/InP quantum-dash lasers for gas sensing, IPRM 2014, 2 pages)

Rows:
- `laser.other` `inp` 1150 um ridge laser (Fig. 1 typical device): CW / pulsed thresholds ~111 / ~107 mA, CW / pulsed
  power 5.3 / 7.0 mW at 350 mA (end of sweep), spectrum peak ~1980 nm at 160 mA, all `extracted_from_figure` from the
  embedded figure image (pixel calibration on the axis box and grid; uncertainties in notes); length 1150 um.
- `laser.other` `inp` 2.5 um x 600 um HR / as-cleaved ridge: threshold "as low as" 35 mA (best, measured); ridge
  width and length.
- `laser.dbr` `inp` LC-DBR design (row_kind design): kappa ~40 cm-1 (simulated, approx) at 2 um ridge width; duty
  cycle 79 % as `fill_factor` 0.79 (derived, w undefined, D253); ridge width 2 um.

Not entered: modal gain ~45 cm-1 and internal loss 18 cm-1 "for the 1.9 and 2 um lasers" (no parameter; device type
not named); 100 um broad-area lasers (no values); target grating lengths "200-300 nm" (unit as printed, likely um;
no laser grating-length parameter); ridge width of the Fig. 1 device (not stated with the figure; the study's ridge
lasers are 2.5 um, kept in notes only).

Fab / facility: empty. "have been designed, processed and characterized" is passive; authors at CNRS LPN (7) and III-V
Lab (1) (D80b). The SEM databar "LPN-CNRS" in Figs. 2-3 is an instrument label, not a fabrication statement. No
facility acknowledged.

## Judgment calls for the auditor

1. cheng2023b D259a scope: values of the three figures adapted from the authors' own OECC 2020 paper were removed
   everywhere they are restated (Table 1 Ith headers, Table 2 "This Work", abstract), including the headline 40.1 GHz,
   and the 40.1 GHz 14.7 mA trace in the unattributed Fig. 5(b) (same trace). Alternative under a literal D408 reading
   (only the attributing figure is out): add thresholds 0.70 / 1.05 mA (Table 1) and 40.1 GHz at 14.7 mA, 223.15 K
   (p.6 Sec. 3.2; Fig. 5(b)), measured. The ~848.5 nm rows cite Fig. 3 (unattributed) although the sentence also cites
   the adapted Fig. 6.
2. cheng2023b Table 1 elements: Cp (pad) and Ca / Cd (model elements) entered as `capacitance_ff`, Rm,total as
   `series_resistance_ohm`; Rp and Rj left out. 32 rows; trim if the coordinator prefers one bias per temperature.
3. serries2001 "total power efficiency" entered as `wpe_pct` (operating point and one / two facets not stated).
4. serries2001 maximum powers per temperature with statistic `best` (wu2025b precedent for a rollover maximum); the
   300 K device B value "at least 120 mW" with qualifier ge.
5. papatryfonos2014 LC-DBR row as `laser.dbr` row_kind design (laser never fabricated; only etch tests shown);
   alternative `reflector.bragg`. Platform `inp` from "the structures reported here" (InAs/InP Qdash).
6. papatryfonos2014 Fig. 1 thresholds read by extrapolating the L-I trace (no printed threshold for this device).

## Registry gaps (skipped value + locator, proposed definition)

- `differential_quantum_efficiency_pct` (laser): serries2001 p.3 / Fig. 5 (A 25 -> 5.9 %, B 33 -> 19 %); "external
  differential quantum efficiency above threshold, as defined by the paper" (already listed under D678).
- `internal_loss_per_cm` and `internal_quantum_efficiency_pct` (laser, amplifier): serries2001 p.3 (72 % / 71.5 %;
  6.9 / 5.8 printed with "%"), papatryfonos2014 p.1 (18 cm-1); "internal loss / efficiency from a cavity-length
  series" (babichev2025 and hazan2022 notes hold the same kind of value).
- `threshold_current_density_a_per_cm2` (laser): serries2001 Fig. 4 (D677 / D678 gap).
- `modal_gain_per_cm` (laser): papatryfonos2014 p.1 (~45 cm-1).
- `photon_lifetime_ps` / `recombination_lifetime_ps` (laser): cheng2023b p.10 (5.5 -> 4.1 ps; 170 -> 113 ps);
  wu2025b has the same skipped pair.
- `aperture_diameter_um` (laser.vcsel): cheng2023b p.3 / Fig. 2(b) caption (~4.8 um, Helmholtz estimate) (D678 gap).
