# Batch lit_29 report (distill subagent, 2026-10-29)

Dry-run `batch lit_29: +27 components, +168 metrics; errors 0` (no warnings). ASCII, no e-mail, no quotes (all ten
sources `restricted_local_only`). Page-1 title / authors checked for all ten cached texts: all match their source rows.
No `garbled_text_layer` flags. Not audited or merged.

## Per paper (components / metrics)

- liu2025a (3 / 19): polymer (EpoCore / EpoClad) gap crossings, perpendicular (crossing.other; Table I per-crossing
  < 0.35 dB E11 / < 0.40 dB E21 as measured, two-crossing < 0.81 dB, simulated < 0.33 dB, measured FMC / SMC widths
  12.0 / 5.07 um, core 4 um from Fig. 1(b) label) and angled 33.5 / 36.8 deg (per mode / polarization ranges, simulated
  < 0.54 dB); adiabatic tapered asymmetric DC E21 <-> E11 (splitter.directional_coupler per D165, simulated CR21 > 90 %
  over S+C+L, design widths / gap / Lc). Not entered: Fig. 3 gap sweeps; DC measured data (near fields only); S-bend
  length. Fab org_guangdong_university_of_technology borderline (in-house facilities, 9 / 12 authors GDUT, D84b).
- weigel2023 (2 / 9): 16x4 crossing-free multilayer routing network (crossing.multilevel, judgment call; 10.2-11.3 dB
  fiber-to-fiber O1 / O3 / O4, additional loss 0.2-1.3 dB author_estimate since it subtracts a cited simulated 3D-MMI
  loss, n_inputs / n_outputs, 250 um output pitch); PolyBoard reference waveguide (2.0 +/- 0.1 dB coupling +
  propagation, 3.2 x 3.2 um, R 1500 um). Not entered: O2 (fabrication error), Fig. 5 reproducibility spreads, 3D MMI
  losses (refs. [27] / [29]), 4x1 MMI (only its inherent 6 dB; geometry-only, not a row). Fab empty (passive voice;
  platform called the authors' technology only; D84a M1D.4), all authors Fraunhofer HHI.
- croce2026 (1 / 18): SRSN-on-SiN apodized vertical GC: 1.78 dB per coupler at about 1547 nm (derived, (T - prop) / 2),
  1-dB BW about 31 nm, simulated 1.37 / 1.21 dB and 37 / 35.9 nm, back-reflection about 1 % -> 20 dB simulated, full
  stack geometry, period 929-1024 nm and fill factor 0.2-0.762 (derived). Not entered: period count (20 / 21 / 15+
  conflict), SiO2 buffer 180 nm (no parameter), Si-on-SiN design. Fab org_university_of_southampton (T.D.B. performed
  the fabrication, author contributions).
- zhou2022a (2 / 21): multimode GC with shifted poly-Si overlay for GI-FMF (LP01 1.36 dB, LP11 2.21 dB, 1-dB BW 34 / 32
  nm, peaks; author_estimate because normalization used estimated input-GC / ADC spectra; simulated 1.1 / 1.56 dB, 33
  nm; geometry); TE0-TE1 ADC mode mux (mode_converter.mdm_mux, crosstalk > 22.3 dB 1510-1610 nm). Fab org_imec (MPW).
  Not entered: ADC gap 200 nm (not allowed for mode_converter; sentence cites [17]), per-period widths (plot), cited
  -2.8 / -3.88 dB.
- desmet2020 (6 / 24): FLDW fused-silica waveguide (0.88 dB/cm OFDR derived from 176 dB/m round trip, MFD 12.8 / 12.1
  um, 2.17 dB fiber-to-fiber), active SMF butt coupling 0.43 dB per facet (derived), FLICE V-groove interface (1.24 dB
  mean of 3, 2.15 dB mean of 5, nonuniformity 0.25 dB, simulated 0.22 dB and 1 dB per 2.5 um, pitch / channels /
  sidewall angle), 41.5 deg polished mirror (0.25-0.55 dB derived, 2.4-2.7 / 2.5-2.8 dB before / after curing), full
  interposer on PIC (11.8 dB, about 2 dB per interface derived), Europractice MPW TE GC (7.9 dB reference pair, 26 nm,
  spec about 4 dB at 1558 nm / 10 deg). Fab org_ghent_university (authors state they wrote waveguides / V-grooves;
  all authors Ghent University - imec). Not entered: facet / mirror roughness, writing depth, NA, interposer 1-dB BW
  22 nm (gap).
- oh2023 (3 / 33): metasurface free-space SMF-to-MCF couplers A (1x4, 26 um) and B (2x2, 42 um) as
  fiber_interface.fan_out (min IL 1.2 dB O-band, Table III per-mode IL at 1310 nm, MDL 0.1 / 0.2 dB, PDL <= 0.1 dB (A),
  worst crosstalk 46.3 / 40.1 dB (A) and 53.8 / 40.7 dB (B), A transmittance loss 0.7 / 0.6 dB, simulated < 0.2 dB,
  pitches, 790 nm pillars); coupler C as design row (< 0.7 dB simulated). Not entered: Table II amplitude overlaps,
  working distances, phase-error loss analysis (0.8 dB modeled), coupler D (plot only). Facility
  org_center_for_nanoscale_systems; fab org_harvard_university borderline (see decisions).
- tian2023 (1 / 3): suspended SiN TriPleX tips in InP trenches (chip_chip_coupler.other; simulated MFD 2.7 x 0.9 um,
  500 um suspended length). Not entered: 2 um (+/- 1 um) tolerance within 0.5 dB (no parameter; 1 dB not reached),
  bending 30 um, cited 0.5 dB/facet, 50 um pitch / 32 channels (not allowed for chip_chip_coupler). Fab empty.
- pruessner2024 (3 / 16): bilayer SiN TE-to-TM rotators (polarization.psr per pintus2019) on AIM SiN-only platform:
  wafer A 75 um (PER about 20 dB best / 15 dB mean, IL <= 0.2 dB 800-925 nm, < 0.5 dB 725-1000 nm), wafer D 225 um and
  300 um (IL about 0.6 dB 750-800 nm; 300 um PER > 10 dB 790-950 nm). Wafer-level IL statements entered on the row of
  the device the paper marks in Fig. 6 (nevlacsil2020 precedent). Not entered: rotation angles (no parameter), wafer B /
  C and Fig. 9 devices (angle only, no rows), simulated < 0.1 dB (family statement). Fab org_aim_photonics.
- shahwar2025 (3 / 13): TIR-mirror MZI PBS on 3 um SOI (PER >= 10 dB / 180 nm, >= 15 dB / 80 nm, > 15 dB / 50 nm, TE
  25 dB best at 1550 nm, total loss about 2.5 dB, simulated >= 30 dB / 100 nm and > 40 dB, footprint); TIR mirrors 46.5
  deg (0.05 TE / 0.06 TM dB) and 117.5 deg (0.08 / 0.08 dB) as waveguide_platform.bend (cascade fit). Not entered:
  Fig. 10 caption 120 nm span (conflicts with text; caption also swaps TE / TM colours), model crosstalk -20 / -18 dB,
  MMI dimensions. Fab empty: VTT (MPW run at VTT) missing from the registry.
- wang2022b (3 / 12): dynamic polarization controller (polarization.compensator; dynamic PER > 25 dB, static 28 dB
  author_estimate, 20 dB fiber-to-fiber, on-chip 3 dB derived, footprint); 2D GC 7 dB per coupler (D167); TiN heater
  phase shifter (1970 ohm, about 3 pi at 50.56 mW, V_pi 5.6 V, rise 11 / fall 5.9 us, about 30 kHz derived). Not
  entered: fiber angle 80 deg (reference unclear), locking speed (loop count only). Fab empty (CSiP180Al process, no
  org named).

## Orgs missing from the registry

- Southampton Nanofabrication Centre (part of the Zepler Institute, University of Southampton): croce2026 p.8
  acknowledgements (facility where fabrication was carried out).
- Europractice (MPW fabrication service): desmet2020 p.6-7 Sec. 2.6 (PIC fabricated via the Europractice MPW service;
  fab role per D83d).
- VTT Technical Research Centre of Finland: shahwar2025 p.8 Sec. 5 (devices manufactured in an MPW run at VTT; fab).

## Decisions for the coordinator

1. oh2023 fab org_harvard_university: authors at Harvard (4) and Corning (3); fabrication passive but the authors cite their own cleanroom
   facilities (p.9) plus the Harvard CNS facility statement (p.1). Kept borderline; empty if D80b is read strictly.
2. weigel2023 MWRN as crossing.multilevel (crossing-free vertical routing; alternatives splitter.other).
3. zhou2022a CE basis author_estimate (estimated calibration spectra) vs measured.
4. liu2025a angled-crossing value pairs entered as ranges (port order of the printed pairs not explicit).
5. wang2022b CSiP180Al process: fab left empty (no org named in the text).

## Registry gaps

- In-plane crossing gap (crossing): liu2025a 5 um design / 4.87 um measured mean (p.3; p.5 Fig. 10(c)). Proposed
  `crossing_gap_um`: length of the waveguide discontinuity cut into a crossing waveguide at the intersection.
- Crossing angle (crossing): liu2025a 33.5 / 36.8 deg (p.5; p.6 Fig. 13). Proposed `crossing_angle_deg`: angle between
  the crossing waveguides.
- Polarization rotation angle (polarization): pruessner2024 87.6 deg at 882 nm (p.6 Fig. 4(b)), 87.2 deg at 840 nm
  (p.6). Proposed `rotation_angle_deg`: output polarization rotation angle atan(P_TM / P_TE) as defined by the paper.
- gap_nm and layer2_thickness_nm for polarization: pruessner2024 SiO2 spacer 50 / 100 nm, SN 150 / 220 nm (p.3 Table 1)
  for bilayer rotators. gap_nm for mode_converter: zhou2022a ADC 200 nm (p.4). gap_nm for fiber_chip_coupler (vertical
  gap of a bilayer GC): croce2026 SiO2 buffer 180 nm (p.5).
- bw_1db_nm for fiber_interface: desmet2020 interposer 22 nm (p.11 Sec. 3.4).
- Mirror angle (micro_optics, waveguide_platform): desmet2020 41.5 deg (p.10 Fig. 10); shahwar2025 46.5 / 117.5 deg
  (p.9 Fig. 9). Proposed `mirror_angle_deg`: physical angle of a reflecting facet as stated.
- mmi_width_um / mmi_length_um for polarization: shahwar2025 MMIs 15 x 800 um (p.8).
- pitch_um / n_channels for chip_chip_coupler: tian2023 50 um / 32 channels (p.1-2).
- 0.5-dB alignment tolerance (re-occurrence of D77 / D81 rejection): tian2023 +/- 1 um within 0.5 dB, lateral and
  vertical (p.2 Fig. 4(b)).
- Free-space working distance (fiber_interface): oh2023 345 um input, 70 / 105 um output (p.4 Table I).
