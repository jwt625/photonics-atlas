# lit_317 batch report

Batch lit_317: lit:hulme2015, lit:guan2018, lit:suh2018a, lit:huang2019d (papers cited in other papers' benchmark tables;
only values each paper reports itself are entered). Distilled 2026-11-28 (verified_on). Totals: 22 components, 69 metric
rows. Validation: `merge_component_staging.py data/_staging/components/lit_317 --dry-run` -> +22 components, +69
metrics, errors 0 (the two warnings it prints are on merged guo2024a / ni2025b rows, not this batch).

Page-1 title check: all four match their source rows. hulme2015 (Opt. Express 23(5) 5861) and guan2018 (Opt. Express
26(7) 7920) are Optica open-access publisher copies. suh2018a is arXiv 1801.05174v1 (2018-01-16), "Searching for
Exoplanets Using a Microresonator Astrocomb", of the Nature Photonics paper; huang2019d is arXiv 1901.07112v1
(2019-01-21), "Thermo-refractive noise in silicon nitride microresonators", of the Phys. Rev. A paper. Both preprints:
values from the preprint only, journal versions unread (noted on every component of the two papers). None is a
correction or erratum; no garbled text layer.

## lit:hulme2015 (fully integrated hybrid Si 2D beam scanner): 8 components, 34 metrics

| component | class | metrics |
|---|---|---|
| cmp_lit_hulme2015_grating_emitter | free_space_emitter.grating_emitter | 11: 0.127 deg/nm measured; theta steering 4.4 deg (laser tuning) and 3.6 deg (2D demo); theta beam width 0.6 deg; period 550 nm, width 2.3 um, grating etch 50 nm, rib etch 275 nm, Si 500 nm, BOX 1 um, slab 225 nm (derived) |
| cmp_lit_hulme2015_opa_uniform | free_space_emitter.other | 5: simulated SMSR 5.4 dB (0 deg) / 0.5 dB (10 deg); 32 channels, 4 um pitch, 126 um width |
| cmp_lit_hulme2015_opa_gaussian | free_space_emitter.other | 6: simulated SMSR 13.9 / 8.2 dB; 32 channels, 3.4 / 7.1 um pitch, 144 um width |
| cmp_lit_hulme2015_laser_1gain | laser.tunable | 2: threshold 94 mA; gain region 1.4 mm |
| cmp_lit_hulme2015_laser_2gain | laser.tunable | 2: threshold 168 mA; gain region 0.8 mm |
| cmp_lit_hulme2015_pin_phase_tuner | phase_shifter.other | 2: 160 mW/pi (MZ test structure, thermo-optic regime); 3-dB bandwidth > 300 kHz |
| cmp_lit_hulme2015_pin_phase_tuner_testrun | phase_shifter.other | 1: > 50 MHz (derived to kHz), run without III-V bonding |
| cmp_lit_hulme2015_pd_470um | photodetector.iii_v_on_platform | 5: mean 0.57 A/W and 45 % QE at -5 V; Fig. 12 spectral ranges 0.54-0.70 A/W and 42-57 % (1505-1605 nm, figure read); length 470 um |

Not entered:
- Psi-axis results of the 2D steering demo (23 deg steering, 1 deg beam width, > 70 % background suppression = 5.5 dB in
  the conclusion, 138 resolvable spots; p.13 Sec. 6.4, p.14 Sec. 7): the paper fabricated both a uniform and a
  Gaussian-spacing array (p.5) and never says which one the measured PIC carries. D159: in the notes of both array rows.
  Theta-axis values are on the grating_emitter row because both arrays use the same emitter (p.5).
- Laser tuning 34.5 nm and 0.28 nm/mW (p.9, Fig. 10): printed for "the laser" while the PIC carries one laser of each
  design (p.4); D159, in both laser-row notes. Angle tuning 0.034 deg/mW measured / 0.030 predicted: no parameter and
  laser not named.
- 41 nm tuning and 5.5 mW of the earlier laser design: values of the authors' ref. 12 (rule 3, D259).
- Design tuning 0.127 +/- 0.02 deg/nm over 1555-1605 nm: stated with ref. 13 (rule 3); the measured 0.127 deg/nm is entered.
- 14 mA/pi of the test-run modulators: no current-per-pi parameter (registry gap below).
- SOAs (1.5 mm pre-amplifier, 3 mm channel amplifiers, parasitic lasing at 200-400 mA from taper reflections, 93 %
  gain-element yield): geometry only, no performance parameter: not a row.
- GRIN (photonic-crystal) lens: calculated focal length 473 um, 64 um PD-feed width, expected 41 deg span / 1.3 deg
  resolution; the measurement failed (proximity-correction errors): no parameter / no measured value: not a row.
- Fig. 9 SEM labels (InP taper 19.1 um long, 510 nm tip; ring-to-bus coupler 0.90 um waveguide, 0.33 um gap): geometry
  only and not tied to one laser design (D159): notes only. MMI splitters (31): no values. Yields (97 % phase
  modulators, 100 % photodiodes): no parameter.
- Simulated main-lobe power fractions (53 / 46 % uniform, 48 / 45 % Gaussian): no parameter (array-row notes).

Judgment calls:
- Three-way split of the OPA: common grating-emitter row (theta axis) plus two array-design rows (psi-axis design values);
  the alternative is one as-measured PIC row carrying 23 x 3.6 deg (coordinator question 1).
- Theta beam width 0.6 deg put on the emitter row (set by the emitter, which both arrays share; emitter length not printed).
- p-i-n phase tuners as `phase_shifter.other` (aflatouni2015 precedent) although they ran thermo-optically on the PIC;
  the test-run device is its own row (same design, separate process run without III-V).
- PD averages "for the wavelengths available in the PIC": 1565-1600 nm inferred from the laser spectra of Fig. 10
  (wavelength_inferred, reason in notes).
- p_pi_mw with `band: unspecified` (no wavelength stated for the MZ test-structure measurement).
- process_name "hybrid silicon process (refs. 14, 15)" only on the III-V rows (lasers, PD); SOI-only rows left empty.

Missing fab / facility orgs: none. Fabrication is passive (p.7 Sec. 4), all authors at UCSB, no facility named; fab empty
on all rows (D80b).

## lit:guan2018 (III-V/Si hybrid Vernier external-cavity laser): 8 components, 27 metrics

| component | class | metrics |
|---|---|---|
| cmp_lit_guan2018_ecl | laser.tunable | 12: 11 mW max (plane not stated), WPE 4.2 % (on-chip), threshold 30 mA, tuning 60 nm (1515-1575), SMSR 55 dB best (~1553 nm read) / > 46 dB (1525-1575), linewidth 37 kHz best / < 80 kHz (7 wavelengths), RIN < -135 dB/Hz, simulated mode spacing ~0.18 nm; RSOA 600 um, ridge 1.9 um |
| cmp_lit_guan2018_rsoa_ssc_butt | chip_chip_coupler.butt | 5: 0.73 dB (active alignment), ~2.8 dB best (bonded); simulated 0.18 dB / 96 % mode match, 2.82 dB with a 2 um gap |
| cmp_lit_guan2018_ring_r1 | resonator.ring | 3: FSR 4.99 nm (author_estimate), Q 5500, R 20 um |
| cmp_lit_guan2018_ring_r2 | resonator.ring | 3: FSR 6.13 nm (author_estimate), Q 4800, R 16.3 um |
| cmp_lit_guan2018_wsr | reflector.other | 1: side-mode extinction > 8 dB over 1510-1570 nm (simulated, extracted model) |
| cmp_lit_guan2018_output_dc | splitter.directional_coupler | 1: 37 % to output (design statement) |
| cmp_lit_guan2018_mpd_tap | splitter.directional_coupler | 1: 2 % monitor tap (design statement) |
| cmp_lit_guan2018_output_edge_coupler | fiber_chip_coupler.edge | 1: MFD 5 um (author_estimate) |

Not entered:
- Q of the highest WSR reflection peak "about 8000" (p.6): q_loaded is not allowed on reflector rows (WSR notes).
- RSOA extracted waveguide loss 12 /cm (p.7): no laser internal-loss parameter (internal_loss_per_cm is an open
  registry candidate, D431).
- Simulated misalignment penalties (+1.2 dB for 0.5 um vertical, +0.5 dB for 0.5 um horizontal, Fig. 3): loss at a
  fixed offset, no parameter (tol_1db is the offset for 1 dB).
- Authors' split of the 2.8 dB (~2 dB gap, rest misalignment), "additional unaccounted loss 1.2 dB", total loss ~4 dB:
  estimates without a parameter.
- Mode hop 0.1 nm near 160 mA (Fig. 7(a)), tuning accuracy +/- 1.25 GHz (OSA-limited), coherent-link BER results
  (system level), Table 1 values of other works (rule 3).

Judgment calls:
- Intracavity rings R1 / R2 as `resonator.ring` (D400); the dual-ring + Y-junction WSR as `reflector.other` (fan2020
  feedback-arm precedent).
- 0.73 dB entered as per_interface measured: the sentence names "the SSC coupler" without the counterpart; the section is
  about RSOA-to-SSC coupling (noted).
- Ring FSRs author_estimate (measured vs extracted-model origin not stated, D76); ring Q values measured, wavelength
  1525-1575 nm inferred from the measured span.
- Linewidths `derived` (reference linewidth subtracted; kHz -> Hz); the wavelengths of the best SMSR / linewidth points
  and the 7-point linewidth span read off Fig. 10.
- DC split ratios and the 5 um MFD entered as author_estimate design statements; the edge coupler's platform left empty
  (facet layer not stated, D422).

Missing fab / facility orgs: none named. Si chip "fabricated at a CMOS foundry" and RSOA "built in a III-V foundry"
(p.7 Sec. 3), neither named; assembly passive. Fab empty on all rows. Authors at Columbia University and Elenion
Technologies (affiliation only; the affiliation-foundry rule lives in config, not here).

## lit:suh2018a (microresonator astrocomb; arXiv preprint): 2 components, 4 metrics

| component | class | metrics |
|---|---|---|
| cmp_lit_suh2018a_wedge_disk_3mm | resonator.disk | 2: unloaded Q ~3e8 (author_estimate, D403, C band inferred); R 1500 um (derived) |
| cmp_lit_suh2018a_soliton_comb_22ghz | laser.comb | 2: repetition rate ~22.1 GHz; pulse width 145 fs (sech2 fit, derived, D84c) |

Values from the arXiv preprint 1801.05174v1 only (journal version unread). Not entered: Allan deviation of the locked
frep/4 (~10 mHz at 1000 s), f0 standard deviation < 1 MHz, spectral span (~1525-1580 nm before HNLF broadening; no comb
span parameter, D81), NIRSPEC calibration precision (system level), pump power (not printed). D396: one physical disk,
two class rows with cross-notes. Judgment: the Q sentence describes this work's resonator (ref. 44 cited only for the
fabrication), kept as author_estimate (D408 attribution test, suh2016 precedent).

Missing fab / facility orgs: none. Fabrication passive with ref. 44 (fab empty); the Kavli Nanoscience Institute appears
only in the support list (D83e), the JPL / Caltech research statement is a contract statement.

## lit:huang2019d (thermo-refractive noise in Si3N4 microresonators; arXiv preprint): 4 components, 4 metrics

| component | class | metrics |
|---|---|---|
| cmp_lit_huang2019d_ring_fsr1thz | resonator.ring | 1: FSR 1000 GHz (printed 1 THz) |
| cmp_lit_huang2019d_ring_fsr99ghz | resonator.ring | 1: FSR 99 GHz |
| cmp_lit_huang2019d_ring_fsr88ghz | resonator.ring | 1: FSR 88 GHz |
| cmp_lit_huang2019d_ring_fsr20ghz | resonator.ring | 1: FSR 20 GHz |

Values from the arXiv preprint 1901.07112v1 only (journal version unread). FSRs are author_estimate (used as device
labels; origin not stated, D76; 1 THz -> GHz keeps the basis, D256a). Fab org_epfl + facility
org_center_of_micronanotechnology ("All samples were fabricated at the Center for MicroNanoTechnology (CMi) at EPFL",
p.5; D448, ji2024 / herr2012 precedent); process_name "photonic Damascene reflow process (refs. 23, 24)".

Not entered:
- The paper's main result, the thermo-refractive frequency-noise spectra per resonator (Fig. 4(c), 10 kHz - 10 MHz) and
  the integrated TRN frequency instability of the 1 THz ring (about 240 kHz, p.4): no registry parameter (gap below).
- "Typically Q > 10^7" for the sample family (p.3): D254, not entered per device (notes).
- R ~23-1200 um: range over the set, per-device radii not printed. Fig. 4(b) SEM cross-section labels (2.0 um x 0.8 um,
  SiO2 cladding, air above): which resonator not stated (D159), notes only.
- dn/dT 2.45e-5 /K and the Table I material constants: cited / literature medians (rule 3); 150 kHz estimate (p.2) rests
  on them; FEM simulations (Fig. 1) have no parameter.

Judgment call: the four resonators are entered as rows with only an FSR so the TRN measurements have a home once a
noise parameter exists; an auditor may prefer to drop them as near-label rows.

## Registry gaps (skipped value, locator, proposed definition)

1. `frequency_noise_hz_per_rthz` (resonator, laser; unit Hz/sqrt(Hz)): single-sided cavity / laser frequency-noise
   amplitude spectral density at a stated offset frequency (offset and noise type in condition). Skipped: huang2019d
   Fig. 4(c) TRN spectra of the 1 THz / 99 / 88 / 20 GHz rings (p.4). Related open candidate frequency_noise_hz2_per_hz
   (D431); one of the two forms should be chosen.
2. `frequency_instability_khz` (resonator; kHz): integrated rms resonance-frequency fluctuation from thermal noise as
   stated (integration method in condition). Skipped: huang2019d about 240 kHz for the 1 THz ring (p.4).
3. `i_pi_ma` (phase_shifter; mA): drive current for a pi phase shift of a carrier-injection phase shifter. Skipped:
   hulme2015 test-run modulators 14 mA/pi (p.11, Fig. 11(b)).
4. `q_loaded` widened to reflector (or a reflection-peak Q): guan2018 WSR highest-peak Q about 8000 (p.6).

## Coordinator questions

1. hulme2015: keep the D159 handling of the psi-axis headline (23 deg x 1 deg, 5.5 dB) and the 34.5 nm laser tuning in
   notes, or add an as-measured PIC row (free_space_emitter.other, array variant "not stated") carrying 23 deg / 1 deg /
   5.5 dB? Recommendation: keep D159 (the paper fabricated both arrays and both laser designs and names neither for the
   measurements).
2. huang2019d: keep the four FSR-only resonator rows (recommended, they anchor a later noise gap-fill) or drop them.
