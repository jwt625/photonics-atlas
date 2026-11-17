# lit_178 batch report

Distilled 2026-11-16 under the pic-component-distill skill (Contracts v4-v7, DevLog-007 rulings through D615).
Papers: lit:sacher2014b, lit:chang2023, lit:li2013a, lit:wan2019. Page-1 titles match the source rows; no correction /
erratum; no garbled text layer. Totals: 9 components, 81 metric rows. Dry-run: `+9 components, +81 metrics; errors 0`
(one WARN on cmp_lit_ni2025b_pimmwc, another batch).

## lit:sacher2014b (Optics Express 2014, Si3N4-on-SOI dual-level grating coupler) - 3 components / 39 metrics

- `cmp_lit_sacher2014b_dual_level_gc` (fiber_chip_coupler.grating, si_sin_multilayer, fab org_astar_ime): 20 rows.
  Measured -1.3 dB (74 %) at 1536 nm, 1-dB bandwidth 80 nm, `loopback_half` + `derived` (single-GC spectrum is the
  stated square root of the two-GC transmission, D542 / D554); peak wavelength measured; worst-case back-reflection
  -16 dB as `ge 16` author_estimate (rests on the assumption that all ripple comes from the GCs; band edges 1496-1576
  nm read off the Fig. 6 arrow, `wavelength_inferred`); simulated -1.0 dB / 82 nm and +/-50 nm offset bandwidths
  94 / 72 nm; FDTD 1-dB alignment sensitivity about 2 um (simulated); demux-PIC loss-breakdown estimate 1.5-2 dB per GC
  (author_estimate, no index-matching fluid); geometry: 21 deg, 16 periods (11 + 5, derived), 400 nm Si3N4 /
  65 nm Si / 2 um BOX, 900 nm output width, two taper stages 21.5 / 40 um, footprint 27 x 87 um (derived).
- `cmp_lit_sacher2014b_uniform_gc_design` (row_kind design): simulated -1.8 dB / 114 nm, period 1.4 um (derived).
- `cmp_lit_sacher2014b_mrr_demux_1x4` (wdm.mrr, soi_strip, fab org_astar_ime): 16 rows. FSR about 11.4 nm, spacing
  about 2.5 nm after tuning, thru-port extinction > 15 dB, drop-port fiber-to-fiber peak -5.3 to -6.8 dB (4 rings),
  thru-port peak about -5 dB, 3-dB width about 0.5 nm, loaded Q about 3100, heater power < 35 mW per ring; ring
  geometry (R 7.5 um, 500 nm, gap 230 nm, 2.5 um coupler, 150 nm Si, 2 um BOX).
- Not entered: 135 nm inter-level SiO2 gap (gap_nm not allowed on fiber_chip_coupler); Fig. 2(c) per-period tooth
  widths / gaps / offsets (design labels per period); simulated directionality 80 % / > 80 % (no parameter); 3D-FDTD
  x-misalignment +/-100 nm effect (< 0.1 dB, < 1 nm; no parameter); Si3N4-Si adiabatic transition (geometry only, its
  loss is lumped with ring couplers and waveguides, 1-2 dB, p.10); TiN heater 1.5 um above the Si3N4 (heater_gap_um not
  allowed on wdm); "40 nm range roughly the 0.5-dB bandwidth through two GCs" (approximate, no parameter); Fig. 1
  comparison points (other works, rule 3).
- Fab / org: "Grating couplers were fabricated in the Si3N4-on-SOI photonics platform in Fig. 2(b) at IME, A*STAR"
  (p.7) -> org_astar_ime. process_name left empty (no PDK / process name printed; sacher2017 precedent; sacher2014a
  used "custom Si3N4-on-SOI process at IME, A*STAR" - coordinator may align).
- Judgment call: demux fab org_astar_ime is borderline. Sec. 3 says "we fabricated ... on the platform described in
  Fig. 2(b)" (authors at Toronto and IME); the platform is placed at IME only by the Sec. 2.2 sentence. Recommendation:
  keep (the platform sentence names the org with the process); empty it if D395 is read strictly.

## lit:chang2023 (JLT 2023, monolithic polarization controller and tracking loop, GF 90 nm SOI) - 1 component / 3 metrics

- `cmp_lit_chang2023_pol_tracker` (polarization.compensator, soi, fab org_globalfoundries, process_name "GlobalFoundries
  90WG (90 nm SOI CMOS-photonic process), university program"): compensated output-power range <= 1 dB over 1000
  static SOPs (-17 +/- 0.5 dBm) and <= 1 dB under 2 pi rad/s scrambling, both as `pdl_db` (velha2016 precedent);
  longest stabilization time 500 us (13 initial SOPs) as `tracking_time_us`. All at 1310 nm.
- Not entered: loop bandwidths 16.6 / 23.5 kHz (calculated estimates; no polarization parameter); error-free tracking up
  to 1256 rad/s (no parameter); BER / receiver sensitivity (link level); SAR ADC 491.4 uW, FSM 626.64 uW (simulated
  electronics; power_consumption_w not allowed on polarization); DAC LSB 3.17 mA / 200 mA per phase shifter (drive
  range, no P_pi); FSM area; 50:50 DC ratio (analysis assumption); PSR, DCs, phase shifters, monitor PD and edge
  couplers have no individual metrics, so no separate rows.
- Fab / org: GLOBALFOUNDRIES thanked "for providing silicon fabrication through the 90WG university program" (p.9) ->
  org_globalfoundries. Optelligent thanked for device packaging (p.9): packaging only, no fab role (D934 precedent;
  org_optelligent already registered).
- Journal extension of the authors' ECOC 2022 paper (ref. [14]); values kept (D408: no value sentence or caption cites
  it).

## lit:li2013a (Optics Express 2013, double-etched apodized grating coupler, 340 nm SOI) - 3 components / 23 metrics

- `cmp_lit_li2013a_double_etch_gc` (fiber_chip_coupler.grating, soi, fab empty): 21 rows. Measured -1.5 dB (70.8 %) at
  1560 nm and 3-dB bandwidth 54 nm, `loopback_half` + `derived` (two-GC link, lossless-waveguide and equal-GC
  assumptions stated; fiber / connector loss normalized out); simulated design -0.97 dB (80 %), 1-dB 31 nm, 3-dB 53 nm,
  about 1 % reflection (20 dB, simulated, D83f); simulated with fabricated depths -1.3 dB / 53 nm; etch depths design
  90 / 190-200 nm and SEM about 85 / 210 nm; 340 nm Si, 2 um BOX, 23 periods (4 + 19), length about 13 um, 10 um
  grating width, 500 um taper.
- `cmp_lit_li2013a_double_etch_gc_dg_m10` / `_dg_p10` (groove widths -10 / +10 nm in the mask): about 1.8 / 1.7 dB,
  derived from the Fig. 5 labels (0.3 / 0.2 dB below the -1.5 dB line), peak wavelengths about 1573 / 1553 nm read off
  Fig. 5.
- Not entered: period 548-610 nm and groove fraction 0.08-0.4 (p.3; the single-etched design of ref. [8], not this
  device); minimum feature about 135 nm (role ambiguous for layout); access-waveguide slab about 100 nm (waveguide, not
  the grating); simulated groove-width / etch-depth tolerances (< 0.15 dB, < 0.3 dB; no parameter); fiber tilt 10 deg
  kept in the condition only (measurement setting; no design angle printed).
- Fab / org: "was fabricated on a commercial 8-inch 340-nm-thick SOI wafer ... using CMOS-compatible technology" (p.5),
  passive, no org named; all authors at IME, A*STAR -> fab empty (D80b, D84a). Acknowledgment is a SERC grant
  (funding, not a facility). No process name.
- Judgment call: the dg siblings are separate rows (different mask design, rule 9) with values derived from the
  labelled 0.2 / 0.3 dB deviations; their simulated counterparts (Fig. 2) were not added.

## lit:wan2019 (IEEE PTL 2019, Fiber-Interconnect Silicon Chiplet Technology) - 2 components / 16 metrics

- `cmp_lit_wan2019_fisct` (fiber_interface.other, platform empty, fab empty): 8 rows. Peak-signal penalty of the
  passive FISCT path versus active alignment of the same two-GC circuit: about 0.67 dB (86 %) at the designed position
  g5, 1.2 dB (75 %) for a 1 um +x offset, 3 dB (50 %) for a 1 um -y offset (measured, scope fiber_to_fiber, excludes
  the common GC / waveguide loss, method reference_structure); Fig. 4(b) means of repeated insertions at g5 / g6 / h5 /
  h6 read off the plot (0.83 / 0.70 / 0.47 / 0.37, converted to dB, extracted_from_figure); fiber MFD about 10 um
  (specification). Wavelength 1610 nm inferred (measured GC peak).
- `cmp_lit_wan2019_focusing_gc` (fiber_chip_coupler.grating, soi, fab empty): measured peak 1610 nm, design 1550 nm
  (author_estimate), theoretical 30 % / -5 dB (simulated), 250 nm Si, 3 um BOX, 9 deg fiber angle, grating length
  about 15 um.
- Not entered: interlayer gap 20 um between carrier and chip (no parameter on fiber_interface); 54.7 deg ferrule taper
  and 300 um carrier (geometry with no parameter); "submicron" alignment accuracy (no number); absolute coupling
  losses (not reported, data in volts); Fig. 2 SEM scale bars.
- Fab / org: fabrication sentences are passive, all authors at Georgia Tech -> fab empty (D80b). NSF ECCS-1542174 /
  ECCS-1810081 are grants, not facilities (D80c). Nanoscribe is the printing tool, not an org role.
- Judgment call: the relative penalties are stored as `insertion_loss_db` with scope fiber_to_fiber and the reference
  stated in condition / excludes; `coupling_efficiency_pct` was not used because 86 / 75 / 50 % are ratios to the active
  reference, not absolute coupled fractions.

## Missing fab / facility orgs

None. All orgs used are in the registry (org_astar_ime, org_globalfoundries). Optelligent (chang2023, p.9, packaging
assistance) is registered and has no component role.

## Registry gaps (skipped value + locator + proposed definition)

1. `gap_nm` on fiber_chip_coupler: sacher2014b 135 nm SiO2 between Si3N4 and Si grating teeth (p.5). Proposed: vertical
   gap between the two levels of a dual-level / multilayer grating coupler.
2. `directionality_pct` (fiber_chip_coupler): sacher2014b simulated 80 % (uniform) / > 80 % (p.5-6, Fig. 3(b)).
   Proposed: fraction of the radiated power directed toward the superstrate (simulated, definition in condition).
3. Polarization tracking rate (polarization, switch_fabric): chang2023 error-free up to 1256 rad/s (p.9, Fig. 11(c)).
   Proposed `max_tracking_rate_rad_per_s`: highest SOP rotation rate tracked at the stated BER / power criterion.
4. `bw3db_khz` widened to polarization (loop bandwidth): chang2023 closed-loop small-signal bandwidth 23.5 kHz
   (calculated, p.5).
5. `heater_gap_um` on wdm / resonator: sacher2014b TiN heater 1.5 um above the Si3N4 level (p.4 Fig. 2(b)).
6. Stand-off gap on fiber_interface: wan2019 interlayer gap 20 um between the Si carrier and the photonic chip (p.3).
