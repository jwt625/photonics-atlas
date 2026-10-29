# Batch lit_14 report (distill subagent, 2026-10-29)

Dry-run `batch lit_14: +39 components, +177 metrics; errors 0`. ASCII, no e-mail, no addresses; quotes only a few words
(open-licence mutter2024 / lapointe2025, plus short wording citations). Not audited or merged.

## Per paper (components / metrics)

- beeck2021 (3 / 14): III/V-on-TFLN (on sapphire) SOA (on-chip gain 11.8 dB, 3-dB width 45 nm, Psat_in -7.96 dBm derived
  from 160 uW 3-dB compression), multimode ring laser (427 / 23 uW at 20 / 60 C derived to mW, 4.3 mW intracavity
  author_estimate on the nominal 10% coupler), single-mode EO-tunable laser (21 nm coarse, 180 pm fine, 6.92 pm/V derived
  180 pm / 26 V, 0.77 mW best, linewidth < 1.5 MHz). Not entered: ring-mirror VpiL 5.15 V cm (EO metric), SOA details
  from [8]. Platform `other`. Fab empty ("we developed", Ghent + Stanford).
- davenport2016 (11 / 61): four Si/III-V SOA designs by Si width 0.95 / 1.10 / 1.40 / 1.60 um (Table IV G0, Pin,s, 2.3 V
  at 280 mA, geometry; 1.4 um: 1-dB 30 nm, 3-dB 66 nm); same four devices before AR coating as laser.heterogeneous rows
  (Ith, 2-sided slope efficiency, > 40 mW for 1.4 um); III-V/Si taper (waveguide_platform.transition: 1.0 / 0.25 / 0.75 dB
  derived from the two-length method, < 0.1 dB simulated, Table III geometry); passive Si waveguide (0.5 dB/cm derived
  from 0.02 dB / 400 um); polished Si facet (9 dB/facet). Not entered: Table IV Ps (material saturation power; Table II
  heads it Ps,out, abstract / conclusion print 14 / 16.25 dBm saturated output without design match), 11 K/W thermal
  impedance (devices in general), contact resistivity, prior-work values in Sec. II / Table II, design-only Fig. 3-9
  curves, tip field reflectivity 1e-3 (no parameter). Conflicts noted: 3-dB width 66 (text) / 69 (Fig. 15) / 65 nm
  (conclusion); Si facet reflection 0.28 vs 0.28%.
- matsumoto2018 (7 / 37): flip-chip InP SOAs (600 um straight on 1x8 splitter, 10 dB in-line author_estimate; 800 um
  7-deg angled, 15.3 dB derived and 23 dB chip gain author_estimate; 4-ch array 9.5 dB author_estimate, 62.5 um pitch);
  SOA-Si butt coupling (chip_chip_coupler.butt: 7.7 / 2.6 dB both interfaces author_estimate, Table I per-interface excess
  2.3 / 2.8 dB, MFD ~3 um, gaps); dual-core SSCs 7x3 (1.6 dB/facet measured, 1.5 simulated) and 3x3 SiON (loopback_half
  1.4 / 2.3 dB derived); 4x4 Si switch (1 dB author_estimate, footprint). Not entered: predicted tolerance budgets
  (< 1.6 / 2.2 / 4.4 dB), 1x8 splitter (only nominal 9 dB), 1 dB / 0.8 dB propagation, die-shear, ripple values (notes).
- otterstrom2019 (3 / 23): Brillouin racetrack as amplifier.other (gain > 30 dB, net > 20 dB, NF 38.5 / 15 dB simulated),
  as nonreciprocal.isolator (28 dB peak) and passive resonator.ring (Q 1e6 / 2e5, FSR 5.02 / 4.87 GHz, loss 0.29 / 0.89
  dB/cm derived from 6.7 / 20.6 m^-1, coupler mu^2 ranges as %). Not entered: group velocities (Table I labels swapped),
  gain bandwidth 10 MHz -> sub-MHz, 2.5 MHz / 350 kHz isolation widths, GB / Gamma / Omega_B, laser threshold (no number).
- guo2016 (1 / 11): AlN microring SHG (2500 %/W, 12% at 27 mW, Qi 4.6e5 / 1.5e5, QL 2.3e5 / 1.16e5, 20.9 / 11.3 pm/K
  derived, width, thickness, footprint). Not entered: R 30 um, bus widths / gaps (no frequency_converter parameter),
  temperature FWHM 7.7 C, g, extinction 0.75, Q ~1e6 cited [24].
- mutter2024 (2 / 6): PPRKTP waveguide BWOPO (frequency_converter.other, 8.4% derived via Manley-Rowe, 409 nm period,
  22 mm, 9.8 um) and the ion-exchanged waveguide (0.16 dB/cm at 798.9 nm). Not entered: 325 nJ threshold (energy),
  21 / 98 GHz output widths and 1514.6 / 1688.7 nm centres, 296 um2, d_eff. Fab KTH (authors' "we" fabrication steps).
- lapointe2025 (3 / 9): cached text is the Research Square preprint v1. BIG Faraday rotator waveguides ID13 / ID14
  (nonreciprocal.other, 0.13 / 0.14 dB fiber_to_fiber excl. Fresnel); isolator with two Polarcor polarizers (26.5 dB mean
  1510-1600 nm, > 25 dB C-band, 0.8 dB mean IL excl. polarizers, < 1.5 dB author_estimate incl. vendor 0.5 dB, 0.47 dB
  free-space lower bound). Not entered: FOM 346 deg/dB, MFD 9.4 um (no nonreciprocal mfd), "> 100 nm" bandwidth, bulk BIG
  values [21], 15-20 um cladding range.
- pintus2017 (4 / 6): R 35 um single-ring isolator (> 25 dB for 40-180 mA, author_estimate, borderline), two-ring
  cascaded isolator (~28 dB at 1503.7 nm), four-port ring circulator (11 / 6.7 dB author_estimate, sentence cites [35];
  9.15 dB simulated), two-ring circulator design (18.3 dB simulated). Not entered: 32 dB / 2.3 dB excess loss (stated as
  the authors' earlier demonstration [25], D259), resonance split / thermal shift data (no parameter), 8.7 dB I/O
  waveguide loss estimate, coupling 10.45%.
- white2022 (5 / 10): Kerr SiN ring isolators (1.8 dB IL / 16.6 dB, 5.5 dB IL / 23.4 dB at 90 mW), two-ring cascade
  (35 dB, ~5 dB IL), DFB-chip ring (up to 13.6 dB at 65 mW), ring array Qi ~5e6. Facility SNSF + SNF. Not entered:
  isolation thresholds 12.9 / 6.5 mW (no parameter); intro values 1.3 / 4.6 dB conflict with Sec. III (noted).

## Organizations missing from the registry

- TIA SCR of AIST (Tsukuba Innovation Arena Super Clean Room), matsumoto2018 p.6 Acknowledgement (facility).
- Yale SEAS cleanroom; Yale Institute for Nanoscience and Quantum Engineering, guo2016 p.5 Acknowledgment (facilities).
- Not needed (no fab statement): AEPONYX (lapointe2025 p.1), Svenska Laserfabriken AB (mutter2024 p.1), II-VI Inc. (BIG
  slab supplier, lapointe2025 p.6).

## Judgment calls

- One physical device entered as several class rows when the paper characterizes it in distinct roles: davenport2016
  SOA vs pre-AR-coating FP laser; otterstrom2019 amplifier / isolator / passive resonator; coordinator may prefer fewer.
- matsumoto2018 Table I per-interface misalignment excess entered as insertion_loss_db per_interface with
  includes / excludes (registry has no excess_loss_db for chip_chip_coupler); fab AIST on the SSC rows from the
  "fabricated in an advanced process line at AIST" statement, borderline on the switch row.
- pintus2017 single-ring Fig. 8 and circulator 11 / 6.7 dB kept as author_estimate (D80i borderline); delete if D259a
  is applied strictly.
- guo2016 fab empty although "we anneal our device" (D80b borderline); otterstrom2019 "room temperature" not converted.
- davenport2016 fab empty: fabrication-assistance thanks name a person without printed affiliation.
- Platforms `other` for III-V/TFLN, III-V/Si, AlN, RKTP, BIG; `soi` for Ce:YIG-bonded Si rings (song2025a precedent).

## Registry gaps (value skipped, locator, proposed definition)

- radius_um, gap_nm, bus_width_nm for frequency_converter: guo2016 R 30 um, gaps 0.6 / 0.5 um, bus 0.8 um (p.3); also
  radius_um / gap_nm for nonreciprocal (pintus2017 R 20 / 35 um, gap 200-260 nm, p.4-5; white2022 D 200 um, p.6).
- pump_threshold_nj (frequency_converter): mutter2024 325 nJ pulse-energy OPO threshold (p.3); "optical pump threshold
  as pulse energy (pulse width, repetition rate in condition)".
- isolation_threshold_mw (nonreciprocal): white2022 12.9 / 6.5 mW (p.9); "input power at which a nonlinear isolator
  reaches 3 dB isolation".
- isolation_bw_mhz (nonreciprocal) and gain_bw_mhz (amplifier): otterstrom2019 2.5 MHz (> 10 dB) and 10 MHz -> sub-MHz
  (p.4-5); "frequency width over which isolation / gain meets the stated level".
- nonreciprocal_split_nm (nonreciprocal): pintus2017 0.32 nm at 140 mA, 0.302 nm at 200 mA (p.4-5); "CW-CCW resonance
  wavelength split induced by the nonreciprocal phase shift (bias in condition)".
- mfd_chip_um for nonreciprocal: lapointe2025 9.4 um (p.5).
- excess_loss_db for chip_chip_coupler: matsumoto2018 2.3 / 2.8 dB (p.5 Table I).
- thermal_resistance_k_per_w for amplifier: davenport2016 11 K/W (p.9).
- back_reflection_db for waveguide_platform (already proposed by lit_11): davenport2016 field reflectivity 1e-3 (p.8).
