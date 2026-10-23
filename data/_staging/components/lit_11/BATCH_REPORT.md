# Batch lit_11 report (distill subagent, 2026-10-23, condensed by the coordinator)

Dry-run `batch lit_11: +52 components, +386 metrics; errors 0`. ASCII, no e-mail, no quotes. Not yet audited or merged
(paused by the owner).

## Per paper (components / metrics)

- ni2025a (2 / 51): crossing.mmi four-mode and dual-polarization SPMW crossings on 220 nm SOI (per-mode crossing loss at
  1550 nm and band bounds, crosstalk, simulated values, Table 2 / 3 geometry). Measured IL per_component (cascade division
  not shown). Fab empty.
- shen2019 (7 / 47): GeSbS GC (geometry, back-reflection 14.7 dB derived), GeSbS rings R = 100 / 15 um (losses
  author_estimate, D76), GeSbS-Si butt and adiabatic couplers (waveguide_platform.transition 2.7 / 0.7 dB; fab
  org_astar_ime for the Si part), IME Si GC oxide- / air-clad. Not entered: transition back-reflection and 1-dB band (not
  allowed), cited values.
- zaoui2014 (5 / 49): backside-mirror GCs (uniform TE 1.08 dB / TM 1.14 dB, nonuniform GC1 design, GC2 0.74 / 0.62 dB with
  bandwidths and wafer stats, GC3 0.73 dB), all loopback_half derived. Fab empty.
- ma2026 (2 / 16): coaxial dual-core fiber fan-ins (fiber_interface.fan_out, per-port IL air vs index-matching, n_channels).
  Paper-level averages not entered (D254). No affiliations printed.
- nauriyal2023 (2 / 21): SiO2 mode converter on SiN inverse taper with CO2-fused fiber array (fiber_chip_coupler.edge, silica
  per D82f; per-facet loopback_half derived, ranges, simulated, geometry); SiN nanotaper reference. Fab
  org_university_of_rochester, facility org_cornell_nanoscale_facility.
- seok2019 (6 / 19): 240x240 MEMS switch (switch_fabric.mems), switch cell (0.019 dB/cell, 0.7 dB, 70 dB ER, switching
  times), Si rib waveguide, MMI crossing, stitching joint (simulated), GC array. Fab UC Berkeley (D83c), facility Marvell
  Nanolab. Cited values from ref. [7] not entered.
- song2008 (5 / 35): Michelson TO switches with / without deep trench (switch_fabric.other, D158; P_pi derived, rise /
  fall, ER, IL), MZI references, Ti heater (phase_shifter.thermo_optic). Fab org_astar_ime.
- suzuki2025 (5 / 15): O-band 32x32 PILOSS switch (switch_fabric.mzi_mesh; on-chip loss mean / range derived,
  xt_bandwidth, crosstalk, power), MZ element, intersection, waveguide, UHNA edge coupler. Fab AIST. UHNA MFD "~4.0 mm"
  typo not entered.
- huang2026 (9 / 43): layer-1 / layer-2 SiN waveguides, annealed / unannealed rings, kappa- and L-tapers (mdB -> dB
  derived), offset taper, hybrid rings. Fab org_university_hong_kong; HKUST NFF staff thanks not entered (D84b borderline).
- shamsansari2022 (4 / 22): X-cut TFLN rings samples A / B / C (lnoi_rib, mean Qint), auxiliary z-cut ring (kappa values,
  platform empty). Facility org_center_for_nanoscale_systems. Absorption-only quantities not entered (gap).
- davis2020 (2 / 39): apodized contra-DC filter wdm.bragg_cdc (channel width as bw_3db_nm, sidelobe, crosstalk, IL, FSR,
  geometry); 16-channel demux (spacing, grid author_estimate, Table 2 crosstalks, heater range). Fab org_applied_nanotools.
- deng2026a (3 / 29): MZ4 lattice CWDM filter (wdm.cascaded_mzi; single device and wafer statistics over 61 / 30 dies),
  compact TOPIC MZI vs conventional (peak-wavelength std, FSR author_estimate). Fab org_imec.

## Orgs missing

Institut fuer Mikroelektronik Stuttgart (zaoui2014 affiliation; not needed: no fabrication statement).

## Registry gaps proposed

back_reflection_db for crossing / waveguide_platform; bw_1db_nm for waveguide_platform; il_nonuniformity_db for
fiber_chip_coupler; bw_0p5db_nm and xt_bandwidth_nm for wdm; kappa_abs_mhz (resonator); tuning_efficiency_ghz_per_mw or
fsr / group index for switch_fabric; center_wavelength_nm for switch_fabric.
