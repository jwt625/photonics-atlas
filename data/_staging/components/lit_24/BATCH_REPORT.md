# Batch lit_24 report (distill subagent, 2026-10-29)

Dry-run `batch lit_24: +26 components, +190 metrics; errors 0`. ASCII, no e-mail, no quotes (all 8 sources
`restricted_local_only`). Not audited, not merged.

## Per paper (components / metrics)

- gentry2015 (1 / 8): IBM 12SOI 45 nm CMOS body-Si microring pair source (resonator.ring): Qtot 31k / Qo 114k / Qext 43k
  (fit), linewidth 6.2 GHz -> 6200 MHz derived, FSR1 / FSR2 756.6 / 758.4 GHz (Fig. 3(a) annotations), outer radius 22 um,
  width 1.08 um. Not entered: pair rate, CAR, FWM efficiency, beta_fwm / n2 (D250); FSR difference 1.8 GHz measured /
  1.4 GHz simulated (gap); core thickness only by citation [46]. Judgment: fab org_ibm (process "IBM 12SOI" named, "fabricated
  within a CMOS foundry", foundry not named separately; borderline).
- hosseinnia2026 (10 / 51): SiN (170 nm LPCVD) rings R = 400 / 350 / 300 um, GFSM all-pass resonator R = 340 um (Qi ~2.1e7
  mean, FSR 64.9 GHz, SEM gap 1428 nm / width 2075 nm, design 1425 / 2100 nm), 5-pole Butterworth filters 1 GHz (BW 1.03 GHz,
  IL ~2 dB de_embedded, rejection > 55 dB as crosstalk_db, FSR 64.5 GHz, tuning 145 mW total / < 30 mW per cavity, design kappas
  simulated) and 520 MHz (BW 481 MHz derived), single-pole (7.5 GHz, FSR ~68 GHz, 16 dB rejection, gap 1450 nm) and 3-pole
  (FSR 40.27 measured / 39.94 simulated, kappas, simulated > 70 dB) as wdm.mrr; edge coupling ~2 dB per facet, 26 %
  end-to-end; grating couplers > 5 dB (scope unspecified). Not entered: ripple 0.4 / < 0.1 dB (gap), abstract claims of
  > 400 GHz / one-FSR tuning (no measurement shown), Fig. S1 / S2 design-study Q and IL values, S.4 tip mode ~2 um
  (single-pole chip only, D159). Judgments: R = 350 / 300 um "maintain Q >= 1.0e7" entered as q_loaded ge (unqualified Q
  rule) although context suggests intrinsic; their FSR ~80 / ~93 GHz taken as measured; fab org_georgia_institute_of_technology
  (in-house process at GT IMS; authors also at OEwaves; D83c, borderline), facility org_institute_for_matter_and_systems
  (printed "Institute of Materials and Systems (IMS)").
- liu2022a (1 / 10): suspended Si PhC nanobeam cavity: linewidth 0.71 pm (measured), Qexp 2.17e6 as q_loaded derived
  (lambda / delta-lambda), Qth 1.2e8 as q_intrinsic simulated, lattice 460 nm, tapered periods 329.81-439.853 nm, 30 holes,
  6 um2, 220 nm / 3 um BOX. Wavelength 1540.36 nm read from the Fig. 10(b) axis (inferred). Not entered: mode volume (gap),
  GA design variants, base structure. Fab empty (passive, all authors one university).
- sinclair2020 (4 / 24): SiO2-clad Si3N4 ring at 780 nm (Q 1.38e6 loaded, FWHM 570 fm -> 0.57 pm, ~0.2 dB/cm and 0.4 %
  coupling from the Eq. (1) fit (derived, D76), FSR 99 pm / 49 GHz measured on a same-path-length lower-Q ring, TDWS 13.1 pm/K
  simulated, geometry; radius 300 um from the 600 um diameter); air-clad width series R = 300 um (best Q per width from
  Fig. 4(b), extracted); PMMA (6.18 pm/K) and PUA (0.2 fm/K) cladding designs (row_kind design). Not entered: ER printed as
  46.8 % (definition unclear), Fig. 4(a) average-Q series, laser-locking error response. Fab empty; James Watt
  Nanofabrication Centre staff thanks only (not a facility statement).
- zhu2024 (3 / 29): TFLN racetrack 4.5 um x 10 mm, gap 0.6 um (Qi 29.32e6, QL 19.56e6, kappa_i 6.4 MHz, loaded 9.6 MHz,
  five more annotated Qi of the mode family, 1.3 dB/m -> 0.013 dB/cm author_estimate); array rows for the length series
  (3 um) and width series (10 mm), mean of top-50 Qi per device read off Fig. 3. Not entered: Fig. 4 RF-calibrated Q
  16.07e6 / 18.39e6 (device not identified, D159). Platform lnoi_rib (600 nm film, ~325 nm etch; cut not stated).
  Fab org_harvard_university ("We fabricate", all authors Harvard).
- gonzalezandrade2019 (3 / 25): slot-waveguide 1x2 splitter (splitter.other), nominal and +/-25 nm biased siblings:
  per-output transmission 3 +/- 0.5 dB over 1260-1650 nm both polarizations (cascade regression, insertion_loss_db range),
  imbalance < 0.42 dB TE / < 0.24 dB TM (derived from ER), MZI ER > 20 / > 25 dB, simulated EL < 0.5 dB and IB < 0.3 dB,
  full design geometry (WI, WR, WJ, GS, GA, GB, GT, LS, LT). Judgment: fab org_centre_de_nanosciences_et_de_nanotechnologies
  (fabrication "performed at the Plateforme de Micro-Nano-Technologie/C2N"; C2N owns the platform and hosts most authors;
  borderline: could be facility-only). RENATECH = program acknowledgement.
- oka2023 (1 / 8): Si 90-degree hybrid (four 2x2 MMIs + delays): excess loss < 0.4 dB (wavelength inferred from the
  C-band measurement span), measured |phase error| < 5 deg over 24 chips / 2 wafers, simulated worst case < 1.3 deg,
  footprint <= 185 x 185 um, arm width 0.9 um. Not entered: CMRR > 28 dBe (D81), yield 99.99 / 99.94 % (gap). Fab empty
  (passive "was fabricated", all authors Fujitsu Optical Components).
- wang2014 (3 / 35): 8-channel hybrid mode demux with grating polarizers (mode_converter.mdm_mux): excess loss per channel
  (mux + demux pair, de_embedded, not halved), dominant and accumulated crosstalk per channel at ~1560 nm (16 rows);
  TE- / TM-type grating polarizers (polarization.other) with simulated ER > 25 / > 30 dB and 70 nm etch. Not entered:
  PBS / ADC parameters (ref. [15], authors' own earlier work, D259), Fig. 2 crosstalk of the earlier device, "> 20 dB
  for 60-80 nm etch" (polarizer type not stated, D159), grating geometry (gap below). Fab org_zhejiang_university.

## Fab / facility organizations missing from the registry

- Plateforme de Micro-Nano-Technologie/C2N (gonzalezandrade2019 p.4 Acknowledgements): facility of C2N; not entered as
  facility_org_ids.
- Alias candidate: "Institute of Materials and Systems (IMS)" at Georgia Tech (hosseinnia2026 p.3) for
  org_institute_for_matter_and_systems.

## Coordinator decisions requested

1. gentry2015 fab org_ibm from the named IBM 12SOI process (no separate foundry statement).
2. gonzalezandrade2019 C2N as fab_org_ids vs facility (platform not in registry).
3. hosseinnia2026 R = 350 / 300 um unqualified Q as q_loaded vs q_intrinsic (context: "maintain" after an intrinsic Q).
4. hosseinnia2026 out-of-band rejection as crosstalk_db (jeong2013 precedent) vs extinction_db.

## Registry gaps

| gap | skipped value (locator) | proposed definition |
|---|---|---|
| `passband_ripple_db` (wdm) | hosseinnia2026 5-pole 1 GHz 0.4 dB, 520 MHz < 0.1 dB (p.8 Sec. 6) | peak-to-peak in-band ripple of a flat-top filter passband, positive dB |
| `mode_volume_lambda_n3` (resonator) | liu2022a 0.32 (lambda/n)^3, simulated (p.1, p.7 Table I) | effective mode volume in units of (lambda/n)^3, definition (max field vs peak energy density) in notes |
| `fsr_mismatch_ghz` (resonator) | gentry2015 1.8 GHz measured, 1.4 GHz simulated (p.2-3, Fig. 3(a)) | difference of adjacent FSRs (dispersion-induced D2-type mismatch) around a stated resonance |
| period_nm, fill_factor, grating_width_um, fiber_angle_deg, taper_length_um for polarization | wang2014 TE / TM grating polarizers: period 630 / 1000 nm, duty cycle 0.5, 10 um width, 10 deg fiber, 300 um taper (p.5-6) | grating geometry of grating-based polarizers (same definitions as fiber_chip_coupler) |
| `yield_pct` (splitter, any) | oka2023 99.99 % / 99.94 % for phase error < 5 deg (p.2 Sec. III) | fraction of devices meeting the stated criterion (criterion, population and estimation method in condition) |
