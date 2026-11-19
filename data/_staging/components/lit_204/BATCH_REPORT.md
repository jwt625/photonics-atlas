---
batch: lit_204
date: 2026-11-18
papers: lit:liu2022f, lit:zhu2017, lit:zhang2022e
validation: merge_component_staging.py --dry-run, 0 errors (+14 components, +74 metrics)
---

# lit_204 batch report

Page-1 title check: all three cached texts match their source rows. IEEE copies (zhu2017, zhang2022e) carry the
institutional download stamp (ignored). No `garbled_text_layer`.

| paper | components | metric rows |
|---|---|---|
| liu2022f | 8 | 32 |
| zhu2017 | 5 | 32 |
| zhang2022e | 1 | 10 |
| total | 14 | 74 |

## lit:liu2022f (review, Frontiers of Optoelectronics 2022)

A review of SOI thermo-optic phase shifters by authors who all sit at CUMEC. Almost all values are cited from other
works (Tables 1-3, Figs. 3-5, 8-10, 12-15, 18-20, 22-24) and are not entered (rule 3). Entered only the CUMEC
devices the text presents as the authors' own results with no citation in the sentence or caption:

- `hybrid_tops`: hybrid-heater TOPS, P_pi ~18.61 mW (p.4, Fig. 6(c) fit), measured.
- `folded_tops_f01` ... `f21`: folded-waveguide TiN-heater TOPS series (Fig. 16 / 17), one row per fold count
  (1, 5, 9, 13, 17, 21): P_pi from Fig. 17(a), rise / drop time from Fig. 17(b) (folds 5-21), all
  `extracted_from_figure`; widths 450 / 500 nm (p.11) `design_target`.
- `multipass_grating_tops`: TE0-TE1 antisymmetric-grating multi-pass TOPS, P_pi 6.7501 mW (Fig. 21(c) fit label),
  rise 7.100 us / fall 9.667 us (Fig. 21(d) oscilloscope readouts), measured.

Fab `org_chongqing_united_microelectronics_center` on all rows ("fabricated it on the CUMEC silicon foundry
platform", p.4; "we have fabricated ... on the CUMEC silicon platform", p.11; p.14). `process_name` empty (only
"CUMEC silicon (foundry) platform" printed, no PDK / node). Platform `soi_strip` for the hybrid TOPS (Fig. 1(e)
"strip waveguide"), `soi` for the others (strip / rib not stated).

Not entered:
- Table 1 / Table 3 CUMEC basic TOPS (TiN 19.12 mW/pi, silicide 21.75, doped Si 21.96, with heating / cooling
  times): credited to ref. [49], the authors' own 2020 symposium paper (D259 / D408).
- Table 3 CUMEC rows for the hybrid (6.0 / 6.0 us, FOM 111.66, 3.65 x 200 um), folded (2.75 mW/pi, 21.1 / 8.1 us,
  59.0 x 278 um) and multi-pass (6.75 mW/pi, 6.2 / 6.6 us, 18.3 x 450 um) devices: the table credits them to ref.
  [45] (Passaro et al., not a CUMEC paper); values in a row carrying a citation are cited work (rule 3 / D80i).
  Listed in component notes. The folded row's times match the 21-fold point of Fig. 17(b); the multi-pass times
  differ from the Fig. 21(d) readouts.
- Folded waveguide "spacing of 554 nm" (gap vs pitch not stated) and the "5.0 um semicircle" bend (text says the
  radius is much larger than 5.0 um): ambiguous, not entered.
- Fig. 17(c) FOM2 curve (model, minimum at 2 folds), Fig. 11 temperature simulation, typical 2 um / 220 nm / 2 um
  stack (stated as typical for SOI TOPS in general, not for these devices), MZI extinction in Fig. 6(b) / 21(b) (not
  stated), phase-shift spans in Fig. 6(c) / 21(c).
- Wavelength: not stated for any CUMEC measurement -> `band: unspecified` with a note on every P_pi row.

## lit:zhu2017 (IEEE JSTQE 2018)

All-silicon defect-mediated waveguide photodetector (vertical L-shaped p-n junction, one arm of a modulator MZI).

- `hv_pd_3mm` (photodetector.other, power-monitor operation): dark current 1.6 / 4.1 nA at -1 / -3 V, responsivity
  3 / 4.7 mA/W, saturation > 11 dBm in-arm, dark power ~0.01 uW, geometry (500 x 220 nm rib, 100 nm slab, 3 mm).
- `lv_pd_3mm`, `ll_pd_3mm` (photodetector.other): comparison junctions, responsivity at -3 V read off Fig. 2(d).
- `hv_apd_1mm` (photodetector.apd): breakdown onset ~-6.5 V, responsivity ~0.54 A/W at -9 V, < 0.01 A/W at
  -6.4 V, 41.5 mA/W at -6.8 V, dark current 0.7 uA (-6.8 V) / 80 mA (-9 V), 3-dB OE bandwidth 7 / 15 / 26 / ~16 GHz
  at -3 / -6 / -9 / -6.8 V, gain 10 / 60 / > 1000, GBP 28 THz, 765 mW at -9 V, geometry.
- `fiber_facet_coupling` (fiber_chip_coupler.edge): -4 dB/facet, `author_estimate` (origin not stated).

Responsivities and the saturation bound are `author_estimate`: they rest on the in-arm power the paper estimates from
-4 dB/facet coupling and a -3 dB split. Gains and GBP `derived` (gain = responsivity normalized to -1 V, stated).
Unit conversions `derived` (D256). Fab `org_astar_ime` (acknowledgment "for device fabrication", D448). Platform
`soi_rib`.

Not entered: dynamic range > 44 dB and noise floor ~-33 dBm, 30-40 % response drop over 1520-1620 nm, +29 % / +26 %
current change from 296 to 324 K, BER in-arm sensitivities and SNRs of the 28 Gb/s link, 30.6 pJ/bit (no registry
parameter); the 10 um monitor projection (~0.03 dB IL, ~10 pA at -30 dBm; hypothetical design, judgment call c);
the 1 mm Si modulator (EO bandwidth > 20 GHz, IL ~6 dB) is an EO-atlas item (rule 2); ref. [28] all-Si PD values
(rule 3). Conflict noted: 80 mA dark current at -9 V (p.6) vs the Fig. 5(a) inset (~85-90 mA).

## lit:zhang2022e (VLSI Symposium 2022)

- `ingaas_apd` (photodetector.apd, platform `other` per the III-V-on-SOI PD precedents arafat2024 / baumgartner2020):
  responsivity 0.99 A/W at 1570 nm (unity gain, on-chip, GC loss calibrated out), EQE 78 % (`derived`), dark
  current 7.6 nA at 90 % Vbr (bias_v -55.8 computed from Vbr -62 V), Vbr -62 V, gain > 70 (best, -59 V,
  Pin -48.3 dBm), absorber 100 x 12 um, 1 um InGaAs, 220 nm SOI, 3 um BOX (Fig. 2 label).
- Fab `org_national_university_of_singapore` (first-person "we realized ... the fabrication", Fig. 1 caption; all
  authors NUS).

Not entered: punch-through ~-47 V, Idark activation energy 0.297 eV (InP reference 0.283 / 0.284 eV), RMS roughness
1.39 nm, SU-8 bond layer < 150 nm (no registry parameter / not a photodetector parameter), grating coupler and taper
(no reported value; GC loss used for calibration but not printed), Table I values of refs. [5]-[11] (rule 3). The
temperature-dependent I-V (Fig. 13) prints no numbers.

## Judgment calls

- (a) liu2022f is a review; own CUMEC devices entered where the sentence and caption carry no citation (D80i
  "clearly reports it as its own result"); Table 3 CUMEC rows tagged [45] left out although they describe the same
  devices. Coordinator question: [45] may be a misprint for the authors' own ref. [49]; if the hybrid, folded or
  grating devices were first reported there, D259 / D408 would remove the entered rows. The text itself cites no
  earlier report for them, so they are kept.
- (b) Folded TOPS: one row per fold count (rule 9 sibling designs), values read off Fig. 17 (+/- 0.2 mW, +/- 0.3 us);
  fold counts read off the x-axis.
- (c) zhu2017 10 um monitor projection not entered as a `design` row (a scaling remark, not a design).
- (d) zhu2017 coupler row typed `fiber_chip_coupler.edge` from the printed "dB/ facet" wording and the chip-edge
  light path of Fig. 1(b); the coupler structure is not described.
- (e) zhu2017 Fig. 2(d) comparison devices (L-V, L-L) entered as rows with figure-read responsivity at -3 V; the
  text ratios (10x, 1.5-2x) agree only roughly with the curves (noted).
- (f) zhu2017 bandwidth / gain / GBP rows carry `band: c_band` inferred (test wavelength not stated in Sec. IV-A /
  IV-B; 1550 / 1553.3 nm elsewhere in the paper).
- (g) zhang2022e responsivity `measured` with ref_plane on_chip; the GC-loss calibration value and method are not
  stated (bian2025 precedent).
- (h) zhang2022e dark-current bias -55.8 V computed from "90% Vbr" and Vbr -62 V (noted); gain bias -59 V signed from
  the Fig. 12 axis (text prints "~59 V").

## Missing fab / facility orgs

None. All needed orgs exist (`org_chongqing_united_microelectronics_center`, `org_astar_ime`,
`org_national_university_of_singapore`).

## Registry gaps (skipped values, proposed definitions)

- `dynamic_range_db` (photodetector): linear-response range of a detector, max / min detectable power. zhu2017
  > 44 dB at -3 V (p.3 Sec. III-A).
- `activation_energy_ev` (photodetector): Arrhenius activation energy of the dark current. zhang2022e 0.297 eV
  (p.1 Results, p.2 Fig. 14).
- `punchthrough_voltage_v` (photodetector): bias at which the depletion reaches the absorber of a SACM APD.
  zhang2022e ~-47 V (p.1 Results, Fig. 10).
- `rx_sensitivity_dbm` (photodetector, candidate already listed in D436): in-arm power for a stated BER and bit rate.
  zhu2017 about -11 / -6 / -2 dBm (10 Gb/s, BER 1e-12) and -8 / -5 / -2 dBm (28 Gb/s, BER 1e-3) for B2B / 10 km /
  20 km (p.6, Fig. 10).
