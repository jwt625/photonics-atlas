# lit_286 batch report

Distilled 2026-11-25. Papers: lit:wang2013, lit:jiang2018a, lit:liu2017a (all Optics Express, Bragg / contra-DC
filter family; selected as benchmark-table citations). Page-1 titles match the source rows; no correction / erratum;
no garbled text layer (liu2017a p.6 text layer is column-interleaved and was read from the page render). Total
37 components / 158 metric rows. `merge_component_staging.py --dry-run`: 0 errors (2 warnings belong to other
batches: guo2024a, ni2025b).

## lit:wang2013 (32 components / 114 metrics)

Silicon slot-waveguide Bragg gratings, imec passive SOI via ePIXfab (UBC).

- 14 uniform gratings `cmp_lit_wang2013_ubg_wg{1,2}_{in,out}{10..40}` (reflector.bragg, soi_slot), one per Table 1
  design (WG1: slot 150 nm, period 420 nm, inside 10 / 20 nm, outside 10-40 nm; WG2: slot 200 nm, period 430 nm,
  inside and outside 10-40 nm): stop-band width read off Fig. 9 (`stopband_width_nm`, level not stated, log axis
  +/-5 %); WG1 inside-20 nm entered as > 20 nm from the text ("more than 20 nm", marker at the top frame, ~24 nm);
  extinction > 40 dB for WG1 outside-10 nm (Fig. 7 raw spectrum) and about 40 dB for the five other WG1 gratings
  (Fig. 8, "all the devices exhibit"); period, 1000 periods, arm width 270 nm (design).
- 16 phase-shifted gratings `cmp_lit_wang2013_psbg_wg*_n{100..500}` (resonator.bragg, soi_slot), one per N (rule 9):
  Q from the text for WG1 outside-40 N = 200 (800) and N = 500 (1.55e4), WG2 inside-40 N = 500 (about 3e4); the other
  12 read off Fig. 11(b) (log axis, +/-10 %). Unqualified Q -> `q_loaded`; c_band inferred (design Bragg wavelength
  close to 1550 nm, Fig. 11(a)). N per side and arm width as geometry.
- `cmp_lit_wang2013_slot_wg1` (waveguide_platform.straight): simulated group index 3.35 at 1550 nm, arm width, 220 nm.
- `cmp_lit_wang2013_y_branch` (splitter.y_branch, soi_strip): ~3 dB extra loss of the reflection path attributed to
  the Y-branch, `author_estimate` (assumes full grating reflection; it is the nominal split, excess not stated).
- Not entered: intrinsic Q 5.89e4 and critically coupled Q 2.95e4 (p.6, computed from an assumed 10 dB/cm loss taken
  from cited work, rule 3); strip Bragg-grating Q 1e5, strip grating sensor Q 27600 / 59 nm/RIU, earlier slot-grating
  sensor results 340 nm/RIU, Q 1.5e4, LOD 3e-4 RIU (p.3 / p.10, authors' earlier papers refs. [13], [16], [28], D259);
  slot-ring values of other groups (p.3); FDTD spectrum of WG1 outside-40 N = 50 (Fig. 4(c), no number stated besides
  the 1550 nm peak); calculated neff 1.85 / 1.80 (no parameter; in core_material); WG1 outside-40 N = 100 Q (no blue
  marker visible in Fig. 11(b), D156); centre wavelength "about 1550 nm" of the Fig. 7 grating (center_wavelength_nm not
  allowed for reflector); slot width and corrugation width (no reflector / resonator parameter, in core_material);
  mode converter (5 um coupling length "to ensure that the coupling loss is negligible", cited refs. [32-34], no
  value); grating couplers (no value); BOX 2 um / 220 nm layer on the grating rows (in core_material; no layout
  template for Bragg classes).
- Fab: "we designed and fabricated our devices using the imec standard passive silicon photonic technology, accessed
  through the ePIXfab foundry service" (p.3 Sec. 2) -> `org_imec`; CMC Microsystems "for enabling the fabrication of the
  devices through ePIXfab" (p.11 Acknowledgments) -> `org_cmc_microsystems` (D398, zhang2015a precedent).
  process_name "imec standard passive silicon photonic technology accessed through ePIXfab, 193 nm optical
  lithography, 200 mm SOI".
- Missing orgs: **ePIXfab** (fab / MPW access, p.3 Sec. 2 and p.11 Acknowledgments; already in the org-round backlog);
  **Centre for High-Throughput Phenogenomics at the University of British Columbia** (facility, "assistance with SEM
  imaging", p.11 Acknowledgments; borderline facility per D80c, SEM imaging only, parent org_university_of_british_columbia).

## lit:jiang2018a (2 components / 23 metrics)

Loop bandwidth-tunable filter of two multimode anti-symmetric waveguide Bragg gratings (MASWBG) with adiabatic
couplers and Ti/W heaters, 220 nm SOI (Zhejiang University).

- `cmp_lit_jiang2018a_loop_maswbg_filter` (wdm.bragg_cdc, soi, fabricated): drop-port 3-dB bandwidth 13 nm (0 V) and
  1.0 nm (13 V on one heater); SLSR > 30 dB / 18 dB at those states; IL < 2 dB drop and through (normalized to a GC
  pair, `per_component`, wavelength inferred from Fig. 4 / Fig. 6 spans); through-port pass/stop contrast ~23 dB;
  centre-wavelength tuning > 13 nm (Fig. 7: 1575 to 1589 nm); tuning efficiencies 50 pm/mW (bandwidth tuning, printed
  ~20 mW/nm, derived) and 25 pm/mW (wavelength tuning, printed ~40 mW/nm, author_estimate); geometry (1100 nm width,
  300 nm period, 500 um grating, ADC 150 um / 200 nm gap, 175 nm Ti/W heater, 220 nm / 3 um BOX / 2 um cladding).
- `cmp_lit_jiang2018a_single_maswbg_sim` (design): FDTD single filter 3-dB bandwidth 14 nm, SLSR ~20 dB, period 296 nm,
  width 1.1 um (simulated period differs from the fabricated 300 nm).
- Not entered: bandwidth tuning range "about 12 nm (1.455 THz)" / "over 1.455 THz" (no parameter; registry gap);
  passband ripple < 0.5 dB (p.8; registry gap); heater resistance 650 ohm (p.7; `heater_resistance_ohm` not allowed for
  wdm; registry gap); heater "sheet resistance" printed as 1.2 uOhm m (a resistivity unit, p.5; no parameter); corrugation
  width "delta = 0.25" (unit not printed in Sec. 3; 0.25 um "grating teeth" in the simulation); THz forms of the
  bandwidths (kept in conditions; nm values printed); ADC and Heater3 phase shifter (geometry only / no values).
- Fab: "fabricated using electron-beam lithography on a standard commercial SOI wafer" (p.5), passive, no org named:
  fab empty (D80b). No facility acknowledgment. No missing org.

## lit:liu2017a (3 components / 21 metrics)

Apodized subwavelength-grating contra-directional coupler bandpass filter, 220 nm SOI (Shanghai Jiao Tong University).

- `cmp_lit_liu2017a_cdc_a5_gmin230` (wdm.bragg_cdc, soi, fabricated): SLSR 27 dB at 12-nm detuning (measured), 3-dB
  bandwidth 8.8 nm and IL 2.5 dB (abstract; tied to the 27 dB device), geometry (Gmin 230 nm, Lc 100.3 um, SWG period
  378 nm / 50 %, N 300, 500 nm widths, footprint ~113 x 2 um2 = 226 um2 derived, 220 nm / 3 um BOX / 1 um cladding).
- `cmp_lit_liu2017a_cdc_a5_gmin200` (fabricated; Fig. 2(a) simulated design and Fig. 4 blue curve): simulated IL ~1.8 dB
  (a = 5); geometry.
- `cmp_lit_liu2017a_cdc_a7_gmin200_design` (design): simulated IL ~2.6 dB (a = 7).
- Not entered: uniform SWG contra-DC (a = 0, fabricated) sidelobe levels ~-4.5 dB at 10 nm / -7.5 dB at 22 nm
  (measured) and -5.1 dB at 6.8 nm / -8.3 dB at 12 nm (simulated) - absolute normalized levels, not SLSR (registry
  gap), so the uniform device has no row; Gmin 170 nm device (Fig. 4 green, no stated value; not read off the noisy
  curve); "other sidelobes below -30 dB", "rest sidelobes below -45 dB" (absolute levels); sidelobe improvement ~23.4 dB
  and ~4 dB (relative); simulated reflection < -18 / -27 dB (no wdm reflection parameter); "3-dB bandwidth ~10 nm from
  the simulation" (p.4, uniform vs apodized design ambiguous, D159, in notes); 20 dB of the authors' earlier conference
  paper (ref. [31], D259); apodized Bragg contra-DC 30 dB / 829.4 um (ref. [21], cited). Centre wavelength not stated:
  IL rows `band: unspecified`.
- Fab: "were fabricated on a silicon-on-insulator (SOI) wafer" (p.5), passive: fab empty (D80b). Facility
  `org_center_for_advanced_electronic_materials_and_devices` ("support of device fabrication by the Center for Advanced
  Electronic Materials and Devices of Shanghai Jiao Tong University", p.6 Acknowledgments; cai2021 / hu2020 precedent).
- Journal extension of the authors' conference paper (ref. [31]): its own values kept.

## Judgment calls for the auditor

1. wang2013 granularity: one row per design and per N (rule 9) -> 30 grating rows, 12 Q values and 13 stop-band widths
   read off log-axis figures (Fig. 11(b), Fig. 9).
2. wang2013 "about 40 dB" for all WG1 uniform gratings (Fig. 8) entered on each of the five WG1 rows as `approx`
   (stated per device "all the devices exhibit"), not treated as a D254 family typical.
3. wang2013 Fig. 9 "bandwidth" -> `stopband_width_nm` with "level not stated" (the ~60 nm stopband precedent, D717),
   not `bw_3db_nm`.
4. wang2013 Y-branch ~3 dB kept as `insertion_loss_db` `author_estimate`; delete if the auditor judges a nominal split
   attribution not a component value.
5. wang2013 Q rows c_band inferred (no per-device resonance wavelength); polarization te from the TE grating couplers.
6. jiang2018a bandwidth-tuning efficiency (printed mW/nm of bandwidth change) stored as `tuning_efficiency_pm_per_mw`
   50 pm/mW, reading the bandwidth change as the stop-band edge shift of the one heated grating; the wavelength-tuning
   40 mW/nm `author_estimate` (doubling argument) vs the bandwidth-tuning 20 mW/nm `derived` (650 ohm, 0-13 V, ~12 nm).
7. jiang2018a / liu2017a platform `soi` (etch depth not stated; D422 / D423 not `soi_strip`).
8. jiang2018a IL wavelengths `wavelength_inferred` from the plotted passband (Fig. 4, 1568-1581 nm) and through-port span
   (Fig. 6, 1560-1590 nm).
9. liu2017a abstract-only values (8.8 nm, 2.5 dB) assigned to the Gmin 230 nm device via the shared 27 dB SLSR sentence.

## Registry gaps (proposed)

- `bw_tuning_range_nm` (wdm): span of the tunable passband width, jiang2018a "about 12 nm (1.455 THz)" p.6 Sec. 3.
- `ripple_db` (wdm, splitter): in-band passband ripple, jiang2018a "less than 0.5 dB" p.8 Sec. 4.
- `heater_resistance_ohm` widened to wdm / resonator: jiang2018a 650 ohm, p.7 Sec. 3.
- `sidelobe_level_db` (wdm, reflector): highest sidelobe level of a normalized response, positive dB below the reference
  (as distinct from SLSR relative to the main lobe): liu2017a uniform contra-DC ~4.5 / 7.5 dB measured, p.6 Sec. 4.
- `center_wavelength_nm` widened to reflector: wang2013 uniform grating "about 1550 nm", p.8 Sec. 3.1.
- `corrugation_width_nm` (reflector, resonator, wdm, laser): sidewall-grating corrugation depth, wang2013 Table 1
  (10-40 nm), jiang2018a.
