# lit_125 batch report (distill, 2026-11-11)

Papers: han2022, johnson2020, tahara2024, lin2021, hammond2022, shi2023, zeng2023. All seven cached texts are the
source-row papers (page-1 titles match); none is a correction / erratum; no garbled text layer. No supplement is
cached for any paper (lin2021 refers to Supplement 1 for several values). Figure values were read on page renders
of the cached PDFs. Validation: `merge_component_staging.py data/_staging/components/lit_125 --dry-run` -> +23
components, +209 metrics, 0 errors (the one warning printed concerns merged row `cmp_lit_ni2025b_pimmwc`, not this
batch).

## Per paper

| paper | components | metric rows | notes |
|---|---|---|---|
| han2022 | 3 | 22 | elliptical-taper crossing (fabricated), linear-taper crossing (fabricated, figure reads only), no-taper crossing (`design`, simulated only) |
| johnson2020 | 1 | 17 | MMI crossing, `crossing.mmi`, `soi_strip` |
| tahara2024 | 5 | 25 | metastructure GC (fabricated), flat-spectrum and 9-deg designs (`design`), Si waveguide (OFDR), on-chip SSC |
| lin2021 | 9 | 78 | four bi-layer edge-coupler designs, single-layer reference coupler, two SiN2-SiN1 transition rows (Wwg 0.38 / 0.52 um), SiN1 waveguide, 20 um bend (separate wafer run) |
| hammond2022 | 2 | 26 | single- and dual-polarization inverse-designed GCs, GF 45CLO |
| shi2023 | 2 | 10 | embedded multimode polymer waveguide, MPO / MT connector |
| zeng2023 | 1 | 31 | 4-channel O-band CWDM angled MMI on Ge-doped silica (`wdm.other`) |
| total | 23 | 209 | |

No paper has 0 rows.

## Values deliberately not entered

- han2022: simulated fabrication tolerance (IL change <= 0.02 dB, Fig. 7, p.7), the L3 sweep of Fig. 2 (design
  exploration), Table 3 comparison rows (cited works).
- johnson2020: backscatter -55 dB measured (p.7, Fig. 4(b)) and simulated -35.7 / -46.6 dB (p.5): no back-reflection
  parameter on `crossing` (registry gap below); fabrication-bias tolerance (Fig. 8) and wavelength-shift sensitivity;
  Table 1 comparison rows (cited).
- tahara2024: simulated power split Pu / Pd / Pr / Pp (Fig. 4(a)); beam divergence 8.3 x 7.2 deg (no
  `beam_divergence_deg` on fiber_chip_coupler, registry gap); PMF-to-SMF total 4.0 dB (kept in notes, the per-GC
  value is entered); spectral-oscillation amplitudes; simulated tolerances (Fig. 6).
- lin2021: simulated optimum coupling ~1 dB/facet at WEC ~0.15 / ~0.20 um and fiber-to-tip efficiency TM ~92 % / TE
  ~87 % at WEC 0.15 um (design sweep points, no fabricated or named design row); 3-dB alignment tolerances (D81);
  absolute TE 1-dB tolerances (only relative values in the text, absolutes in the uncached supplement); Fig. 3(d)
  measured Ltran 25 / 75 um points (no labelled values); SiN1 propagation loss at other wavelengths and the
  simulated loss spectrum (supplement not cached); Fig. 4(d) per-wavelength points beyond the best / worst reads.
- hammond2022: IL device-to-device spreads 0.89 dB (single) and 2.4 dB (dual), PDL variation 2.1 dB: notes only (no
  spread parameter for IL); standard-resolution simulated efficiencies 1.2 / 3.0 dB (notes).
- shi2023: bulk material loss 0.05-0.07 dB/cm (supplier material value), 3-dB misalignment tolerances (D81),
  adjacent-channel crosstalk < -44 dB (registry gap), channel bandwidth 234 GHz and 23 GHz x m (registry gap),
  30 Gb/s link result and 1.5 dB penalty (system level), pitch 250 um (`pitch_um` not allowed on waveguide_platform,
  D250).
- zeng2023: WMMI width sensitivity 43.75 pm/nm measured and 50 / 0.1 / 0.6 pm/nm simulated (registry gap); TM
  centre red-shift 2 nm (simulated); Table 3 comparison rows (cited); the SSC is cited from the authors' ref. [25]
  and not characterized here.

## Fab / facility organizations

- Missing from the registry (fab role):
  - "Reichle & De Massari AG (R&M)" (also printed "Reichle & De-Massari Holding AG"): assembled the MT ferrule
    receptacles (connectorization service), shi2023 p.3-4 Sec. 3 and acknowledgment p.9. Proposed fab on
    `cmp_lit_shi2023_mpo_mt_connector` (assembly only).
  - "SHIJIA, China" (printed "the PLC foundry, SHIJIA, China"): fabricated the AMMI CWDM, zeng2023 p.6 Sec. 3.
    Proposed fab on `cmp_lit_zeng2023_ammi_cwdm`.
- Printed-name check: han2022 prints "Singapore Advanced Micro Foundry" (p.5 Sec. 3), mapped to `org_amf`; the
  printed form is not an alias in `org_aliases.csv` (alias candidate). lin2021 prints "Advanced Micro Foundry" (p.3).
- No facility_org_ids in this batch (no shared facility named in any paper).

## Judgment calls

1. johnson2020 fab `org_university_of_bristol`: borderline. The fabrication section is first person ("we used" the
   resist, EBL and RIE steps, p.5) and all three authors are at Bristol; no fabricating org is named otherwise.
   Under a strict D80b reading the coordinator may empty it.
2. shi2023 waveguide fab empty: first-person board steps, but authors at SJTU and TTM Technologies (D154). Panasonic
   is the polymer supplier (note only).
3. lin2021 bend row: from a separate wafer run whose site is not stated, so fab is empty; other lin2021 rows `org_amf`.
4. lin2021 coupling losses use the paper's (Pout - Pprop - Pin) / 2: scope `loopback_half`, basis `derived` (D80a,
   D516 / D542 halving); printed ranges (+/-) kept in notes, n_samples 3 (3 chips, one device each, p.9) on the
   Fig. 4(c) values.
5. lin2021 transition losses are Fig. 5(c) slope labels (`measured`); polarization assigned by line style and leader
   lines. The 488 nm pair (0.28 / 0.27) has no leader lines and is assigned by marker proximity (flag for the audit).
   The transition is split into two rows by SiN1 width (0.38 um for 405-532 nm, 0.52 um for 594-640 nm; rule 9).
6. lin2021 platform `sin` on all rows; for the bi-layer couplers the facet layer is SiN2 (core_thickness 75 nm,
   D82f); the transition rows use core_thickness = SiN1 150 nm (lower) and layer2_thickness = SiN2 75 nm (upper),
   with width_nm = SiN2 Wbase and lower_width_nm = SiN1 Wwg.
7. hammond2022 per-GC IL from two-GC loopbacks: scope `loopback_half`, basis `measured` (no split arithmetic printed;
   D441 / D452 precedent). Single-pol centre wavelength: text and Fig. 5(a) say 1555 nm, Fig. 5 caption 1570 nm;
   1555 nm entered with the conflict in notes. Dual-pol simulated efficiency: text -5.6 dB vs Fig. 2 caption -3.0 dB;
   text entered, conflict noted (D417).
8. hammond2022 dual-pol polarization extinction stored as `crosstalk_db` (per_db not allowed on fiber_chip_coupler;
   it is the power ratio between the intended and the other output port, D424 PSR rule analogue). Band-edge span
   1525-1610 nm for the across-band ranges taken from the Fig. 6(c) / (d) axes.
9. tahara2024 GC efficiency 1.1 dB / 78 % `derived` + `loss_breakdown` (subtracted terms are the paper's own OFDR and
   SSC-pair measurements, D80a, not D428). Back reflections from printed % (9 % coupler, 4.5 % SSC) converted to dB
   and kept `author_estimate` (the paper estimates them from fringe amplitudes; D256a). Design etch depth 96 nm vs
   the 97 nm stated for the fabricated grating: 96 entered with a conflict note. Core thickness 210 nm is the design
   assumption (TEM-motivated), `design_target`. SSC platform empty (structure not described, D422 / D423).
10. han2022 cutback-slope losses `measured` (standard fit, D80a); the figure range rows `extracted_from_figure`. The
    elliptical crossing CT trace touches about -39 dB at noise peaks while the text says below -40 dB: printed bound
    kept, conflict noted.
11. zeng2023 per-channel ILs are fiber-to-fiber (text says they include coupling and propagation loss); wavelengths
    are the Table 1 channel design wavelengths with `wavelength_inferred: true`. Channel spacing 20 nm
    `author_estimate` (design grid, D82a). Simulated BPM ILs scoped `device_total` (AMMI only).
12. shi2023 0.48 dB/cm (Fig. 10(c) table) entered as `prop_loss_db_per_cm` with the condition that it is insertion
    loss normalized by length including the oil-matched end facets (the paper calls the facet term very small); the
    auditor may prefer to keep it only in notes.

## Registry gaps (skipped value + locator, proposed definition)

1. `back_reflection_db` on `crossing` (and `waveguide_platform`): johnson2020 -55 dB measured backscatter (p.7, Fig.
   4(b)), simulated -35.7 / -46.6 dB (p.5). Proposed: widen `back_reflection_db` to crossing ("reflection back into
   the input port, positive dB below the input").
2. `beam_divergence_deg` on `fiber_chip_coupler`: tahara2024 FFP 8.3 x 7.2 deg at 1540 nm (p.7); same candidate as
   D437.
3. `crosstalk_db` on `waveguide_platform`: shi2023 adjacent-waveguide crosstalk < -44 dB (p.6), about -60 dB at the
   adjacent waveguide centre (p.5). Proposed: widen crosstalk_db to waveguide_platform (array crosstalk, wording in
   condition).
4. Bandwidth-length product of multimode waveguides: shi2023 23 GHz x m (p.1, p.9) and 234 GHz for a 10 cm channel at
   780 nm (p.8). Proposed: `bw_length_ghz_m` (GHz*m, waveguide_platform / fiber_interface) and `bw3db_ghz` widened
   to waveguide_platform.
5. Fabrication sensitivity of the centre wavelength: zeng2023 43.75 pm/nm vs MMI width (measured, p.6-7, Fig. 7(b)),
   50 pm/nm simulated (p.5). Proposed: `width_sensitivity_pm_per_nm` (pm/nm, wdm / resonator / fiber_chip_coupler:
   centre-wavelength shift per nm of the stated dimension, dimension in condition).
6. Device-to-device spread of insertion loss: hammond2022 0.89 dB / 2.4 dB over six devices on three wafers (p.11).
   Proposed: allow statistic `range` with value / value_max only when both ends are printed, or a parameter
   `il_spread_db` (max minus min IL over a stated population).
