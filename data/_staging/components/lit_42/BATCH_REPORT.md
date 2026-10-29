# Batch lit_42 report (distill subagent, 2026-10-29)

Dry-run `batch lit_42: +52 components, +316 metrics; errors 0` (one WARN about another batch's row,
cmp_lit_ni2025b_pimmwc-m18). ASCII, no e-mail, no addresses; quotes only on cohen2024 (open_license_ok). Page-1 title check:
all 8 texts match their source rows. Rows built by a scratchpad script (one spec file per paper).

## Per paper (components / metrics)

- cohen2024 (15 / 61): 1x7 WSS (switch_fabric.wss: adjacent crosstalk > 25 dB on a 10 GHz grid, > 20 dB for the 5-channel 8 / 10 GHz demux,
  channel transmission variation < 0.75 dB, about 50 mW per racetrack, footprints); second-order racetrack filter as switch_fabric.other (D407:
  1 dB drop loss, 2.1 GHz bw_3db_ghz, gaps 190 / 370 nm); Table I test structures: R = 20 um reference ring, three standardized-coupler bend
  sections (Rmin 3 / 4 / 5), four linear tapers and one Fourier taper (waveguide_platform.other), 2 um multimode waveguide, three full hybrid
  racetracks (Qi 1.64-1.89e6). All Table I values author_estimate (weakly-coupled method = assumed coupling regime, D403; ng not stated for the
  test devices). Fab org_aim_photonics (+ org_suny_polytechnic_institute for the WSS chips, "fabricated through an AIM Photonics MPW program at
  the SUNY Polytechnic Institute"). Not entered (switch_fabric gaps, kept in notes): FSR 54.5 GHz, ng 3.54, roll-off 5.3 dB/GHz, power coupling
  18 / 0.8 %, bistability > 4.1 dBm; grid detuning 0.8 / 0.7 GHz; < 0.5 dB deviation from nominal drop loss (D401 analogue); ring Table I
  structure loss (definition unclear).
- ding2017 (11 / 31): 4x4 dilated Benes MZI-SOA switch (switch_fabric.mzi_mesh: 1.3 dB ON-path loss from the Fig. 5 power budget
  author_estimate, 22.6 dB passive loss, crosstalk 47 / 50 / 27 dB, 6 / 3 ns, 250 mW), MZI element (crosstalk 8-15 dB), QCSE phase modulators
  1000 / 900 um (phase_shifter.other, Vpi 9 / 9.5 V), SOAs 230 / 250 um (gain 5 / 6.3 dB, off-state attenuation 15 / 18 dB, 1 V), and
  loss-budget terms (MMI 0.5 dB, waveguide 6 dB/cm, S-bend / circular bend 0.2 dB, strong-weak transition 1 dB; author_estimate, origin not
  stated). Not entered: IPDR / penalty / control-current tolerance (system), transparency currents 3.7 / 4.2 mA (gap), SOA 3-dB gain bandwidth
  22.5 nm (SOA length not stated, D159), MZI capacitance 0.5 pF (not allowed for switch_fabric), 16x16 emulation values.
- lu2016a (9 / 51): 16x16 Benes EO switch (6.7 / 14 dB all-cross / all-bar on-chip, crosstalk 30 / 20 / 10 dB, xt_bandwidth > 30 nm,
  3.2 / 2.5 ns, TO 0.881 W, EO 0.289 W), MMI crossing (< 0.05 dB cutback, > 30 dB, full geometry and cross-section), 2x2 MMI (0.22 / 0.4 dB excess,
  geometry), 2x2 MZI element (switch_fabric.other, 30 / 18 dB), p-i-n phase shifter (P_pi 3.28-5.88 mW over 56 elements, about 1 dB FCA loss),
  TiN heater (about 35 mW/pi, 0-26 mW correction), apodized GC (about 5 dB/facet packaged), tap coupler (0.4 dB, 10 %), connection waveguides
  (1.18 dB/cm derived by the authors' loss breakdown). Fab org_astar_ime. Not entered: +/- 1 dB path-loss variation (+/- form), 1.17 W sum,
  39.5 fJ/bit (assumed traffic).
- eid2016 (1 / 24): FSR-free MRR with bent CDCs (wdm.mrr, soi_strip): measured / fitted / designed drop loss, 3 dB width (GHz and nm), ER,
  center wavelength, kappa_o as kappa_per_cm (fit 55.3, design 68 cm-1, m-1 -> cm-1 derived), geometry. Fab org_university_washington
  (e-beam fabrication at the University of Washington, p.9). Not entered: SMSRadj 20.7 / SMSRmin > 15 dB (gap), fitted
  7 dB/cm loss (prop_loss not allowed for wdm), dispersion, corrugation depths.
- fan2025 (5 / 60): 8x8 router and 6x6 demux AWGs (wdm.awg, 800 nm Si3N4: peak IL, IL ranges, nonuniformity, AXT / NXT ranges per input #4 and
  all combinations, wavelength deviation, 19.98 pm/K, full Table I geometry), MMI mode converter (simulated < 0.4 dB), R = 20 um bend (simulated
  junction loss), inverse-taper edge coupler (2.5 um spot size, author_estimate). Fab org_ligentec. AWG2 footprint: text 1.3 x 0.3 mm2 entered,
  Table I prints 1.2 x 0.3 (noted). Not entered: foundry design-manual 0.2 dB/cm, simulated grid-snapping improvement.
- morichetti2021 (7 / 46): FSR-free 4th-order Vernier filter (41 / 37 / 53 GHz widths, < 1 dB drop loss, through isolation 17.2 / > 16 dB,
  off-band 20 / > 30 / > 33 dB, 90 nm tuning, radii, design FSRs and Ki, gaps), hitless filter with VOAs (> 35 dB disconnection), p-i-n VOA
  (phase_shifter.other, D155 analogue: added loss vs bias, 80 / 400 ns), TiN heater (480 ohm, 0.7 um), polarization-diversity add-drop
  (PDL 1.2 dB derived, > 40 / > 17 dB, 7 dB fiber-to-fiber), crossing (< 0.06 dB, > 40 dB), suspended-taper edge coupler (3 dB/facet,
  WDL < 0.2 dB). PSR / PRC: no own numbers (AMF PDK), no row.
- munk2019 (3 / 21): 8-channel 17 GHz ARMA DWDM (wdm.cascaded_mzi: spacing 0.133 nm / 17 GHz, FWHM 0.11 nm, crosstalk 28 mean / 22 worst,
  >= 25 dB adjacent-channel suppression in the QAM-16 test, 22 dB fiber-to-fiber, 1.3 mm path imbalance, cross-section), rib waveguide
  1.8 dB/cm, vertical GC 10 dB. Not entered: As2Se3 trim patch (only cited index changes and qualitative months-long stability: no row),
  group-delay variation, temperature printed with an inconsistent unit (25 +/- 0.001 with K).
- pommarede2017 (1 / 22): 16x100 GHz echelle (wdm.eg: < 2 dB IL de-embedded, < 1 dB uniformity, crosstalk 13-15 dB, 100.1 +/- 1.9 GHz,
  26.0 GHz / 0.195 nm 3-dB width, 1543 nm; simulated IL / uniformity / crosstalk; order 20, about 195 facets, 300 nm Bragg period, 1.5 um I/O
  width, stack). Rowland radius / FPR diameter and I/O separation not entered (role ambiguous).

## Judgment calls (coordinator to confirm)

1. cohen2024 D408: the Table I sentence (p.3) ends with a citation of the authors' IPC 2022 paper [21]; values entered as this paper's
   results (all author_estimate) with a note. If D259 applies, delete the 13 Table I components (keep wss_1x7, filter_2nd_order).
2. morichetti2021 fab org_amf: device fabricated on a commercial 220 nm platform citing the AMF PDK (ref. 24) plus a statement that it was made
   in a commercial silicon foundry (p.6); the foundry is not named in the text (borderline).
3. pommarede2017 fab org_cea: fabrication on the standard CEA platform with 200 mm pilot-line tools; authors at CEA LETI and III-V lab
   (parent org per D154; borderline platform-vs-fab statement).
4. cohen2024 standardized couplers as waveguide_platform.bend and width tapers as waveguide_platform.other (dostart2020 precedent);
   per-instance scope inferred from structure loss = average loss x stated length (consistent for all rows).
5. ding2017 MZI element as switch_fabric.mzi_mesh (cell characterized in the mesh, D158); lu2016a stand-alone 2x2 MZI as switch_fabric.other;
   EO phase shifters (QCSE, p-i-n) and the p-i-n VOA as phase_shifter.other.
6. cohen2024 filter width as bw_3db_ghz: the paper calls the same width FWHM (abstract) and 3 dB linewidth (Fig. 5 caption).

## Missing orgs

- Tower-Jazz, Migdal HaEmek (munk2019 p.4 Sec. III-A, fab): registry has org_tower_semiconductor only (rename; no name-only mapping): fab empty.
- Testing and packaging (TAP) facilities at Rochester Institute of Technology (cohen2024 p.4 Sec. III; packaging of the WSS): facility empty.
- University of Washington Nanofabrication Facility (eid2016 p.13 Acknowledgments): facility empty.
- Polifab, Politecnico di Milano (morichetti2021 p.7; staff thanks for assembly only, not needed).

## Registry gaps

- switch_fabric: fsr_ghz, group_index, power_coupling_pct, power_handling_dbm (cohen2024 filter 54.5 GHz, 3.54, 18 / 0.8 %, 4.1 dBm; p.4-5);
  filter roll-off `rolloff_db_per_ghz` (switch_fabric / wdm: off-resonance transmission slope, cohen2024 5.3 dB/GHz, p.1); capacitance_ff
  (ding2017 MZI 0.5 pF, p.7).
- wdm: `side_mode_suppression_db` (drop-port suppression of non-selected resonator modes relative to the selected one; eid2016 SMSRadj 20.7,
  SMSRmin > 15 dB, p.9); prop_loss_db_per_cm for wdm (eid2016 fitted 7 dB/cm, p.11).
- amplifier: `transparency_current_ma` (ding2017 3.7 / 4.2 mA, p.4).
- switch_fabric: `ipdr_db` (input power dynamic range at a stated penalty; ding2017 13 dB at < 0.5 dB, p.5) - system-level, probably reject.
