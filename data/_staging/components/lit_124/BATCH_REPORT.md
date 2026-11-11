# lit_124 batch report (distill, 2026-11-11)

Papers: papadovasilakis2023, chen2021a, papadovasilakis2022, zhang2026b, mao2021. All five cached texts match their
source rows (page-1 title); none is a correction / erratum; no garbled text layer. All sources are
`restricted_local_only`: facts and locators only. Validation: `merge_component_staging.py ... --dry-run` -> +24
components, +200 metrics, 0 errors (one pre-existing warning on a merged ni2025b row, not this batch).

## Per paper

| paper | components | metric rows |
|---|---|---|
| papadovasilakis2023 | 6 (BWIC and CWIC at 30:70, 40:60, 50:50) | 44 |
| chen2021a | 5 (1x2 MMI, 4x4 MMI, edge taper, ridge waveguide, TE 1x2 MMI design) | 38 |
| papadovasilakis2022 | 4 (WIC at SR 0.50 / 0.30 / 0.20 / 0.05) | 27 |
| zhang2026b | 8 (3 ASPDs, 2 measured converter links, 2 simulated converter designs, dual-mode switch) | 71 |
| mao2021 | 1 (SWG + slot DC PBS) | 20 |
| total | 24 | 200 |

### papadovasilakis2023 (Bezier vs circular WICs, GF 45-nm monolithic)

- Table 2 SR mean and SD per design (10 dies) as `split_ratio_pct` mean + std rows (fraction -> %, derived); wavelength
  span 1260-1360 nm inferred from Fig. 7 (Table 2 does not state the averaging range).
- IL of the 50:50 devices at 1260 / 1310 / 1360 nm (Table 2, Fig. 8(b)) as `excess_loss_db` mean + std, cutback,
  measured (cascade slope, Eq. (11)). Simulated IL read off Fig. 4(b) (BWIC 0.04-0.05 dB, CWIC 0.125 dB at 1360 nm).
- Footprint 36.3 x 3.8 um2 (derived product) on all three BWIC rows: the abstract states it for "the devices"
  (family statement applied to each, not one representative; auditor may prefer D254 handling).
- Not entered: Table 1 geometry normalized to L0 (L0 not printed); simulated SR targets 0.05 / 0.10 / 0.20 (no
  fabricated device, no printed number); Table 3 "max deviation 1.6 %" conflicts with the 0.6 % in text (note).
- Fab org_globalfoundries (MPW university program acknowledgment, papadovasilakis2023a precedent); process_name
  "commercial 45-nm monolithic process, 300-mm wafer (...)" from p.8.

### chen2021a (Z-cut TFLN TM MMIs, NUS)

- 1x2 MMI 0.268 dB by cutback (slope over 2 / 6 / 12 MMIs) = `excess_loss_db`; simulated 0.157 dB.
- 4x4 MMI: "total IL about 0.63 dB" entered `derived` (it is -10 log10 of the summed printed per-port values);
  `il_nonuniformity_db` 0.31 dB derived. Per-port ILs 6.6 / 6.85 / 6.54 / 6.62 dB not entered as rows (they include
  the 1/4 split; D401 analogue), kept in notes. Conflict: the Fig. 8(a) inset ordering of Port 1 / Port 3 differs
  from the printed assignment (D417 note).
- Edge taper (up-taper to 5 um at a diced facet): about 5 dB per facet, measured (D167), band C inferred.
  `tip_width_nm` 5000 used for the facet-end width (derived); auditor may prefer `width_nm`.
- Ridge waveguide 3.7 dB/cm "estimated" -> author_estimate.
- TE 1x2 MMI "under 0.05 dB" (discussion) as a `design` row, author_estimate (simulation not stated).
- Not entered: MMI length / width tolerances (no parameter); 4x4 access-waveguide width (not stated for the 4x4).
- Fab empty (passive fabrication, all authors NUS, D80b). Facilities named in the acknowledgment are missing (below).

### papadovasilakis2022 (WICs with narrow DCs, GF monolithic)

- Table 1 mean / SD per SR target, pooled over the three width variants and the O-band (population rows, D165).
  SR 0.50 also carries the cascade-macro results: SD 0.6 % at 1310 nm over 6 sites, best-device spectral deviation
  1.2 % (`coupling_variation` 0.012, derived), IL 0.16 dB at 1310 nm (printed; Fig. 7(b) reads 0.14-0.15 dB, D417
  note), 0.08 dB at 1260 and 0.38 dB at 1340 nm, simulated SD 0.4 %, footprint 60 x 40 um2.
- Conflict noted: SD 1.3 % (p.6) vs "mean SD of 1.2 % for the least stable device" (p.10).
- Measurement polarization not stated (TE design): polarization left empty.
- Not entered: 400 nm / 250 nm DC of the Fig. 1(b) SEM (simulation only, no performance); per-site box-plot spread
  0.011-0.026 (note).

### zhang2026b (SWG arbitrary-to-single-mode power dividers, Hebei / Southeast / Fuzhou / PML)

- ASPDs (TE2, TE3, TE0/TE1) as `splitter.other`, row_kind fabricated (on the fabricated links, D80e), all loss values
  simulated. Geometry from Table 1 (W1, W2, W5, W4, Lin, Lout) with roles in `condition`; TE0/TE1 W3 / W4 not entered
  (printed W4 = 1.8 um < W3 = 2.5 um, roles unclear).
- Measured links TE0-TE2 and TE1-TE3 (`mode_converter.converter`): IL and maximum crosstalk at 1550 nm and over
  1500-1600 nm, normalized to a reference link (GCs + ADC mode (de)multiplexers excluded). Simulated TE0-TE2 values
  on the same row; simulated TE0-TE1 and TE0-TE3 schemes (with an SWG pi phase shifter) as `design` rows.
- Dual-mode 2x2 switch (`switch_fabric.other`, D158): P_pi 34.5 mW (wavelength not printed: 1550 nm inferred),
  per-state IL at 1550 nm, excess loss < 1.5 dB and modal ER > 15 dB over 100 nm, TiW heater 200 nm.
- Not entered: TE4-TE7 ASPDs (supplement, family bound < 0.36 dB, D254); duty-cycle tolerance values (notes);
  "footprints below 9.5 um" (family statement); Table 2 "30 x 4" footprint (not tied to one converter); supplement
  multimode crossing (Supplement 1 not cached).
- Fab empty: "we fabricated" on an unnamed platform, authors at four orgs (D80b / D154). The text cites Fig. 9(b) for
  the switch result, the caption says Fig. 11(b) (noted).

### mao2021 (SWG + slot DC PBS, Tsinghua SIGS)

- Measured average IL per polarization and range (cutback over cascaded PBSs), ER per polarization and range as
  `per_db` (wanted / unwanted port ratio), simulated IL / ER bounds over 1260-1680 nm, simulated 1-dB bandwidth > 420 nm.
- Geometry: widths (wc = wt 600, slot 100, SWG taper 106 / 231 nm), 220 nm Si, 3 um BOX, 1 um SiO2.
- Not entered (registry gap): coupling length 4.6 um, gap 100 nm, SWG period 156 nm / tooth 86 nm.
- Not entered: four GCs used for the measurement (geometry only, no performance; not rows); +/- 30 nm tolerance
  simulations (worst IL 1 dB, ER 9.1 dB, notes).

## Missing orgs (not in organizations.csv / org_aliases.csv)

| name as printed | locator | role |
|---|---|---|
| E6NanoFab (facility at National University of Singapore) | lit:chen2021a p.9 Acknowledgements | facility (5 rows) |
| Spin and Energy Lab (SEL), National University of Singapore | lit:chen2021a p.9 Acknowledgements | facility (5 rows) |
| H-chip Technology Group | lit:mao2021 p.11 Acknowledgments ("for device fabrication") | fab (1 row) |

## Registry gaps (proposed)

- `coupling_length_um`, `gap_nm`, `subwavelength_period_nm` on `polarization` (mao2021 Table 1: Lc 4.6 um, wg 100 nm,
  Lambda 156 nm; same candidates as D439). Definitions unchanged; class allowance widened.
- Criterion bandwidth (`criterion_bw_nm`, D539 candidate) would hold zhang2026b's IL < 1 dB and CT < -15 dB
  working bands; entered as wavelength ranges on the IL / CT rows instead.

## Coordinator questions

1. papadovasilakis2023 footprint on all three BWIC rows (family statement) vs D254 (drop to notes)?
2. chen2021a edge coupler facet width as `tip_width_nm` (up-taper end) vs `width_nm`?
3. chen2021a 4x4 per-port ILs kept out of rows (D401 analogue): confirm.
