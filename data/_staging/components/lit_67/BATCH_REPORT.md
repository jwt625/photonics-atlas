# Batch lit_67 report (distill subagent, 2026-11-02)

Dry-run `batch lit_67: +42 components, +290 metrics; errors 0` (the one warning printed, cmp_lit_ni2025b_pimmwc-m18,
belongs to another batch). ASCII only, no e-mail or street text. Page-1 titles of all 8 cached texts match their source
rows; no garbled text layer. iseghem2022 carries a "Corrected 28 July 2022" footer but is the full article, not a
correction notice. Values checked on page renders: chen2022 p.2; chen2024b p.2, 6, 9; grottke2020 p.7; guo2024 p.3-7;
iseghem2022 p.15; limongi2026 p.4; yan2017 p.3-5; zhang2024b p.8, 10. Supplements of chen2024b, iseghem2022, yan2017 and
zhang2024b are not cached.

## Per paper (components / metrics)

- iseghem2022 (3 / 24): LC side-rail phase shifters on iSiPP50G, `phase_shifter.other`: wg400g250, wg450g250,
  wg400g350. Phase shift at 10 VRMS read from Fig. 12 (0.86 / 0.28 / 0.40 pi; each agrees with 50 um / Table 3 L_pi),
  simulated weak / strong anchoring bounds, Table 3 loss (1.53 / 0.833 / 2.257 dB, derived, includes MMIs and recess
  transitions). Not entered: L_pi and Vpi*Lpi (no parameter, in notes), Table 1-2 confinement factors, comparisons to
  refs. [11], [25], [26].
- chen2024b (2 / 41): slow-light Bragg thermal shifter in MZI, AIM MPW. Vpi 1.1 V, P_pi 3.63 mW, 4.4 dB (relative to
  1580 nm) at 1551.5 nm; time constants at 1 - 1/e and 1/e in `thermal_time_constant_us`; stated points plus figure
  readings at 1554, 1556, 1558, 1560 nm. Bragg section alone as `reflector.band_stop` (11 nm from the two band edges).
  Not entered: AIM PDK shifter (quoted with Vpi 3 V and 3.2 V, not the authors' measurement), group index ~24 (cited,
  refs. 22, 26), remaining Fig. 8-9 points near 1554.5-1555.5 nm, Table 1 other works.
- grottke2020 (16 / 82): three MEMS shifters (L 250 / 210 / 150 um), one full-shifter cutback row, and the paper's own
  component sweeps as test-structure rows: oxide/air transition (2), strip-to-slot converter (3), bridge section (6),
  MMI (simulated only). Not entered: other sweep points shown only as curves in Fig. 4, simulated-only bridge designs
  (in notes), Table 1 other works, pull-in voltage, mechanical Q, FWHM pulse, 22 fJ energy (notes).
- zhang2024b (3 / 16): FE ring as `phase_shifter.ferroelectric_nonvolatile` (6.6 dB, 3 levels, endurance 4e4 / 1e6 on a
  dummy capacitor, 1000 s measured, > 10 years fit, ~1.26 dB stack loss), same device as `resonator.ring` (0.14 nm), ITO /
  HAO loaded rib as `waveguide_platform.straight` (180 dB/cm excess). Not entered: writing pulse, writing energy 5.05 nJ,
  Pr, RBER (no parameter, in notes), Q (supplement), off-chip PDs (discrete test parts), Table 1 other works.
- limongi2026 (2 / 22): TiN heaters on LPCVD SiN, 810 nm (92 mW, 8.5 kHz, 20 / 19 us) and 1550 nm (120 mW, 3.83 kHz, 38 /
  43 us). Cold resistance read off Fig. 4, hot value from Table II. Not entered: safe-operating V / I / P limits (no
  parameter, in notes), heater length and metal thicknesses in the device (not printed).
- yan2017 (5 / 25): graphene heaters on PhC waveguide, Z-shaped 20 um (1070 / 650 pm/mW, 3.99 mW per FSR, 0.75 / 0.525 us,
  19.41 kohm), ~5 um, ~3 um, straight-shaped; PhC waveguide as `waveguide_platform.slow_light` (n_g ~25). Not entered:
  FOM (notes), theoretical 420 ns (definition not stated), group index curve points, comparisons to other work.
- guo2024 (7 / 56): TiN mid-IR shifters on IMECAS MPW: symmetrical MZI 2.35 um and 3.27 um, spiral asymmetrical MZI; focusing
  subwavelength GCs (7.3 dB, 9.1 dB); bends (0.106, 0.217 / 0.218 dB/90). Not entered: 3-dB splitter (SEM only), Table
  I-II other works, 35 mW of Table II (unexplained against 70 mW/pi, in notes).
- chen2022 (4 / 24): FE-SOI ring switch (8.9 dB, endurance, retention), same device as `resonator.ring` (0.2 / 0.1 / 0.03 nm,
  Q ranges read off Figs. 13, 17), loaded rib (excess loss read off Fig. 12), GC (peak read off Fig. 12, scope
  unspecified). Not entered: n_levels (no count printed), Pr, write pulse, Fig. 13 sibling coupling lengths (in notes).

No paper was stopped on: none is a wrong document or correction-only.

## Missing orgs

- Fondazione Bruno Kessler (FBK), Center for Sensors and Devices, Trento, Italy: limongi2026 p.1 affiliation, p.3 Sec. II-B
  first-person process. fab_org_ids left empty on both rows; should be fab once registered (D84a).
- Munster Nanofabrication Facility (MNF), University of Munster, Germany: grottke2020 p.4 Sec. 4 ("at the" facility).
  facility_org_ids left empty on all 16 rows; should be facility once registered.

## Registry gaps (skipped value, locator, proposed definition)

- `vpi_l_v_cm` (phase_shifter): grottke2020 0.113 / 0.042 / 0.084 V cm (p.8-9, Table 1); iseghem2022 0.2198 / 0.4987 /
  0.5710 V.mm (p.16 Table 3). Half-wave voltage x length as printed, operating point in condition.
- `write_pulse_us` (phase_shifter, ferroelectric / PCM): zhang2024b and chen2022 -5 V, 100 us for 90 % of the maximum peak
  shift. Pulse width reaching a stated fraction of full state change.
- `write_energy_nj` (phase_shifter): zhang2024b 5.05 nJ (p.10 Table 1). Already deferred once as switching energy (D81);
  listed only as a further case.
- Heater safe-operating limit (phase_shifter): limongi2026 Table II 179 / 136 mW, 15.3 / 15.9 mA, 11.7 / 8.6 V. Maximum heater
  power before stated degradation onset (criterion in condition).
- Photonic-crystal lattice geometry on `waveguide_platform.slow_light` (period_nm and a hole-diameter parameter): yan2017 390
  nm, 193 nm (p.2).
- fsr_nm on phase_shifter (MZI test vehicle): grottke2020 9.8 nm, yan2017 ~4 nm, guo2024 ~1.8 nm: in notes.

## Judgment calls for the auditor

1. grottke2020 IL 0.47 dB: the cutback section (p.6-7) gives no Lpt; Table 1 assigns it to the 210 and 150 um rows. Entered on
   ps_cutback (spectrum) and on both rows as Table 1 prints it, rather than a D159 removal. Geometry of the three MZI devices
   beyond Lpt and del is not printed.
2. grottke2020 component sweeps entered as 11 test-structure rows (one per stated design, rule 9); wavelength 1550 nm
   `wavelength_inferred` since Sec. 6 states none for the sweeps. Fig. 4 caption swaps wr1 and wr2 against text and legend:
   text and legend followed. Oxide/air boundary classed as `waveguide_platform.transition`, bridges as `.other`.
3. iseghem2022 length 50 um on wg450g250 and wg400g350 is not printed per device; it follows from Sec. 2.3.1 and Fig. 12(b) x
   Table 3. Fab org_imec rests on Sec. 3 naming iSiPP50G as the underlying platform (no "fabricated by"); LC post-processing
   org not stated. Table 3 loss basis `derived` although the paper says estimated.
4. chen2024b P_pi 3.63 mW `derived` (P = I x V, p.8). IL is relative to 1580 nm (scope on_chip_excess), not absolute. The
   abstract's 1.3 dB end is not on any plotted point (Fig. 8(c) minimum magnitude about 2 dB); entered as a range row with an
   inferred span. Text says tau_r 0.8-1.8 us for all wavelengths, Fig. 9 reads 0.63 us at 1560 nm. `reflector.band_stop`
   for the transmission-mode grating section, stop-band contrast level not stated.
5. zhang2024b vs chen2022: same lab, same gate stack, same endurance and 10-year values, different ER and peak shift. zhang2024b
   does not attribute any value to chen2022, so D408 keeps both; check whether Fig. 4(b) / Fig. 5 reprint chen2022 Fig. 10 / 12.
   Endurance is on a capacitor, not the ring (condition). Excess dB/cm under `waveguide_platform.straight` rather than a
   per-length phase-shifter loss (D250).
6. Retention > 10 years as 3.1536e8 s `derived` with qualifier gt: an extrapolation of a 1000 s linear fit; could be
   `author_estimate`.
7. yan2017 fab DTU: contributors S.Y. (HUST + DTU), Y.D. and X.Z. (DTU), D83c. 19.41 kohm is the figure label R2, tied to the Z
   shape only by the text's ratio. 5 dB / 8 dB / 1.1 dB wavelength span 1530-1540 nm is inferred. 10 um PhC length vs 20 um
   graphene overlap "covering the slow-light waveguide" conflict flagged in notes. Discussion prints 1.04 vs 1.07 nm/mW.
8. guo2024 headline devices have no printed heater length (sweep 300-700 um). GC scope per_coupler with method unspecified. 32 kHz
   `derived` ("corresponding to" rise and fall, not a sweep). Footprint 60000 um2 `author_estimate` (product computed here from
   a table entry estimated from a photo). Bend 2.25 um value sits in a 2.35 um appendix.
9. limongi2026 OX2 Design 1: 1.8 um used (Table I, Sec. II-B); Sec. II-A prints 1.5 um. chen2022 fab empty (passive fabrication
   text, D80b); zhang2024b fab NUS (author contributions).
