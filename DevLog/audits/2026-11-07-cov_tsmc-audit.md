---
title: Fresh-context audit of component batch cov_tsmc (TSMC COUPE ECTC 2025, NVIDIA ISSCC 2026 23.1; OFC 2026 M4B.2 and M2A.7 checked)
date: 2026-11-07
mode: read-only audit subagent; patch validated on a scratchpad copy of the batch (patch_component_staging.py 8 changes, re-apply 0 changes; merge_component_staging.py --dry-run "+4 components, +12 metrics; errors 0", only the pre-existing WARN on merged row cmp_lit_ni2025b_pimmwc-m18). Real batch CSVs not modified, nothing merged
patch: data/_staging/components/cov_tsmc/patch.yaml
---

# Audit cov_tsmc (2026-11-07)

Texts read in full: packaging atlas `references/ectc51687.2025.00015/text.md` (5 pages) with page renders p.2-p.4;
EO atlas `references/song2026/text.md` (3 pages) with `page_03.png` and `img_p03_1.png`; OFC 2026 M4B.2 extracted
text plus a 110 dpi render of its 3 PDF pages (scratchpad); EO atlas `references/patel2026/text.md` with `page_03.png`.
Page-1 titles match the source rows for all four. Fig. 23.1.5 (top left) re-read by a pixel scan of the embedded image
(plot frame located on the pixel grid: 0 / -50 dB at 9.24 px/dB, 1260 / 1360 nm at 6.12 px/nm). Locator convention
checked: `p.N` = text.md page (ECTC Fig. 5-8 on p.3, Fig. 4 on p.2; ISSCC figures on p.3, Fig. 23.1.1 caption on p.2).

BATCH_REPORT counts (4 components, 13 metrics) and its paper summaries are correct. One report statement is wrong: "strip
both rows' fab and the benchmark loses its only measured loopback_half TSMC GC value". The COUPE-GC row has an empty
platform, and `build_benchmark.py` `_family` places an empty-platform component only through `family_override` or
`unset_platform_family` (neither lists it), so the row reaches no column whatever its fab (Q6).

D259 / rule 3 check: the ECTC paper cites [3] (Yeh et al., IEDM 2024, TSMC; registered as `lit:yeh2024`, cached) after
"net insertion loss of 0 dB" (p.3 Sec. IV.A) and in the Fig. 6 caption. The cached yeh2024 text reports other numbers
(COUPE FAU coupling loss 0.3 dB, SPGC peak loss < 1.3 dB, 1-dB bandwidth about 20 / 25 nm in its Fig. 6 labels); none
of 1.2 dB, 0 dB / 0.04 dB or +/-1.7 nm appear there. The ECTC paper calls these its first COUPE silicon results (p.2
Sec. I; p.4 Sec. VI). So the [3] marks credit the PIC process, and no value is reproduced from earlier work.

## Counts

| | ok | imprecise | wrong | miss (added) |
|---|---|---|---|---|
| metrics (13) | 8 | 4 | 1 | 0 |
| components (4) | 2 | 2 | 0 | 0 |

ok metrics: coupe_gc-m4, -m5; coupe_lens_path-m1, -m2; song2026_rx_mrr_filter-m1 to -m4.

## Findings

| row | finding | evidence (locator) | patch |
|---|---|---|---|
| coupe_gc-m1 (1.2 dB lt, loopback_half) | value, qualifier, scope ok ("less than 1.2 dB (half-loopback)"); imprecise `wavelength_inferred: true`: the Fig. 6 x-axis states the band for this spectrum. Fig. 6 is a smooth curve without wavelength ticks; the text states the value as measured, so basis measured stands | p.3 Sec. IV.A; p.3 Fig. 6 axis "O-band wavelength (nm)"; p.1 Abstract | wavelength_inferred empty |
| coupe_gc-m2 (1-dB BW about 25 nm) | ok value; same band imprecision | p.3 Fig. 6 label "1dB bandwidth ≈25nm"; p.1 Abstract | wavelength_inferred empty |
| coupe_gc-m3 (+/-1.7 nm lt, range) | ok value (Fig. 7(b) points span about -1.5 to +1.5 nm on the render); band stated: "in the O-band region" | p.1 Abstract; p.3 Fig. 7(b); p.5 Sec. VI | wavelength_inferred empty |
| coupe_gc-m4 (PIC-wafer GC 1-dB BW about 20 nm, derived) | ok: 25 nm minus the printed "5 nm more"; the same GC before COUPE processing kept as a condition (a process stage, not a sibling design). A benchmark gc_bw cell takes the best value (25 nm), so the condition row does not displace it | p.3 Sec. IV.A; p.1 Abstract | none |
| coupe_gc-m5 (pitch 127 um) | ok, design_target ("offers a fiber spacing of 127 um") | p.3 Sec. III | none |
| coupe_lens_path-m1, -m2 (net 0 dB mean, 0.04 dB std) | ok values (Fig. 7(a) "Average = 0dB", "Sigma = 0.04dB"; points about -0.05 to +0.05 dB on the render); scope de_embedded (Q4) | p.3 Fig. 7(a); p.3 Sec. IV.A; p.2 Sec. II | none |
| coupe_lens_path (component) | imprecise core_material: the lens material is printed (Si) | p.2 Fig. 4 "Si lens"; p.3 Fig. 5(a) "Si Lens with ARC film" | core_material |
| song2026_gc-m1 (about 3.8 dB, extracted_from_figure, unspecified) | value ok: audit pixel scan gives the trace top edge -3.6 to -3.9 dB over 1300-1316 nm, line about 0.3 dB thick, so a line centre about -3.8 dB; plateau range 1300-1316 nm ok. Imprecise `includes`: it holds a guess ("presumably input and output GC ..."), which rule 6 excludes for an unspecified scope | p.3 Fig. 23.1.5 top left; p.1 | includes empty; notes with the re-read and the Fig. 23.1.7 fact |
| song2026_gc-m2 (1.9 dB le, loopback_half, author_estimate) | wrong: no two-coupler measurement is stated (Q2); the halving is the distiller's estimate | p.1; p.3 Fig. 23.1.5, Fig. 23.1.7 | delete_metrics |
| song2026_gc (component) | notes describe m2; after the delete they must not. Additive: Fig. 23.1.7 shows separate Laser, TX and RX fibers at the FAU and labels a "Backside metal" layer in the cross-section (role not stated; not called a GC reflector) | p.3 Fig. 23.1.7 | notes |
| song2026_rx_mrr_filter-m1 (Q 4000, author_estimate) | ok (Q3) | p.1 | none |
| song2026_rx_mrr_filter-m2 to -m4 (~5 um radius design_target; 9 channels design_target; 200 GHz author_estimate per D82a) | ok; radius stated for the PIC's rings in general, noted | p.1; p.1 Abstract; p.2 Fig. 23.1.1 caption | none |
| coupe_gc, rx_mrr_filter (components) | ok: class / subtype, platform (empty for the COUPE GC: the paper says only "SiPh PIC platform", GC layer not stated, D422; soi for the ISSCC parts: "65nm SOI SiPh", p.3 Fig. 23.1.6), host ids, fab (Q1) | as cited in the rows | none |

## Rulings requested (points 1-5)

1. **fab_org_ids = org_tsmc on the ECTC rows. Recommendation: keep.** No sentence of the form "fabricated by" or "we
   fabricated" appears in the paper. The paper does name TSMC as owner of both the wafer and the process: "TSMC's COUPE
   wafer" (p.2 Sec. I), the "TSMC Compact Universal Photonic Engine (COUPE)" (p.1 Abstract), "the COUPE process itself"
   and "COUPE-GC processes" (p.3 Sec. IV.A, Fig. 6 caption), and "TSMC has been developing COUPE" (p.2 Sec. I). That is
   more than the D80b exclusions (all authors at one org, "we developed"). It matches the precedents that accept a
   foundry named for the device's process: D912 (munk2019, a process name naming the foundry) and D920 ("states GF for
   the device or its flow"). A strict D80b reading ("explicit fabrication statement") would strip both rows. If the
   coordinator rules that way, the D925 own-staff rule would still attribute the rows to TSMC in the benchmark (all
   authors TSMC, p.1). The data tables would lose the fab.
2. **ISSCC grating-coupler rows.**
   - m1: keep as is (extracted_from_figure, scope unspecified, about 3.8 dB, wavelength 1300-1316 nm). This is the
     owner-requested envelope value (DevLog-015 request 1). Only the speculative `includes` text is removed.
   - m2: no locator states a two-coupler assumption. The text says only "A PIC TX bus spectrum sweep is shown" and
     "grating couplers used for fiber connections" (p.1). Fig. 23.1.7 (p.3) shows separate Laser and TX fibers, so a
     GC-in / GC-out bus is plausible. Nothing states the path content, the normalization, or that the bus loss is
     negligible. Basis cannot be `derived` (D80: arithmetic on the source's stated measurement of two couplers), and
     `author_estimate` misattributes the assumption to the authors.
   - Recommendation: delete m2 (patch). Fallback if the coordinator keeps it: author_estimate (never derived),
     loopback_half, qualifier le, with the note "two-coupler path not stated; inferred from Fig. 23.1.7 fiber labels".
     Basis filter D901 keeps it out of the benchmark either way.
3. **RX filter Q 4K. Recommendation: author_estimate, class wdm.mrr, both as entered.**
   - Basis: the text says "RX filter Q is 4K, selected using an in-house link modeling tool, and validated by device
     test chip measurements" (p.1). The number is a selected design value. The validation was on separate test chips,
     and no data, statistic or method is shown. Not `measured`: no measurement of this chip or of a shown test
     structure. Not `simulated`: the tool selected a target, and the value is not printed as a simulation output.
     author_estimate follows D82 (design-stated performance not computed in the paper) and matches the merged M4B.2
     row (MRR Q 4200, author_estimate).
   - Class: the RX rings drop each wavelength onto the PD of its lane, are tuned by a peak-finding loop on the RX PD
     current, and are ordered by radius to cancel crosstalk (p.1). They are channel filters in the WDM path, so D400
     gives wdm.mrr, not resonator.ring.
4. **ECTC net lens-path 0 dB mean. Recommendation: keep the row; scope de_embedded; class and parameter acceptable.**
   - Scope: per_interface is for chip-chip interfaces. This path is inside one stacked engine: GC, support Si, ARC,
     embedded lens (p.3 Sec. IV.A, Fig. 2(b)). The value is COUPE-GC loss minus the same GC's PIC-wafer loss, with the
     coupler removed against a reference measurement. That makes it de_embedded with method reference_structure.
   - Parameter: the paper defines the quantity itself as "the net insertion loss contributed by the additional optical
     path within COUPE" (p.2 Sec. II). insertion_loss_db therefore matches the paper's own definition, net of the Cu
     reflector's 0.5 dB gain.
   - Class: micro_optics.integrated_lens is the closest subtype. The path's only optical element is the embedded Si
     micro-lens; support Si and ARC are its substrate and coatings.
   - Caveat for the coordinator: a class table shows this row as a lens path with 0 dB IL. The label and notes say
     "net of the Cu reflector gain", and the inherent path loss is not stated (not to be derived from the 0.5 dB
     simulated / "silicon" gain). If micro_optics IL is ever ranked, exclude this net value.
5. **Misses: none in either paper.**
   - ECTC: the values not entered are registry gaps, out of scope, or not stated (see Registry gaps). The PIC-wafer GC
     loss is only said to match the COUPE value. The 800 um support-Si thickness has no micro_optics parameter. Micro-lens
     geometry is not printed. Daisy-chain resistance and RF bandwidth are electrical; the RF bandwidth is also simulated.
   - ISSCC: TX ring values (Q about 4.5K, dip depths, about 200 GHz spacing on the TX bus) are EO-atlas scope.
     song2026-a holds Q 4500 and ER 17 dB, and its notes cite the about -4 dB baseline. RX sensitivity -16.0 dBm OMA is a
     receiver figure. Heater energy 0.76 pJ/b measured / 0.49 pJ/b estimated (Fig. 23.1.6 notes e, f) covers TX + RX
     rings of the link, with no per-ring power or efficiency. Fig. 23.1.5 top right gives heater DAC code only, with no
     physical unit. The 9 um hybrid-bond pitch is packaging, not a photonic component. The FAU and lens carrier chip
     have no metrics. A GC 1-dB width from the envelope is correctly not entered: ring-cut steps, and the path content
     is not stated.
   - OFC M2A.7 = eo:patel2026: distiller conclusion confirmed. Table 1 (p.3) lists 10 MRMs by DOI of other works. Every
     Fig. 3 point is labelled with a cited DOI. Fig. 1-2 are models and illustrations: Fig. 1(c) "desired" region,
     Fig. 2(c) generic S21. The intro says the paper "reports experimental results at high bit rates" (p.1), but no own
     device data appears in the text or the p.3 render. The TSMC COUPE sentence (p.1) concerns a product announcement.
     0 rows is correct.
   - OFC M4B.2: no missed component value.
     - The merged rows `cmp_ofc2026_m4b2_vgc` (1.3 dB, 20 nm, < +/-1.7 nm) and `cmp_ofc2026_m4b2_rx_mrr_filter` (Q 4200,
       200 GHz, 9) match the text (Sec. 2, Fig. 1(b)).
     - MRM Q about 4500 is EO scope. The 300 uA photocurrent sink is a driver property.
     - Fig. 3(d) (render) prints heater power 0.76 pJ/bit for the link, not per ring. The DFB-array source (230 GHz,
       3 dBm per wavelength) and the 4 m PM fiber are setup equipment (rule 13).
     - Fig. 1(d) (cited from [3]) labels a Si microlens and a Cu reflector, with no values.

## Other questions

6. COUPE-GC benchmark placement: the row's platform is empty (correct under D422), so it reaches no benchmark
   column. The paper states a silicon photonics PIC platform ("TSMC has developed a 300 mm SiPh PIC platform", p.1
   Sec. I; Fig. 6 caption credits the "PIC and COUPE-GC processes"). Recommendation: a D914 `family_override` entry
   (family siph) for `cmp_ectc51687_2025_00015_coupe_gc`, so that 1.2 dB lt (loopback_half) can fill tsmc.siph gc_il.
   The data row keeps its empty platform. Do not override the lens-path row: no benchmark row uses micro_optics.
7. Merged M4B.2 GC row (outside this batch, information only): its 1.3 dB / 20 nm equal the SPGC labels of the TSMC
   platform paper it cites as [2] (yeh2024 Fig. 6 labels "Peak loss < 1.3dB", "1dB BW ~ 20nm"). Its +/-1.7 nm spread
   equals the TSMC ECTC 2025 value. M4B.2 prints these without a citation in that sentence, so rule 3 does not
   strictly apply. They read as foundry platform values restated by NVIDIA. The rows are already author_estimate
   ("how obtained not stated") and outside the benchmark basis filter. Recommendation: add a cross-note on
   `cmp_ofc2026_m4b2_vgc` in a later data pass; no deletion.

## Registry gaps confirmed

- `il_gain_db` (or a general IL-delta parameter): Cu reflector IL gain 0.5 dB. The text says simulation and silicon;
  the Fig. 5(b) caption says simulation (p.3 Sec. IV.A, Fig. 5(b)).
- `beam_angle_variation_deg`: < +/-0.1 deg across samples after FAU assembly (p.3 Fig. 8, Sec. IV.A; p.5 Sec. VI).
  `fiber_angle_deg` is a geometry tilt and does not fit.
- `tdecq_penalty_db`: TDECQ 1.61 -> 1.68 dB through a COUPE loopback at 53.125 GBd PAM4 (p.4 Sec. IV.A, Fig. 9).
- `il_change_db` (pending from pk_oi): < 0.25 dB after MR 3x + TC-C 300, TC-G 1000, DH 85/85 1000 h, HTS 175 C
  1000 h (p.4 Sec. V.A, Fig. 11).

## Orgs

org_tsmc exists. No facility is named: the acknowledgment lists internal TSMC organizations only (p.5). The ISSCC
acknowledgment names internal NVIDIA teams only (p.2). Missing orgs: none.
