# lit_161 batch report

Distilled 2026-11-16 under pic-component-distill Contracts v4-v7. Papers: lit:chen2023c (46 pages), lit:shahin2025a
(3 pages). Total 12 components, 89 metric rows. `merge_component_staging.py --dry-run`: 0 errors (the only warning is
on the merged ni2025b rows, not on this batch). Page-1 titles match the source rows. chen2023c is the arXiv v1
preprint of the Nature Communications paper (journal version not read). Neither file is a correction or erratum.

## lit:chen2023c - Sb2S3-on-Si PIN-heater non-volatile devices, 5-bit (9 components, 56 metrics)

| component | class | metrics |
|---|---|---|
| ring_r30 | resonator.ring | 11: FSR 2.42 nm, a->c shift 0.394 nm, notch depths a ~14.7 / c ~9 dB (Fig. 1(d) reads), radius 30 um, gap 280 nm, width 500 nm, 220 nm core, ~120 nm etch, 100 nm slab (derived), 2 um BOX |
| ring_ps_10um | phase_shifter.phase_change | 8: 0.326 pi (derived 2 x 0.394 / 2.42), L_pi ~30.7 um (length_um derived, blundell2025 precedent), c-state 0.72 dB per pi (ring extraction), simulated 0.26 dB per pi and L_pi 38 um, 10 um segment, width, core |
| sbs_transition | waveguide_platform.transition | 1: simulated 0.013 dB per facet (99.7 % mode coupling) |
| mzi_switch_30um | switch_fabric.other | 6: extinction 13 dB (a) / 15 dB (c), IL ~2.2 / ~1.5 dB (Fig. 2(e)-(f) reads), 2 x 2 ports |
| mzi_ps_30um | phase_shifter.phase_change | 3: full pi phase shift, endurance 50 cycles (100 events, derived), 30 um per arm |
| mmi_50_50 | splitter.mmi | 7: simulated excess loss < 0.1 dB and 1-dB BW > 60 nm, figure-labelled 75 x 4.053 um, 1.038 um ports, 2 x 2 ports |
| adc | splitter.directional_coupler | 14: measured IL 2.0 (a) / 0.5 dB (c), ER ~10 / 11 dB, ER ~15 dB after 1,150 cycles; simulated IL 0.1 / 0.3 dB, ER > 15 dB, ring-loss-corrected IL ~0.85 dB / ER 25 dB; Lc ~79 um, gap 420 nm, widths 409 / 450 nm |
| adc_ps | phase_shifter.phase_change | 4: 32 levels at 1340 nm, endurance > 800 cycles (derived from > 1,600 events) and 1,150 cycles (2,300 events, slight degradation), retention > 77 days (6,652,800 s, derived) |
| trim_mzi_40um | phase_shifter.phase_change | 2: extinction 24 dB after phase-error correction, 40 um per arm |

Fab `org_university_washington` (author contributions p.18: R.C. fabricated, D395). Facility
`org_stanford_nano_shared_facilities` ("Part of this work was performed at the Stanford Nano Shared Facilities (SNSF)",
p.18; pre-merger name, D80d; same wording and handling as merged chen2024a). Platform `soi_rib` (220 nm, ~120 nm partial
etch) as for chen2022c / zheng2020. Wafer supplier printed "WaferPro" (p.15) in notes only.

Values not entered and why:
- c-Sb2S3 hybrid-waveguide loss 0.024 dB/um (p.5, Fig. 1(d)): per-length phase-shifter loss (D250); entered in its
  per-pi form (0.72 dB). Supp. S2.3 (p.29) restates the ring loss as "0.76 dB/um", which conflicts with p.5 (D417 note).
- Simulated per-pi loss: main text 0.26 dB/pi (p.5) vs supplement ~0.23 dB/pi (p.25); 0.26 entered, 0.23 noted.
- Delta n_eff ~0.018 (p.3, p.25), level step 0.50 +/- 0.16 dB (p.12), SET 200 ms reducible to ~100 us (p.5, p.17),
  pulse amplitudes / durations: no parameter (pulse data in conditions / notes).
- Abstract / discussion "IL < 1.0 dB", "ER > 10 dB" for ring, MZI and DC together (p.1, p.3, p.15): family-level
  statement (D254).
- Table S1 30 / 40 / 50 nm DC designs (p.28), the a-phase-matched DC design (Fig. S4, 0.3 dB port difference) and the
  "~34 um" Lc for 50 nm Sb2S3 (p.8): design-only, geometry only (rule 9).
- MMI measured spectra (Fig. S6(c), ~0.1 dB fluctuation): no loss value printed; "3 um" port label ambiguous.
- Material data (ellipsometry n / k, XRD, Raman, thermal conductivity 0.2 / 0.4 W/m/K, AFM stripe thickness Table S3,
  Sb2S3 enthalpy): not component metrics. Fig. 5(a) coarse levels and Fig. S10 partial crystallization: no level count
  printed. Heat-transfer simulation (relaxation within a few us, p.35): no parameter.
- Values the paper cites (GST / Sb2Se3 pulse lengths, 1 mm ferroelectric L_pi, ref. 19 a-Sb2S3 loss): cited (rule 3).

Judgment calls:
1. Asymmetric DC classed `splitter.directional_coupler` like the same group's Sb2S3 QC-DC (chen2024a), not
   `switch_fabric.other` as for the chen2022c GST 2x2 coupler; actuator row `adc_ps` per D396.
2. Balanced 30 um MZI as `switch_fabric.other` (D158) plus actuator row; the 40 um phase-error-corrected MZI as
   `phase_shifter.phase_change` (its function is trimming; extinction of an interferometer is allowed on phase shifters).
3. MZI c-state: p.6 calls it "a bar state with an extinction ratio of 15 dB", Fig. 2(f) shows the cross port high; the
   condition follows the figure, conflict in notes (D417). Trim MZI: text / caption 24 dB vs Fig. 6(b) label ~25 dB.
4. Switching events halved to cycles with the paper's own equivalence (p.33: 1,150 cycles = 2,300 events; zheng2020
   precedent): 1,600 events -> > 800 cycles, 100 events -> 50 cycles, `derived`.
5. Measured IL / ER wavelengths are the figure-marker positions (1327 / 1335 nm, +/- 2 nm, `wavelength_inferred`);
   the 1,150-cycle ER and the 24 dB trimmed ER carry `o_band` inferred.
6. The bare-Si to Sb2S3-loaded transition is a fabricated-chip part with only a simulated value (D80e; chen2024a
   oxide-window precedent). The main text says "verified", the supplement shows a mode-overlap calculation: `simulated`.
7. SNSF set as facility on all rows; the paper does not say which part of the work was done there (the Stanford
   co-authors measured the film thermal conductivity, p.18).
8. ring_r30 platform / etch from the shared device description (p.3, p.15), not restated per device.

## lit:shahin2025a - deeply recessed Ge/Si waveguide PD, imec (3 components, 33 metrics)

| component | metrics |
|---|---|
| ge_pd_w200 | 13: dark ~20 nA, 0.88 A/W (-2 V), 0.55 A/W (0 V), ~106 GHz (-2 V), Fig. 4 six-die ranges at -3 / -2 / -1 / 0 V, TEM Ge width ~0.2 um and thickness 193 nm, recess 190 nm, 220 nm SOI, 2 um BOX |
| ge_pd_w300 | 10: dark 6 nA, 0.93 A/W, ~106 GHz (-2 V; Table I "This Work"), Fig. 4 ranges, width 0.3 um, SOI stack |
| ge_pd_w400 | 10: dark 4 nA, 0.98 A/W, 85 GHz (-2 V), Fig. 4 ranges, width 0.4 um, SOI stack |

Class `photodetector.ge_waveguide`, platform `soi`, fab `org_imec`, `process_name` "imec 300-mm silicon photonics
platform" ("fabricated in imec's 300-mm silicon photonics platform", p.1; D455). Responsivities `ref_plane on_chip`,
method `reference_structure` (grating-coupler loss from a reference waveguide, 0.35 dBm at the device; merged shahin2025
precedent), TE grating coupler, 1310 nm. Bandwidths fitted from S21 within the 110 GHz range (`measured`).

Values not entered and why: Fig. 2(b) dark-current box plots over 10 dies (printed single-die values used); Fig. 2(c)
responsivity at other biases (log axis, flat beyond -1 V, not read); Fig. 3 per-bias single-die S21 crossings (the
Fig. 4 die ranges cover the same biases); Table I rows [2], [3], [5], [6] (other works); conclusion "less than 10 nA"
(summary of the 300 nm device, Table I value entered). Absorber length not printed.

Judgment calls: the TEM geometry (p.1, Fig. 1) is assigned to the 200 nm device ("average Ge width of around 200 nm");
recess depth 190 nm (p.3) `design_target`, origin not stated; 200 nm -> 0.2 um widths `derived` (D157); the -1 V and
-2 V Fig. 4 ranges for the 200 nm device include one outlier die each (noted).

## Missing fab / facility orgs

- Washington Nanofabrication Facility / Molecular Analysis Facility (facility) - lit:chen2023c p.18 acknowledgments
  ("Part of this work was conducted at the Washington Nanofabrication Facility/ Molecular Analysis Facility"). Already
  requested in D417 / D586; still absent from `organizations.csv`.

## Registry gaps

- Multilevel step size: chen2023c 0.50 +/- 0.16 dB per level (p.12, Fig. 5(b)); proposed `level_step_db` (phase_shifter,
  switch_fabric): transmission change per non-volatile level step, statistic / std in notes.
- Effective-index change delta n_eff: chen2023c ~0.018 simulated at 1310 nm (p.3, p.25); candidate already listed in
  D417.
- Switching pulse duration / energy: chen2023c SET 200 ms (reducible to ~100 us), RESET 150-550 ns (p.5-12); candidate
  already listed in D417.
- A dedicated L_pi parameter would avoid `length_um` carrying a calculated L_pi (here 30.7 um derived, 38 um
  simulated; blundell2025 precedent followed).
