# lit_203 batch report

Distilled 2026-11-18 under the pic-component-distill skill (Contracts v4-v7). Papers: shimizu2024, chrysostomidis2021,
ghosh1996, nykolak1993. Output: 15 components, 65 metric rows. `merge_component_staging.py --dry-run`: +15 / +65,
0 errors (the one warning printed is on an existing ni2025b row, not this batch).

Page-1 checks: all four texts are the registered papers. nykolak1993 page 1 opens with the end of the preceding paper's
reference list (Chu and Ghafouri-Shiraz); ignored. ghosh1996 and nykolak1993 values were checked against the page renders
(Table I of both papers, Fig. 1-3 axes, gain-compression values).

## ghosh1996 (5 components, 26 metrics)

- `er_powa_amp1_5p9cm` (amplifier.rare_earth, glass): threshold 8 mW, net fiber-to-fiber gain 4.5 dB at 80 mW (1536 nm),
  small-signal gain 3.7 dB at 70 mW (975 nm diode), 2.8 dB at 38 mW (Fig. 2 read, extracted_from_figure), 3-dB
  compression output 0.6 dBm, length / width / film / lower-cladding geometry.
- `er_powa_amp2_6cm_9um`, `er_powa_amp3_6cm_8um`: Table I thresholds (9 / 10 mW) and 80 mW gains (4.2 / 3.7 dB),
  geometry. Signal wavelength not printed with Table I: 1536 nm with `wavelength_inferred`.
- `er_glass_wg_amp1` (waveguide_platform.straight): Er absorption 1.5 dB/cm (difference of 1.5 um and 1.3 um insertion
  losses, derived), 1.3 um fiber-to-fiber insertion loss 2.4 dB (measured), background loss about 0.1 dB/cm
  (author_estimate).
- `er_powa_36cm_model` (row_kind design): modeled 30 dB net gain for a 36 cm version at 80 mW (simulated).
- Not entered: ~1 dB coupling loss per interface ("from previous cutback measurements", rule 3); bulk target-glass
  absorption 1.6 dB/cm (bulk material); lifetimes 14 / 10 ms (no parameter); 0.5 dB penalty for 975 vs 980 nm pumping
  (difference, no parameter); residual pump transmission ~1/3 (Fig. 3, no parameter); 1 mm bend radius (projection);
  Fig. 4 curves other than the printed 30 dB point.
- Fab: `org_lucent_bell_labs` on the four fabricated rows ("we have fabricated and tested", p.2; all authors Lucent
  Technologies, Bell Laboratories; fabrication-assistance thanks p.3). No facility.

## nykolak1993 (3 components, 9 metrics)

- `er_powa_4p5cm` (amplifier.rare_earth, glass): ~15 dB net gain (input SMF to output multimode fiber, 1537 nm, 280 mW
  980 nm pump), 3.3 dB/cm (derived), 3-dB compression output +3.5 dBm, geometry (4.5 cm, ~5 um, ~1.5 um).
- `er_glass_wg` (waveguide_platform.straight): measured absorption 5.5 dB/cm at 1530 nm.
- `output_facet_smf` (fiber_chip_coupler.edge): ~3 dB waveguide-to-output-SMF coupling loss from the sensitivity budget
  (author_estimate, per_facet, C band inferred).
- Not entered: excess noise factor Nsp (approaches 1 at low input, Fig. 3; no amplifier parameter); gain polarization
  dependence 0.3 dB (5 um) / 0.8 dB (7 um), Table I (no allowed parameter; the 7 um waveguide has no other value, so no
  row); 6-dB receiver-sensitivity improvement and BER results (system); ASE spectrum (no parameter); 2.5 / 3.5 dB filter
  and isolator losses (setup equipment).
- Fab empty: passive "were fabricated by RF-sputter deposition" (D80b); all authors AT&T Bell Laboratories
  (`org_bell_labs` would be the time-correct id if a later ruling sets fab). No facility.

## chrysostomidis2021 (5 components, 23 metrics)

- `edwa_5p9cm` (amplifier.rare_earth, al2o3): active-region net gain 8.5 / 6.5 dB at -28 / -10 dBm spiral input and
  1.44 / 1.10 dB/cm (author_estimate: rest on the estimated coupling / MMI / transition terms, vagionas2021 precedent),
  measured chip net loss 22.9 / 24.9 dB (fiber_to_fiber), geometry.
- `si3n4_waveguide` (waveguide_platform.straight, sin): 0.14 dB/cm at 1532 nm (measured), 1.4 um x 200 nm.
- `si3n4_al2o3_vertical_adiabatic_coupler` (waveguide_platform.transition, other): 0.5 dB per transition from a 2-6-12
  cascade reference die (measured, cutback, test_structure true, band unspecified), taper geometry.
- `pump_signal_mmi` (wdm.other, sin): 1.7 dB signal port / 8.3 dB pump port at 1550 nm, 2.7 dB pump port at 980 nm
  (author_estimate, origin not stated).
- `fiber_si3n4_interface` (fiber_chip_coupler.edge, sin): 10 dB signal (C band) / 12 dB pump (980 nm) per interface,
  no inverse taper (author_estimate).
- Not entered: signal enhancement 29.3 dB peak and the WDM enhancement ranges (no parameter); "strong saturation starts
  around 3.5 dBm chip input" (not a defined saturation power, D580); 18.8 / 15.2 dB fiber-to-spiral totals (sums of the
  entered estimates); ~9 mW pump at the active region (estimate); Table I values of other works and the 0.5 dB/interface
  of ref. [19] (cited); Si3N4 vertical tip thickness 30 nm (no parameter); BER, eye openings, per-channel powers,
  TOBPF > 30 dB adjacent-channel suppression (setup filter); > 7 dB projected net gain.
- Fab empty: fabrication sentences passive, no org named (D80b). No facility (grants only).

## shimizu2024 (2 components, 7 metrics)

- `ppln_opa_preamp` (amplifier.parametric, platform empty): gain > 5 / > 10 / > 15 dB at 31.0 / 33.0 / 34.6 dBm SHG pump
  per PPLN over both probe bands (module plane), plus a Fig. 5 read of the 15-dB case peak about 17 dB
  (extracted_from_figure).
- `ppln_opc` (frequency_converter.sfg_dfg): the same OPA as phase conjugator, conversion gain > 5 / > 10 / > 15 dB stored
  as power_conversion_efficiency_pct > 316.2 / 1000 / 3162.3 % (derived, abe2025 precedent).
- Not entered: repeater NF 6.3-7.4 dB and Fig. 6 NF spectra (repeater = OPA + GEQ + EDFA; no OPA-only NF printed); GEQ
  insertion loss ~6 dB (GEQ not described); "gain of the OPAs was ~15 dB" in the C-band power-tolerance loop (same
  operating point as the > 15 dB rows); all transmission results (system level). EDFAs are fiber amplifiers (out of
  scope, D80f).
- Fab empty (no fabrication statement, all authors NTT; shimizu2023 precedent); platform empty (D422).

## Missing fab / facility orgs

None. All fab statements either name no org or map to an existing id (`org_lucent_bell_labs`).

## Judgment calls

- (a) ghosh1996: the ~1 dB per-interface coupling loss is "from previous cutback measurements" (p.2), so it is not
  entered (rule 3); the 0.1 dB/cm background loss computed with it is this paper's new result and is entered as
  author_estimate (rule 4), with the arithmetic (0.07 dB/cm unrounded) in notes.
- (b) shimizu2024: one gain row per operating point spans 1529.16-1619.19 nm with a note that the probe covers only the
  C and L bands (no light between 1562.64 and 1583.27 nm); the two OPA units (C-band input and L-band input) are one
  design row (abe2025 precedent).
- (c) shimizu2024: the polarization-diverse OPA subsystem stays in scope as amplifier.parametric plus a
  frequency_converter.sfg_dfg row for the OPC function (D396; shimizu2023 / abe2025 precedents), not removed as a
  bench-top assembly (D642), because its core parts are the authors' own PPLN waveguide modules.
- (d) nykolak1993: the ~15 dB gain is kept although the preceding sentence cites the co-authors' OFC'93 postdeadline
  paper (ref. [4], titled "15 dB net gain demonstration"); the gain sentence itself cites nothing and points to this
  paper's Fig. 1 (D408 clause). Borderline; the auditor may rule otherwise.
- (e) Psat rows in ghosh1996 and nykolak1993: 3-dB compression output powers entered in `psat_out_dbm` with the 3-dB
  definition in the condition; `ref_plane` unspecified (the output plane is not printed).
- (f) ghosh1996 amplifiers no. 2 / no. 3 get the 1.4 um film and amplifier no. 1 also the 15 um lower cladding from the
  process paragraph; no. 3 (8 um, 6.0 cm, other wafer) is a separate row from no. 1 (8 um, 5.9 cm).
- (g) chrysostomidis2021 transition loss: band unspecified (wavelength of the cascade measurement not printed; the loss
  breakdown applies 0.5 dB at both 1550 nm and 980 nm).

## Registry gaps

- `nsp` (amplifier): spontaneous-emission / excess noise factor, dimensionless; nykolak1993 Fig. 3 (p.2), ~1 at low
  input rising to ~6.5 near +5 dBm output. Definition: "population-inversion / excess noise factor Nsp as defined by the
  paper (definition and number of modes in condition)".
- `pdg_db` (amplifier): polarization-dependent gain, positive dB; nykolak1993 Table I (p.2): 0.3 dB (5 um), 0.8 dB
  (7 um). Or widen `pdl_db` to amplifier with the definition "polarization dependence of loss or gain".
- `signal_enhancement_db` (amplifier): pump-on minus pump-off signal output; chrysostomidis2021 p.3-4 Fig. 2(c) 29.3 dB
  peak at 1532 nm (also open from vagionas2021).
- `conversion_gain_db` (frequency_converter): idler output / signal input in dB; shimizu2024 p.4 (> 5 / 10 / 15 dB),
  now stored as `power_conversion_efficiency_pct` (abe2025 precedent).
- `tip_thickness_nm` (waveguide_platform.transition): end thickness of a vertically tapered layer; chrysostomidis2021
  p.3 Si3N4 tapered from 200 nm to 30 nm.
