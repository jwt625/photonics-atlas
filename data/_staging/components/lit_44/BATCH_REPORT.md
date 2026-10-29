# Batch lit_44 report (distill subagent, 2026-10-29)

Dry-run `batch lit_44: +38 components, +170 metrics; errors 0` (the only WARN is on merged row
cmp_lit_ni2025b_pimmwc-m18, not this batch). ASCII, no e-mail, no quotes (all five sources restricted_local_only).
Page-1 title / authors match the source rows for all five papers.

## Per paper (components / metrics)

- hinumwagner2025 (3 / 26): Si3N4 all-pass rings at 852 nm on LPCVD wafers (resonator.ring): Fig. 9 example
  W700 / R80 / gap 400 (Q 4.2e5, FWHM 2.0 pm, ER 6.9 dB, FSR 1.2 nm), Fig. 16 die-to-die target W700 / R80 / gap 800
  (means read off the figure, stated sigmas as `std`), W500 / R80 / gap 800 (ER approx 12 dB best). Geometry incl.
  BOX 2.2 um (ellipsometry). Not entered: per-design / per-wafer bar means of Figs. 10-15 (about 48 bars per figure),
  "< 5 %" die spread and "+30 % Q" (relative / paper-level), PECVD ER variability, test-structure propagation loss
  0.8-1.2 printed "dm cm-1" (unit garbled; coordinator may decide dB/cm), upper-cladding thickness (Table 1 2.4 um vs
  text 1.6 um), AFM roughness / refractive indices (no parameters). Fab empty (TU Graz + ams-OSRAM Group, facility
  unnamed). D408: journal extension of their SPIE 2023 paper, values kept.
- liu2026 (5 / 49): ATSWG 3-dB splitter (splitter.adiabatic; excess 0.94 dB mean at 1550 by 7-stage cut-back slope,
  0.2 dB best at 1480, simulated 0.05 / < 0.08 dB, split range from Fig. 5(b), full geometry, footprint derived);
  three asymmetric siblings Gu/Gb = 5 / 6 / 7 (simulated ratios as printed, measured upper-port ratios read off
  Fig. 5(c), Gu derived); TE GC (approx 5 dB loopback_half, 8 deg). Not entered: "120 nm" bandwidth (no criterion),
  band-average 0.94 dB +/- 0.1 dB (conflicts with the 0.2 dB minimum and Fig. 5(d)), Table 2 "1.39" (unattributed),
  asymmetric-splitter IL of Fig. 5(e) (legend by ratio), "< 5 %" ratio variation (sample unclear). Fab empty (commercial
  300 mm line, unnamed).
- tebeneva2024 (2 / 8): bulk crystalline Ge WGM disks (resonator.disk, platform other), a = 1.5 mm: q_loaded
  1.1e7 TE / 1.2e7 TM (Lorentzian), q_intrinsic 2.2e7 / 2.4e7 (prism) and 2.2e7 (hemisphere); a = 1.35 mm: q_intrinsic
  2.2e7 ("same values"). Not entered: Qmat estimate, TPA coefficient, Sec. 4.3 power-dependent FWHM / Q and Fig. 4
  thermal widths (resonator not identified, D159). Fab empty (six orgs).
- brun2014 (26 / 69): SiGe/Si graded-index mid-IR platform: straight waveguides 3.3 / 7.0 um (prop loss < 1 at 4.5,
  < 1.5 at 5.65, < 2 dB/cm at 7.4 um, FP fringe contrast, D394), Y-junctions x2 (excess, split ratio), 12 S-bends
  (waveguide_platform.bend, insertion_loss_db per_component), 6 X-junctions (crossing.other, crossing_loss_db), 4
  evanescent couplers (split ratios, Table 5 geometry). Not entered: coupler loss "negligible", BPM 0.4 dB Y-junction
  expectation (design unspecified), X2 / X3 intersection widths at 4.5 um (Table 3 5.4 / 6.6 vs text 5 / 7 um).
- shoaa2025 (2 / 18): Sb2Se3 OPS on n-doped poly-Si heater, SiN 400 nm (phase_shifter.phase_change: 0.43 pi, ER
  mean 12.4 / 14 / 10.5 dB and best 15.2 dB, 7900 cycles, heater resistance range read off Fig. 5, geometry);
  poly-Si taper transition (simulated 0.07 dB per taper; printed 0.14 dB for two). Not entered: OPS loss 0.13 /
  0.15 dB/um (D250), switching energies 19.2 / 0.54 uJ, pulse / threshold voltages, delta neff, bare-MZI IL < 3 dB
  (no class for the test MZI), abstract "up to 12.5 dB" (conflicts with 15.2 dB peak), 85 % mode overlap.

## Missing fab / facility orgs

- "Micro and Nanofabrication Platform of CEA-Leti MINATEC" (brun2014 p.11 Acknowledgments): facility for fabrication
  support; facility_org_ids not entered.
- "Optoelectronics Research Centre, University of Southampton" (shoaa2025 p.12 Acknowledgment, "research was
  conducted at"): facility not entered.
- "ams-OSRAM Group" (hinumwagner2025 p.1 affiliation): not needed (no fab statement); registry has org_ams_ag and
  org_ams_osram_international only (no name-only mapping).

## Judgment calls

- hinumwagner2025: the 4.2e5 Q equals lambda / FWHM (loaded) although abstract / conclusion call it intrinsic:
  entered as q_loaded with a note; Fig. 9(a) FSR 1.2 nm conflicts with Fig. 2 / Fig. 16(a) (about 0.7 nm at R 80 um),
  entered as annotated with a note; LPCVD-1 / LPCVD-2 treated as one design for the 12 dB ER row.
- liu2026: subtype adiabatic (tapered SWG coupler, xu2018 precedent); simulated ratios entered as printed although
  Fig. 3(c) curves read higher; measured excess 0.94 dB as `measured` (cascade-slope fit, D80a).
- tebeneva2024: bulk WGM resonators kept in scope (resonator.disk); q_intrinsic `derived` per D403 (critical coupling
  determined from the data, maximum contrast versus gap); hemisphere Q0 placed on the 1.5 mm row (text implies it).
- brun2014: fab org_cea_leti borderline ("our 200 mm Si manufacturing facilities", fabrication-support thanks to the
  CEA-Leti platform; two co-authors at III-V Lab, D83c); Table 1 Y-junction "transmission loss" entered as
  excess_loss_db; Table 1 per-function values from series structures kept `measured` (division not shown).
- shoaa2025: ER of the MZI switching kept on the phase-shifter row (extinction_db allowed for phase_shifter); taper
  per-transition value from printed simulated terms (D83f).

## Registry gaps

- fill_factor for splitter: liu2026 SWG duty cycle 0.5 (p.4 Table 1); def as for gratings (tooth / period).
- tip_width_nm for splitter: liu2026 SWG taper tip W2 / WT 100 nm (p.2, Table 1).
- crossing_angle_deg (crossing, geometry): brun2014 X-junction angles 70 / 80 / 90 deg (p.9 Table 3); angle between
  the crossing waveguides.
- y-branch geometry (branch_angle_deg, splitter): brun2014 2.6 / 2.4 deg (p.9 Table 2); notch length / width 25-55 /
  2 um not proposed (single paper).
- switching_energy_uj (phase_shifter): shoaa2025 set 19.2 uJ / reset 0.54 uJ (p.2, p.7); electrical energy per
  state change (D81 deferred switching energy; concrete skipped value now).
- pcm_thickness_nm / pcm cell width (phase_shifter, geometry): shoaa2025 20 nm, 3 um (p.6).
- per-length phase-shifter loss (dB/um): shoaa2025 0.13 / 0.15 dB/um (p.6, Fig. 3(b)); rejected in D250, listed only
  as a further skipped value.
