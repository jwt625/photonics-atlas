# Batch lit_03 report (distill subagent, 2026-10-22, transcribed by the coordinator)

10 papers, 30 components, 165 metric rows; dry-run `batch lit_03: +30 components, +165 metrics; errors 0`
(log `logs/merge_component_staging_20261022T220808.log`). verified_on 2026-10-22 on every row.

## Per paper

- brisson2023 (NbN SNSPD, 200 mm SOI): 1 component / 8 metrics. snspd_u20: on-chip detection efficiency
  quantum_efficiency_pct 81.5 % (100 Hz DCR), 89.7 % (5 kHz DCR), 50 % (200 MHz flux), 2.3 K, TE, ref_plane
  on_chip, GC loss excluded; geometry Si 300 x 400 nm, NbN 5 nm / 0.1 um wide / 20 um. Not entered (no parameter):
  11 kOhm/um nanowire resistance (<1 % uniformity), Ic 4.62 uA, 3.2 ns decay, 200 MHz max count rate, DCRs; GC loss
  not reported (no GC row). fab org_cea_leti borderline ("we start the fabrication"; CEA-Leti + CEA-IRIG; 200 mm line
  taken as Leti).
- hu2023 (Ge-Si PD, inductive gain peaking): 3 / 18. peaked_ge_pd bw3db 80 GHz (bias empty: Sec. 3.2 none, Table 1
  4 V, Fig. 4(b) 2/4/6 V); responsivity 0.5 A/W fiber-referred and >0.5 A/W 1530-1565 nm, 1.0 A/W internal (derived,
  coupling excluded); dark current 3 nA at -1 V, 6 nA at -4 V; Ge 0.6 um design / 0.58 um TEM, 350 nm, 35 um.
  unpeaked_ge_pd bw3db 23/40/42 GHz at -2/-4/-6 V, 21 fF (S11 fit). ssc (suspended Si edge coupler) 3 dB per facet
  author_estimate (origin not stated). Not entered: 31 ohm series R (no parameter), responsivity vs temperature
  (curves), TDECQ/BER/FOM (link), 170 pH inductor (design, notes). No fab org stated.
- qi2024 (InGaAs/InP SPAD module): 1 / 6. ingaas_spad (photodetector.spad, inp): PDE 40 % at 238 K 1550 nm
  (ref_plane module), 45.7 % max at 248 K; dark current 0.4 nA best near breakdown (bias -70 V with note); breakdown
  70 V; 137 fF (derived from 0.137 pF); active diameter 25 um in absorber_width_um with note. Gating IC / readout not
  rows. Not entered (no parameter): DCR, afterpulse, hold-off, gate width 117 ps, jitter 119 ps, punch-through 35 V.
  fab empty ("we design and fabricate"; USTC, Chongqing ORI, QuantumCTek).
- virot2014 (Ge APD): 2 / 19. ge_apd dark 18 nA at -1 V, 610 uA at -7 V; responsivity 0.4 A/W unity gain, 8 A/W
  with gain; gain 20 at -26 dBm, 10 at -11.25 dBm (both -7 V); bw3db >40 GHz unity, ~11 GHz at gain ~17; GBP
  >190 GHz; capacitance 18/5/~4 fF at 0/-2/-3 V; Ge 300 nm 10 x 10 um, WG 500 x 220 nm, BOX 2 um; fab org_cea_leti
  (author contributions). ge_pin_long (photodetector.other) 1.2 A/W. Not entered: gain >140 (bias not stated),
  excess noise 5.24, k_eff ~0.4, fitted intrinsic width 280 nm, Q-factor / BER. Text extraction garbles symbols; all
  values checked on page renders.
- song2021 (InGaAs PDs on Si and native InP): 12 / 54, all photodetector.vertical. 6 array pixels (Si / InP x 20/30/40
  um): mean dark current of 64 pixels at -1 V (Fig. 3 labels; std and yield in notes), mesa diameter, 1 um absorber,
  100 um pitch, 64 channels; Si 40 um also 5.71 nA best and 0.72 A/W fiber-referred. 6 high-speed PDs (10-40 um) dark
  current at -8 V; 10 um bw3db 11.2 GHz. Not entered: other responsivities (Fig. 3(e) labels ambiguous); InP 40 um
  0.57 A/W text p.2 conflicts with the figure label on the 20 um Si curve; dark-current density, activation energy,
  J_bulk/J_surf; other bandwidths (inset only). facility org_ucsb_nanofabrication_facility; fab empty (passive).
- wang2022a (GeSn PD at 2 um): 3 / 12. gesn_wpd_l75 dark 5700 nA (derived from 5.7e-6 A), responsivity 0.525 A/W at
  2004 nm (on-chip, derived), 20 x 75 um, MQW stack 360 nm (derived). gesn_wpd_l25 bw3db 6 GHz at -7 V. ge_gc CE
  18.4 % (simulated), period 553 nm, fill factor 0.42 (derived from 0.58 empty), etch 200 nm. Not entered: EAM (IL
  10.88-12.91 dB, ER 2.02 dB, modulator out of scope), WG 500 x 850 nm (geometry only), 0.38 A/cm2. No fab org stated.
- hosseini2015 (PZT stress-optic PS, TriPleX): 4 / 27 (electrode widths 10/20/30/40 um). v_pi_v from Fig. 6 VpiL
  ~22/13/12.3/13 V cm with L = 1 cm, extracted_from_figure. W30: rise_time_us 0.253 (derived; exponential tau, not
  10-90 %), bw3db_khz 629.1 (derived by authors from tau), p_pi_mw 0.0003 author_estimate. Geometry SiN 25 nm x 4.4
  um, 8/8 um SiO2, 10 mm. Not entered: MZI ER ~25 dB (extinction_db not allowed for phase_shifter), 3 nF, 30 ohm,
  430 nJ/bit, 287 ns (text) vs 280 ns (figure). process_name TriPleX; fab empty.
- meng2023 (GSSe PCM memory): 1 / 3. gsse_pram_4bit (phase_shifter.phase_change) IL 0.12 dB all amorphous
  (per_component, 1550 nm inferred), 80 um pad, heater 200 nm. fab org_george_washington_university;org_mit
  (contributions). Not entered: GSSe thickness (40/30/20 nm inconsistent), 12 dB over 16 states, Table 1 values,
  ~500k cycles, switching times, 6-state cell; double-sided-heater design has no registry metric.
- oz2023 (MoS2 heater on Si ring): 2 / 15. mos2_heater ~100 pm/mW (derived from 0.1 nm/mW), ~15 mW per FSR
  (derived), rise/fall 26/24 us (10-90 %), heater 283 um x ~2 um, 30 nm gap, WG 400 x 220 nm, BOX 2 um. si_mrr Q
  ~4000 (loaded, unqualified), ER >10 dB, FSR 1.42 nm. Not entered: heater excess loss ~1.5e-3 dB/um, breakdown ~1 mW.
- mourgelas2021 (LWIR chalcogenide pedestal): 1 / 6. chg_pedestal_wg 0.9 dB/cm mean (7-11 um, TE+TM, 2 WGs), 0.5
  dB/cm best TM; core 4.1 um, width ~26.5 um, IG2 lower cladding 7.7 um in box_thickness_um (note), 0.25 um cap; fab
  org_university_of_southampton. Not entered: Fig. 5(b) TM ~0.24 dB/cm at 11 um (below the text's 0.5), mode sizes,
  film indices.

## Fab / facility orgs missing from the registry

- George Washington University Nanofabrication and Imaging Center (GWNIC): meng2023 p.13 ack, p.11 Methods (facility).
- NIST Center for Nanoscale Science and Technology (CNST): meng2023 p.13 (thin-film analysis; borderline facility).
- Micro-Nano Fabrication Unit at Technion: oz2023 p.19 "devices were fabricated at" (facility).
- LioniX BV (TriPleX): hosseini2015 p.1 affiliations; no explicit fabrication statement (no row change).

## Judgment calls

1. wang2022a GeSn/Ge MQW waveguide PDs as photodetector.ge_waveguide (alt. other).
2. meng2023 amplitude-only PCM memory as phase_shifter.phase_change.
3. qi2024 discrete SPAD chip in a fiber-coupled module (inp, ref_plane module): in scope?
4. hosseini2015 v_pi_v from Fig. 6 VpiL / 1 cm; 253 ns exponential tau in rise_time_us with note.
5. song2021 siblings per pixel diameter and substrate; high-speed devices separate rows.
6. hu2023 un-peaked PD geometry restates the Sec. 2 design.
7. brisson2023 fab org borderline.
8. song2021 Si-substrate rows platform `other` (no III-V-on-Si heteroepitaxy enum value).

## Registry gaps (proposed)

dark_count_rate_hz (photodetector snspd / spad); afterpulse_probability_pct (hold-off in condition);
detector_timing_jitter_ps (photodetector; timing_jitter_fs is laser-only); max_count_rate_mhz, recovery_time_ns;
critical_current_ua (snspd); dark_current_density_ma_per_cm2; series_resistance_ohm (photodetector);
excess_noise_factor (apd); capacitance_ff for phase_shifter (nF scale); extinction_db for phase_shifter (with type in
condition); per-length excess loss for phase_shifter; cycle_endurance (phase_shifter, switch_fabric); n_states
(phase_shifter.phase_change).
