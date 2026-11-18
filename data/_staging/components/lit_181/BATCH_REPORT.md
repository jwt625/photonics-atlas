# lit_181 batch report

Papers: lit:kiewiet2025, lit:weng2021, lit:pfeifle2014, lit:wang2018d, lit:xue2017. verified_on 2026-11-18.
All five cached texts are arXiv copies whose page-1 titles match their source rows; none is a correction. They are
preprints / author versions of the listed journal papers (kiewiet2025 v1 2025-04-23 of LPOR; weng2021 v2
2021-02-20 of Nat. Commun.; pfeifle2014 v3 2014-02-22 of Nat. Photon.; wang2018d of Optica; xue2017 of LPOR):
values are what the cached copy reports; journal versions unread. Dry-run: +28 components, +100 metrics, 0 errors
(the one WARN printed is for merged row cmp_lit_ni2025b_pimmwc, not this batch).

## lit:kiewiet2025 (micro-transfer printed CW / mode-locked lasers at 800 nm on SiN)

Components 9 / metric rows 35:

| component | metrics | content |
|---|---|---|
| fp_coupon | 8 | FP coupon printed on a bare Si test substrate: Ith 48 mA, > 70 mW at 150 mA, 0.66 W/A, WPE > 20 % (derived), 796 nm, ~2.1 V at 150 mA (figure), 1 mm, 2 um ridge |
| rsoa_coupon | 4 | internal gain > 30 dB and 15 nm width above 20 dB (both derived: 6 dB fiber coupling removed), 1 mm, 2 um |
| butt_coupler_imec | 6 | simulated coupling 96 % (overlap), 86 % (max FDTD), > 50 % (within tolerances), 92 % (no reflection); 3000 nm / 60 nm facet section |
| butt_coupler_ebl | 5 | simulated overlap 84 %; 3700 nm x 300 nm SiN, BOX 3.3 um, 2 um top clad |
| shallow_taper | 3 | 0.92 dB per taper at 790 nm (taper-number cutback, Supp. Fig. S3) |
| sagnac_mirror | 1 | 75 % reflection (author_estimate, origin not stated) |
| mll_3p2ghz | 4 | 3.2 GHz, 525 lines in the 10-dB band, centre ~798.6 nm (figure), 51 fs pulse-to-pulse jitter (derived) |
| mll_7p5ghz | 1 | 7.5 GHz (EBL platform) |
| mll_9p2ghz | 3 | 9.2 GHz, Ith 46.9 mA (Fig. 4(b) legend), > 4 mW waveguide-coupled CW (derived) |

Not entered and why:
- Fundamental RF Lorentzian linewidth 519 Hz, RF extinction ~50 dB, pulse energies 0.16 pJ (3.2 GHz) / 0.27 pJ
  (7.5 GHz), 10-dB optical bandwidth 3.5 nm / 1.7 THz, threshold current density 2.4 kA/cm2: no registry parameter
  (gaps below).
- Text "threshold of 48 mA or 2.4 kA/cm2" for "a fully-integrated butt-coupled extended-cavity laser" (p.5): names
  no device and repeats the coupon numbers of p.4; Fig. 4(b) prints 46.9 mA for the 9.2 GHz laser. Only the legend
  value is entered (D159 / D417), conflict in notes.
- Facet distance (< 500 nm in the FIB cross-section, minimum ~450 nm from the ~85 deg recess-etch angle, p.3): the
  platform of the Fig. 1(d)-(f) sample is not stated, so not entered on either coupler row (D159); in notes.
- Simulated facet reflections (-12 dB at 0 deg, -70 dB at 7 deg into the RSOA mode; 6 % for the FP facet): no
  amplifier / laser facet parameter; in notes.
- Grating coupler (output of all lasers): insertion loss "extracted with a cut-back structure" but not printed; no
  row. Low-loss SiN spiral: no loss or length printed; no row.
- Projections (50 mW waveguide-coupled power, 3 pJ pulses, > 15 nm Vernier tuning): not results.
- Supp. Figs. S7-S9 (mode-locking maps, FP-mode L-I of all three lasers, RF / optical spectra) have no page renders;
  only the stated values are used.

Fab / facility: org_imec on the imec-platform rows (3.2 and 9.2 GHz lasers, imec butt coupler, shallow taper):
"made on the imec 200 mm SiN platform" (p.5) and the imec co-authors "provided the wafer" (p.9), the kiewiet2026 /
D455 construction. Coupons and the EBL platform: fab empty (dual Ghent University - imec / imec affiliations,
passive "in-house" wording; D433 / D395, kiewiet2026 precedent). No missing orgs.

Judgment calls:
- FP coupon on a bare Si test substrate is `laser.other` (heterogeneous subtype is "on a PIC"); platform `gaas` for
  both coupons; assembled lasers and the III-V/SiN couplers `other` (kiewiet2026 precedent).
- Shallow-etch taper within one SiN layer: `waveguide_platform.other` (xiao2022 precedent, D417).
- Sagnac mirror used on both platforms: fab empty.
- Mode-locked lasers: `laser.comb`, `repetition_rate_ghz` (pulse train characterized, D83b); CW Fabry-Perot mode
  values are operating conditions on the same rows.
- 3.2 GHz 525-line spectrum: text ties it to 85 mA, the Fig. 4(e) caption to 90 mA (D417 note).
- "> 4 mW" waveguide-coupled output assigned to the 9.2 GHz laser: the sentence names no device, but Fig. 4(b) is
  the only extended-cavity L-I shown and reaches ~4.3 mW. Auditor may prefer notes-only (D159).

## lit:weng2021 (gain-switched laser driven soliton microcombs)

Components 6 / metric rows 18:

| component | metrics | content |
|---|---|---|
| si3n4_ring | 2 | loaded linewidth ~20 MHz, loaded Q ~1e7 (derived) |
| si3n4_soliton_comb | 4 | frep 9.716 GHz (locked to fgs); demonstrated average pump power 8 / 40 / 10 mW (DFB / FP subharmonic / chirped DM GSL) as `pump_threshold_mw` le |
| edge_coupler | 1 | 3 dB lensed-fibre-to-waveguide loss per facet (D167) |
| dfb_laser | 4 | SMSR ~55 dB (derived: DM 62 dB minus 7 dB), ~10 ps pulses (derived, Gaussian assumed), ~1546.3 nm (figure), 1 mW average GSL power |
| fp_laser | 2 | 175 GHz mode spacing, 4 mW gain-switched output |
| dm_laser | 5 | 165 GHz mode spacing, SMSR ~62 dB, 13 mW at 120 mA, ~2 nm temperature tuning (author_estimate), ~1548.0 nm (figure) |

Not entered and why:
- MgF2 whispering-gallery resonator and its comb (diamond-shaped polished crystalline rod, Q ~1e9): out of scope,
  bulk crystal (D411).
- Dispersion D2 = 2 pi x 15 kHz (Si3N4, measured) and 2 pi x 2 kHz (MgF2): no registry parameter.
- Si3N4 "X-band frep (~10 GHz)" sentence carries ref. [26] (D80i).
- Gain-switching bandwidths (DFB up to 20 GHz, FP effective 7 GHz, DM up to 14 GHz): no parameter (not a 3-dB
  modulation bandwidth).
- DFB side modes ~250 GHz from the lasing mode: stopband side modes, not a cavity mode spacing (fsr definition).
- Comb span (~1530-1570 nm in Fig. 2(d)): no parameter; 100 % deterministic excitation and > 20 MHz soliton steps:
  no parameter. Simulation parameters (rate equations, LLE): generic, not tied to a device.

Fab / facility: org_epfl on the Si3N4 rows ("J. L. designed and fabricated the silicon nitride resonator", p.9;
J. L. at EPFL only; D395), process_name "Photonic Damascene Process" (printed). No facility named.
Missing orgs (vendors of purchased devices under test, fab role; rows left empty):
- "NTT Electronics" (Methods p.8; DFB laser manufacturer) - not in organizations.csv / org_aliases.csv (org_ntt is
  the parent group; no alias exists).
- "Eblana Photonics" (Methods p.8; FP and DM laser vendor).

Judgment calls:
- The three commercial packaged lasers are the gain-switched sources under study, kept as device-under-test rows
  (D155, vines2019 precedent), not setup equipment; platform empty (D422).
- `pump_threshold_mw` with qualifier `le`: the paper calls the demonstrated average pump power "the power
  threshold"; no lower failing power is printed, so the stored value is an upper bound; ref_plane fiber with the
  on-chip value (~4 / ~20 / ~5 mW) in condition. Auditor may prefer condition-only.
- One comb row for the three pump sources (same ring, rule 9 operating points).

## lit:pfeifle2014 (coherent terabit communications with Kerr combs)

Components 5 / metric rows 11:

| component | metrics | content |
|---|---|---|
| ring_17ghz | 5 | FSR 17 GHz, loaded Q 8e5, 2 um x 750 nm, sidewall 78 deg (derived from 12 deg off vertical) |
| ring_25ghz | 1 | loaded Q 2e6 |
| comb_17ghz | 2 | line spacing 17 GHz (RF beat), 6 data lines |
| comb_25ghz | 2 | line spacing 25 GHz (< 6 MHz off design), 20 data lines |
| edge_coupler | 1 | ~3 dB per facet (D167) |

Not entered and why: on-chip pump powers 33 / 29 dBm ("needed for Kerr comb generation", not a threshold
measurement) are conditions; 1.35 mm bend radius is only the mode-solver radius; ring 2 geometry (Methods states
2 um x 750 nm without naming the device, Fig. 2 is experiment 1) entered on ring_17ghz only; design FSR 25 GHz kept
in notes (measured spacing on the comb row); comb power stability < 1 % over 3 h, data rate, EVM, BER, OCN0R, DI /
waveshaper extinction (setup or system metrics); the 50 uW toroid threshold is cited (ref. [2]).

Fab / facility: "Samples have been fabricated at the EPFL Center for Micro- and Nanotechnology (CMI)" (p.6) ->
fab org_epfl + facility org_center_of_micronanotechnology on all rows (D448). No missing orgs.

## lit:wang2018d (monolithic QD DFB laser array on Si)

Components 4 / metric rows 22:

| component | metrics | content |
|---|---|---|
| dfb_array | 8 | 6 lasers, 20 nm spacing, peak wavelengths ~1240-1340 nm and periods 188.8-207.3 nm (Fig. 5(b)), > 0.5 mW CW / > 1.5 mW pulsed per facet, 2.2 um ridge, 50:50 grating |
| dfb_1mm | 6 | Ith 12 mA, 0.024 W/A and 0.5 % WPE at 49 mA, ~20 ohm slope resistance, ~0.45 mW at 50 mA (figure), 1000 um |
| dfb_1p2mm | 3 | kappa ~41.7 /cm (author_estimate from kappa L ~5, infinite-grating assumption), defect mode ~1321.1 nm (figure), 1200 um |
| dfb_fig6 | 5 | SMSR ~50 dB at 60 mA, 8.6 pm/mW self-heating, 1.2 nm shift to 60 mA, 110 pm/K (derived), ~50 K/W (derived) |

Not entered and why: threshold current density 550 A/cm2 and current tuning 0.03 nm/mA (no parameters; D83g);
FDTD output-coupler values (reflectivity ~1 % vs ~10 %, output efficiency ~82 %, absorption 7 %): no laser facet
parameter; 0.8 nm stopband (no laser stopband parameter); 2.2 um x 1.5 mm two-mode DFB (17 nm TE10-TE00
spacing vs 15.5 nm simulated): no parameter; 3.4 um grating etch depth is from an SEM of a previous test run
(Fig. 2(c)); PL, TD density, QD density (material). Supplement 1 (array LIV, etch-depth study, methods) is not cached.

Fab / facility: empty. "fabricated into broad-area FP lasers ... and the DFB laser array" is passive and the
authors span Sun Yat-sen University, UCL, Bristol and Sheffield; growth site not stated (D80b). No facility named.

Judgment calls: four rows (array, 1 mm Fig. 5(d) device, 1.2 mm Fig. 5(c) device, Fig. 6 device). The Fig. 5(c)
device (~1321 nm) and the Fig. 6 device (~1300 nm) emit on different channels, so they are separate; the Fig. 6
device length is not printed (2.3 kA/cm2 at 60 mA implies ~1.2 mm; not entered). The "> 0.5 / > 1.5 mW per facet"
sentence names no device and Fig. 5(d) ends at ~0.45 mW, so it sits on the array row.

## lit:xue2017 (high-efficiency dark-pulse Kerr combs)

Components 4 / metric rows 14:

| component | metrics | content |
|---|---|---|
| ring1 | 4 | R 100 um, FSR ~231 GHz (author_estimate: "corresponding to" the radius, method not stated), loaded Q 7.7e5, ~4.7 dB dip |
| ring1_comb | 5 | 31.8 % pump-to-comb efficiency, 209 mW on-chip comb power, 40 lines (1513-1586 nm), 7 dBm mean per line, 23 dB line-power spread (derived) |
| ring2 | 2 | loaded Q 8.6e5, ~8.5 dB dip |
| ring2_comb | 3 | 5.2 % through port, 10.6 % overall (derived), 24 mW through-port comb power |

Not entered and why: effective hot-cavity detunings / widths (119 / 336 MHz, 46 / 270 MHz; comb-state quantities);
OSNR > 40 dB (no parameter); pump power drops (4.5 / 5 dB); Fig. 2 simulations (generic parameters, no device);
ring geometry (not printed). Both rings were used in the authors' earlier paper (ref. [8]); the value sentences carry
no citation and ring 2 uses a different resonance, so values are entered (D408), with a note.

Fab / facility: empty (no fabrication statement; Birck Nanotechnology Center is an affiliation only). No missing orgs.

## Registry gaps (skipped value, locator, proposed definition)

| parameter (proposed) | class | skipped values | definition |
|---|---|---|---|
| rf_linewidth_hz | laser | kiewiet2025 519 Hz (p.6, Fig. 4(i)) | Lorentzian / -3 dB width of the fundamental RF beat of a mode-locked laser or comb (fit type in condition) |
| pulse_energy_pj | laser | kiewiet2025 0.16 / 0.27 pJ (p.5) | average output power / repetition rate as stated (reference plane in ref_plane) |
| bw_10db_nm on laser | laser | kiewiet2025 3.5 nm (p.5, Fig. 4(e)) | allow the existing bw_10db_nm for comb / mode-locked laser spectra |
| threshold_current_density_a_per_cm2 | laser | kiewiet2025 2.4 kA/cm2 (p.4); wang2018d 550 A/cm2 (p.4) | threshold current per pumped area (D431 / D433 candidate) |
| dispersion_d2_khz | resonator | weng2021 D2/2pi 15 kHz Si3N4 (p.8) | second-order dispersion coefficient D2 / 2 pi as reported |
| comb_span_nm | laser | weng2021 Fig. 2(d) ~1530-1570 nm (figure only); xue2017 1513-1586 nm (in condition) | spectral span of a comb at the stated level (D418 candidate) |
| facet_reflectivity_pct | laser, amplifier | wang2018d ~1 % / ~10 % FDTD (p.4); kiewiet2025 6 % FP facet, -12 / -70 dB RSOA facet (p.3-4, Supp. Fig. S6) | power reflectivity of a laser / SOA facet into the guided mode |
| osnr_db | laser | xue2017 > 40 dB (p.3) | optical signal-to-noise ratio of comb lines (reference bandwidth in condition; D440 candidate) |
| current_tuning_pm_per_ma | laser | wang2018d 0.03 nm/mA (p.5) | static wavelength shift per mA of drive current (D418 candidate) |
