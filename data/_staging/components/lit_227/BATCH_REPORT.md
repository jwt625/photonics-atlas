# lit_227 batch report

Papers: lit:fujita1999, lit:wang1998, lit:byun2009, lit:zirngibl1996 (all laser papers). Page-1 titles match the
source rows; no correction / erratum; `garbled_text_layer` false for all four (garbled equation / table text read from
the page renders). verified_on 2026-11-20. Dry run of `merge_component_staging.py`: +18 components, +72 metrics,
0 errors; the one warning names the merged row cmp_lit_ni2025b_pimmwc, not in this batch.

| paper | components | metric rows |
|---|---|---|
| fujita1999 | 5 | 24 |
| wang1998 | 4 | 15 |
| byun2009 | 4 | 12 |
| zirngibl1996 | 5 | 21 |

## fujita1999 (GaInAsP-InP microdisk injection lasers, IEEE JSTQE 1999)

Rows (fab org_yokohama_national_university on all 5):
- `laser.other` 3 um disk: CW threshold 150 uA at 298 K (stored 0.15 mA, derived); pulsed 3 um devices from Fig. 12 as
  condition rows (with chamber cleaning 0.31-0.41 mA, without 0.73-0.98 mA, extracted, +/-10 %); simulated 20-80 uA
  (ideal disk, w = 0.8 um, D = 1-8 cm2/s, Fig. 7(b)); lasing near 1.63 um (1630 nm approx, derived); thermal
  resistance 1.5e5 K/W (author_estimate: rests on the typical 0.1 nm/K); radius 1.5 um (derived); sidewall angle 80 deg
  (SEM, measured).
- `resonator.disk` same 3 um disk (D396 / D400): below-threshold FWHM 0.5 nm (lasing mode) / 0.7 nm (nonlasing mode) as
  `linewidth_pm` 500 / 700 (derived); Q 3300 / 2300 as `q_loaded` (authors' lambda / dlambda arithmetic, derived);
  total cavity loss 30 cm-1 -> 130.3 dB/cm (author_estimate, index not printed; power coefficient per tau_p = n_eq /
  (c alpha), p.4); doublet interval 0.6 nm -> `mode_splitting_ghz` 67.7 approx (derived); radius.
- `laser.other` 2 / 5 / 8 um sibling disks: pulsed thresholds read off Fig. 12 (2 um ~0.20 mA; 5 um 0.90-1.41 mA without
  and ~0.69 mA with chamber cleaning; 8 um ~2.6 mA); 2 um simulated 8-20 uA (Fig. 7(a), w = 0.4 um); 5 um thermal
  resistance ~7e4 K/W read off Fig. 14 (author_estimate, agrees with the printed fit 7.9e5 K um^1.5/W); radii.

Not entered:
- Threshold current density 2.1 kA/cm2 and effective 0.86 / 0.22 kA/cm2 per well (p.6; no parameter, registry gap).
- Spontaneous emission factor 6e-3 (p.8, fit of Fig. 15; no parameter) and the calculated 0.31 / 0.75 projections.
- Red shift 12 nm/mA (Fig. 13; static current tuning in nm/mA, D83g).
- Total scattering loss 25 cm-1 (30 cm-1 minus the 5 cm-1 broad-area absorption, loss-breakdown term; in notes).
- Critical pulsed / CW thresholds 130 / 340 uA (assumed T0 = 40 K); calculated mode intervals 110 nm / 10 nm; sidewall
  roughness 8.5 / 0.88 nm (no parameter); simulated internal differential QE 50 / 80 / 95 % (no laser parameter);
  FDTD Q ~1600 and post scattering > 5 cm-1 (Fig. 5; cell-size-limited model, no fabricated counterpart);
  Table II model inputs; optimum exposed disk width 0.6-0.7 um (design, no parameter).

Fab / facility: first-person process statements (p.2, p.6 Sec. III), all authors at Yokohama National University ->
fab. Acknowledgment thanks persons at Furukawa Electric and Elionix for help with the experiment: staff thanks, not
entered (D84b / D72). No facility.

## wang1998 (2.2 um InAs-InGaAs-InP highly strained MQW lasers, IEEE JQE 1998)

Rows (laser.other, inp, fab empty, all pulsed 5 us / 500 Hz, RT, as-cleaved facets):
- 50 um x 1000 um: threshold 450 mA (measured); length / stripe width (design_target as printed in Fig. 5 caption).
- 50 um x 800 um: threshold ~500 mA (Fig. 5 read); lasing near 2.2 um (2200 nm approx, derived); FP mode spacing 8 A
  as `fsr_nm` 0.8 (derived); geometry.
- 50 um x 600 um: threshold ~550 mA (Fig. 5 read); geometry.
- 40 um x 800 um (Fig. 5 inset): output > 60 mW per facet (gt, best, detector-saturation limited); threshold ~550 mA
  (inset read); geometry.

Not entered:
- Threshold current density 900 A/cm2 and maximum external quantum efficiency 28 % (p.1, p.3; no laser parameter).
- Fig. 5 end-of-sweep powers of the 50 um devices (about 9.5 / 10 / 5.8 mW; sweep ends, not maxima).
- PL peak 0.57 eV / FWHM 43 meV (RT, laser wafer) and the 9 K PL / X-ray data (material characterization, Figs. 1-4).

Fab / facility: empty. "were fabricated" / "was grown" are passive; abstract "We report the fabrication" and
"demonstrated a successful growth" judged not enough under D80b (see judgment call 3). All authors at National Taiwan
University (org_national_taiwan_university exists). No facility (acknowledgment thanks one person for the detector).

## byun2009 (integrated 394 MHz femtosecond Er waveguide laser, IEEE PTL 2009)

Rows (fab empty):
- `laser.comb` mode-locked laser (platform other: Er aluminosilicate + P-doped silica): repetition rate 394 MHz
  (0.394 GHz derived); pulse 440 fs (autocorrelation, measured; Fig. 4(e) label 438 fs); transform-limited 300 fs
  (derived, Table II footnote, D84c); simulated 310 fs; timing jitter 24 fs (integration upper limit printed as 20 MHz in
  Sec. IV and 10 MHz in Sec. I / Fig. 4(f), condition says so); average output 1.2 mW at 400 mW pump (ref_plane
  unspecified); mode-locking threshold 160 mW pump as `pump_threshold_mw` (ofc2026 Th1F.6 precedent); spectrum peak
  ~1557 nm (Fig. 4(a) read); chip footprint 18 x 44 mm (derived).
- `amplifier.rare_earth` Er-doped straight test waveguide (separate chip): peak gain 1.8 dB/cm at 1532 nm (pump level
  240 mW assigned from Fig. 3).
- `waveguide_platform.straight` same test waveguide (D396): pump absorption 0.4 dB/cm at 976 nm (D575 precedent).
- `waveguide_platform.transition` Er-to-P-doped mode converter: < 0.15 dB (author_estimate, origin not stated; C band
  inferred).

Not entered:
- Optical spectrum FWHM 8.4 nm measured / 8.6 nm simulated (Table II; `bw_fwhm_nm` not allowed for laser and FWHM not
  equated with 3 dB) -> registry gap.
- RF sidemode suppression 80 dB (Fig. 4(c)); intracavity power 12 mW and pulse energy 30 pJ; post-EDFA 7.4 nm / 340 fs
  (setup amplifier); loop-mirror 10 % output coupling (no output-coupling parameter; 90 % reflectivity would assume a
  lossless mirror); SBR modulation depth 14 %, recovery 2 ps, saturation fluence 25 uJ/cm2, +1000 fs2 (purchased
  mirror, vendor not named, no parameters); Table I indices, Aeff, beta2 and n2 (model inputs; dispersion rejected D81);
  Er section 5 cm and silica section 20 cm (in core_material; `length_um` would be ambiguous for a two-section cavity).

Fab / facility: empty. Fabrication sentences passive with no org (process cited to ref. [17]); authors at MIT and
CyOptics (org ids exist / not needed). No facility.

## zirngibl1996 (18-channel multifrequency laser, IEEE PTL 1996)

Rows (fab org_lucent_bell_labs, borderline, on all 5):
- `laser.other` MFL: 18 channels lasing CW (measured) and 24 designed (design_target); channel spacing 103 GHz
  (measured); CW thresholds 82 mA total uncooled and 63 mA at 11 C TE cooler; fiber power -2 dBm total and -14.6 dBm
  per channel (derived, authors' arithmetic); next-passband side modes suppressed >= 20 dB (`smsr_db`, ge); longitudinal
  mode spacing 1.7 GHz as `fsr_ghz` (author_estimate, method not stated); lasing around 1515 nm; chip 9 x 18 mm2
  footprint (derived); 1 um active stripe.
- `wdm.awg` intracavity WGR: 24 channels; design spacing 100 GHz and FSR 2400 GHz (author_estimate, D82a); filter FWHM
  35 GHz (`bw_fwhm_ghz`, author_estimate, origin not stated); multiplexer IL about 10 dB (author_estimate,
  loss_breakdown, S band inferred).
- `waveguide_platform.straight` processed passive waveguide ~4 dB/cm and reference unprocessed waveguide 1 dB/cm
  (measured, method unspecified, S band inferred).
- `laser.other` 1 mm uncoated FP bar from the amplifier material (test structure): 20 mW per facet at 200 mA; length.

Not entered:
- FP-bar threshold current density printed "1200 kA/cm2" (implausible unit, likely a misprint) and differential QE 26 %
  (no laser parameter).
- SNR 30 dB, 1.24 Gb/s direct modulation with 3 dB ER, channel-spacing reproducibility < 1 GHz wafer to wafer, 1.7 dB
  ASE ripple of the active-passive transition (no parameters; transition loss only "small").
- FSR > 1850 GHz / bandwidth < 50 GHz design criteria (based on the authors' ref. [3], rule 3 / D259).

Fab / facility: see judgment call 4. No facility.

## Missing fab / facility orgs

None. Registry ids used: org_yokohama_national_university, org_lucent_bell_labs (time-correct 1996 Lucent
Technologies, Bell Labs Innovations; ghosh1996 precedent).

## Judgment calls for the auditor

1. fujita1999: pulsed 3 um thresholds (Fig. 12) and the simulated 20-80 uA (ideal disk) are condition rows on the 3 um
   CW row (same design, D32 / D80e); the 2 / 5 / 8 um disks are sibling rows from Fig. 12 points alone.
2. fujita1999 resonator row: 30 cm-1 total cavity loss converted to 130.3 dB/cm (power coefficient, author_estimate) and
   the 0.6 nm doublet converted to 67.7 GHz `mode_splitting_ghz` (derived, approx); both could instead stay in notes.
3. wang1998: Fig. 6 spectrum (wavelength, 8 A mode spacing) assigned to the 50 um x 800 um device by the 500 mA = Ith
   caption vs the Fig. 5 thresholds (alternative under D159: notes only). Fab left empty despite the abstract's "We
   report the fabrication".
4. zirngibl1996: fab org_lucent_bell_labs from "We have previously reported on the MFL fabrication [6]" (D84a
   analogue) plus all authors at Lucent Bell Labs; strict D80b reading would leave it empty.
5. byun2009: laser platform `other` (two glass stacks) and Er test waveguide `glass` (aluminosilicate, n 1.60, ghosh1996
   precedent); transition `other`. Mode-locking threshold as `pump_threshold_mw`.
6. zirngibl1996: 1.7 GHz mode spacing and 35 GHz WGR FWHM author_estimate (origin not stated, D76) while the stated
   waveguide losses are measured (results paragraph that calls for separate measurements; D167 analogue).

## Registry gaps (value skipped + locator + proposed definition)

- `threshold_current_density_a_per_cm2` (laser): wang1998 900 A/cm2 (p.3), fujita1999 2.1 kA/cm2 (p.6), zirngibl1996
  printed 1200 kA/cm2 (p.2). Def: threshold current per pumped area as printed (area assumption in condition). Earlier
  candidate (D431).
- `differential_quantum_efficiency_pct` (laser): wang1998 28 % maximum external (p.1, p.3), zirngibl1996 26 % (p.2).
  Def: external differential quantum efficiency (both facets or per facet in condition); internal efficiency separate.
- `spontaneous_emission_factor` (laser, unit 1): fujita1999 6e-3 (p.8, fit of Fig. 15). Def: fraction of spontaneous
  emission coupled into the lasing mode, extraction method in notes.
- `bw_fwhm_nm` allowed for laser: byun2009 8.4 nm measured / 8.6 nm simulated output-spectrum FWHM (p.3 Table II).
- `rf_sidemode_suppression_db` (laser.comb): byun2009 80 dB (p.2, Fig. 4(c)). Def: suppression of RF supermode /
  spurious tones relative to the repetition-rate tone, span / RBW in condition.
- `pulse_energy_pj` (laser): byun2009 30 pJ intracavity (p.2). Earlier registry candidate (DevLog-007 audit lists).
- `output_coupling_pct` (reflector, laser): byun2009 loop mirror 10 % (p.2). Def: power fraction coupled out of the
  cavity by the stated mirror.
