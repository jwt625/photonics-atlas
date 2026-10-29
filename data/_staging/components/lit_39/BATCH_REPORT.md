# Batch lit_39 report (distill subagent, 2026-10-29)

Dry-run `batch lit_39: +21 components, +155 metrics; errors 0` (the only warning concerns lit:ni2025b, another batch). ASCII, no
e-mail, no quotes. Page-1 title / authors match the source row for all six papers (zhang2017a is a 2-page Optica
Memorandum; slaby2022 a 2-page IPC paper). No garbled text layers. Not yet audited or merged.

## Per paper (components / metrics)

- dana2024 (5 / 21): 3D-printed six-mode photonic lantern on a 7-core fiber, `mode_converter.mdm_mux` (huang2018 precedent),
  platform polymer. Full device: free-space loss mean 2.7 dB (device_total, 12 input/pol, 1520-1600 nm) and per-input range
  1.197-3.23 dB (Fig. 10(a) annotations); holography IL 0.9 dB to a virtual matched fiber (derived: measured coupling
  matrix projected on simulated fiber modes); simulated 0.8 dB. Shortened-taper sibling butt-coupled to a 1 m six-mode
  fiber: 4.8 dB mean, range 2.533-5.434 dB (Fig. 10(b)). Simulated-only sections (D80e): MUX 0.17 dB; output taper 0.3 dB
  (n = 0.8) and 0.2 dB facet overlap (`fiber_chip_coupler.other`); source interface 97% coupling. Not entered: MDL 4.4 dB
  measured / 1.4, 0.29, 0.5 dB simulated and PDL < 0.2 dB (not allowed for mode_converter, gap); OVNA system MDL; ~1.4 dB
  fiber-coupling estimate; mode purity 95.2 / 94.8%; 0.12 dB core-misalignment calculation. Fab
  org_hebrew_university_of_jerusalem (contributions p.14: printed by a HUJI-only author).
- si2026 (2 / 24): inverse-designed 2 x 2 um reflector (`reflector.other`: simulated R > 96% mean, ~97% peak, > 96% under
  +/-10 nm bias; R_eff 92-96% author_estimate as a lower bound from intrinsic Q, D403; footprint, 650 nm port, stack) and
  400 um F-P cavity (`resonator.photonic_crystal`: Q_L ~1e5 and 1934.1 MHz linewidth of a representative resonance at an
  unstated wavelength (1500-1600 inferred), Q_i ~1.4e5 author_estimate, Q_L 4.70e4-1.54e5 and FWHM 9.83-33.84 pm at four
  resonances, FSR 0.724-0.763 nm, finesse and ng derived, 100 nm gap, 500 nm width, stack). Not entered: the GC (only a
  relative ~30 dB back-reflection suppression), finesse-based loaded R_F 0.870-0.959, the ~100 nm measurement-window
  bandwidth, 250 nm minimum feature. Fab empty (passive fabrication text).
- simard2015 (3 / 22): uniform MZI-IBG (`reflector.bragg`: kappa ~28.5 /cm derived from ~2850 /m, 276 nm period, 720 um,
  1.5 um width), square-shaped dispersion-less MZI-IBG (`reflector.bragg`: 3-dB bandwidth 4 nm, SLSR > 15 dB measured, C band
  inferred from Fig. 8 axis; 1.5 mm, 1 um), 2x2 MMI (`splitter.mmi`: simulated 0.1 dB excess loss, 5 x 90 um, 1.5 / 1.0 um
  ports, 100 um tapers). Not entered: pi-phase-shifted sibling (no printed value, no row), excess ports ~20 dB below
  reflection, fitted delta kappa 200 /m and SRA 8% / 4%, group-delay std 2.0 ps (gap), relative run-to-run changes. Fab
  org_university_washington (e-beam lithography at UW, p.8).
- ding2026 (6 / 42): AlN-on-sapphire (platform other). Microcavity-1 racetrack (Q_i 5.4M TM00 / 4.6M TE00 author_estimate
  per "assuming under-coupling", Q_L 2.8M / 2.7M, FSR 17 GHz, widths, gap, 3.9 mm Fig. 1(b) length); Microcavity-2 ring
  (Q_i 4.8M / 4.7M, Q_L, pumped-mode Q 3.5M, FSR 113 GHz, TE00-TM10 splitting 33.3 GHz derived, SEM 1.2 um / 72 deg);
  its Dirac soliton comb (`laser.comb`, 113 GHz, D396); platicon microresonator (Q_i 2.4M, FSR 225.1 GHz, G 43.0 GHz);
  Microcavity-3 780 nm width-varying racetrack (Q_i 2.2M / 1.6M, Q_L 1.4M / 0.9M, 1.2 / 2.5 um widths, 100 um coupling
  length, 600 nm gap); 820 nm SRL (`laser.other`: threshold 50 mW, linewidth < 220 Hz derived, 5 mW on-chip, 6 nm
  tuning, FSR 80 GHz). Not entered: most-probable Q 3.1M / 1.1M (population mode, no statistic), absorption-limited Q /
  loss (Supplementary Sec. 6 not cached), beta2-beta4, simulation kappa inputs, pump powers, frequency-noise floor. Fab
  org_tsinghua_university (contributions p.8); AlN films from co-authors at Institute of Semiconductors CAS / UCAS (note).
- zhang2017a (4 / 35): best near-critically coupled racetrack (Q_L 5.0M measured, Q_i 10.0M author_estimate, 38 MHz best
  linewidth, R 80 um), ring/racetrack family row (Q_i ~1.5M at 800 nm, ~4M at 2.4 um, D165), straight waveguide (2.7 dB/m ->
  0.027 dB/cm derived; intrinsic upper bound 1.5 dB/m -> < 0.015 author_estimate), bend R = 80 um (9.3 dB/m -> 0.093
  derived); stack design_target (NanoLN wafer, D402). Not entered: ring-down lifetime 4.2 ns. Fab org_harvard_university
  ("we fabricate", all authors list Harvard).
- slaby2022 (1 / 11): inverse-designed 1x3 SiN splitter on GF 45CLO (`splitter.other`): excess loss 2.48 dB mean and split
  30 / 36 / 33% author_estimate (simulated s-bend loss subtracted), simulated 0.91 dB and 33.8 / 32.5 / 33.8%, 49 um2
  design region. Paper's "insertion loss" is loss beyond the ideal split -> excess_loss_db (D43). Fab org_globalfoundries.

## Missing orgs

- Peter Brojde Laboratory for Miniature Integrated Systems (dana2024 p.14, acknowledgements and author contributions: the
  lantern was printed there; facility candidate, not entered).

## Judgment calls (for the audit)

1. dana2024 holography IL 0.9 dB as `derived` (projection of the measured matrix on simulated fiber modes); free-space and
   fiber-coupled losses `device_total` (include the MCF-core interface).
2. dana2024 shortened-taper butt-coupled device as a separate row (text: taper shortened for that experiment).
3. dana2024 output taper / source interface as `fiber_chip_coupler.other` (3D-printed coupler to fiber); simulated-only rows.
4. simard2015: CMC Microsystems "contribution and technical support" not a fab / facility org (no fabrication or MPW wording;
   D398 needs "chip fabrication support"). MMI simulated 0.1 dB entered once for both access widths.
5. ding2026: pumped-mode Q 3.5e6 printed without qualifier entered as q_intrinsic (compared in the text with the 4.8e6
   intrinsic value; a loaded 3.5e6 would exceed every labelled loaded Q). The skill default for an unqualified Q is q_loaded.
6. ding2026: SRL resonator (80 GHz) kept separate from Microcavity-3 (identity not stated, D159).
7. si2026: q_loaded / linewidth of the representative resonance carry the measurement window as inferred wavelength.
8. zhang2017a Q_i 10.0e6 author_estimate (near-critical coupling read from the transmission inset, D403).

## Registry gaps

- `mdl_db` for mode_converter (repeat of the lit_25 proposal): dana2024 measured 4.4 dB (p.8, holography), simulated 1.4 dB
  device / 0.29 dB MUX / 0.5 dB taper (p.4, p.7). Definition: mode-dependent loss of a mode (de)multiplexer, per device as
  stated in condition.
- `pdl_db` for mode_converter: dana2024 max polarization dependence < 0.2 dB (p.8, Fig. 10(a)).
- `group_delay_ripple_ps` (reflector, wdm): simard2015 in-band group-delay std 2.0 ps (p.12, Fig. 8(b)). Definition: in-band
  group-delay ripple (std or peak-to-peak as stated in condition).
- `back_reflection_suppression_db` or a relative form of back_reflection_db (fiber_chip_coupler): si2026 inverse-designed
  GC ~30 dB lower back-reflection than a conventional GC (p.4, Fig. 3(e)); only a relative value is given.
- statistic `mode` (most probable value of a distribution): ding2026 most probable Q_i 3.1e6 (1550 nm, ~4400 resonances) and
  1.1e6 (780 nm) (p.4, Fig. 1(g, h)).
