# lit_99 batch report (2026-11-06)

All six cached texts match their source rows (page-1 title); none is another paper, a correction or an erratum. Dry-run:
+22 components, +177 metrics, 0 errors (the one warning, ni2025b m18 / m4, is an existing merged row, not this batch).

| paper | components | metrics |
|---|---|---|
| sun2025a | 5 (phase_shifter.thermo_optic: 2; resonator.ring: 2; wdm.mrr: 1) | 43 |
| wu2025a | 2 (phase_shifter.other) | 23 |
| akhlaghi2015 | 3 (photodetector.snspd) | 19 |
| anthony2019 | 4 (photodetector.ge_waveguide; photodetector.apd; fiber_chip_coupler.edge; waveguide_platform.straight) | 32 |
| iadanza2024 | 2 (photodetector.iii_v_on_platform) | 9 |
| wen2022 | 6 (photodetector.iii_v_on_platform: 4; fiber_chip_coupler.grating: 1; laser.other: 1) | 51 |

Source versions: sun2025a and wu2025a are arXiv-only source rows (no journal DOI in the row; nothing to compare).
wen2022 is the arXiv v2 text of the Nature Communications paper: same title and abstract claims; journal version unread
(D430 / D433). Garbled text layers: wu2025a p.19 is the reference list only (no value taken from it); iadanza2024 is
garbled on all 4 pages (digits dropped): every value was read from page renders (p.1 rendered from the PDF in the
scratchpad, p.2-4 cached renders).

## Not entered, and why

sun2025a
- Soliton microcomb of the 36 um ring (single soliton via heater scans, 40 mW on-chip pump, stable > 30 min, Fig. 3): no
  comb metric printed (spacing, span, power); no laser.comb row. Pump line near 1565 nm read from Fig. 3(c) only as a note.
- Vernier design statements (about 13 GHz offset per two comb lines, > 70 THz clear range): design statements, notes.
- Predicted 30 pm/mW for a no-pedestal ring and the FEM K_eff curve: simulation of a design not built; note only.
- Grating couplers (Fig. 1(b)): no loss printed. Heater length / width: not printed.
- Resonance wavelength of the Q scans: not printed; band c_band with wavelength_inferred (mode family described in the
  1550 nm band; filter axis 1535-1537.5 nm).

wu2025a
- 218-day non-volatility (bar-port ratio 74.2 % -> 73.6 % +/- 0.7 % over 5232 h, Fig. 5(f)): D159. The caption assigns
  it to "MZI6", the text to the earliest trimming experiment detailed in Supp. Section S2, which is the O-band MZIO1; the
  design (C band vs O band) is ambiguous. Bound in both component notes.
- Index change delta n (0.0085 / 0.0173 / 0.016 C band; 0.0067 / 0.0093 O band): no parameter (registry gap below).
- Threshold voltage Vth 7.9-8.4 V (10 s pulses): no parameter (registry gap below).
- Loss: summed MZI output power stable within +/-0.15 / 0.13 / 0.075 dB (C band) and +/-0.1 / 0.19 dB (O band), called
  measurement error; no insertion-loss value printed, so none entered.
- Simulated temperature rise 20.2 K/mW at the WG centre, 3.2 K/mW at the undercut edge: no parameter.
- 15 MZI units of Fig. 6 ("distinct undercut thermo-modulated structures"): designs not given, no rows.
- Table 2 (comparison with fs-laser, Ge implantation, PCM trimming): other works / symbols only.

akhlaghi2015
- Designed cavity Q about 275, simulated absorption 98.4 % (29 % without cavity), resonances 1541 / 1543 nm: no Q /
  center-wavelength parameter on photodetector (gap below); in notes.
- Total measured jitter 90 / 72 ps FWHM (includes the 46 ps optical pulse) and electronic estimates 65 / 53 ps: notes;
  the detector jitters 77 / 55 ps are entered as derived.
- Saturated QE levels 1.04 / 0.99 of the cavity devices: sigmoid asymptotes, notes only.
- Passive-reference absorption eta_A 0.928 (57.2 um nanowire, transmission cutback): passive structure, no parameter.
- NbTiN film Tc 7.16 K and Jc: material properties, no parameter. Grating-coupler efficiency: not in the main text.
- Bias currents (3.5 / 5.0 uA) and the critical currents: Ic values not printed; bias currents in condition.

anthony2019
- alpha_sum 0.03 /um and alpha_Ge 0.0017 /um (73 dB/cm at 1900 nm): photodetector absorption coefficient, no parameter.
- Raman strain 0.12-0.15 %, bandgap narrowing 0.0375 eV: material analysis, no parameter.
- 11.3 GHz bandwidth (ref. [22]), > 6 GHz APD bandwidth (ref. [33]), 340 GHz GBP (ref. [32]): cited (rule 3).
- Si width under the Ge: only implied ("consistent with the wider end of the taper"); not entered.
- Taper 5 um -> 500 nm over 250 um: taper_length_um not allowed on photodetector; in core_material.

iadanza2024
- Waveguide-coupled responsivity "R~10%" at 1350 nm and "R~2%" near 1550 nm (-1 V, 5 K, Fig. 8(b)): the paper prints
  responsivity in %, unit undefined (its top-illumination text says 15-40 % while Fig. 6(a) plots 0.13-0.51 A/W); not
  entered.
- Dark current vs temperature (Fig. 9(a)): bias not stated (dark_current_na requires bias).
- Trap activation energies 2.0 / 29.0 / 132.0 meV, ideality factor, saturation current: no parameter.
- Device widths "100-500" (unit not printed), active volume ~1e-4 um3, ~0.003 lambda^3: not entered.
- f3dB > 70 GHz and 50 GBd reception "in earlier generations" (ref. [4] = wen2022): cited, rule 3.
- Grating couplers (Fig. 8(a), normalized spectra only), Bragg / zone-plate reflectors (SEM only): no metric, no rows.
- Fig. 6(b) simulated photocurrents: model, not entered.

wen2022
- Data reception (50 GBd OOK BER 3.21e-5; 100 Gbit/s 4PAM BER 1.17e-2): no parameter. A subset was presented at OFC 2021
  (ref. [43]); no value of that subset is entered anyway.
- SThM self-heating about 15 K at 3 V (T500, a 500 nm T-shape device) and simulated about 50 K under 3.16 mW
  detection: no parameter; T500 has no other metric, so no row.
- Simulated i-region absorption 10-20 %: supplement, note only.
- Fig. 5(b) I-V under 0.1-3.16 mW illumination, Fig. 6(c) bandwidths at 0 / -1 V: no printed values; the -1.5 V
  "> 70 GHz" is entered.
- Supplementary grating-coupler transmission / efficiency and waveguide loss (Supp. Fig. 6): not cached.
- Table 1 rows of other works: rule 3.

## Missing fab / facility orgs

- Carnegie Mellon University (sun2025a p.1 affiliation; p.2-3 first-person fabrication; would be fab on all 5 rows if
  registered, D419 / D448 first-person + stated site). Not in the registry.
- Bertucci Nanotechnology Laboratory at Carnegie Mellon University (sun2025a p.8 Acknowledgments, "acknowledge the use of"):
  facility candidate, parent CMU, all 5 rows.
- Materials Characterization Facility (CMU) (sun2025a p.8 Acknowledgments, "the use of"): facility candidate, all 5 rows.
- Supplier notes only (no row field): NGK Insulators (sun2025a SiCOI chip, in registry), STAR Cryoelectronics
  (akhlaghi2015 NbTiN-coated SOI wafers).
- Used orgs exist: org_amf, org_university_of_british_columbia, org_astar_ime, org_cmc_microsystems, org_ibm_research_zurich.

## Judgment calls

1. sun2025a heaters as separate `phase_shifter.thermo_optic` rows (tuning efficiency, time constant, bandwidth, heater
   geometry), rings as `resonator.ring` (36 um Q and 2.4 nm tuning range) and the 18 um filter as `wdm.mrr` (comb-line
   channel selector, D400 / D459), with D396 cross-notes; precedents chang2026a, dong2010. Platform `other` for 4H-SiCOI
   (wang2021 precedent).
2. sun2025a 36 um ring Q_i 1.4e6 `measured`: Fig. 3(a) dip reaches about zero and Q_i = 2 Q_L (D403 / D463). The filter
   Q_i > 1e6 stays `author_estimate` (no fit shown). FSRs 475 / 963 GHz `author_estimate` ("estimated", method unstated).
3. sun2025a 40 kHz bandwidth kept as printed (`derived` from the 7 us constant, the conversion is not printed and
   1/(2 pi tau) gives about 23 kHz; D417 note). 200 mW tuning power from the Fig. 2(c) legend (`extracted_from_figure`).
   Filter tuning range 300 GHz converted to 2.36 nm at 1536 nm (`derived`). Filter loss as `drop_loss_db` < 1 dB
   (on-chip, de-embedding method not stated).
4. wu2025a classed `phase_shifter.other` (non-volatile trimming element; jayatilleka2021 precedent), platform
   `soi_strip` (full etch stated p.18), fab org_amf (AMF MPW). Phase offsets `derived` (Methods 6.2 arithmetic on own
   P-T data). P_pi 1.25 mW read from Fig. 3(e) as the reversible thermo-optic operating point of the same heater (one row
   per class, not a second row). Table 1 "edge spacing between WG and heater" entered as `heater_gap_um` 2; deep-trench
   span as `length_um`. Fig. 5(b) MZI3 (text) vs MZI4 (caption) noted; same design.
5. akhlaghi2015 QE values stored in % from printed fractions (`derived`, D256); the two cavity devices as one range row
   (97-102 %, 1541-1543 nm, n 2) because the QE-to-resonance pairing is not stated. Jitters 77 / 55 ps `derived`
   (quadrature subtraction printed). TW reference detectors as separate rows (`test_structure` true). Fab UBC from the
   author contributions (D395 / D439).
6. anthony2019 p-i-n responsivities `derived` with ref_plane on_chip (internal values de-embedded with the paper's own
   measured coupling and propagation losses, D394 analogue); APD responsivities `measured` with ref_plane empty (plane not
   stated); APD gain `derived` (ratio to the p-i-n). Edge-coupler losses per_facet `measured` (D167) and propagation
   losses as separate rows (stated, measured on test structures). Fab IME + CMC (D398).
7. iadanza2024 and wen2022 PDs: class `photodetector.iii_v_on_platform`, platform `iii_v_on_si_epi` (TASE monolithic
   growth on SOI; mauthe2020 merged precedent uses the same platform). iadanza2024 responsivities read from the Fig. 6(a)
   A/W axis, not from the text's "%" range (D417 note). Log-axis dark-current-density reads (iadanza2024 Fig. 11, wen2022
   Fig. 5(c)) kept as `extracted_from_figure` with the A/cm2 -> mA/cm2 conversion noted; alternative: `derived` (D256).
8. wen2022 one row per design (T 200 / T 350 / S 350 / S 500) with device-labelled metric rows (T1 / T2, S1 / S2,
   S3 / S4); printed responsivities and EQEs `derived` (6 dB de-embedding, EQE formula), other devices read from the
   Fig. 5 bars. T2 saturation powers split by D435: only -0.5 V (-3.2 dBm) lies inside the measured input range
   (`measured`); the others exceed the highest measured input power (`author_estimate`). Grating coupler 6 dB as
   `author_estimate` per_coupler including the waveguide (origin in the uncached supplement). T3 as an LED entered as
   `laser.other` (D396, light-source class, label says "not a laser"); alternative: no row (only the 1550 nm EL peak).

## Registry gaps (skipped value + locator + proposed definition)

- `index_change` (phase_shifter): wu2025a delta n 0.0173 (p.13 Sec. 3.2), 0.0085 (p.11), 0.016 (p.20), 0.0067 (p.23),
  0.0093 (p.24). "Permanent / induced change of the (effective or material) refractive index, unitless, which index in
  condition". Same family as the delta_neff candidate of D417.
- `threshold_voltage_v` (phase_shifter): wu2025a Vth 7.9-8.4 V for 10 s pulses (p.8 Sec. 3.1). "Drive voltage above
  which a non-volatile change starts (pulse duration in condition)".
- `absorption_per_um` or `absorption_db_per_cm` (photodetector): anthony2019 alpha_sum 0.03 /um, alpha_Ge 0.0017 /um,
  73 dB/cm at 1900 nm (p.2-4). "Optical absorption coefficient of the detector section (lumped or material, which in
  condition)".
- `center_wavelength_nm` and `q_loaded` widened to photodetector (cavity-enhanced detectors): akhlaghi2015 resonances
  1541 / 1543 nm (p.4), designed Q about 275 (p.3).
