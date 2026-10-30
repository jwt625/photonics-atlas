# Batch lit_50 report (distill subagent, 2026-10-29)

Dry-run `batch lit_50: +30 components, +153 metrics; errors 0` (one WARN about another batch's row,
cmp_lit_ni2025b_pimmwc-m18). ASCII only, no e-mail, no addresses; quotes of a few words only on valdez2025 / deng2024
(open_license_ok). Page-1 title check: all 6 texts match their source rows (no wrong document, no correction / erratum).
Rows built by a scratchpad script (one spec file for all papers).

deng2024 `garbled_text_layer` (page 13): page 13 is the reference list. Every value entered comes from text pages that read
cleanly (pp. 1-11, checked character by character for the +/- / >= / <= signs) and was cross-checked against the page
renders (page_06 Fig. 4, page_09 Fig. 7). No value was dropped because of the garbled layer.

## Per paper (components / metrics)

- lu2015 (2 / 21): point-symmetric broadband PBS (polarization.pbs, test set 1): < 0.5 dB loss with the GCs calibrated out
  over the C-band (insertion_loss_db: polarization does not allow excess_loss_db), through-port isolation > 20 dB over
  1477-1602 nm, cross-port > 20 dB over 1460-1602 nm, ER > 20 dB for both modes over 1477-1602 nm, ER > 10 dB over > 175 nm
  (= the 1460-1635 nm measured span), simulated isolations (125 / 110 nm spans, > 35 dB at 1495 nm), length 97.4 um, stack.
  3 dB TM broadband coupler sub-element as a splitter.directional_coupler design row (FDTD: 50 % TM cross coupling, TE cross
  coupling < -22 dB over 1480-1580 nm; Fig. 2(b) labelled geometry: 500 nm gap, 22.5 / 13 um coupling sections, 1 um tapers).
  Not entered: simulated common 105 nm span (overlap of the two port spans); phase-shifter section widths 400 / 600 nm and
  S-bend 2 x 5 um (no role parameter); Table 1 rows of other works.
- sun2022 (3 / 15): sidewall-grating DFB (laser.dfb: Ith 104 mA, SMSR >= 29 dB and 1555.81 nm at 170 mA, kappa ~15 cm-1,
  period 238 nm, 2.5 um ridge, 1.92 um ridge height, 1200 um); PMC stepped-height waveguide as waveguide_platform.straight
  (internal loss 9/cm -> 39.09 dB/cm derived, W0 1.38 um, D0 3.3 / D 1.92 um, 490 um); 50 um deep-etched taper
  (waveguide_platform.other, simulated 0.044 dB). Not entered: PMC TM purity > 94 % (140-190 mA) and 98.2 % at 180 mA,
  simulated PCE 97.3 % (no polarization efficiency / purity parameter; no psr row created), DFB TE purity 99.8 %, redshift
  0.020 nm/mA, taper reflection 7e-6, Neff values, corner width 0.4 um.
- valdez2025 (4 / 46): 1D TWIG GC (81.1 % / 0.91 dB at 1555.5 nm, 1 dB bw 20 nm, back reflection 0.1-4.5 % -> 13.5-30 dB
  derived, 24 local periods, 13 um wide, 150 um taper, full / partial etch 220 / 70 nm, 0 deg, stack); focusing TWIG (85.4 % /
  0.69 dB at 1546.4 nm, 1 dB bw 20 nm, 41 x 16 um); optimized design row (simulated 91 %, 34 nm 1 dB bw over 1530-1564 nm,
  Table 1 initial period 637 nm and D = 85 % -> fill_factor 0.85); 500 x 220 nm waveguide 1.35 dB/cm (own Fabry-Perot fit).
  GC efficiencies scoped loopback_half (paper's Eq. 8 takes the square root of the two-coupler transmission after removing
  the own-fit waveguide loss). Not entered: foundry average -1.2 dB/cm (foundry value), grating reflectivity 4.35 % (no GC
  reflectivity parameter), d1 / d2 offsets 194 / 246 nm, radial angle 22 deg and 24.35 um offset, array-level tolerance trends
  (30 nm shift, 85 -> 50 %, -7 dB back reflection for +10 nm bias), short-wavelength back reflection about -20 dB.
- deng2024 (11 / 51): six SiN 180-degree bends (waveguide_platform.bend, 638 nm, cutback, wafer means; std in notes):
  circular 0.378, Euler 0.293, constant-width TOPIC theta_p 52.5 deg 0.212 and 22.5 deg 0.204, varying-width TOPIC 0.017,
  traditional varying-width (W_max 1.4 um) 0.242 dB/bend; Si TOPIC add-drop rings R = 0.7 um (FSR 10.48 THz / 59.61 nm),
  R = 1.2 um (6.20 THz / 35.84 nm, FWHM 167 GHz, drop loss 0.42 dB, drop ER 28.1 dB) and the R = 2 um WGM ring with embedded
  doped-Si heater + UCUT (FSR 3.423 THz, 5.85 mW per pi, ~9 % coupling, 0.81 um straights, 150 nm gap, 220 nm); spiral
  doped-heater phase shifter (P_pi 1.50 mW); 32x100 GHz filter (FWHM 75 GHz, IL 1.91 mean / 1.59-2.55 range, nonuniformity
  0.96 derived, channel isolation >= 15.75 dB as crosstalk_db, cumulative crosstalk 15.18 dB, 32 ch / 100 GHz, 1 in / 36 out).
  Not entered: ring roundtrip losses (~0.05 dB for R >= 1.2 um; 0.047 / 0.032 dB at R = 2 um; no parameter), filter tuning
  efficiency 283 GHz/mW per channel (author estimate, no GHz/mW parameter), W_max of the best varying-width TOPIC (plotted
  only), Fig. 5(b)-(c) and Fig. 4(a) sweeps (plotted only), loss-reduction ratios (> 22x / > 14x, derived claims),
  interleaver (no own measured values; DC ratios 0.5 / 0.29 / 0.08 in notes), Supplementary Note5 8x400 / 16x200 GHz filters
  (supplement not cached).
- ribeiro2016 (5 / 12): 4x4 universal MZI mesh (switch_fabric.mzi_mesh: 6.9 dB on-chip longest path at 1550 nm, crosstalk
  > 20 dB, 4 x 4, stack); MZI unit cell (mzi_mesh per D158: 0.9 dB, ER > 45 dB); Ti heater (phase_shifter.thermo_optic:
  P_pi 15 mW derived from ~30 mW per 2 pi, pi-change time 0.25 ms -> rise_time_us 250 derived); PDK 2x2 MMI (imbalance 0.01 dB
  specification); 1 % monitor tap DC (author_estimate). Not entered: "up to 4 kHz" (maximum drive rate, not a 3-dB bandwidth),
  0.21 rad/mW (same data as P_pi), pi/100 phase accuracy, 0.25 dB / 1 h stability, 3.8 mm path-length difference.
- taballione2019 (5 / 8): 8x8 SiN processor (switch_fabric.mzi_mesh: on-chip transmission >= 60 % for the longest path ->
  <= 2.22 dB author_estimate, 8 x 8); MZI directional couplers (split ratio mean 49.7 % / std 12.6 % over 128, derived from
  fractions); thermo-optic phase shifters (average phase range 4.59 rad -> 1.46 pi derived); untapered facet to PM fiber
  array (~2.9 dB/facet, measured per D167, C-band inferred); double-stripe waveguide 0.2 dB/cm (author_estimate, origin not
  stated). Not entered: 0.5 dB/facet with tapering (cited [33]); Appendix Table 1 platform coefficients (cited); 5-95 %
  splitting-ratio range and phase offset 3.5 +/- 1.85 rad (no matching parameter); quantum metrics (HOM visibility, gate
  fidelities: out of scope).

## Judgment calls (coordinator to confirm)

1. deng2024 rings all wdm.mrr (R = 0.7 / 1.2 um rings are add-drop filter building blocks characterized by FSR, FWHM, drop
   loss and drop ER, eid2016 precedent; D400). Alternative: resonator.ring for R = 0.7 and R = 1.2 (then FWHM would need
   linewidth_mhz 167000, derived).
2. sun2022 "internal loss for PMC waveguide ... is 9/cm" read as a power attenuation coefficient (cm-1) and converted to
   39.09 dB/cm (derived, flagged in notes). If the coordinator reads it as 9 dB/cm or prefers not to convert, change / delete
   m1 of cmp_lit_sun2022_pmc_stepped_ridge_wg (the row then has no performance metric and should be deleted).
3. sun2022 PMC entered only as its waveguide (waveguide_platform.straight), not as polarization.psr: the TM purity (%) has no
   polarization parameter and converting Stokes S1 to a PER needs an assumption. A gap-fill could add the psr row (D396).
4. lu2015 isolation (per output port) and ER (per input mode) both entered as per_db with the definition in condition
   (cheng2023 / zheng2023 precedent); the 10 dB ER row carries the 1460-1635 nm measured span because Table 1 prints > 175 nm.
5. lu2015 fab org_university_washington: devices fabricated by a named UW staff member at the University of Washington WNF
   (eid2016 precedent); the facility itself is missing from the registry.
6. ribeiro2016 fab org_imec;org_ghent_university on the mesh / cell (imec passive SOI via Europractice MPW + heaters "we
   processed" by the Ghent University-IMEC authors, liu2025b precedent); heater row org_ghent_university only; MMI / tap
   org_imec only.
7. taballione2019 fab empty (LioniX co-authors, but no fabrication statement); 60 % transmission and 0.2 dB/cm entered as
   author_estimate (measurement not described; p.10 frames 0.2 dB/cm as the design goal of the cited cross-section).
8. valdez2025 period 637 nm / fill factor 0.85 only on the design row (initial uniform values before apodizing
   optimization); the fabricated 1D row has no period_nm, so the gc_1d top view stays schematic.
9. deng2024 32x100 GHz filter IL scope `unspecified` (Fig. 7(b) is normalized transmission; normalization reference not
   stated); channel isolation as crosstalk_db (type not named), accumulative crosstalk as crosstalk_cumulative_db.

## Missing orgs

- University of Washington Nanofabrication Facility (WNF), part of NSF NNIN (lu2015 p.10 Acknowledgments; facility of the
  fabrication): facility empty (also missing for eid2016, chen2024a, fang2021).
- Applied Nanotools, commercial foundry (valdez2025 p.4 Sec. 5, abstract, p.7 conclusion; fab): fab empty.
- University of Glasgow / James Watt Nanofabrication Centre (sun2022 p.1 affiliation, p.4 Acknowledgments; staff thanks only,
  not needed as a facility).
- Europractice MPW service (ribeiro2016 p.3 Sec. 3; MPW access provider, D398 fab role): not in registry.
- QuiX BV, Enschede, Netherlands (taballione2019 p.1 affiliation; no fab role stated).

## Registry gaps

- polarization: `conversion_efficiency_pct` / output polarization purity in % (sun2022 PMC TM purity 98.2 % at 180 mA,
  > 94 % over 140-190 mA, simulated PCE 97.3 %, p.2-4; aamer2012 PCE also skipped). Definition: fraction of the output power in
  the target polarization for a rotator / converter, method (Stokes S1, power ratio) in condition.
- resonator / wdm: `roundtrip_loss_db` (deng2024 0.05 / 0.047 / 0.032 dB, p.7; extracted from add-drop spectra by the model of
  ref. [62]). Definition: ring round-trip power loss in dB, extraction model in notes.
- wdm: `tuning_efficiency_ghz_per_mw` (deng2024 filter 283 GHz/mW per channel, author estimate, p.10-11) or a frequency form of
  tuning_efficiency_pm_per_mw.
- laser: `tuning_efficiency_nm_per_ma` / current-tuning coefficient in wavelength (sun2022 0.020 nm/mA, p.3; existing
  fm_efficiency_ghz_per_ma is frequency-based).
- fiber_chip_coupler: `reflectivity_pct` for a grating's back-reflection into the waveguide (valdez2025 Fabry-Perot fit 4.35 %,
  p.5).
- waveguide_platform: `back_reflection_db` / reflection for etch-depth transitions (sun2022 simulated 7e-6, p.2) - single
  simulated value, probably defer.
