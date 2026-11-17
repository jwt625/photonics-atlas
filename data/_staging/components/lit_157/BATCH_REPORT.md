# Batch lit_157 report

Distilled 2026-11-16 under the pic-component-distill skill (Contracts v4-v7). Papers: lit:hickstein2019, lit:du2024,
lit:chen2023d, lit:chen2021b, lit:yan2021. Totals: 22 components, 153 metric rows. Validation:
`merge_component_staging.py data/_staging/components/lit_157 --dry-run` -> +22 components, +153 metrics, 0 errors (the
one warning concerns another batch, cmp_lit_ni2025b_pimmwc). Page-1 titles match the source rows for all five texts;
none is a correction / erratum; no garbled text layer flagged.

## lit:chen2021b (Optics Letters 2021; cached arXiv 2101.06994) - 4 components / 33 metrics

- `er_lnoi_amp_5mm` (amplifier.rare_earth, lnoi_rib): net internal gain 5.2 dB / > 10 dB/cm at 1531.6 nm, 1.8 dB /
  3.6 dB/cm at 1550 nm, 0.5 dB at -10 dBm signal, transparency pump < 1 mW, internal conversion efficiency 0.2 %,
  signal-enhancement span >= 50 nm (1520-1570 nm), geometry.
- `er_lnoi_wg_5mm` (waveguide_platform.straight): 1.13 dB/cm Fabry-Perot fringe value, 1 dB on-chip at 1530 nm, 5 dB
  on-chip at 980 nm (17 - 12 dB reference comparison), geometry.
- `er_lnoi_ring_r100` (resonator.ring): linewidth 17.5 pm, Qi 176,000, ~2 dB/cm, radius 100 um.
- `lensed_fiber_facet` (fiber_chip_coupler.edge): 11 dB two-facet coupling at 1530 nm (loss_breakdown), 6 dB per facet at
  980 nm (half of the short-waveguide 12 dB), fiber-to-fiber ~12 dB (1530 nm) and 17 dB (980 nm).
- Not entered: signal-enhancement peaks (Fig. 2(b)), "at least 50 dB" dynamic range, projected ~1 % saturated conversion
  efficiency, Er-absorption share of the loss (rests on "typically ~400,000" Q of undoped rings, no data shown), bulk
  Er:LN comparison values (refs. 22-24).
- Judgment calls: all gain rows `author_estimate` (net gain = enhancement minus the 1 dB loss estimate that rests on an
  assumed near-critical coupling, D403 / bonneville2020 precedent). FP-fringe 1.13 dB/cm entered `measured` as a D394
  analogue, although the facet reflectance is a simulated modal value rather than the bulk Fresnel value; audit may
  prefer `author_estimate`. Fig. 4 signal wavelength not printed: the 0.5 dB row is 1531.6 nm `wavelength_inferred`; the
  0.2 % row has no wavelength. The printed rib height + slab (320 + 340 nm) is below the 700 nm film; both kept.
- Fab: none (passive sentences; CityU + Tianjin authors, D80b). Suppliers in notes: OST photonics (Er:LN crystal),
  NANOLN (ion slicing). No facility named.

## lit:yan2021 (cached arXiv 2105.00214v1, page 1 dated 3 January 2022) - 3 components / 21 metrics

The cached copy is the arXiv preprint of the listed journal paper; values are what this preprint prints, the journal
version was not read.

- `er_lnoi_spiral_amp_5p3mm` (amplifier.rare_earth, lnoi_rib): 8.3 dB max internal net gain and ~15.6 dB/cm at 1530 nm
  (-10.7 dBm signal, 10.78 mW pump), 7.3 dB figure read at -5.1 dBm signal, 40 nm net gain bandwidth (1530-1570 nm),
  length, footprint, width, sidewall, film, BOX.
- `er_lnoi_ring_r30` (resonator.ring): Q_L 5e4 (measured), Q_I 5.4e4 and ~6.86 dB/cm (author_estimate, D403 / D76),
  radius, width.
- `dual_period_gc` (fiber_chip_coupler.grating): 13.4 dB (1550 nm) and 16 dB (980 nm) per coupler (D167), periods 900 /
  1050 nm, duty cycles 0.33 / 0.46 (undefined, D253).
- Not entered: min bend radius 25 um (no bend-radius parameter on amplifier), "thickness around 350 nm" (layer role not
  stated; never guess), ~3.64 dB spiral loss (note), comparisons with refs. 29-33.
- Judgment call / conflict (D417): the printed "net gain bandwidth of 1530-1570 nm" is kept, but Fig. 5(d) points near
  1535 / 1540 / 1550 / 1570 nm read below the 3 dB level its shading marks (all points 1520-1570 nm are above 0 dB).
- Fab: org_shanghai_jiao_tong_university ("we fabricated", p.3 conclusion; all authors SJTU, D72 / D80b). Staff
  thanks for ICP-RIE help (no org) is not a facility.

## lit:hickstein2019 (Nature Photonics 2019; cached arXiv 1806.07547v1) - 5 components / 30 metrics

- One frequency_converter.shg row per waveguide width (650 nm thick air-clad LPCVD Si3N4, 12 mm, widths 1.9 / 2.0 /
  2.1 / 2.2 / 2.3 um): peak CW SHG efficiency (2.1 um printed 0.0025 %/W `measured`; others read off Supp. Fig. S6 on
  the x10^-4 %/W axis), photo-induced grating period (Supp. Fig. S5 dashed means / Fig. S3(c)), width, thickness,
  length, BOX.
- Not entered: fs-pumped ~1 % total conversion efficiency (Fig. 2(a)) and "in some cases spanning 60 nm" CW bandwidth
  (waveguide not identified, D159; bound in notes); chi(2)eff 0.5 pm/V (no parameter); grating lengths 4.45 / 1.05 /
  6.63 mm (no grating-length parameter on frequency_converter; in notes); Fig. 3 analytical projections; f-2f / fceo
  SNR 30 dB (system result); 700 nm chip (no values).
- Judgment calls: `poling_period_um` used for the self-organized (all-optically poled) QPM grating period, with the
  mechanism in notes; audit may prefer a registry gap. Supp. Fig. S5 period axes are labelled mm while the values are
  um (noted). Main text "SONGs extend for 2-6 mm" vs the 1.05 mm fit for 2.1 um (D417 note). Methods once say
  "600-nm thickness" next to the 650 nm sample (noted). Widths printed in nm somewhere in the text keep
  `design_target`; 2.2 um only printed in um -> `derived` (D256).
- Fab: org_national_institute_of_standards_and_technology ("The waveguide fabrication took place at NIST in
  Gaithersburg", p.6 Methods A; stated place, D448). No facility named.

## lit:du2024 (Optics Express 2024; cached arXiv 2312.17464v2) - 4 components / 37 metrics

- Three fiber_chip_coupler.edge rows, one per wafer tip width (160 / 165 / 175 nm): per-facet loss as `loopback_half`
  + method `cutback` (coupler pairs, propagation removed by the 3-22 mm length series, halving not shown: D167 /
  D452). 165 nm: best 0.64 dB (printed, measured) + median figure read; 160 nm: median 1.17 dB (printed) + best figure
  read; 175 nm: both figure reads; simulated per-facet loss from the Fig. 5 model curve on each; two taper stage lengths,
  straight width 650 nm, Si 250 nm, BOX 3 um, cladding 2 um, UHNA7 MFD 3.2 um (specification).
- `uhna7_smf28_splice` (fiber_interface.other, silica): splice loss < 0.1 dB, MFDs 3.2 / 10.4 um, ~1 cm UHNA7 tip.
- Not entered: ten-day stability +/- 0.1 dB and +/- 0.1 dB within +/- 10 um holder movement (no parameter; the holder
  movement is not a fiber-to-chip displacement, so not tol_1db); photon-pair source results (coincidence rate,
  heralding efficiency, CAR, g2: no registry parameters, D250); 8 mm Si waveguide loss (not printed); Table 1 / Table 3
  values of other works.
- Conflict noted (D417): BOX 3 um (Sec. 3.1) vs 2 um (Fig. 1 caption); 3 um entered.
- Fab: none (passive, no fabricator named; authors at NUS, SUTD, A*STAR IME, TII). No facility named.

## lit:chen2023d (cached arXiv 2307.11671v1, preprint source row) - 6 components / 32 metrics

- Four frequency_converter.shg rows (adapted / periodic poling x 3 / 21 mm): peak efficiency 138 / 135 / 9500 / 1100
  %/W (measured, peak wavelengths read off Fig. 2 and flagged inferred), poling-period traces read off the Fig. 2
  insets, length, width 1.8 um, etch 350 nm, film 600 nm. Adapted 21 mm also: 82.5 % absolute conversion (16.5 mW SH
  from 20 mW) and 200 pm/K temperature tuning (printed 0.2 nm/oC, derived).
- Population row (D165): average intrinsic normalized efficiency 2044 +/- 150 %/W/cm2 `author_estimate` (Eq. 13 rests
  on the calculated dispersion factor and an ideal sinc model).
- `tfln_rib_wg` (waveguide_platform.straight): 0.76 dB/cm (1550 nm) and 0.69 dB/cm (775 nm) inferred from resonator Q
  (resonators not shown, author_estimate).
- Not entered: SH bandwidth 0.97 nm and group-velocity mismatch 164 fs/mm (no frequency_converter parameters),
  theoretical limits 10500 %/W and 2388 %/W/cm2, simulated 0.34 nm/C, Fig. 3(a) other lengths, self-calibrated ratio
  (Fig. 3(b)), mean transmissions Tf 0.085 / Tsh 0.040 (population calibration inputs, in conditions), duty cycle 49 %
  +/- 4 % (fill_factor not allowed on frequency_converter; in core_material), projections for 90 mm, Fig. 4 values of
  other works.
- Judgment call: the 0.2 nm/oC tunability sits in the 21-mm paragraph and is placed on the adapted 21 mm row (noted).
- Fab / facility: University of Arizona (fab; p.7 author contributions "P.C. fabricated the device" + p.7
  acknowledgment) and "OSC cleanroom at the University of Arizona" (facility, p.7) are missing from the registry; ids
  left empty.

## Missing fab / facility orgs (for the org round)

| Name as printed | Role | Paper | Locator | Rows |
|---|---|---|---|---|
| University of Arizona | fab (author P.C., all authors at University of Arizona units) | lit:chen2023d | p.7 author contributions; p.7 acknowledgments | all 6 chen2023d rows |
| OSC cleanroom at the University of Arizona | facility | lit:chen2023d | p.7 acknowledgments | all 6 chen2023d rows |

## Registry gaps (value skipped, locator, proposed definition)

- frequency_converter phase-matching bandwidth: chen2023d 0.97 nm (p.5), hickstein2019 "in some cases spanning 60 nm"
  (p.3, device not identified). Proposed: `bw_fwhm_nm` / `bw_3db_nm` widened to frequency_converter (D429 candidate).
- frequency_converter group-velocity mismatch: chen2023d 164 fs/mm (p.5). Proposed `gvm_fs_per_mm`.
- effective chi(2) of an induced nonlinearity: hickstein2019 0.5 pm/V (p.8, 2.1 um waveguide). Proposed
  `chi2_eff_pm_per_v` (frequency_converter).
- QPM grating length distinct from device length: hickstein2019 1.05 / 4.45 / 6.63 mm (Supp. Fig. S5). Proposed
  `grating_length_um` widened to frequency_converter.
- poling duty cycle on frequency_converter: chen2023d 49 % +/- 4 % (p.3). Proposed `fill_factor` widened.
- coupling stability over time: du2024 +/- 0.1 dB over ten days (p.6). Proposed `coupling_stability_db` (span and
  duration in condition).
- amplifier signal dynamic range and signal enhancement: chen2021b >= 50 dB (p.4), enhancement spectrum (Fig. 2(b)).
  Proposed `dynamic_range_db`, `signal_enhancement_db` (amplifier).
- min_bend_radius_um on amplifier: yan2021 25 um (p.1).
