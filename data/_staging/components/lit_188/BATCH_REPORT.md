# lit_188 batch report

Papers: lit:yu2014, lit:lu2019a, lit:fontaine2019, lit:deotare2009a, lit:heide2022. verified_on 2026-11-18. All five
cached texts match their source rows (page-1 titles checked); none is a correction. All five are arXiv copies: yu2014
(arXiv 1404.7532, preprint of the APL 2014 paper), lu2019a (arXiv 1805.04011 v1; preprint title "Chip-integrated
visible-telecom photon pair sources for quantum communication" vs the Nature Physics title "... entangled photon pair
source ..."), fontaine2019 (arXiv 1803.04126 v2 of the Nature Communications paper; Supplementary Material not
cached), deotare2009a (arXiv 0905.0109 v1 of the APL paper), heide2022 (arXiv 2202.10949 v1 of the OFC 2022 demo
paper). Values come from the cached copies; journal versions unread. Dry-run: +28 components, +66 metrics, 0 errors
(the one warning concerns cmp_lit_ni2025b, not this batch).

## lit:yu2014 (InP PhC Fano structure, all-optical switching)

Components 19 / metric rows 26:

| component | metrics | content |
|---|---|---|
| cmp_lit_yu2014_sym_tb{1,0p6,0p4,0p2,0}_fig1 (`resonator.photonic_crystal`, 5 rows) | 6 | Qt 10400 / 4000 / 2700 / 4200 / 7000 (Fig. 1(c) labels), Qv ~1.2e4 on the open-waveguide row |
| cmp_lit_yu2014_asym_d{0p5a,1a,2a,3a}_fig2 (`resonator.photonic_crystal`, 4 rows) | 4 | Qt 4500 / 5200 / 1800 / 3500 (Fig. 2(c) labels) |
| cmp_lit_yu2014_sym_tb{1,0p1,0}_fig3 (`resonator.photonic_crystal`, 3 rows) | 6 | Qt 1.1e4 / 6.1e3 / 8.6e3, Qv ~1.5e4 each |
| cmp_lit_yu2014_fano_cavity_1556, _lorentz_cavity_1540, _fano_cavity_ber | 3 | Qt 3.8e3 at 1556 nm, 5.2e3 at 1540 nm, 1.5e3 |
| cmp_lit_yu2014_fano_switch_1556, _lorentz_switch_1540 (`switch_fabric.other`) | 4 | switching contrast 14 / 4 dB, 90-10 % decay 30 / 80 ps (~110 fJ pump) |
| cmp_lit_yu2014_fano_switch_ber (`switch_fabric.other`) | 2 | eye-diagram extinction 5 dB at 0.67 mW, 8.7 dB at 1 mW (10 Gbit/s RZ-OOK) |
| cmp_lit_yu2014_lensed_fiber_input (`fiber_chip_coupler.edge`) | 1 | ~8.5 dB input coupling loss, author_estimate (origin not stated) |

Not entered:
- BER values (< 1e-9, < 2e-7; p.8), mode volume 0.44 (lambda/n)^3 (p.3), spacing between resonance extremes ~1.7 nm
  (p.8), Fabry-Perot fringe period 0.5-0.6 nm (p.4), chirp: no parameters (in notes where useful).
- Fit parameters t_B^2 and gamma2/gamma1 (FDTD / FEM estimates): notes only.
- Lattice constant / hole radius (a = 447 nm, R = 116 +/- 0.8 nm, Rc = 0.85R, h = 340 nm; Fig. 1(b) caption): in
  core_material, no metric rows (period_nm for a 2-D PhC lattice and a hole radius are not clear registry fits).

Judgment calls:
- Fig. 2(c)(i) (D = 0, f = 1.1, t_B^2 = 0.2, Qt 4200) has the same parameters and spectrum as Fig. 1(c)(iv): treated as
  the same structure, one row (cross-note).
- Qt basis: Lorentzian (t_B^2 = 0) and inverse-Lorentzian (t_B^2 = 1) fits `measured`; Fano-shape fits use a t_B^2
  (and for the asymmetric set gamma2/gamma1) taken from simulation (Methods p.11) -> `derived` (D80a). Qv rows
  `author_estimate` (D403; Fig. 1 value rests on FDTD). Figure-printed Qt labels kept with the method basis and a
  Fig. locator (not `extracted_from_figure`: the numbers are printed labels, nothing read off an axis).
- Fig. 1 / Fig. 2 Qt rows: wavelength not stated; `s_band` inferred from the plot axes (1516-1527 nm). Fig. 3 rows and
  the coupler: `c_band` inferred from the Fig. 3 axes. BER cavity: `band unspecified`.
- All-optical switch elements `switch_fabric.other` (D158 / D407; ofc2026 M2E.5 precedent) with the cavity Qt on a
  separate `resonator.photonic_crystal` row (D396). Decay times ps -> us `derived` (D256).
- Fig. 3 Qv ~1.5e4 is one sentence for the three structures; entered on each of the three rows (it is a per-structure
  "similar Qv" statement, not a family typical value on one representative row; D254 noted for the audit).
- Fab org_technical_university_of_denmark ("Y. Y. and K. Y. fabricated the samples", p.12; both DTU Fotonik). No
  facility named.

## lit:lu2019a (Si3N4 microring visible-telecom photon-pair source)

Components 5 / metric rows 18:

| component | metrics | content |
|---|---|---|
| cmp_lit_lu2019a_sin_ring_r25_pair_source (`resonator.ring`) | 13 | loaded Q 1.52e5 / 1.04e6 / 1.93e5 at 668.38 / 933.62 / 1547.90 nm, linewidths 2950 / 310 / 1000 MHz (derived), pump notch 5.53 dB (derived from 28 % transmission), R 25 um, 500 nm Si3N4, 3 um BOX, bus widths 560 / 1120 nm, 33 um pulley coupling length (design) |
| cmp_lit_lu2019a_ring_sfwm_opo (`frequency_converter.other`) | 1 | parametric oscillation onset ~0.29 mW pump (printed ">~290 uW") |
| cmp_lit_lu2019a_facet_pulley_wg (`fiber_chip_coupler.edge`) | 2 | 3.9 dB / facet at 668.4 nm, 2.3 dB / facet at 933.6 nm (lensed fiber) |
| cmp_lit_lu2019a_facet_straight_wg (`fiber_chip_coupler.edge`) | 1 | 4.2 dB / facet at 1547.9 nm |
| cmp_lit_lu2019a_mode_id_rings (`resonator.ring`, test structure) | 1 | Q > 1e5 (one statement for the three bands, band unspecified) |

Not entered:
- Photon-pair flux, CAR (up to 3800 +/- 200), Klyshko efficiencies, detection efficiencies: photon-pair metrics are not
  registry parameters (D250); detectors / filters are setup (rule 13).
- Photon extraction efficiencies 84 % / 20 % (signal / idler waveguides, p.11): no parameter (registry gap below).
- Frequency mismatch 0.16 GHz / 3.86 GHz (p.6), mode numbers, simulated coupling Q curves (Fig. 2(e,f)), wavelength
  tuning 630-810 nm across pump wavelength / ring-width series (Fig. 6): no parameters or not component metrics.
- Fabricated ring width of the pair-source device (only the ~1140 nm design target and the 1105-1165 nm Fig. 6 series
  are printed) and the pulley gap (design range 200-250 nm only): not entered.
- Mode-splitting magnitudes of the test rings: not printed.

Judgment calls:
- Fab empty: X.L. "led the design, fabrication, and measurement" (p.10) with two affiliations (NIST CNST, Maryland
  NanoCenter) and no stated place (D83c, he2026 precedent). The UMD-NIST cooperative agreement is a funding
  acknowledgement (D80c). No facility.
- Facet couplers split by port (pulley vs straight waveguide; rule 9), values `measured` (printed per-facet, D167).
- OPO onset as `frequency_converter.other` `pump_threshold_mw` on a function row of the same ring (D396, mckenna2022
  precedent); uW -> mW `derived`.
- Ring radius 25 um and coupling length 33 um `design_target` from the design section; the measured modes carry the
  designed mode numbers, the fabricated radius is not separately stated (note).

## lit:fontaine2019 (MPLC Laguerre-Gaussian mode sorter)

Components 1 / metric rows 11:

| component | metrics | content |
|---|---|---|
| cmp_lit_fontaine2019_mplc_lg_sorter_210 (`mode_converter.mdm_mux`, platform other) | 11 | measured IL 5.8-6.3 dB over 1510-1620 nm; simulated IL 2.5 / 3.2 / 3.2 dB at 1565 / 1510 / 1620 nm; total crosstalk worst 5.5 dB, mean 7.2 dB; per-mode crosstalk 28.7 / 30.4 dB (derived by the authors); 210 inputs / outputs; 89.8 um spot pitch |

Not entered:
- MDL 8.7 / 12.5 / 13.3 dB measured and 3.3 / 6.8 / 6.5 dB theoretical at 1565 / 1510 / 1620 nm (p.5): `mdl_db` is
  allowed only for fiber_interface (registry gap below).
- Maximum loss variation between any two LG modes 1.7 dB at 1565 nm (p.5): `il_nonuniformity_db` not allowed for
  mode_converter (registry gap below).
- Channel capacity 6.25 bits/photon (simulated 7.15): no parameter.
- 0.49 dB excess loss per SLM reflection (p.5): a property of the purchased SLM; the paired "approximately 0.82dB of
  total loss" wording does not reconcile with the 5.8-6.3 dB IL, kept out.
- The 325-mode device (Supplementary Material, not cached).
- 12 um pixel-blur simulation curves (Fig. 4(a)): simulated variant, not a design of the device.

Judgment calls:
- Scope: free-space MPLC with fiber-array input built on an LCoS SLM: kept in scope as `mode_converter.mdm_mux`,
  platform other, by analogy with D424 (LCoS / MEMS free-space parts with fiber I/O). The output side is a free-space
  beam characterized by off-axis digital holography (no fiber). Flag for the audit if D424 should not extend to mode
  multiplexers.
- IL scope `device_total` (mean squared singular value of the measured transfer matrix, input spots to recovered
  field). Crosstalk sign: the paper defines total crosstalk as "power in the desired mode relative to the total power in
  all other modes" yet prints negative dB; stored as positive suppression magnitudes with the printed sign in notes.
- Fab empty: no fabrication / assembly statement naming an org; SLM vendor (Holoeye) as a note only (purchased part, not
  the device under test).

## lit:deotare2009a (coupled Si PhC nanobeam cavities)

Components 3 / metric rows 11:

| component | metrics | content |
|---|---|---|
| cmp_lit_deotare2009a_double_nanobeam_s146 (free-standing) | 4 | even-mode Q 1e5-2e5 (3 separations, ~1523-1530 nm); simulated Q > 1e6 (FDTD); 220 nm Si, 500 nm beam width |
| cmp_lit_deotare2009a_double_nanobeam_s136_onsub (on SiO2) | 4 | even-mode Q 1.5e4-2.0e4 (4 separations, ~1540-1562 nm); 220 nm, 500 nm, 2 um BOX |
| cmp_lit_deotare2009a_double_nanobeam_s136_free (after release) | 3 | Q ~3.4e4-4.0e4 read off Fig. 3(d) (`extracted_from_figure`); 220 nm, 500 nm |

Not entered:
- Single-nanobeam Q 7.5e5 and simulated > 1e7 (ref. 21, authors' earlier paper; rule 3 / D259).
- "1.4 x 10^7" in the odd-mode sentence (p.2): not tied unambiguously to the odd mode or the single cavity (D156 /
  D159). Fig. 2(a) legend (even above odd) also conflicts with the text (odd higher); noted on the simulated row.
- 70 nm simulated differential even / odd shift and "resonance tuning over a 20 nm range" (static tuning across
  devices with different gaps): no nm splitting parameter; tuning_range_nm would misdescribe a device series.
- Mode volume ~0.7 (lambda/n)^3, simulated Q points of Fig. 3(b,d): not entered.
- Gap d per device: only read off the Fig. 1(c) / Fig. 3 axes (about 110-180 nm) and d = 100 nm for the SEM in Fig. 1(a,b);
  kept in notes (not tied to the Q rows device by device).

Judgment calls:
- Separation series entered as one row per cavity design (s = 146 nm free-standing; s = 136 nm on-substrate) with
  `range` values and n_samples (D165). The released s = 136 nm cavities are a separate row (different guiding stack)
  with a cross-note.
- Fab org_harvard_university and facility org_center_for_nanoscale_systems: "Device fabrication was performed at the
  Center for Nanoscale Systems at Harvard" (p.3) is a stated place (D448; hickstein2019 / sun2017 precedents); all
  authors at Harvard SEAS. SOITEC wafer: supplier note.
- Platform `soi` for both the free-standing and the oxide-supported nanobeams (asano2017 precedent; no suspended-Si
  enum), stack in core_material / cladding.

## lit:heide2022 (off-axis digital holography, OFC 2022 demo)

Components 0 / metric rows 0. The paper is a characterization-method demo. The only device value is the MDL of a
6-mode photonic lantern, plotted in Fig. 3(a) (about 1.0-1.6 dB over 191.3-196.2 THz, read off the plot) and Fig. 3(b)
(about 1.05-1.1 dB at 193.4 THz over ~2000 s), p.3. Not entered: `mdl_db` is not allowed for mode_converter, and the
paper states it cannot separate the lantern's wavelength dependence from the measurement apparatus (p.2; D159-type
ambiguity), so even with the parameter the attribution would need a ruling. Photonic-lantern makers (CREOL authors)
not stated as fabricator.

## Missing fab / facility orgs

None. Orgs used are in the registry: org_technical_university_of_denmark (yu2014 fab, p.12), org_harvard_university
and org_center_for_nanoscale_systems (deotare2009a fab / facility, p.3).

## Registry gaps (proposed)

1. `mdl_db` for `mode_converter` (D250 rejected it for lack of a skipped value; now skipped): fontaine2019 MDL 8.7 dB
   at 1565 nm, 12.5 dB at 1510 nm, 13.3 dB at 1620 nm measured; 3.3 / 6.8 / 6.5 dB theoretical (p.5, Fig. 4(a));
   heide2022 6-mode photonic lantern ~1.0-1.6 dB over the C band (p.3 Fig. 3(a), attribution caveat). Definition: as
   for fiber_interface, mode-dependent loss = ratio of the largest to smallest squared singular value of the transfer
   matrix, in dB, at the stated wavelength.
2. `il_nonuniformity_db` for `mode_converter`: fontaine2019 maximum loss variation between any two LG modes 1.7 dB at
   1565 nm (p.5, Fig. 4(d)). Definition: max minus min per-mode insertion loss.
3. Resonator photon-extraction (escape) efficiency in % (kappa_ext / kappa_total of the extraction port): lu2019a 84 %
   signal / 20 % idler (p.11 Supp. Sec. II). `power_coupling_pct` is a bus-to-ring coupling coefficient, not this
   ratio. Proposed `extraction_efficiency_pct` (resonator, wdm), port in condition.
