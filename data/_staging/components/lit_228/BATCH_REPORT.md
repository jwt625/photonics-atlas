# lit_228 batch report

Papers: lit:sato2008, lit:alloush2021, lit:mason2000, lit:gopinath2007, lit:staring1996. Page-1 titles match the
source rows (alloush2021 has no page_01.png render; text page 1 carries the title). No `garbled_text_layer` flags.
verified_on 2026-11-20. Dry run of `merge_component_staging.py`: +17 components, +113 metrics, 0 errors; the one
warning names the merged row cmp_lit_ni2025b_pimmwc, not in this batch. Fab orgs: only sato2008 (org_ntt).

| paper | components | metric rows |
|---|---|---|
| sato2008 | 2 | 15 |
| alloush2021 | 1 | 13 |
| mason2000 | 4 | 25 |
| gopinath2007 | 5 | 31 |
| staring1996 | 5 | 29 |

## sato2008 (MOVPE InAs/InGaAs MQW on InP, 2 um broad-area lasers, JSTQE 2008)

Rows: two `laser.other` broad-area FP lasers (three 3 nm vs three 5 nm InAs wells; 40 um x 900 um stripe, uncoated,
CW): threshold current derived from the printed Jth (1.49 / 1.58 kA/cm2 x 40 um x 900 um = 536.4 / 568.8 mA, D431;
the Fig. 9(a) 25 C knee reads about 540 mA at 600 dpi); maximum output power > 12 mW at 25 C (both), > 6 mW at 50 C
(5 nm); T0 38 / 51 K (15-40 C) and 17 / 34 K (above 40 C) from the authors' fit (measured); thermal drift 1050 /
1400 pm/K (derived from nm/K); stripe width, cavity length.

Not entered:
- Lasing peaks 2.050 / 2.320 um (p.4, Fig. 8): the value sentence cites the authors' own Electron. Lett. 2007 paper [12]
  (D259 / D408); the conclusion and the abstract bound (> 2.3 um) restate it without a citation, and Fig. 11 plots the
  same wavelengths. Kept out under the strict reading; see judgment call 1.
- Jth 1.49 / 1.58 kA/cm2 itself (registry gap: threshold current density; stored as derived threshold_ma).
- PL peaks, XRD, AFM, annealing results (material, not component).

Fab: org_ntt on both rows ("we fabricated 40-um-wide stripe broad-area lasers", p.3 Sec. IV; all five authors at NTT
Photonics Laboratories, NTT Corporation; rule 12 first person, one org). Missing alias: "NTT Photonics Laboratories"
-> org_ntt (p.1 affiliation footnote). No facility.

Conflict (D417): 3 nm laser tuning rate printed +1.05 nm/K in the text (p.5) vs +1.01 nm/K on the Fig. 11 label;
text value kept, both in notes.

## alloush2021 (sub-GHz InP monolithic mode-locked laser, PTL 2021)

Row: one `laser.comb` (D83b: pulses characterized) InP extended-cavity MLL with two MIRs, 40.5 mm folded cavity:
repetition rate 0.946 GHz PML (Table I prints GHz, measured) and 0.88-0.99 GHz HML range (derived); pulse-to-pulse
RMS jitter 3.65 ps (computed from the Lorentzian RF linewidth, derived; kiewiet2025 precedent), integrated jitter
23.63 ps PML (1-8 MHz), 550 / 600 fs HML at 880 / 990 MHz (20-100 kHz, measured); pulse widths ~500 ps PML,
200 / 335 ps HML (ps -> fs, derived); lengths 40.5 mm cavity, 1.5 mm gain, 50 um absorber; 4.5 x 1 mm footprint.
Conditions: 17 C holder, 143 mA gain, absorber -3.7 V.

Not entered: RF beat-note linewidth 70.75 kHz PML (Table I 70 kHz) and < 1 Hz HML (registry gap: RF linewidth of an
MLL); RF power transmission to the on-chip PD (-11 / -16 dB; electrical PCB / bond-wire network); Table I columns for
refs. [2], [3], [2] (rule 3). MIRs, booster SOA and on-chip PD have no optical metric (no rows). Optical spectrum inset
(Fig. 2) not read (small inset; title states 1550 nm).

Fab empty: "The laser chip is fabricated" (passive, no org); co-author at SMART Photonics is an affiliation only. No
facility. Cross-note: similar to merged cmp_lit_guzman2017_ec_mll_1ghz (the authors' ref. [3]) but a different chip.

## mason2000 (SGDBR laser with integrated SOA, PTL 2000)

Rows:
- `laser.tunable` SGDBR + SOA (54 nm design): quasicontinuous tuning > 50 nm (measured) and 54 nm design
  (author_estimate); SMSR > 35 dB over the range and 46 dB at ~8 dB SOA gain (Fig. 5); peak output > +8 dBm
  (ref_plane unspecified); nominal mirror peak spacings 5.5 / 5.0 nm (fsr_nm, author_estimate, lee2022 precedent);
  kappa 300 cm-1 (+/- 30 printed, origin not stated, author_estimate; value from the page render, the text layer drops
  it); 350 nm waveguide layer.
- `amplifier.soa` integrated SOA (600 um): peak gain 8.5 dB at 100 mA, 1550 nm (calculated with unprinted waveguide
  losses, author_estimate); output saturation ~6 mW at 150 mA -> 7.78 dBm (derived; Fig. 4 marks the 1 dB compression
  point).
- `fiber_chip_coupler.edge` curved, flared output guide to the 7.125 deg AR-coated facet (andreou2019 precedent):
  ~2 dB added propagation loss (author_estimate, per_component); calculated effective reflectivity < 2.5e-5 ->
  back_reflection_db > 46.0 (simulated, D83f); 300 um length, 2 um width, ~6 um flared facet width (tip_width_nm).
- `laser.tunable` SGDBR without SOA (90 nm design): 72 nm tuning 1502-1574 nm (measured), 90 nm design, peak
  spacings 7.5 / 7.0 nm design, threshold 20 mA, 2 mW at 100 mA, mirror lengths 476 / 740 um.

Not entered: transparency current 5.2-14.3 mA and calculated unity-gain current 14 mA (no parameter); Fig. 4 legend
gains 3.8 / 7.1 / 8.5 dB (legend not tied to the 25 / 50 / 150 mA curves unambiguously, D156); 40 dB power-control
range; ~6 dB power variation over tuning (general statement); facet angle (no parameter, D250); effective reflectivity
< 1e-4 (general statement); tuning currents (notes).

Fab empty: no fabrication statement naming authors or an org; authors at Agility Communications and UCSB (D80b).

## gopinath2007 (980 nm passively mode-locked SCOWLs, PTL 2007)

Rows: five `laser.comb` rows, one per Table I device (A 3 mm / 0.3 mm absorber; B 5 / 0.3; C 10 / 0.3; D 10 / 0.5;
E 10 / 0.8), platform gaas: maximum average mode-locked power with drive current and absorber bias (Table I); device
length (mm -> um, derived); cross-section from the Fig. 1 caption on every row (w 5.8 um ridge, h 5.0 um waveguide,
t 4.4 um slab; D558 practice for a shared printed cross-section). Device B adds threshold 440 mA, slope efficiency
0.73 W/A, free-running 975 nm, repetition rate 7.92 GHz, pulse width 16 ps (derived to fs). Device E adds the
mode-locked wavelength range 973-985 nm.

Not entered: pulse energy 62 pJ (registry gap: pulse energy, already a candidate in D429 / D433); spectral width
0.96 nm (no laser spectral-width parameter); near-field mode size 4.8 x 3.9 um (device not named, definition not
printed; D159, notes); M2 values of Device A (no parameter); locking ranges 600-1600 mA / 0.3-1.2 V and the Fig. 4
stability map (notes); facet coatings 95 % / 8 % (no reflectivity parameter on laser; notes). Values in the
introduction from refs. [6]-[14] (rule 3).

Fab empty: passive fabrication section; acknowledgment thanks P. O'Brien and J. Wilson for laser fabrication
assistance without naming their org; all authors at MIT Lincoln Laboratory (D80b, D543). See judgment call 3.

## staring1996 (nine-channel PHASAR multiwavelength laser, PTL 1996)

Rows:
- `laser.other` nine-channel multiwavelength laser: threshold 101-122 mA over the 8 addressable channels (16 C);
  fiber-coupled power 0.09-0.37 mW (lensed SMF); SMSR > 15 dB (channels 1-6); linewidth 21 MHz (derived to Hz);
  longitudinal-mode spacing ~0.06 nm (channel 4, fsr_nm); nominal 400 GHz grid (author_estimate); 9 channels; ~6 mm
  cavity; 500 um gain sections; 3.5 x 2.5 mm2 footprint; 2.5 um ridge.
- `wdm.awg` 11x1 PHASAR (in-cavity): design spacing 400 GHz, FSR 38.75 nm, centre 1550 nm, angular insertion loss
  2 dB by design (il_nonuniformity_db, author_estimate), 50 arms, 11 / 1 ports, 500 um minimum bend radius.
- `waveguide_platform.straight` passive ridge: 20 dB/cm from Fabry-Perot contrast on straight waveguides (measured,
  D394; "estimated" quoted; facet reflectance not printed; 1550 nm inferred) and the ridge cross-section.
- Two `laser.other` reference FP array elements: 500 um gain section alone 38 mA at 20 C ("uniformly", typical); with
  a 500 um passive section 45 mA.

Not entered: PHASAR fiber-to-fiber IL 24.7 dB, crosstalk < -20 dB and 3-dB width 1.7 nm (device with gain sections
cleaved off): the sentence cites [7], the authors' IPR 1996 paper with nearly the same title (D259 / D408); see
judgment call 2. Per-channel thresholds of Fig. 5 (range row covers them); 1.2 dB butt-joint gain ripple (no
parameter); adjacent-order emission 20 / 35 dB below the peaks.

Fab empty: passive fabrication sentences; coating thanks to a named person without an org; authors at Philips
Optoelectronics Centre and Delft University of Technology (D80b, D543).

## Judgment calls for the auditor

1. sato2008 lasing wavelengths (2.050 / 2.320 um) left out because the only value sentence cites the authors' own
   Electron. Lett. 2007 paper [12] (D259 / D408 sentence clause), although Fig. 8 / Fig. 11 plot them without a
   citation and the abstract / conclusion repeat them. Alternative: enter them as measured (this invited paper
   re-presents the spectra). The Jth, T0, power and tuning-rate sentences carry no citation and are entered.
2. staring1996 PHASAR measured IL / crosstalk / 3-dB width left out under D408 because the sentence ends with [7] (the
   authors' own conference version of this work). If the auditor reads [7] as the conference version that this letter
   extends (D408 keep clause), three rows can be added on cmp_lit_staring1996_phasar_11x1 (fiber_to_fiber IL 24.7 dB,
   crosstalk_db 20 gt, bw_3db_nm 1.7, all p.2 Sec. IV).
3. Fab empty on gopinath2007 (staff thanked for laser fabrication assistance, their org not printed; every author at
   MIT Lincoln Laboratory) and staring1996 (coating thanks). D84b would give org_mit_lincoln_laboratory as a borderline
   fab only if the staff's org were printed.
4. sato2008 threshold_ma derived from Jth x stripe area (D431) assumes the paper normalized by 40 um x 900 um; the
   Fig. 9(a) knee supports it for the 3 nm laser (about 540 vs 536 mA).
5. mason2000 curved output guide typed `fiber_chip_coupler.edge` (andreou2019 precedent) with insertion_loss_db
   per_component for the 2 dB added propagation loss (no fiber coupling reported); alternative waveguide_platform.bend,
   which does not allow back_reflection_db.
6. gopinath2007 Fig. 1 cross-section (w / h / t) entered on all five device rows (caption: "a typical" device);
   alloush2021 and gopinath2007 typed `laser.comb` (mode-locked lasers, guzman2017 / liu2019b precedent).

## Registry gaps (skipped value + locator + proposed definition)

- threshold_current_density_ka_per_cm2 (laser): sato2008 1.49 / 1.58 kA/cm2 at 25 C (p.4 Sec. IV); "threshold
  current per pumped area as printed (area definition in notes)". Already a candidate (D431, D433, D677, D678).
- rf_linewidth_hz (laser): alloush2021 70.75 kHz PML (p.3 Sec. III, Fig. 2), < 1 Hz HML (Table I); "3-dB width of the
  fundamental RF beat tone of a mode-locked laser (fit in condition)". Candidate since D431.
- pulse_energy_pj (laser): gopinath2007 62 pJ (p.2 Sec. III, abstract); "average power / repetition rate as printed".
  Candidate since D429 / D433.
- laser spectral width (FWHM of a mode-locked spectrum): gopinath2007 0.96 nm (p.2 Sec. III).
- beam quality M2 (laser): gopinath2007 Device A 1.4 x 1.93 CW, 1.16 / 1.61 mode-locked (p.3).
- transparency current / unity-gain current (amplifier): mason2000 5.2-14.3 mA, 14 mA (p.2-3 Sec. III).
- facet angle (fiber_chip_coupler): mason2000 7.125 deg (p.2 Sec. II); rejected before (D250), listed for the count.

## Missing orgs / aliases

- Alias "NTT Photonics Laboratories" (also "NTT Photonics Laboratories, Nippon Telegraph and Telephone (NTT)
  Corporation") -> org_ntt; sato2008 p.1 affiliation footnote; fab role (rows already set to org_ntt).
- No other fab / facility org is needed by a row.
