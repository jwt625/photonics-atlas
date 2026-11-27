# lit_301 batch report

Distilled 2026-11-27 (verified_on 2026-11-27). Papers: lit:herr2012, lit:ye2023a, lit:xiang2022a, lit:ashtiani2019,
lit:ito2019. Totals: 27 components, 117 metric rows. `merge_component_staging.py data/_staging/components/lit_301
--dry-run`: +27 components, +117 metrics, errors 0 (the two warnings it prints belong to merged guo2024a / ni2025b rows).

Page-1 title check: ye2023a, xiang2022a, ashtiani2019 and ito2019 match their source rows (Optica open-access journal
PDFs; ashtiani2019 page 1 carries a "Corrected: 31 August 2022" line, the article itself, not an erratum). herr2012 is
arXiv 1111.3071v1 (2011-11-13), titled "Universal Dynamics of Kerr Frequency Comb Formation in Microresonators", the
preprint of the Nature Photonics paper of the source row (same authors, same experiments): accepted as the same work
(D430 / D433), values from the preprint only, noted on every herr2012 row.

## lit:herr2012 (3 components / 4 metrics)

- `cmp_lit_herr2012_sin_comb_76ghz` (laser.comb): 76 GHz line spacing (p.2, Fig. 1(a)), `channel_spacing_ghz`
  (p.2 "line spacing", caption "repetition rate"; no pulses, broad RF beat note; D82g / D83b, boust2020).
- `cmp_lit_herr2012_sin_ring_76ghz` (resonator.ring, D396 pair of the comb row): resonance width ~200 MHz
  (`linewidth_mhz`, c_band inferred from the EDFA pump setup).
- `cmp_lit_herr2012_sin_ring_200ghz` (resonator.ring): "200 GHz" ring class as `fsr_ghz` author_estimate (D82a,
  churaev2023), "typ. radius 100um" figure label (`extracted_from_figure`, statistic typical).
- Not entered: all MgF2 crystalline whispering-gallery resonator values (68 / 43 / 35 GHz combs, ~1 MHz linewidth,
  80 / 500 mW pump, 24 / 29 FSR primary spacing, 1.4 MHz mismatch, 35 dB beat-note SNR): mm-scale polished crystalline
  bulk resonator, out of scope (D411; weng2021 MgF2 rod precedent). Comb span > 300 nm (no registry parameter, D81).
  3 W pump stays in the condition. Model inputs of the mu_th estimate (n2, Aeff, kappa, D2 = 10 kHz) belong to the
  MgF2 system. Several-hundred-MHz beat-note differences in Si3N4 (p.12): no component parameter.
- Fab / facility: org_epfl + org_center_of_micronanotechnology from "SiN samples were grown and fabricated in the
  CMI-EPFL nano-fabrication facility" (p.9; D448, pfeifle2014 precedent). No missing org.
- Judgment calls: 200 MHz width entered only on the Fig. 1(a) ring (caption ties it there; p.2 states it for the
  Si3N4 rings in general, D254 keeps it off the 200 GHz ring). No FSR entered for the 76 GHz ring (not stated).

## lit:ye2023a (6 components / 37 metrics)

- OPA `cmp_lit_ye2023a_opa_64ch` (free_space_emitter.other, si_sin_multilayer): measured steering 120 deg (theta) and
  13.9 deg (psi, 1540-1630 nm), resolution 0.052 / 2.72 deg, SMSR 9.96 dB as `slsr_db`; simulated 120 / 14.2 deg,
  0.043 deg, 11.4 dB; total loss 12.66 dB `device_total` `derived` (2.5 mW in, 136.15 uW main lobe; recomputation
  gives 12.64 dB, printed value kept, noted); 64 channels, average pitch 31.25 um.
- Loss-budget terms (p.7) on the part rows, all `author_estimate` (origin not stated, D702): edge coupler 2.5 dB
  per_facet; MMI 0.36 dB for the 6-level cascade -> 0.06 dB per_component (D682 / D702 per-part convention, printed
  value in notes); SiN-Si transition 0.2 dB; antenna emission + side-lobe loss 9.6 dB.
- Transition: simulated > 96.5 % (1500-1600 nm), gap 250 nm, 100 um coupling length, SiN 1 um -> 300 nm, Si 140 ->
  500 nm, 400 nm SiN, 220 nm Si, 3 um BOX. Phase shifter: P_pi 18.79 mW measured, 250 um TiN heater. Antenna: simulated
  emission loss 1.487 dB at 1550 nm, Si reflector period 1.2 um / duty 0.5 (condition says reflector, not the SiN
  grating).
- Not entered: projected maximum output ~1.714 W for 3.2 W input and the < 0.05 W per-channel Si power (projection;
  no free_space_emitter output-power parameter, D558 gap); Table 1 values of other works; reflector dual-layer offset
  0.83 um (no parameter); 2 mm array width and 10 um minimum pitch (notes).
- Wavelength: budget terms, P_pi and total loss have no printed measurement wavelength; 1550 nm inferred from the
  design wavelength (p.5).
- Fab: empty (passive "The chip is fabricated on SOI wafer", no org; authors at CUG and HUST). No missing org.

## lit:ashtiani2019 (12 components / 36 metrics)

- OPA `cmp_lit_ashtiani2019_opa_8x8`: ~7 deg 2-D steering at 1502 nm (measured), 43 dB from -2 dBm coupled to
  ~-45 dBm main lobe (`de_embedded`, `author_estimate`: how the coupled power was set is not stated), 64 elements,
  11 um pitch, 77 x 77 um aperture (footprint derived).
- Grating-coupler element: simulated ~30 % at 1500 nm, 2.5 x 3 um from Fig. 4(b) labels. Thermal phase shifter: 350 ohm
  measured, 200 um. Waveguide 500 x 220 nm: < 2 dB/cm measured (wavelength inferred 1502 nm). Crossing: simulated
  < 0.3 dB, isolation > 30 dB. Seven directional couplers (`dc1`-`dc7`, sibling rows per rule 9): FDTD ratio pairs
  and coupling lengths from the Fig. 4(c) table.
- Not entered: I_pi 4.5 mA (no drive-current parameter on phase_shifter; D439 candidate, aflatouni2015 precedent);
  P_pi not computed from I_pi^2 R (would assume a constant heater resistance); estimated per-element output ~38 dB below
  the coupled power (estimate, no parameter); input grating coupler, Y-junctions (ref. [18] design, no values),
  Y-junction bend radius 1.2 um (geometry only), Fig. 4(a) 6 / 4 um and Fig. 4(b) 5 um labels (not tied to a named
  dimension, D156); simulated array-factor patterns (Fig. 2).
- Fab: org_astar_ime with process_name "IME 180 nm silicon-on-insulator (SOI) photonic process" ("The chip is fabricated
  in the IME 180 nm ... process", p.4; Contract v7 named-process sentence, aflatouni2015 precedent). No missing org.
- Judgment call: Fig. 4(c) "Ratio (%)" pairs (e.g. 81/5) carry no port labels; first number entered as the through
  port and second as the coupled port, from the p.6 wording "transmission and the coupling coefficients" and the
  second number growing with coupling length. Both values are entered with the reading in the condition; an auditor
  may prefer D156 removal.

## lit:ito2019 (4 components / 14 metrics)

- LSPCW emitter `cmp_lit_ito2019_lspcw_antenna` (free_space_emitter.other): chip-level fan-beam values only: 22 deg
  steering for a 23 nm sweep, delta-theta 0.08-0.15 deg (FWHM), delta-phi 23-40 deg without the lens; design geometry
  (L 1.2 mm derived, 10 nm / 200 nm shallow grating, 210 nm Si, 2 um BOX, 80 um pitch, 32 LSPCWs).
- SSC 3 dB per_facet (`measured`, D167; wavelength 1530 nm inferred: the fabricated device's centre wavelength).
  MZ switch element (switch_fabric.other, D158): 13 mW bar-to-cross as `p_pi_mw`, theoretical < 0.2 dB
  (`simulated`). Six-stage switch tree: 78 mW total with all stages driven (`power_consumption_w`, derived).
- Not entered: every value measured through the off-chip acrylic prism lens (2D range 40 x 4.4 deg, average 0.15 deg,
  4256 resolution points, ~0.1 deg delta-phi, 0.30 deg phi step, 9 dB fiber-to-beam total, 15.3 mm focal length;
  D411 / D558 zhang2021a precedent); LSPCW-to-wire taper 0.3 dB (theoretical, cited to ref. [18], rule 3); radiation
  coefficient alpha 50-100 dB/cm from the NFP and 100 dB/cm design (registry gap); simulated upward emission ratio
  41-60 % and delta-phi 18-44 deg (no directionality parameter); 2-8x upward-power gain (relative to earlier work);
  Discussion 0.06 deg "in a discrete device" and 27 deg (device not identified, D159); 0.04 deg serial array (ref.
  [21]); 100 kHz-order TO response (ref. [20]); PhC lattice 394 nm / hole 192 nm / shift 95 nm (no parameter, in
  core_material; D558 gap).
- Fab: empty ("a 200 mm diameter SOI and a Si photonics CMOS process", no org, no node; process_name empty). No missing
  org.

## lit:xiang2022a (2 components / 26 metrics)

- DFB `cmp_lit_xiang2022a_dfb_8um_800um` (laser.dfb, inp): output 177 / 134 / 86 mW and thresholds ~46 / 54 / 88 mA at
  -10 / 20 / 50 C; slope > 0.36 W/A; series resistance ~1.3 ohm; T0 ~78 K (10-60 C); SMSR > 55 dB (two operating
  ranges); 8.6 nm temperature tuning; 0.12 nm/K -> 120 pm/K (derived); thermal resistance ~27 K/W; RIN < -157 dB/Hz
  at 500 mA and ~-148 dB/Hz at 200 mA; relaxation oscillation ~8 GHz at 700 mA; Lorentzian linewidth 394.4 kHz
  (200 mA), ~250 kHz (100 mW), <= 300 kHz above 300 mA (kHz -> Hz derived); 8 um ridge, ~800 um, 50 % duty (derived).
- Uniform-grating 500 um DFB `cmp_lit_xiang2022a_dfb_uniform_500um`: kappa ~10 /cm `author_estimate` (n_eff in the
  formula not stated), Bragg wavelength ~1546 nm.
- Not entered: ASE stopband ~0.73 nm (stopband_width_nm allowed only for reflector; registry gap); designed kappa L ~1
  and simulated confinement factors 4.6 / 3.8 % (design, no parameter); control sample without dual waveguide
  (qualitative); abstract / conclusion bounds > 170 / > 175 mW (restate 177 mW); Table 1 values of other works;
  "900 kHz" upper end of the Fig. 11(b) trend (the 250-394 kHz points are entered).
- Fab: empty ("fabricated with the similar fabrication process in [19]", passive, no org; authors at HUST, Ori-chip,
  Zhejiang University and Trinity College Dublin). No missing org.
- Judgment calls: RIN measured on a TO-packaged laser of the same design kept on the chip row (condition says
  packaged); output powers `ref_plane chip` (facet not stated).

## Missing fab / facility orgs

None: every stated fab / facility org is in the registry (org_epfl, org_center_of_micronanotechnology, org_astar_ime).

## Registry gaps (skipped value, locator, proposed definition)

| Proposed parameter | Class | Skipped value | Locator | Definition |
|---|---|---|---|---|
| `i_pi_ma` (drive current, D439 candidate) | phase_shifter | 4.5 mA | ashtiani2019 p.5 Sec. 3 | heater / injection current for a pi phase shift |
| `radiation_coefficient_db_per_cm` | free_space_emitter | 50-100 dB/cm measured (NFP), ~100 dB/cm design | ito2019 p.3 Sec. 3B, p.2 Sec. 2 | power decay rate of a leaky-wave / grating emitter due to emission |
| `upward_emission_pct` (directionality, chen2024c precedent) | free_space_emitter | 41-60 % simulated | ito2019 p.2 Sec. 2 | fraction of emitted power radiated upward |
| `output_power_mw` / power handling (D558 gap) | free_space_emitter | ~1.714 W projected | ye2023a p.9 Sec. 3.2 | emitted optical power at the stated input |
| `stopband_width_nm` on laser | laser | ~0.73 nm ASE stopband | xiang2022a p.5 Sec. 3.1, Fig. 5 | stopband width of a DFB grating from the sub-threshold spectrum |
| PhC lattice constant / hole diameter (D558 gap) | free_space_emitter | a 394 nm, 2r 192 nm, s3 95 nm | ito2019 p.2 Sec. 2 | photonic-crystal lattice constant and hole diameter |
