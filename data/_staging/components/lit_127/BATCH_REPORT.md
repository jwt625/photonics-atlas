# Batch lit_127 report (distiller, 2026-11-12)

Family: phase_shifter / photodetector. Papers: sheng2026, li2018, miller2019, jacques2019, zhou2020, zeng2019. Each cached
text was checked against its source row title (page 1): all six match, none is a correction / erratum. Totals: 25 components,
151 metric rows. Validator: `merge_component_staging.py data/_staging/components/lit_127 --dry-run` -> +25 components,
+151 metrics, 0 errors (one pre-existing warning on a merged ni2025b row, not this batch).

## sheng2026 (1 component, 25 metrics)

- `inp_dual_layer_microheater` (phase_shifter.thermo_optic, inp_membrane): P_pi 1.11 / 1.05 / 1.2 mW at 1550 / 1510 / 1580 nm
  (text) plus 5 Fig. 3(c) reads (1520-1570 nm); phase range about 3 pi; MZI extinction > 23 dB; simulated IL < 0.3 dB;
  1/e time constants 10 / 9.2 us (square drive); pulse-driven rise / fall times 2.17 / 3.22 us (Fig. 5), 0.87 / 6.06 us
  (Fig. 8), 1.04 / 2.22 us (Fig. 9); heater resistance 8.3 kOhm (assumed, author_estimate); geometry (n-InP heater 1.5 um
  wide, 100 nm thick; i-InP 300 nm; lead distance 21 um; functional length 19 um).
- Not entered: FoM values (product of entered values, no parameter); Fig. 7 fall times 3.11 / 2.04 us (caption repeats
  the Waveform 1 parameters for Waveform 3 and gives a different voltage for Waveform 4 than the text implies; cycle not
  stated: D156); power imbalance 1.24 dB (derived by the authors from the extinction, a splitter property); crosstalk and
  2.26 mW/pi / 13 us of the authors' earlier device (ref. [16], D259); system energy percentages; taper length 15 um
  (registry gap); heater cross-section 0.15 um2.
- Orgs: fab empty (passive fabrication wording; authors at TU/e and Tokyo Tech). Facility `org_nanolab_tu_e`
  (p.11 Acknowledgment, cleanroom facility; ma2021 precedent). No missing orgs.
- Judgment calls: 10 / 9.2 us entered as `thermal_time_constant_us` (paper defines tau as the 1 - 1/e time and its rise /
  fall times at 63.2 %; chen2024b precedent); pulse-driven times as `rise_time_us` / `fall_time_us` with the 0.632 pi
  definition in condition (not 10-90 %). Phase range: p.4 measured "almost 3 pi" entered (approx); abstract "more than
  3 pi" and conclusion "over 3 pi" noted as a conflict (D417). Conclusion FoM 1.9 vs 1.81 mW us on p.10 (conflict,
  notes). Printed percentages for the Fig. 8 case refer to the opposite edges of the 10 / 9.2 us pair (notes).
  `heater_thickness_nm` 100 used for the doped n-InP heating layer although the registry definition says metal (flag).
- Registry gap: `taper_length_um` for phase_shifter (15 um, p.2 Sec. 2: adiabatic tapers into the heater section;
  proposed: allow taper_length_um on phase_shifter = length of the mode-transition taper into / out of the tuning section).

## li2018 (1 component, 3 metrics)

- `gst_memory_cell_4um` (phase_shifter.phase_change, sin; amplitude-only memory, D155): n_levels 34 (dual-pulse) and 20
  (single-pulse random programming), probe 1610 nm; cell length 4 um.
- Not entered: ERASE energy 680 pJ and time 250 ns, programming energies 68-135 pJ, settling times about 200 / 500 ns,
  level-error standard deviations (0.416 %, 0.169 %, < 0.5 %, 0.482 %), recrystallization thresholds (0.37 relative
  amplitude, > 150 ns), transmission change up to about 28 % (Delta T, not an extinction), stability claims (cited refs.
  [20], [25]); 2 um GST strip of the simulation (design only, no row); GST / ITO 10 nm thicknesses (core_material only).
- Orgs: fab empty (passive wording; authors at Oxford, Exeter, Munster); no facility named. Supplement 1 not cached.
- Judgment call: the 20-level single-pulse experiment does not restate the device; the paper presents one memory cell
  throughout, so it is on the same row (flag for audit, D159).
- Registry gaps: (1) `switching_energy_pj` on phase_shifter (680 pJ ERASE, p.3 Sec. 2A; proposed: optical or electrical
  energy of one write / erase operation, pulse definition in condition); (2) `write_pulse_us` / programming time on
  phase_shifter (250 ns, p.3; already a D438 candidate); (3) level error / programming accuracy in % (0.482 %, p.4).

## miller2019 (7 components, 33 metrics)

- `ps_1pass`, `ps_3pass`, `ps_5pass`, `ps_7pass` (phase_shifter.thermo_optic, soi): P_pi 15.4 / 4.6 / 2.6 / 1.7 mW;
  minimum IL 1.2 dB at 1570 nm / 2.2 dB at 1594 nm / 4.6 dB at 1601 nm (3/5/7-pass); tau 6.5 us on all four (stated
  independent of the number of passes); multimode width 2.44 um (derived from um).
- `mode_converter_adc` (mode_converter.converter): 0.44 dB per conversion event (passes 1-5) and 1.2 dB (passes 6-7),
  derived; both reproduce from the printed minimum ILs (2.2 / 5; (4.6 - 2.2) / 2).
- `mmi_1x2` (splitter.mmi): excess loss < 0.03 dB per splitter (origin not stated, author_estimate); 1 x 2.
- `opa_512` (free_space_emitter.other): 512 channels, 1.3 um pitch, FOV 70 deg (phi) x 6 deg (theta), 0.265 deg/nm,
  divergence 0.15 x 0.08 deg, peak-to-sidelobe 7.5 dB, nominal emission angle 45 deg (design), grating period 520 nm,
  2 mm grating length, 220 nm SOI, chip 8 x 15 mm.
- Not entered: 3-dB optical bandwidth > 100 nm of the multi-pass shifters (no bandwidth parameter on phase_shifter);
  3.7 % phase variation over 1525-1600 nm; FoM 11.1 mW us; 2-3 dB over 150 nm with optimized converters (Supp. Fig. S2,
  not cached); array power 1.9 +/- 0.2 W (power_consumption_w not allowed on free_space_emitter); effective vs physical
  aperture 1.1 / 1.6 mm; theoretical divergence 0.133 deg; 8 nm corrugation width; 28 um phase-shifter spacing
  (pitch_um not allowed on phase_shifter); comparison values from refs. [7], [12], [33], [34], [39], [40].
- Orgs: fab `org_columbia_university` on the array rows only (first-person "We fabricate this array ... in a university
  cleanroom", p.3; all authors at Columbia, one with a second NCTU affiliation; D72 / D395); test phase shifters and the
  converter fab empty (their fabrication is in Supplement 1, not cached; D515). Facilities on all rows:
  `org_advanced_science_research_center_nanofabrication_facility` (printed "Advanced Science Research Center at the City
  College of New York") and `org_columbia_nano_initiative` (p.4 Acknowledgment). No missing orgs.
- Judgment calls: tau 6.5 us as `thermal_time_constant_us` (printed "phase tuning time tau", used in P_pi x tau;
  definition only in Supp. Fig. S9, not cached); P_pi rows carry 1525-1600 nm with `wavelength_inferred` (no wavelength
  printed with the values); converter rows method `cutback` (series of 3 / 5 / 7 passes), band l_band.
- Registry gaps: (1) `bw_3db_nm` (or a criterion bandwidth) on phase_shifter (> 100 nm, p.3, Fig. 2(b); proposed: allow
  bw_3db_nm for phase_shifter = optical span where IL stays within 3 dB of its minimum); (2) `power_consumption_w` on
  free_space_emitter (1.9 W, p.4, Fig. 4(c); proposed: total phase-shifter electrical power of an OPA, scope in
  condition); (3) `pitch_um` on phase_shifter (28 um, p.3).

## jacques2019 (4 components, 42 metrics)

- `tin_tops_7p5um` (fabricated, soi_strip): P_pi 29.2-31.5 mW (arm pitch 50-200 um), R 540 ohm, 3-dB bandwidth 33 kHz,
  1/e rise / fall 3.7 / 7.2 us, IL < 0.4 dB (below resolution, Table 2), geometry (TiN 7.5 um, 2 um above a 500 x 220 nm
  strip, 320 um, 2 um BOX).
- `npp_si_tops` (fabricated, soi_rib): P_pi 22.8 mW (Table 2) and 22.8-23.3 mW range, Fig. 7 per-interval 23.2 / 22.7 /
  22.1 mW; R 1020 ohm; 85 kHz; 1/e rise / fall 2.2 / 2.0 us; IL < 0.4 dB; simulated P_pi 25.5 mW, tau about 5.8 us, IL
  about 0.008 dB; geometry (2 x 1.0 um N++ strips, 0.8 um buffer, 500 nm rib, 220 / 90 nm, etch 130 nm, 320 um).
- `tin_tops_2um_sim` (design): simulated P_pi 23.9 mW, tau about 10.2 us; 2.0 um TiN.
- `tin_tops_2p5um_opt` (design): projected P_pi about 21.4 mW, tau about 5.6 us (author_estimate: simulation corrected by
  measured offsets; abstract headline).
- Not entered: per-pitch P_pi values of Fig. 8 (legend not in the text layer, no page render); power drift < 0.1 mW;
  thermal crosstalk reductions 0.31 / 0.11 / 0.08 / 0.02 rad with deep trenches (no parameter); frequency-response
  peaking 13 / 17 kHz; FOMs; buffer 0.6 um design variant; Table 1 values (other works).
- Orgs: fab `org_astar_ime` ("fabricated on the same die in a multi-project wafer at A*STAR's Institute of
  Microelectronics (IME) Foundry", p.7; printed "now AMF" kept as IME, D515 rule); process_name set to the IME MPW
  wording. CMC Microsystems and AMF only in a support acknowledgment (p.15): not fab (wang2012 precedent). No missing orgs.
- Judgment calls: Fig. 1(a) caption 25.2 mW vs text 25.5 mW simulated (25.5 entered, note); "optimal" TiN design kept as
  a separate design row because the abstract headline (21.4 mW, 5.6 us) belongs to an unfabricated 2.5 um width; the
  author projection of about 21 mW for a fabricated 2.0 um heater left in notes (not entered on the 2.0 um simulation
  row).

## zhou2020 (7 components, 28 metrics)

- `pt_r700_d250`: responsivity 0.11 A/W at 1993 nm, -1 V; dark current density 45.2 mA/cm2 at -1 V; series R 10.8 ohm.
- `pt_r700_d60`: 3-dB bandwidth 2.7 GHz at 2 um, -5 V (text) plus Fig. 14 reads (0.95 GHz at 2 um / -3 V; 2.4 / 0.75 GHz
  at 1550 nm, -5 / -3 V); series R 22.7 ohm.
- `nopt_d250`: dark current density 31.5 mA/cm2 at -1 V; responsivity 0.022 A/W (Fig. 6(b) read).
- `nopt_d60`: Fig. 14(a) bandwidth reads 2.1 / 0.75 GHz.
- `pt_r600_d250`: about 0.27 A/W across 1565-1625 nm; 0.083 A/W at 1993 nm (Fig. 6(b) read).
- `pt_r500`, `pt_r800`: Fig. 6(b) reads 0.043 / 0.045 A/W.
- Geometry: mesa diameter as `absorber_width_um` (song2021 / chen2019 precedent), absorber 360 nm derived (6 x 60 nm MQW).
- Not entered: specific detectivity 2.137e8 and 6.5699e8 cm Hz^1/2/W, thermal / shot noise; normalized reflection 0.29 vs
  0.72; shunt resistances 396 / 27.5 kOhm; on-off ratio about 2e4; cut-off wavelength 2260 nm and shoulder 1950 nm
  (Fig. 9(b), mesa not stated); bulk 28.7 mA/cm2 and surface 15.6 uA/cm leakage (array regression, notes); surface-leakage
  shares (Fig. 11); band-structure calculation (612.1 meV, 2025 / 2300 nm); > 10 GHz for 20 um mesas (cited).
- Orgs: fab `org_nanyang_technological_university` as D84b borderline (no fabrication sentence; NTU staff thanked for
  electron-beam lithography assistance, p.12). Wafer grower not named. No missing orgs.
- Judgment calls (flag for audit): (1) 45.2 mA/cm2 has no printed mesa diameter; entered on the 250 um row because it
  reproduces from the paper's bulk density and the Fig. 11 250 um surface share (28.7 / 0.63 = 45.6; 60 um would give
  about 39); (2) 31.5 mA/cm2 identified with the 250 um point of Fig. 10(b); (3) Fig. 6 does not restate the mesa
  diameter: the non-trapping and R = 600 nm reads are put on the 250 um rows (R = 700 nm bar equals the 250 um value),
  R = 500 / 800 nm rows say diameter not stated; (4) platform `other` (GeOI); bias values entered negative for reverse
  bias.
- Registry gaps: (1) `specific_detectivity_jones` on photodetector (2.137e8 cm Hz^1/2/W at 2 um, p.11; proposed:
  D* = sqrt(A df) / NEP, units cm Hz^1/2 / W); (2) `cutoff_wavelength_nm` on photodetector (2260 nm, p.7, Fig. 9(b);
  proposed: long-wavelength edge where photocurrent becomes negligible, criterion in condition); (3) `shunt_resistance_ohm`
  (396 / 27.5 kOhm, p.10); (4) photon-trapping hole radius / period on photodetector (500-800 nm / 2 um, p.5; proposed:
  allow period_nm and a hole-radius geometry parameter on photodetector); (5) surface reflectance in % on photodetector
  (0.29 at 2 um, p.6; back_reflection_db candidate D436).

## zeng2019 (5 components, 20 metrics)

- `apd_3t_gap300` (photodetector.apd, soi): breakdown -6 V; responsivity 0.48 A/W at 1550 nm, unit gain at 2 V
  (author_estimate: coupling-loss removal not stated); gain about 15 near breakdown; dark current about 10 uA and 43 A/cm2
  at 5.4 V (derived unit conversions); 3-dB bandwidth 18.9 GHz at 6.4 V plus two Fig. 4(d) reads; Table 1 Rs 5 ohm, Cd
  57.8 fF, Ca 30 fF (S11 fit); Ge 4 x 10 um x 400 nm, 220 nm SOI, 3 um BOX.
- `apd_3t_gap200` / `gap400` / `gap600` / `gap800`: breakdown 4 V (text) and 7.7 / 11.5 / 11.8 V (Fig. 4(b) reads).
- Not entered: eye diagrams 25 / 30 / 35 Gb/s; OMA sensitivity -11.4 dBm (KP4, 25 Gb/s) and -7.8 dBm (BER 1e-12);
  Table 1 resistive / inductive / parasitic elements; simulated field; drawn finger gaps 200-800 nm and finger widths
  300-700 nm (gap_nm not allowed on photodetector; width_nm avoided because the ge_pd layout reads it as the waveguide
  width).
- Orgs: fab empty (passive "was fabricated", no org; all authors at Hewlett Packard Labs, D80b). No facility.
- Judgment calls: breakdown sign as printed (-6 V in the abstract, 4 V in the text); Table 1 / S11 data taken as the
  nominal-gap device (the paper studies mainly nominal 300 nm devices); gain bias 6.4 V read off Fig. 4(a).
- Registry gaps: (1) `gap_nm` on photodetector (drawn P-N finger gap 200-800 nm, p.4-5, Fig. 4(b); proposed: allow
  gap_nm for the lateral multiplication / junction gap of a photodetector); (2) `rx_sensitivity_dbm` (-11.4 dBm OMA at
  25 Gb/s, KP4 FEC, p.5; D436 candidate); (3) `data_rate_gbps` (35 Gb/s open eye, p.5; D534 candidate).

## Missing fab / facility orgs

None: every org named for fabrication or facility use is in the registry (`org_nanolab_tu_e`, `org_columbia_university`,
`org_advanced_science_research_center_nanofabrication_facility`, `org_columbia_nano_initiative`, `org_astar_ime`,
`org_nanyang_technological_university`).
