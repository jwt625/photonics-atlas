# cov_tsmc2 batch report

Date: 2026-11-07. Contract: pic-component-distill v4-v6. One paper: `lit:lu2025a` (OFC 2025 Th1G.2, TSMC,
"Low-loss High-uniformity Silicon Nitride Optical Building Blocks Integrated on Silicon Photonics Platform",
DOI 10.1364/ofc.2025.th1g.2). Page-1 title of `references/lu2025a/text.md` matches the source row; not a correction.

Validation: `uv run --offline python scripts/merge_component_staging.py data/_staging/components/cov_tsmc2 --dry-run`
-> +10 components, +57 metrics, errors 0.

## Components (10) and metric rows (57)

| component | class | metrics | key values |
|---|---|---:|---|
| sm_wg_pecvd_opt | waveguide_platform.straight | 5 | 0.16 dB/cm at 1311 nm (text); figure medians 0.12 / 0.15 / 0.19 at 1271 / 1291 / 1331 |
| mm_wg_pecvd_opt | waveguide_platform.straight | 5 | 0.124 dB/cm at 1311 nm (text); figure 0.085 / 0.12 / 0.14 |
| sm_wg_pecvd_base | waveguide_platform.straight | 2 | ~0.4 dB/cm at 1311 nm (baseline PECVD, text) |
| mm_wg_pecvd_base | waveguide_platform.straight | 2 | ~0.4 dB/cm at 1311 nm (baseline PECVD, text) |
| bend_r30 | waveguide_platform.bend | 6 | median ~0.004 dB per 90 deg at 1311 nm (text); figure 0.0021 / 0.0030 / 0.0050 |
| taper_sm_mm | waveguide_platform.other | 7 | 0.0009-0.0013 dB (figure only), 50 um, 800 nm to 1.5 um |
| crossing | crossing.other | 4 | 0.023 / 0.028 / 0.034 / 0.040 dB (figure only) |
| mmi_1x2 | splitter.mmi | 4 | excess 0.076 / 0.043 / 0.031 / 0.048 dB (figure only) |
| sin_si_transition | waveguide_platform.transition | 10 | ~0.03 dB TE, ~0.06 dB TM at 1311 nm (text); 6 figure medians; PDL < 0.038 dB; Si tip < 90 nm |
| edge_coupler | fiber_chip_coupler.edge | 12 | < 1 dB O-band (loopback config, scope unspecified); PDL < 0.2 dB; per facet TE 0.74-0.89, TM 0.70-0.83 dB (figure medians); std 0.1 dB (1260-1350 nm); 5 um MFD lensed fiber |

All rows: platform `sin` (transition `si_sin_multilayer`), row_kind fabricated, `fab_org_ids` org_tsmc. Fab basis
(D80b): platform statement "on TSMC's silicon photonics platform" (p.1 Abstract) plus the integration statement
(p.1 Sec. 1) and the acknowledgment of TSMC's fabrication teams (p.3); all authors TSMC. No facility.

Figure values: box-plot median lines read from 600 dpi page renders with pixel positions against the frame
(calibrated on the axis end labels); uncertainty per row in notes (0.0002-0.01 dB, 0.01 dB/cm). Where the box is too
thin to resolve the median line, the box center was used and the box span is noted. Text values at 1311 nm are
`measured`; the figure median at 1311 nm is cited in their notes, not entered twice. Method `unspecified` throughout
(the paper names no cutback / reference structure; sample counts not stated).

## Not entered

- LPCVD baseline waveguides (Fig. 2(a), third panel): comparison process, not described in the text (where or how it
  was deposited not stated); boxes span about 0.2-0.44 dB/cm (SM) and 0.0-0.43 dB/cm (MM).
- PECVD baseline at 1271 / 1291 / 1331 nm (figure only): only the 1311 nm "~0.4 dB/cm" text value entered.
- Bend 3-sigma "~0.001 dB" at 1311 nm: no 3-sigma statistic in the registry (kept in the component notes).
- Edge-coupler tip width: "optimized", value not given. SiN thickness, cladding stack, MMI and crossing dimensions:
  not given.
- Thermo-optic coefficients (Si, SiN) and the ~21 dBm power figure: cited from refs [2]-[4] (rule 3).
- Si grating coupler, MZM, MRM, Ge PD in Fig. 1: schematic only, no values.

## Judgment calls

- Bend: `bend_loss_db_per_90` from the quarter-circle schematic of Fig. 2(b); the text gives "median insertion loss"
  without an angle or a statement on subtracting arc propagation loss.
- 1x2 MMI: the axis says "IL (dB)" but the values (0.03-0.08 dB) exclude the 3 dB split -> `excess_loss_db`.
- SM-to-MM taper: in-layer width taper -> `waveguide_platform.other` (precedent: in-layer tapers in the merged table).
- Edge coupler "< 1 dB over the entire O-band" (loopback configuration): scope `unspecified`. Its Fig. 4(a) spectra
  (0.65-0.96 dB TE, 0.79-0.85 dB TM) sit at the level of the per-facet panels Fig. 4(b)-(c), so it is probably a
  per-facet (halved or normalized) value, but the paper does not say. Per-facet panels: scope `per_facet` as printed.
- PECVD baseline: separate process = separate component rows (sm/mm_wg_pecvd_base), ~0.4 dB/cm stated once for both.

## Questions

1. Edge coupler "< 1 dB" loopback statement: keep scope `unspecified`, or rule it `loopback_half` given that Fig. 4(a)
   matches the per-facet panels? Same for the per-facet box plots (`per_facet` as printed vs `loopback_half`).
2. Registry gap: a 3-sigma statistic (bend "3-sigma variation of ~0.001 dB", p.2). Proposal: statistic `three_sigma`
   (value = 3 x standard deviation as printed), so foundry uniformity figures enter without conversion.
3. LPCVD baseline waveguides (Fig. 2(a)): enter as figure-only rows (fab not attributable to the platform), or keep out?
4. Benchmark: the TSMC SiN column can now take SiN 0.16 dB/cm (SM, 1311 nm), SiN-Si transition ~0.03 dB (TE),
   edge coupler about 0.75-0.84 dB per facet at 1311 nm (figure medians) and crossing ~0.034 dB at 1311 nm (figure).
   Use the text values only, or also the figure medians?

## Registry gaps / missing orgs

- 3-sigma statistic (question 2). No missing organizations (org_tsmc exists).
