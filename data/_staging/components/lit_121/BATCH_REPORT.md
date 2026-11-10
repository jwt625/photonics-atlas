# lit_121 batch report (2026-11-09)

All seven cached texts match their source rows (page-1 title); none is another paper or only a correction / erratum; no
garbled text layer is flagged. melus2025 is the corrected version of the article (p.1 states a correction dated 2026-04-03);
the full text is present, so it was distilled. Supplements are not cached for any paper. Figure values were read from the
cached `page_NN.png` renders. Dry-run: +14 components, +151 metrics, 0 errors; the one warning (ni2025b m18 / m4) is on an
existing merged row, not from this batch. All sources are `restricted_local_only`: no quotes in the output.

| paper | components | metrics |
|---|---|---|
| zhu2025 | 3 (crossing.swg 2: without / with side SWGs; mode_converter.converter 1, slot-to-SWG-SW converter, simulated only) | 30 |
| hu2021 | 3 (fiber_chip_coupler.edge 2: headline + 400 nm lower-tip sibling; waveguide_platform.straight 1) | 34 |
| melus2025 | 1 (fiber_chip_coupler.edge, topology-optimized SiN) | 19 |
| tao2025 | 2 (fiber_chip_coupler.grating 2: fabricated TE GC + TM design row) | 26 |
| morishima2021 | 1 (fiber_interface.connector, MCF LC connector) | 5 |
| chen2022a | 2 (splitter.directional_coupler + polarization.other, one physical device, D396) | 17 |
| ito2022 | 2 (polarization.psr; splitter.mmi, simulated only) | 20 |
| total | 14 | 151 |

## Fab / facility orgs

- zhu2025: fab `org_applied_nanotools` (p.9-10 Sec. 4: fabrication carried out at Applied Nanotools with its commercial
  220 nm SOI MPW process). `process_name` "Applied Nanotools commercial 220 nm SOI MPW process (EBL, ICP-RIE)".
- hu2021: fab `org_huazhong_university_of_science_and_technology` (p.4 Sec. 3, first-person fabrication, all authors at
  WNLO, HUST); facility `org_center_of_micro_fabrication_and_characterization` + `org_center_for_nanoscale_characterization_and_devices`
  (p.9 Acknowledgments, facility support). LNOI wafer from NANOLN in notes (supplier).
- melus2025: fab `org_aim_photonics` (p.3 Sec. 2: fabricated on a research variant of the AIM Photonics nitride-only
  (SENS) MPW process; abstract: foundry 300 mm process). `process_name` "AIM Photonics nitride-only (SENS) MPW process,
  research variant (300 mm)".
- morishima2021: fab `org_sumitomo_electric_industries` (p.3 Sec. 3, first-person fabrication, all authors at Sumitomo
  Electric Industries).
- tao2025, chen2022a, ito2022: fab empty (passive fabrication sentences with no org, D80b). ito2022 thanks three named
  people for fabrication support without an org (D84b needs the org; suzuki2014 precedent, D543).
- Missing orgs: none.

## Not entered, and why

zhu2025
- Return loss (RL) of the crossings (simulated < -20 dB, < -40 dB at 1552 nm; side-grating design < -18 dB, about -35 dB
  at 1560 nm) and of the converter (< -20 dB): `back_reflection_db` is not allowed on crossing / mode_converter (gap below).
- Simulated fabrication tolerance (+/-30 nm period / pitch width: IL < 0.5 dB, CT < -35 dB), side-grating geometry
  (150-700 nm distance, n4 = 13), hollow-square widths W1 / W2, grating widths Wi / Wf1 / Wf2: notes only (no parameter).
- Table 1 bandwidth (Exp. 80 nm) is the grating-coupler-limited measurement span, not a device bandwidth.
- Grating couplers and TE reference waveguides: no own numbers.

hu2021
- Fig. 8(a) X-direction 1-dB tolerance (about -1.3 / +1.5 um): axis role not stated (Z is called lateral in Fig. 4); not
  entered. The printed 0.6 dB at 1 um offset is in the note of the Z row.
- Temperature cycling (< 0.01 dB variation, -45 to 75 C), simulated overlay tolerance (< 0.1 dB / < 0.004 dB at 200 nm):
  notes (no parameter).
- Other tip widths of Fig. 7(b) (260-460 nm series): only the 400 nm point is printed in the text; the headline device's tip
  width is not stated (D159: not tied to a Fig. 7(b) point).
- Lower slab widths TW2-TW4 (1.5 / 1.8 / 4 um): notes (no role-specific parameter).

melus2025
- 3-dB alignment tolerances (full widths: 2.75 / 2.83 um horizontal, 3.17 / 3.22 um vertical TE / TM, Fig. 8 caption):
  no 3-dB or vertical tolerance parameter; the horizontal 1-dB half-widths were read off Fig. 8(a) instead
  (`extracted_from_figure`, about 0.8 um, +/-0.1 um).
- Fiber-chip etalon FSR (63 / 53 nm): property of the air gap, not the coupler.
- Table 1 values of other couplers: comparison table of other works (rule 3).

tao2025
- Waveguide attenuation 4.9 dB/cm: printed as a typical value with citations (refs. 5, 43) -> cited value, not entered. The
  GC loss rows that subtract it are `author_estimate` (D428); the 1-dB bandwidth and back-reflection rows do not depend
  on it and stay `measured`.
- Coupling-angle tolerance (< 1 dB drop within +/-2 deg, measured and simulated): no angular-tolerance parameter (gap).
- Intermediate design steps (2D results, SiC 400-550 nm variants > -0.82 dB): not separate designs of interest; notes.

morishima2021
- Random-mating result (average 0.07 dB, <= 0.21 dB for > 97 %, max 0.39 dB, 2688 samples; also in the abstract): the
  Fig. 9 caption and the Grade B sentence cite the authors' preliminary paper ref. 8, so the values are treated as
  reproduced from it (D259a / D408 caption clause) and kept in component notes. **Coordinator decision**: these are the
  paper's headline numbers; if the journal paper is judged to re-present its own measurement (D408), add them back
  (insertion_loss_db mean 0.07, max 0.39, n_samples 2688, per_interface; wavelength not stated).
- Per-test IL / RL maxima of Tables 2-3: one summary row per table (largest IL, smallest RL), per-test values in notes.
- MCF MFD (8.3-8.5 um at 1310 nm, cited ref. 9), < 0.20 deg rotational alignment, 0.7 N mm torque threshold (simulated):
  notes.

chen2022a
- Measured "IL < 1 dB over 1460-1580 nm" rests on a per-port -3 +/- 0.5 dB criterion: a split deviation (D401), not
  entered as loss; the matching 120 nm "operation bandwidth" is entered in `bw_1db_nm` with the definition in the
  condition (lu2015a / D539 precedent).
- Simulated tolerances, TE bandgap 1414-1678 nm and the 4.03 um coupling length: notes.

ito2022
- Port power difference < 0.8 dB, TE purity > 98 %: `imbalance_db` is splitter-only; notes.
- Simulated TM0 -> TE1 conversion 95 % at L = 700 um and the taper geometry (2.0 -> 3.2 um over 700 um): no
  conversion-efficiency or taper-length parameter on `polarization` (gap below); notes. Total length 750 um entered as
  `length_um`.

## Judgment calls

1. zhu2025 per-crossing IL (about 0.4 / 0.1 dB): the paper averages a cascade by the number of crossings after
   normalizing to reference waveguides -> `derived` + `reference_structure` (he2025 precedent); the number of crossings is
   not stated. The 576 nm "IL < 1 dB and CT < -30 dB" span is entered as `simulated` although p.10 once calls Fig. 15
   "measured" (the same sentence and the conclusion say simulation; the measurement stops at 1580 nm). Platform
   `soi_slot` for the SWG slot-waveguide crossing and its converter.
2. hu2021 per-facet losses (0.54 / 0.59 dB) `measured` + `loss_breakdown` (D167): the deducted splice and waveguide loss
   are the authors' own measurements, but the waveguide length and the arithmetic are not printed. The "polarization
   extinction ratio < 0.05 dB" is entered as `pdl_db` (it is the TE / TM loss difference). Platform `sion` (facet layer,
   D82f). `power_handling_dbm` 30 = highest tested power with a stated 0.4 dB degradation (he2019 precedent).
3. melus2025 losses `derived` (Eq. (2) ratio of three own measurements, D80a), scope `per_coupler`. Simulated
   reflectance percentages converted to `back_reflection_db` stay `simulated` (D83f). Lensed-fiber MFD 6.4 um
   `specification` (Table 1; origin not stated).
4. tao2025 platform `other` (4H-SiC; sun2025a / wang2021 precedent). Fill factor is the tooth fraction (groove width =
   (1 - F) x period, p.4). The TM grating coupler is a `row_kind: design` row (one simulated IL value).
5. chen2022a split into `splitter.directional_coupler` (excess loss, bandwidth, geometry) and `polarization.other` (TM / TE
   extinction as `per_db`, pita2023 precedent) per D396. The cascade-slope IL 0.66 dB is `excess_loss_db` `measured`
   (standard fit, the paper's IL is defined beyond the 3 dB split).
6. ito2022 excess on-chip loss (< 2.5 / < 3.8 dB) `derived` + `de_embedded` (device minus straight-waveguide reference).
   MMI excess losses from simulated 99.4 / 99.8 % transmission stay `simulated` (D83f).
7. morishima2021 platform left empty (connector precedent rows have no platform).

## Registry gaps (skipped value + locator, proposed definition)

- `back_reflection_db` on `crossing` and `mode_converter`: zhu2025 crossing RL < -20 dB (sim, p.7 Fig. 8(a)), < -18 dB
  (side gratings, p.8), converter < -20 dB (p.5 Fig. 6). Same definition as for couplers (positive dB below the input).
- Angular (fiber-tilt) 1-dB tolerance `tol_1db_angle_deg` on fiber_chip_coupler: tao2025 < 1 dB drop within +/-2 deg
  (p.8 Sec. 3, Fig. 6(a)). Definition: fiber-angle deviation from the optimum for 1 dB excess loss (+/- half-width).
- 3-dB alignment tolerance and vertical tolerance (`tol_3db_lateral_um` full width or half width, `tol_1db_vertical_um`):
  melus2025 Fig. 8 caption (p.9). Existing candidate (D432).
- `coupling_efficiency_pct` and `taper_length_um` on `polarization`: ito2022 TM0 -> TE1 conversion 95 % (sim, p.4 Fig.
  3(a)), taper 700 um (p.2 Fig. 1). Existing candidate list D439.
- `imbalance_db` on `polarization`: ito2022 port power difference < 0.8 dB (p.7).
