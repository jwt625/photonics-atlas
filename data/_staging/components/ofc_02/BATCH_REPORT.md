# Batch report ofc_02 (OFC 2026, facts only, 2026-10-20)

Transcribed by the coordinator from the batch agent's final report. Dry run: 0 errors; 18 components, 79 metrics from
10 of 12 papers. No e-mail addresses, ASCII only, quotes a few words at most; locators p.~N / pNA plus section/figure.

## Per paper (components / metrics)

- Th3F.6 (1/4, fab org_samsung_electronics, Samsung Foundry 300 mm): microring-assisted Ge APD. Entered 0.82 A/W
  on_chip at -1.0 V, 1302.4 nm (wavelength inferred from the on-resonance I-V wavelength; on-chip power "estimated",
  method not given); bandwidth 22 / 46 GHz at -6.1 / -6.5 V; ring waveguide width 350 nm. Not entered: avalanche gain
  7.5, GBP 165 / 253 GHz, R 7 um, FSR ~9 nm, crosstalk estimate ~10 dB (no parameter / not allowed for the class);
  dark current only as a histogram.
- Th1D.4 (2/11): 4-core-fiber fan-in/fan-out of fs-laser-written glass waveguides plus the waveguide. Measured IL ~0.26
  / ~0.36 dB mean of 60 waveguides (before / after packaging), max < 0.5 dB, fiber_to_fiber at 1310 nm; RL > 45 dB;
  PER > 35 dB. < 0.15 dB per facet and < 0.08 dB/cm are Introduction claims without method (author_estimate). Pitch
  127 / 40 um, 4 channels (design); diameter 18-20 um. fab empty (Shenzhen University and Shenzhen Photonics Valley:
  ambiguous). Not entered: crosstalk < -46.4 dB (crosstalk_db not allowed for fiber_interface), +0.1 dB packaging,
  0.03 dB higher-order modes.
- M1D.2 (2/5): two-section DFB (SMSR 43 dB, 40 mW, 2 x 300 um) and 600 um single-section reference (40 mW at 150 mA).
  Wavelength, material and fab org not stated. Not entered: FM efficiency 1.45 / 0.07 GHz/mA, chirp nonlinearity,
  2.9 GHz excursion (no parameter).
- W2A.15 (3/3): micro-transfer-printed QD U-turn FP laser (laser.heterogeneous) > 100 mW coupled into SiN at 700 mA,
  20 C; laser-to-SiN butt interface ~4 dB per_interface, derived (vs a laser on bare Si), O band inferred; Bezier
  U-turn design row 0.5 dB simulated. fab empty (UCSB plus Tyndall).
- Th1H.1 (1/17): dual-mode DFB: threshold 12 mA; 4.44 / 4.13 mW at 21 / 25 C; SMSR per mode at 12 / 108 mA; mode
  wavelength ranges; spacing 314.6-319.7 GHz; linewidths 634.2 / 369.2 / 722.9 / 463.2 kHz; RIN peak -142 and
  <= -155 dB/Hz (noise-floor limited, qualifier le); length 1200 um. Conflict kept and cross-noted: conclusion puts
  the 369.2 / 463.2 kHz linewidths at 120 mA, Sec. 3 at 108 mA; text cites Fig. 1 where captions mean Fig. 2. Not
  entered: grating period 240 nm (period_nm not allowed for lasers), RO frequency, slope, resistance.
- M2D.2 (4/11, fab org_imec MPW): curved tunable DC (split 40-60 % and < 20 mW simulated; ~45 mW mean measured per
  coupler); ultralow-crosstalk MZI cell ER > 50 dB after bias optimization, ~13 dB unbiased; 4x4 switch fabric
  crosstalk > 50 dB, > 40 dB over > 10 nm, IL < 1.5 dB de_embedded, footprint 4.9e6 um2, 4 ports; vertical
  fiber-array coupler ~3 dB per coupler author_estimate (grating class inferred from the vertical configuration).
- Tu2J.4 (2/5): S/C/L mosaic multiplexer ~3 dB mean measured (reference waveguide subtracted), 2.5 dB simulated,
  43.2 um2, Si 220 nm; gap-filled redesign ~5 dB entered as simulated (paper ambiguous). Class splitter.other (no
  fitting wdm subtype), n_channels dropped. Fab org not stated.
- W4B.6 (1/14): dual-mode GC: measured 3.03 dB at 1553 nm, 1-dB BW 52 nm (TE0-LP01); 3.75 dB at 1551 nm, 54 nm
  (TE1-LP11), scope unspecified (normalization not stated); simulated 2.07 / 2.47 dB, 55 / 57 nm, back reflection
  21.47 dB; design period 500 nm, fill 0.5, etch 70 nm. Foundry not named.
- Th1A.4 (1/2): 7 um cryogenic VCSEL 91 mW at 3 K, 86-91 mW over 3-40 K. Not entered: slope efficiency 1.18 W/A
  (parameter added later in D77; sweep). The 5 um device has no component metric.
- W3E.3 (1/7, fab org_ntt): twin RTF tunable laser, linewidth ~350 kHz during switching, ~300 / ~500 kHz at 20 / 70 C;
  12 / 3 mW; tuning power < 70 mW; 1550.61 nm. Not entered: frequency error +/-2.5 GHz, 100 ns switching.
- Th3D.2: no rows (speckle spectrometer, no component metrics; no spectrometer class).
- W4H.3: no rows (system / network paper).

## Judgment calls

J1 W3E.3 fab org_ntt under D72 ("we developed", "fabricated", all authors NTT). J2 Tu2J.4 splitter.other. J3 M2D.2
coupler grating class inferred. J4 M2D.2 tuning results simulated. J5 Tu2J.4 gap-filled ~5 dB simulated. J6 Th1D.4
Introduction claims author_estimate. J7 W2A.15 butt loss derived. J8 Th1H.1 RIN -155 qualifier le.

## Registry gaps reported

- Classes: wdm.other / wdm.inverse_design (Tu2J.4); spectrometer (Th3D.2).
- Parameters: avalanche_gain, gbp_ghz (photodetector); relaxation_oscillation_ghz, fm_efficiency_ghz_per_ma,
  chirp_nonlinearity_pct, frequency_error_ghz (laser); rms_spectral_width_nm (vcsel). slope_efficiency_w_per_a exists
  since D77.
- Allowances: crosstalk_db for fiber_interface; fsr_nm, radius_um for photodetector; period_nm for laser.
- Orgs missing: "UCSB Nanofabrication Facility" (ofc2026:W2A.15, p.~3, Acknowledgements); "ARIM" (ofc2026:Tu2J.4,
  p.~3, Acknowledgement; grant support, not entered).
