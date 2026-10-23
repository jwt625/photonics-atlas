# Batch lit_10 report (distill subagent, 2026-10-23, condensed by the coordinator)

Dry-run `batch lit_10: +32 components, +216 metrics; errors 0`. Basis mix: measured 72, derived 59, design_target 50,
simulated 24, author_estimate 10, extracted_from_figure 1. Not yet audited or merged (paused by the owner).

## Per paper (components / metrics)

- ashida2017 (2 / 22): resonator.photonic_crystal multi-heterostructure Si PhC nanocavity (Qint best 2.3e6 and mean
  1.50e6 n=12 derived from QL / sqrt(T0), T0 = 0.75; linewidth 0.82 pm; mean resonance 1606.8 nm, std 0.51 nm as
  wavelength_spread_nm; simulated Qideal 2.12e7; geometry); wdm.other 8-channel shifted-L3 drop filter (QL mean 3.13e4
  n=8, spacing 3.9 nm measured / 460 GHz derived, simulated values, n_channels 8). Fab AIST (lithography / etch "in the
  R&D laboratory at AIST"; coordinator may rule facility). Not entered: time-domain Q > 2e6, model estimates; intro 2.2e6
  vs 2.3e6 noted.
- gao2021 (2 / 15): resonator.ring CMP X-cut LN wedge microring 200 um (FSR 2.12 nm, QL 2.1e7 / 5.9e7 / 8.0e7, Qint
  derived, 0.0028 dB/cm author_estimate); fiber_chip_coupler.edge lensed fiber 10 %/facet (measured, D167). Platform
  empty (D168). Fab empty (authors at four orgs).
- jeong2013 (2 / 23): wdm.mrr 5th-order CROW (excess 0.2 / 0.4 dB de_embedded, OBRR > 40 dB as crosstalk_db, FSR ~9.6 nm,
  ng ~4.45 derived, kappa1-3 70 / 25 / 12 % derived, geometry); waveguide_platform.straight ~2 dB/cm cutback (band C
  inferred). Fab AIST.
- radulaski2018 (4 / 19): GaAs L3 PhC cavity with heater (Q ~1500 unqualified -> q_loaded note, ~7 nm tuning); Cr
  microheater (phase_shifter.thermo_optic, 4 kOhm typical); perturbed cavity under SiNx bus (contrast < 3 dB, simulated
  Q values); SiNx semicircular GC 10 dB (measured per D167, origin not stated). Fab empty.
- suk2025 (5 / 25): four near-IR ChG trapezoid rings (Qint 2.3e7 / 1.1e7 / 1.1e7 / 4e6, losses author_estimate);
  tri-layer mid-IR ring (Qint 6.71e7 / 4.13e7 at 3910 nm, > 1e7 over 3.2-4.6 um, mean 8.6e6, 0.0029 dB/cm). Platform
  other. Composition printed inconsistently (text vs Table 1, noted).
- wang2021 (4 / 21): 4H-SiCOI microdisk (FSR 2.07 nm, TE / TM linewidths and Q), SHG 3.91 %/W (frequency_converter.shg),
  cascaded Raman laser (laser.other, thresholds 10 / 14 mW), comb (laser.comb, OPO threshold ~10 mW, spacing 2.08 nm).
  One disk design as three rows by role (judgment call). Fab empty.
- camus2020 (6 / 21): fs-written BGG and silica waveguides (1.6 / 0.5 dB/cm author_estimate, fiber-to-fiber 3.01 / 2.4 dB
  mean of 3, power handling > 40 dBm derived), directional couplers by interaction length (BGG 4 mm / 5 mm / 0; silica
  series row D165). Fab empty.
- nikbakht2022 (3 / 24): shifted / unshifted 3-dB DCs (excess 0.5 / 1 dB, geometry), switch_fabric.other MZI (ER 10 dB,
  3 V, P_pi 50.4 mW derived, heater 1000 um). Fab org_lionix_international.
- zhang2013a (3 / 17): splitter.y_branch PSO Y-junction (excess mean 0.28 dB n=26, std 0.02, range 0.23-0.32, simulated
  values, geometry); conventional Y-junction > 1 dB; TE GC loop ~11 dB fiber-to-fiber. Fab empty (unnamed 248 nm CMOS).
- yu2025 (1 / 29): mode_converter.mdm_mux dual-polarization mode splitter (IL and crosstalk per mode at 1550 nm and over the
  band, simulated values, geometry; Table 1 vs text inconsistencies noted).

## Orgs missing from the registry

Kyoto University Nano Technology Hub (ashida2017 p.10, facility); Australian National Fabrication Facility ACT node
(suk2025 p.7, facility, borderline).

## Registry gaps proposed

passband_ripple_db (wdm); kappa_per_cm for splitter; split_tolerance_bw_nm (splitter; may fall under D250 rejections);
crosstalk_bw_nm (mode_converter); heater_resistance_ohm for resonator / wdm; optical-input self-heating shift; platform
sicoi; single values (switching time, nm/V^2, GC polarization selectivity).
