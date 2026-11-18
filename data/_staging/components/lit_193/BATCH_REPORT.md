# lit_193 batch report

Papers: `lit:zhang2022c`, `lit:koscica2025`, `lit:su2023`, `lit:libsch2006`, `lit:feng2024` (D646 half B, family B).
All five cached copies match their source rows (page-1 titles); `garbled_text_layer` false on all; IEEE download stamps
ignored. Figure values checked on page renders and 300 dpi crops of the PDFs (zhang2022c Fig. 3, 5, 6, 7; koscica2025
Fig. 3, 7; su2023 Fig. 7 + Table I; feng2024 Fig. 2). verified_on 2026-11-18.

Dry run: `merge_component_staging.py data/_staging/components/lit_193 --dry-run` -> +25 components, +114 metrics,
0 errors (the one WARN is on an existing ni2025b row, not this batch).

## Components / metric rows

### lit:zhang2022c (Optics Express 2022, InP DBR laser with SOA for FMCW LiDAR): 4 components / 30 metrics

| component_id | class | metrics |
|---|---|---|
| cmp_lit_zhang2022c_dbr_soa_laser | laser.dbr | 17: threshold 23.5 mA, series resistance 6 ohm, 96 mW at gain 200 / SOA 400 mA (chip, Ge detector), SMSR 53 dB, Lorentzian linewidth 313 kHz (as Hz, derived), tuning range ~2.8 nm, cavity mode spacing 0.29 nm and supermode spacing 10.5 nm (fsr_nm, condition names which), lasing ~1559.3 nm (Fig. 7(a) read), simulated SSC-output divergence 22 / 22 deg, total length 3650 um and footprint (derived), gain / SOA / phase section lengths, 3-4.5 um tapered ridge |
| cmp_lit_zhang2022c_front_mirror_uniform_grating | reflector.bragg | 3: simulated peak reflectivity 27 %, length 38 um, etch 40 nm |
| cmp_lit_zhang2022c_back_mirror_sampled_grating | reflector.bragg | 4: simulated peak reflectivity 80 %, length ~980 um, 31 burst periods, etch 40 nm |
| cmp_lit_zhang2022c_ssc | fiber_chip_coupler.edge | 6: coupling efficiency 64 % (2.5 um lensed fiber) and 44 % (5 um), length 210 um, etch 200 nm, core 300 -> 100 nm |

Fab `org_huazhong_university_of_science_and_technology` on the SSC row only (first-person "we fabricated a spot size
converter", abstract p.1; all authors HUST). No facility named.

### lit:koscica2025 (JLT 2025, in-pocket QD DBR lasers on AIM silicon photonics): 11 components / 38 metrics

| component_id | class | metrics |
|---|---|---|
| cmp_lit_koscica2025_sin_waveguide | waveguide_platform.straight | 3: 0.075 dB/cm (spiral cutback), 1200 nm width, 220 nm SiN |
| cmp_lit_koscica2025_sin_edge_coupler | fiber_chip_coupler.edge | 2: 3.6 dB per coupler (linear test structures), 100 nm tip |
| cmp_lit_koscica2025_laser_sin_coupling_1layer | waveguide_platform.transition | 4: coupling loss 5.4 dB (derived: sphere vs fiber LI minus 3.6 dB and waveguide loss), 3.7 um input width, 75 um taper, 220 nm |
| cmp_lit_koscica2025_laser_sin_coupling_dualcore | waveguide_platform.transition | 7: simulated mode overlaps 90.1 % (2.8 um input, 4 um ridge) and 94.9 % (5.8 um, 6 um ridge), two 220 nm SiN layers 100 nm apart, 75 um tapers, 89 deg III-V facet sidewall (FIB-SEM) |
| cmp_lit_koscica2025_fp_laser_5qd_air | laser.other | 3: T0 49 K (Fig. 3 inset label), 6 um ridge, 4 mm |
| cmp_lit_koscica2025_fp_laser_7qd_air | laser.other | 3: T0 87 K, 6 um ridge, 4 mm |
| cmp_lit_koscica2025_fp_laser_cleaved | laser.other | 3: mean initial threshold ~125 mA (derived, 250 mA aging current "approximately twice"), 6.5 um ridge, 2 mm |
| cmp_lit_koscica2025_dbr_laser_simple | laser.dbr | 4: SMSR 26 dB at 500 mA, 1307 nm, Lorentzian 6.04 MHz (as Hz), 4 mm gain |
| cmp_lit_koscica2025_dbr_laser_ring | laser.dbr | 4: SMSR 32 dB at 300 mA, 1299 nm, Lorentzian 5.67 MHz (as Hz), 4 mm gain |
| cmp_lit_koscica2025_sin_dbr_801 | reflector.bragg | 3: total reflectivity 87 % (author_estimate, origin not stated), 801 periods, 220 nm |
| cmp_lit_koscica2025_si_rings_x4 | resonator.ring | 2: FSR 1100 GHz (printed 1.1 THz) and loaded Q 30.5 k, both author_estimate (origin not stated) |

Fab `org_aim_photonics` on the 6 silicon photonics rows (waveguide, edge coupler, both transitions, DBR, rings; p.2
"fabricated on a 300 mm SOI wafer at the AIM Photonics foundry"), process_name "AIM Photonics foundry, 300 mm SOI
wafer". Laser rows fab empty. Facility `org_ucsb_nanofabrication_facility` on every row (p.8 "A portion of this work was
performed in the UCSB Nanofabrication Facility", D604).

### lit:su2023 (JLT 2023, SIL laser with adjustable Sagnac feedback): 7 components / 35 metrics

| component_id | class | metrics |
|---|---|---|
| cmp_lit_su2023_sil_laser | laser.sil | 16: intrinsic linewidth 390 / 142 / 60 / 100 Hz and integral (1 ms) 63.8 / 28.6 / 15.4 / 40.1 kHz (as Hz, derived) at ASLR reflectivity 0 / 0.11 / 0.32 / 0.46; fiber output 7.7 / 7.0 / 6.0 / 5.1 dBm (Table I); SMSR 59 dB; PER > 20 dB; 1557.65 nm; RIN < -150 dB/Hz (100 kHz-100 MHz) |
| cmp_lit_su2023_dfb_chip | laser.dfb | 4: bare-chip ~40 mW at 220 mA (author_estimate), free-running intrinsic 122.5 kHz and integral 137.3 kHz (as Hz), length 1000 um (specification) |
| cmp_lit_su2023_sin_mrr | resonator.ring | 11: FSR 9.37 GHz, FWHM ~369 MHz, Q_L 5.2e5 (derived from the FWHM), fitted loss 0.15 dB/cm and kappa^2 9 % (derived, ring_extraction), drop IL ~2.1 dB (derived from the fit), heater tuning ~0.937 pm/mW, perimeter 14970 um, 1000 x 800 nm, heater 2700 um |
| cmp_lit_su2023_aslr | reflector.loop_mirror | 1: reflection extinction ~35 dB over the MZI heater sweep |
| cmp_lit_su2023_dfb_to_sin_butt | chip_chip_coupler.butt | 1: ~2.5 dB per interface (author_estimate, method not stated) |
| cmp_lit_su2023_output_ssc_fiber | fiber_chip_coupler.edge | 1: ~3 dB per coupler to the PM fiber array (author_estimate) |
| cmp_lit_su2023_sin_waveguide | waveguide_platform.straight | 1: < 0.2 dB/cm (author_estimate, stated with the process, no measurement shown) |

Fab `org_ligentec` with process_name "Ligentec AN800 standard MPW process" on the 4 Si3N4-chip rows (MRR, ASLR, output
SSC, waveguide; p.2). SIL laser and butt interface fab empty (hybrid assembly, assembler not named, D450). DFB vendor
missing from the registry (below). No facility (ZhangJiang Laboratory thanked for funding and equipment support only).

### lit:libsch2006 (ECTC 2006, MCM LGA package with optical I/O to dual-layer polymer waveguides in PCB): 2 components / 7 metrics

| component_id | class | metrics |
|---|---|---|
| cmp_lit_libsch2006_dual_lens_coupler | micro_optics.other | 3: lens coupling < 1.0 dB Tx and Rx (Table 1, best components, per_interface), collimated beam ~150-200 um (author_estimate) |
| cmp_lit_libsch2006_pwg_45deg_mirror | micro_optics.vertical_taper | 4: mirror coupling < 0.5 dB Tx and Rx (Table 1), 250 um pitch, 2 x 12 channels |

Fab empty (no fabrication statement naming an org; authors at three orgs). Platform empty on the lens row (free-space
path, D422); `polymer` on the mirror row.

### lit:feng2024 (SiPhotonics 2024, 2-page conference paper, in-pocket QD lasers to foundry SiN): 1 component / 4 metrics

| component_id | class | metrics |
|---|---|---|
| cmp_lit_feng2024_qd_laser_etched_facet | laser.other | 4: threshold ~370 mA (Fig. 2(a) kink, +/-20 mA), ~10.7 mW at 1000 mA (integrating sphere), ~0.010 mW fiber-coupled at 900 mA (Fig. 2(b)), lasing 1250-1300 nm (text) |

Facility `org_ucsb_nanofabrication_facility` (p.1 "for fabrication at the UCSB Nanofab facility"); fab empty.

## Values not entered and why

- zhang2022c: residual sweep nonlinearity 0.026 % / 0.02 % of the 24 GHz excursion, RMS 6.17 / 4.88 MHz (p.7, p.10; no
  parameter, registry gap); distance resolution 9.24 mm, velocity 253.3 mm/s (system results); simulated design FSR
  0.3 nm and supermode spacing 10.5 nm (p.3; the measured values are entered); SSC taper loss < 0.2 dB (p.3, cites ref.
  [25], rule 3); laser without SSC (Fig. 5(d), no printed value; simulated 26 / 44 deg divergence in a note); grating
  duty cycle 0.5 (p.3, SEM Fig. 4(b)): "the grating" is not tied to the front or back mirror (D159), in the reflector
  notes; SOA has no isolated performance value (its effect is in the 96 mW row), so no SOA row; monitor PD and phase
  section: no values; 7 deg SOA tilt (no parameter, laser note).
- koscica2025: Fig. 7 population coupling losses (gap size, facet angle, air vs BCB; medians and hero points) not read
  (mixed device types, unlabelled points); the BCB vs air differences 7.0 / 7.3 dB and simulated "up to 40 %" (relative);
  >= 3 dB cleaved vs etched-facet slope-efficiency penalty (relative); maximum lasing temperatures 60 / 105 / 90 C,
  injection efficiency 28.1 %, internal loss 2.82 cm-1, lifetime 6.2 years / mean 2.3 years, TDD 3.0e7 cm-2 (no
  parameters; component notes); PL peaks 1298 nm / FWHM 42 and 37 meV (material, not a component); integrated FP lasing
  range 1285-1315 nm (stated for the family, D254; notes); SiN DBR spectral width 298 GHz (no reflector GHz width,
  definition not stated; registry gap); BCB index 1.56 (cited ref. [38]); prior-work coupling losses > 10 dB and 7.35 dB
  (p.1, cited); excited-state switch ~650 mA and mode hops 20-40 C (notes).
- su2023: locking range 1.6 / 2.2 / 6.3 / 5.4 GHz (no parameter; registry gap); monitor-port powers (Table I, monitor);
  overall loss ~10.3 dB (path total); feedback spectrum IL ~4.2 dB (calculated with R = 1 assumed); model values (K,
  k ~0.4, Q_LD 3e3, alpha_g 5, eta^2 ~1926); ASLR tuning power 11-120 mW (reflector has no tuning_power_mw, D430);
  ASLR "near 0 to 1" reflection ratio (normalized, Fig. 4(b)); Q "up to 10^7" and feedback thresholds in the
  introduction (cited); phase-shifter lengths 750 / 550 um (no metric of their own; 550 um in the ASLR label).
- libsch2006: PWG losses 0.04 dB/cm (850 nm) / 0.12 dB/cm (980 nm) (p.1, cite ref. [12], rule 3); 0.5 dB at +/-50 um
  carrier offset (0.5-dB tolerance not a parameter, D81); placement statistics Table 2 and ~20 re-insertions (assembly
  figures); link total "< 3.0 dB + PWG"; "309-mm" vertical pitch (unit misprint, not corrected); electrical S21 / eye /
  TDR results (not optical components); purchased VCSEL / PD arrays (not characterized as devices).
- feng2024: laser-to-SiN coupling loss (not stated; not computed from the two LI curves); ridge length (not stated);
  pocket 35 um x 3 mm x 6 um (pocket, not a component dimension; in core_material).

## Missing fab / facility orgs (name as printed + locator)

- "Shijia Photons Technology Co., Ltd." (vendor of the purchased DFB, fab role on `cmp_lit_su2023_dfb_chip`), lit:su2023
  p.2 Sec. II-A.
- "NAsPIII/V GmbH" / "NAsPIII-VGmbH" (GaP seed / template MOCVD growth; film step, note only, no fab role),
  lit:koscica2025 p.2 and p.8, lit:feng2024 p.1. Listed for the org round only if the owner wants growth houses.

## Judgment calls

- (a) zhang2022c fab: HUST only on the SSC row (the first-person sentence names the SSC); laser and mirror rows fab
  empty although they share the same monolithic process (Contract v7 per-component fab).
- (b) zhang2022c SSC 64 % / 44 %: `measured`, `per_facet`, `direct` (D167; the paper says "calculated" from fiber and
  Ge-detector powers, no arithmetic shown).
- (c) koscica2025 dual-core input coupler: one row for the 2.8-5.8 um family with the two simulated overlaps as
  conditions (widths vary by device design; no sibling row has measured values).
- (d) koscica2025 / feng2024 laser platform `iii_v_on_si_epi` for the in-pocket lasers, including the DBR lasers whose
  mirrors are SiN / Si (wei2023 precedent); laser-to-SiN couplings `waveguide_platform.transition` with platform
  `other` (monolithic, same die; wei2023 precedent).
- (e) su2023 coupling losses 2.5 / 3 dB `author_estimate` (method not stated; D418 / D617 butt-coupling precedents)
  rather than D167 `measured`.
- (f) feng2024 / koscica2025 laser rows: facility UCSB Nanofab, fab empty (D634 / D82c: the facility owner is not made
  fab; no first-person fabrication statement naming an org).
- (g) koscica2025 cleaved-laser threshold ~125 mA entered as `derived` mean from "aging current ... approximately twice
  the initial threshold current of the average device" (250 / 2).
- (h) koscica2025 SiN DBR 87 % and Si ring FSR / Q `author_estimate` (stated as device properties, origin not stated).
- (i) feng2024 lasing range entered from the text (1250-1300 nm) with the conflicting Fig. 2(c) peak reads (~1233-1252
  nm) in notes (D417).
- (j) libsch2006 Table 1 values: qualifier `lt` + statistic `best` (header "best components fabricated", text "measured
  maximum optical loss from good components"); lens coupling scope `per_interface` (module-to-board), mirror
  `per_component`; band unspecified (VCSEL wavelength not stated in this paper).

## Registry gaps (skipped value + locator + proposed definition)

- `locking_range_ghz` (laser): su2023 1.6 / 2.2 / 6.3 / 5.4 GHz, p.7 Fig. 8. "Self-injection / injection locking range
  in frequency at the stated feedback setting."
- `chirp_nonlinearity_pct` (laser; D431 candidate): zhang2022c 0.026 % / 0.02 % of a 24 GHz excursion, p.7 / p.10.
- `bw_3db_ghz` or a frequency width for reflector: koscica2025 SiN DBR "spectral width of 298 GHz", p.6 (width level
  not stated).
- `max_operating_temperature_k` (laser; D431 candidate): koscica2025 60 / 105 C (Fig. 3) and 90 C with BCB (p.6).
- `internal_loss_per_cm` and `internal_efficiency_pct` (laser; D431 candidates): koscica2025 2.82 cm-1 and 28.1 %, p.4.
- `tuning_power_mw` for reflector (D430 candidate): su2023 ASLR 11-120 mW for reflectivity ~0 -> 1, p.3 Fig. 4(b).
