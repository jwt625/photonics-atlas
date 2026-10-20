# Batch report ofc_06 (OFC 2026, facts only, 2026-10-20)

Transcribed by the coordinator from the batch agent's final report. Dry run: 0 errors, 0 warnings; 22 components,
72 metrics. host_device_ids empty; no EO modulator metrics; no e-mail addresses.

## Per paper (components / metrics)

- M2D.6 (2/9, fab org_globalfoundries, 45SPCLO): 2x2x2-lambda WSS fiber-to-fiber IL 7.167 / 6.822 / 7.289 / 7.792 dB
  (4 paths, O band inferred), rise / fall 58 / 77 us, die area 3.8 mm2 (derived); CRR filter (wdm.mrr) 3-dB bandwidth
  50 GHz, 0.29 nm (paper's own conversion, derived). Not entered: PDL 0.376-0.440 dB (pdl_db not allowed for
  switch_fabric), PSR / V-groove PDL (cited [6]), 35 GHz passband (definition not stated).
- M1D.4 (3/11, fab org_nexus_photonics, D72): SIL laser threshold < 25 mA, SMSR 48 dB, 1566 nm, gain length 1.6 mm,
  pair < 14 mm2; ULL SiN ring Q_i > 30 M at 1560 nm, > 40 M median (C band inferred), radius 850 um (derived);
  SiN-SiN interlayer taper < 0.2 dB at 1560 nm, < 0.25 dB total over C+L, length 1.2 mm. Text cites Fig. 1(c-g) for
  panels captioned Fig. 2 (locators use Fig. 2).
- W1B.4 (3/8, fab empty: three affiliations): 1060 nm SM VCSEL SMSR 40 dB (best), > 28 GHz at 7 mA, pitch 250 um,
  4 channels; PD array > 26.5 GHz (origin not stated); two-microlens-array VCSEL-to-SMF coupling IL < 2 dB and ~1 dB
  best, author_estimate.
- W4B.1 (1/3): FaML pair on a Tower SiN edge coupler IL 0.82 dB per channel loopback_half (mean of 5 pairs near
  1510 nm); 1-dB lateral tolerance 5.3 um; 25 um expanded-beam MFD (design). fab empty pending the registry org.
- Th3C.3 (5/23, fab empty: proprietary process): taper on a 32 um PD < 0.1 dB at 850 nm plus geometry; four Ge/Si PD
  tapers (Table 1 geometry) coupling efficiency > 90 % (DW15) and ~100 % (DW20-30) at 1330 nm; DW20 ~100 % at 850 nm,
  1-dB tolerance > 25 um.
- M4B.2 (2/5, foundry not named): vertical GC 1.3 dB (scope unspecified), 1-dB bandwidth 20 nm, O band inferred; RX
  MRR filter Q 4200 as q_loaded (unqualified Q), 200 GHz grid (design), 9 channels.
- W1J.2: no rows (system paper).
- Th1G.2 (1/4, fab org_applied_nanotools): trimodal MZI mode-selective switch at 1546.5 nm, IL incl. two ID-(de)MUXs
  device_total (< 2 dB TE0, < 2 dB TE1, 4.1 dB TE2); modal crosstalk >= 16 dB.
- Th2A.20 (3/6, fab empty): multicore isolator IL ~0.57 dB (wavelength, isolation not stated); multicore FWDM
  (wdm.tff) de-embedded IL 0.73 / 0.86 dB (C / L), derived via the Fig. 2(d) budget, core-to-core variation <= 0.2 dB;
  pump combiner ~0.2 dB typical, 95 % pump coupling. The 4-core EDFA module itself not entered (fiber amplifier).
- Th3H.4 (2/4, fab empty: NTT + Keio): InP/Si membrane DML array ~2 mW per channel, 6 channels; 8x8 silica MZI mesh
  ~2.1 dB fiber-to-fiber.
- M2E.1: no rows (503 W Yb fiber amplifier, outside PIC scope).

## Judgment calls

Platform values of unstated origin entered as measured with a note (agent followed the ofc_pilot precedent; this
conflicts with D76, which makes them author_estimate: the D76 sweep / OFC audit corrects it). Fiber amplifiers
excluded, their multicore passive parts entered. M2D.6 bandwidth on the CRR row. W4B.1 IL loopback_half.

## Registry gaps reported

Orgs: "Tower Semiconductor (Tower)" (W4B.1, pNA Sec. 2, fabricated and supplied the PICs); "UBC SBQMI Advanced
Nanofabrication Facility" (W4B.1 acknowledgments). Parameters: pdl_db for switch_fabric; wavelength_spread_nm for
fiber_chip_coupler; il_nonuniformity_db for nonreciprocal; tol_0p5db_lateral_um; il_reduction_db; laser inter-channel
wavelength crosstalk. Subtype amplifier.fiber if fiber amplifiers enter scope.
