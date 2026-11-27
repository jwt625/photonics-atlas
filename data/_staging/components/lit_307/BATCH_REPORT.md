# lit_307 batch report

Distilled 2026-11-27. Papers: lit:moss2013, lit:he2018, lit:xu2013. Page-1 titles checked against the source rows
(moss2013 is the arXiv preprint retitled "A Review of New CMOS Material Platforms for Integrated Nonlinear Optics",
same work as the Nature Photonics review); no correction / erratum; no `garbled_text_layer`. Dry run
`merge_component_staging.py data/_staging/components/lit_307 --dry-run`: +7 components, +53 metrics, 0 errors (the 2
warnings are on merged rows of other papers).

| paper | components | metric rows |
|---|---|---|
| moss2013 | 0 | 0 |
| he2018 | 5 | 33 |
| xu2013 | 2 | 20 |

## lit:moss2013 (review, no own results)

No rows. Every device value is credited to cited work, much of it the authors' own earlier papers (rule 3, D259 /
D408; lit_231 fontaine2022 and lit_144 errandoherranz2019 precedents):

- p.4 thermally cycled LPCVD SiN 700 nm, 0.4 dB/cm [57]; p.5 SiN parametric gain 3.6 dB over 150 nm, 6 cm, gamma
  1200 /W/km [57]; Hydex loss 5-7 dB/m, 45 cm spiral [14, 63]; n2 / gamma [63]; p.6 parametric gain +15 dB and +16.5 dB
  conversion [74], zero-GVD points [76].
- p.7-8 Hydex ring Q 1.2 M, 270 um diameter, 7.4 % slope efficiency, 9 mW, 9 % conversion [58]; SiN ring 58 um radius,
  Q 500,000, FSR 403 GHz, 50 mW threshold, 87 lines [57]; Q 65,000 Hydex ring [59].
- p.8-9 sub-100 GHz spiral combs, 725 x 1650 nm, loaded Q 100,000, ~2 W pump [67]; octave comb 1170-2350 nm [66];
  SCG 665-2025 nm [93], > 350 nm in Hydex [92]; p.11 sub-200 fs pulses [70], FD-FWM loop laser and ~10 kHz linewidth
  [15, 71]; p.12 X-SPIDER [14].
- p.15 Table I (n2, gamma, TPA, FOM per platform): material-level values with references [2, 47, 55-57, 63, 76, 127].
- Figures 1-6 (p.22-31): each caption credits the reproduced panels to the cited papers.

Missing fab / facility orgs: none (no rows; acknowledgments list funders and proof-readers only, p.21).

## lit:he2018 (SWG contra-DC mode blocking filters, Optics Express 2018)

Rows:
- `te0_blocking_filter` (mode_converter.other, D567): TE1 pass IL < 1.4 dB and TE0 blocking extinction >= 21.0 dB
  over 1535-1570 nm (measured, normalized to on-chip reference structures); design geometry (period 315 nm, L 10 um,
  bus 600 nm / SWG 800 nm derived from um, 220 nm / 3 um / 1 um stack).
- `te1_blocking_filter` (mode_converter.other): TE0 IL <= 1.0 dB, TE2 IL <= 2.3 dB, TE1 extinction > 25.6 dB over
  1540-1566 nm; design geometry (period 330 nm, L 20 um, bus 1000 nm / SWG 700 nm).
- `te_grating_coupler`: 7.0 dB per port at 1550 nm (measured, D167, method unspecified), period 630 nm, fill factor
  0.48 (derived from 48 %, definition not printed), etch 70 nm.
- `te1_mode_mux`, `te2_mode_mux` (mode_converter.mdm_mux): IL 0.7 / 1.3 dB, scope unspecified, C band inferred;
  access / bus widths.

Not entered:
- SWG duty cycle 60 % and waveguide gap 50 nm on both filters: `fill_factor` and `gap_nm` are not allowed for
  `mode_converter` (in component notes; registry gap below).
- Calculated periods 323 / 338 nm (in notes on the period rows).
- Adiabatic access taper lengths 6.4 / 10.0 / 21.1 / 4.7 / 12.1 um (devices #1 / #2 / #5 / #6 / #7, p.6) and the
  ~0.8 deg taper angle: geometry of separate tapers with no performance value (rule 9).
- Simulated responses (Fig. 6 dashed curves; Figs. 3-4 field maps): no printed values.

Judgment calls:
- TE1 filter "insertion losses ... are 1.0 dB and 2.3 dB ... in the wavelength range": entered as `le` maxima over the
  band (Fig. 6(b) traces, abstract "<=2.3 dB", summary "lower than 2.3 dB").
- TE1 extinction 25.6 dB: body prints no qualifier, summary "below -25.6 dB" -> `gt`; TE0 extinction `ge` from the body
  ">=21.0 dB". The abstract calls both values "crosstalk"; stored as `extinction_db` (blocked-mode suppression, D567
  zhang2022a precedent).
- Mode (de)MUX IL 0.7 / 1.3 dB: no citation on the sentence and the devices are on this chip, so kept as this paper's
  measured values; the design is ref. [11] (another group). Scope (per stage vs MUX + de-MUX pair) and wavelength not
  stated -> `unspecified`, C band inferred. An auditor may prefer `author_estimate`.
- Fab: "We fabricated the devices" (p.5), all authors at SJTU -> `org_shanghai_jiao_tong_university`; facility AEMD
  (acknowledgment "support in device fabrications", p.7) -> `org_center_for_advanced_electronic_materials_and_devices`
  (hu2020 / cai2021 precedent). Applied to all five rows (all on the fabricated chip).

Missing fab / facility orgs: none.

## lit:xu2013 (slotted PhC nanobeam cavity sensor, Optics Express 2013)

Rows:
- `slotted_nanobeam_cavity` (resonator.photonic_crystal): measured Q ~9200 (vacuum, ~1583 nm read off Fig. 2(e)), ER
  > 10 dB, resonance ~1583.0 nm (figure read), Q ~4700 in 25 % NaCl (~1589 nm, Fig. 3(a)); simulated Qtot 3.73e6,
  Qcoupling 8.883e6 (`q_external`), Qrad 6.43e6 (`q_intrinsic`) at 1546.5 nm; geometry a = 410 nm, slot 200 nm, Wy(0)
  1230 nm / Wy(20) 2460 nm / Wx 164 nm (derived from multiples of a), imax 20, 220 nm / 2 um stack, footprint 42 um2
  (16.8 x 2.5 um2).
- `ridge_slot_butt_coupler` (mode_converter.converter, strip-to-slot precedent grottke2020 / deng2016): calculated
  coupling efficiency ~84 % (simulated, 1550 nm inferred), ridge 700 nm, slot 200 nm.

Not entered:
- Bulk refractive-index sensitivity: measured ~410 nm/RIU (p.5, Fig. 3(b)), simulated 437 nm/RIU (p.4) and ~413 nm/RIU
  (p.5): no parameter (registry gap below).
- Simulated mode volume 0.217 (lambda/n)^3 (p.3): no parameter.
- Higher-order mode ~15 dB weaker than the fundamental (p.5-6): no clean parameter.
- Fig. 1(e) / (f) simulated curves (Q > 1e6 over a wide range, slot-width trade-off): curves only.
- Grating couplers (period 645 nm, 50:50 duty, 70 nm shallow etch, 10 um wide), 200 um ridge taper and 300 um slot
  taper: geometry only, no performance value (rule 9).
- Cavity cladding thickness: the 500 nm PMMA covers the chip but a sensing window is opened over the cavity, so no
  `cladding_thickness_um` on the cavity row (noted).

Judgment calls:
- Unqualified Q -> `q_loaded` (skill pitfall). Measured resonance wavelengths are figure reads with
  `wavelength_inferred: true`; note that the 0 % NaCl (DI water) peak in Fig. 3(a) sits near 1571 nm, below the
  ~1583 nm vacuum peak of Fig. 2(e); the paper does not say whether both spectra come from the same device (not
  entered beyond the two readings).
- Simulated Qtot 3.73e6: p.4 says the device is PMMA-covered "for our simulations" of the index response; whether the
  p.3 Q run includes it is not stated (noted on the three simulated Q rows).
- Fab / facility empty: passive "were fabricated" with no org named (D80b); SOITEC wafer supplier in notes.

Missing fab / facility orgs: none.

## Registry gaps

- `gap_nm` and `fill_factor` for `mode_converter` (he2018 p.3 / p.4: gap 50 nm, SWG duty cycle 60 % on both blocking
  filters; same gaps already reported for mode_converter in D533 / D567).
- `sensitivity_nm_per_riu` (resonator, unit nm/RIU): bulk refractive-index sensitivity, resonance shift per refractive
  index unit of the surrounding medium (xu2013 p.5 measured ~410 nm/RIU over n 1.333-1.378 NaCl solutions, linear
  fit; p.4 simulated 437 nm/RIU).
- `mode_volume_lambda_n3` (resonator, unit (lambda/n)^3): effective mode volume (xu2013 p.3 simulated 0.217).
