# lit_182 batch report

Distilled 2026-11-18 (verified_on 2026-11-18). Papers: lit:dmitriev2022, lit:rueda2019, lit:castro2025, lit:liu2019b.
Validation: `merge_component_staging.py data/_staging/components/lit_182 --dry-run` -> +12 components, +66 metrics,
0 errors (the one warning printed is for merged row cmp_lit_ni2025b_pimmwc, not this batch).

All four cached files are arXiv preprints of the listed journal papers (page-1 titles match the source rows; same
authors and results). Values are distilled from the cached preprint only; journal versions unread (D430 / D433). This
is stated in each component's notes.

| paper | cached copy | components | metric rows |
|---|---|---|---|
| dmitriev2022 | arXiv 2112.07398v1 (Phys. Rev. Applied paper) | 7 | 28 |
| rueda2019 | arXiv 1808.10608v2 (Nature paper) | 0 | 0 |
| castro2025 | arXiv 2407.15438v1 (APL Photonics paper) | 4 | 22 |
| liu2019b | arXiv 1812.04550v1 (Optica paper) | 1 | 16 |
| total | | 12 | 66 |

## dmitriev2022 (hybrid integrated dual-microcomb source)

Rows: two Ligentec Si3N4 rings (`ring_150ghz`, `ring_1thz`, resonator.ring), the chip edge coupler
(`edge_coupler`), the two commercial pump diodes (`fp_laser_diode` laser.other, `dfb_laser_diode` laser.dfb) and the two
assembled self-injection-locked soliton comb sources (`sil_comb_150ghz`, `sil_comb_1thz`, laser.comb, platform other as
merged raja2019 rows). Cross-notes between each ring and its comb row (D396).

Not entered and why:
- Parametric-instability threshold P_th 14 / 11 mW: no resonator parameter; entered as `pump_threshold_mw` on the comb
  rows (merged laser.comb precedent), condition says it was measured with the external laser plus booster. Fig. 2(b)
  caption prints ~13 mW for the Fig. 2 ring (noted).
- Thermal-nonlinearity threshold 3.7 / 2.5 mW; D2/2pi 1.38 / 14.3 MHz (dispersion, D81 rejected); coupling coefficient
  eta = 0.42 / 0.59 (kappa_c / kappa, no parameter): notes only (p.8).
- Comb spans (500 nm, > 200 nm) and the nominal "~150 GHz" / "~1 THz" repetition rates: no comb-span parameter; the
  measured D1/2pi is on the ring rows.
- Dual-comb RF values (delta, Delta 7.93 -> 1.70 GHz, 300 nm -> 600 MHz, 100 nm -> 800 MHz): system level.
- Microheater tuning "up to tens of GHz" (p.11): no number.
- Butt-coupling loss diode-to-chip: not printed (it enters P_pump).

Judgment calls:
- kappa_0 / kappa_c `measured`: the Methods fit includes backscattering (doublet fit), which fixes the coupling regime
  (D587 / D465 precedent). The printed unqualified "Q-factor ~1.8e6 / ~1e6" equals omega / kappa_0, not the loaded
  omega / (kappa_0 + kappa_c) (about 1.07e6 / 0.42e6), so it is entered as `q_intrinsic`, basis `derived` (authors'
  conversion), D519 precedent.
- gamma/2pi (34 / 331 MHz, "backward-wave coupling rate ... (mode splitting)") as `mode_splitting_ghz` derived
  (dirani2019 precedent).
- Edge coupler "insertion losses as low as -1.1 dB on both sides of a chip" (p.2): read as per side, `per_coupler`,
  `best`, basis `author_estimate` (no measurement or method shown, reads as a chip property; nader2025 / D418 rather
  than D167). Flag for the audit.
- Pump-to-comb efficiencies 25 % / 40 % `author_estimate`: P_pump is the diode power reduced by a coupling loss that is
  not printed. The printed approximate powers give 25.7 % / 42.5 %.
- Laser-diode characteristics (35 GHz mode spacing, 1535 / 1545 nm, ~200 / ~100 mW, SMSR ~50 dB) `author_estimate`
  (stated without a measurement; datasheet vs own measurement not said).
- Beat-note linewidths (W_L 0.5 kHz, W_G 68 kHz) put on the 150 GHz comb row: the inset is in Fig. 2(e) (the Fig. 2
  prototype, FP diode, ring identified as the 150 GHz class by p.4); the p.8 Methods sentence cites "Fig. 3(e, f)",
  which holds no beat-note inset (D417 note).
- Supp. Note 1 comb-line position spread 0.9 nm over 7 chips: `wavelength_spread_nm` on the 1 THz ring row,
  statistic range, n_samples 7.
- Comb rows fab empty (assembly maker not stated; Ligentec only on the chip rows, D617 / Contract v7 per-part fab).
  process_name empty ("commercial multi-project wafer (MPW) runs" names no process).

Missing orgs: "Seminex Corp., USA" (fab role: vendor of the FP laser diodes, p.11 Supp. Note 2 and p.8 Methods; the
Methods parenthetical may also cover the DFB diodes) -> fab on `cmp_lit_dmitriev2022_fp_laser_diode` after the org
round (DFB row only if a ruling reads the Methods sentence that way).

## rueda2019 (resonant electro-optic frequency comb)

0 rows. The device is a machined single-crystal LiNbO3 whispering-gallery-mode disk (R = 2.45 mm, minor radius 1.5 mm,
h = 0.4 mm; p.5 and Methods "We fabricate a lithium niobate WGM resonator") in a 3D copper microwave cavity with a
silicon-prism coupler: a discrete bulk mm-scale resonator, out of scope (D411; tebeneva2024 / zhang2025e precedents).
Values seen and not entered: Q_o 1.4e8, critical coupling gamma = gamma' = 2pi x 0.35 MHz, FSR ~8.9 GHz, g = 2pi x
7.43 Hz, microwave Q 241.4, estimated Vpi 260 mV, 180 comb lines / ~1.6 THz (11 nm) span at 20 dBm microwave power and
317 uW optical input. The Vpi / EO comb values would be EO-atlas material if that atlas takes bulk resonant modulators.

## castro2025 (mode-hop-free tunable lasers at 780 nm, GaAs-on-SiN)

Rows: `vernier_laser` (laser.tunable, platform other, Nexus fab), its design-stated parts `front_sagnac_mirror`
(reflector.loop_mirror, 100 % `author_estimate`) and `monitor_tap_mmi` (splitter.mmi, 15 % `author_estimate`), and the
external SFWM test ring `sin_ring_r1p49mm` (resonator.ring, sin; fab not stated).

Not entered and why:
- 645 pm phase-tuning mode hop: text "likely between two Vernier peaks" vs Fig. 3(a) caption "mode hops at the cavity
  FSR" (ambiguous quantity).
- Ring heater map ranges 0-60 / 150-190 mW and 23-90 mW phase settings (Fig. 3(d-g)): map settings, not a tuning
  figure of merit.
- 92.4 Hz SIL linewidth: Zhang et al. ref. [27] (rule 3). Corato-Zanarella comparison values (ref. [26]): rule 3.
- Etched-facet front-mirror laser variant (Rb lock, p.6): no component value; 10-minute lock stability is a system
  result.
- Lensed fiber spot 2 um / working distance 10 um, > 35 dB fiber isolator: setup (rule 13); the angled edge coupler and
  the monitor photodiode have no performance value (no rows).

Judgment calls:
- One laser row for the 15-laser chip design; the two Fig. 2(a) lasers (different QW stack thickness) are separated by
  condition on the SMSR rows (D165 array-level practice). Threshold, linewidth, output and MHF values come from
  unnamed representative lasers of the same design.
- Printed conflicts kept with notes (D417): threshold 32 mA (text) vs ~30 mA (caption); tuning range > 17 nm per gain
  chip (entered) vs 20 nm (abstract) and > 15 nm (Sec. 1 / 2); output "over 10 mW" (Sec. 1) vs "up to 10 mW"
  (conclusion), entered as approx 10 mW, reference plane unspecified.
- MHF range as `tuning_range_nm` 0.217 nm (printed 108 GHz / 217 pm, rees2020 / kiewiet2026 practice), the 1 W
  extrapolation 0.62 nm `author_estimate` (D435), single-element ranges from the Fig. 3 labels (11.1 / 15.6 pm), ring FSR
  1.3 nm from the single-ring mode hop on the laser row (tran2019 precedent).
- Test ring: Q_i and the 144 MHz intrinsic width `author_estimate` (single Lorentzian, D403); wavelength 775.8 nm read
  off the Fig. 4(b) axis (`wavelength_inferred`), section heading says 780 nm; 20 GHz FSR `author_estimate` (nominal).
- Facility `org_ucsb_nanofabrication_facility` on all four rows ("A portion of this work was performed in the UCSB
  Nanofabrication Facility", p.6; D604 practice). process_name empty (Nexus "heterogeneous GaAs-on-SiN device
  platform" names no process).

Missing orgs: none (org_nexus_photonics, org_ucsb_nanofabrication_facility in the registry).

## liu2019b (20 GHz passively mode-locked QD laser grown on Si)

Row: `qd_mll_20ghz` (laser.comb, platform iii_v_on_si_epi, facility UCSB Nanofab, fab empty: passive growth / processing
sentences, D80b).

Not entered and why:
- RF 3-dB linewidths 1.8 kHz and 2.7 kHz: no RF-linewidth parameter (registry gap, D431 candidate `rf_linewidth_hz`).
- RF tone SNR 64 / 66 dB, SA isolation resistance ~15 kOhm, mode-locking region 75-200 mA / 1-5 V, ~10 ps pulses at
  high current, SA length 14 % of the cavity (no parameter), ~600 nm isolation etch (not a waveguide etch).
- Group index 3.66 "previously obtained" (rule 3).
- 4.1 Tbit/s PAM-4 transmission over 64 channels, BER, 2.7 / 3.1 bit/s/Hz: system level (data_rate_gbps is a D534
  registry candidate).

Judgment calls:
- Threshold 42 / 58 mA assigned to SA reverse bias 0 V / 2 V from the Fig. 2(a) legend (text gives only the rise with
  bias).
- Single-facet output 17.8 mW at 200 mA, 0 V read off Fig. 2(a) (`extracted_from_figure`, +/-0.5 mW); not printed.
- Per-mode optical linewidth 10.6 MHz is the average over lines amplified by an external SOA (Fig. 4(a) legend), noted.
- Single-line RIN -133 dB/Hz includes the external SOA (condition and note).
- Stage temperature 18 C entered as temperature_k 291.15 on the measured rows.

Missing orgs: none.

## Registry gaps (skipped value + locator + proposed definition)

- Parametric (Kerr) oscillation threshold on `resonator`: dmitriev2022 14 / 11 mW (p.8 Methods). Proposed: allow
  `pump_threshold_mw` on resonator ("parametric oscillation threshold of the resonator, reference plane in condition").
  Entered on the comb rows meanwhile.
- Thermal-nonlinearity (thermal bistability) threshold: dmitriev2022 3.7 / 2.5 mW (p.8). Proposed
  `thermal_bistability_threshold_mw` (resonator).
- Comb span: dmitriev2022 500 nm / > 200 nm (p.5), rueda2019 ~1.6 THz (out of scope). Proposed `comb_span_nm` (laser);
  previously deferred (D81 / D418).
- RF beat-note linewidth of a mode-locked laser: liu2019b 1.8 kHz / 2.7 kHz (p.4, Fig. 3(c)). Proposed `rf_linewidth_hz`
  (laser, D431 candidate).
- Mode-hop-free tuning in frequency: castro2025 108 GHz (p.4; stored as 0.217 nm). D538 candidate.
- Registry title: lit:castro2025 fine; lit:liu2019b `sources.csv` title prints "41 Tbit/s" where the page-1 title and
  abstract print "4.1 Tbit/s" (decimal point lost): fix the registry title.
