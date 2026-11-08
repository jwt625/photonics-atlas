---
title: Fresh-context audit of component batch cov_psiq (PsiQuantum Nature 2025 + SI, re-distill of bench_01 alexander2024 rows)
date: 2026-11-07
mode: read-only audit subagent; patch validated on a scratchpad copy of the batch (patch_component_staging.py 21 changes, re-apply 0 changes; merge_component_staging.py --replace --dry-run "+16 components, +31 metrics; errors 0", only the pre-existing WARN on merged row cmp_lit_ni2025b_pimmwc-m18). Real batch CSVs not modified, nothing merged
patch: data/_staging/components/cov_psiq/patch.yaml
---

# Audit cov_psiq (2026-11-07)

Source `lit:alexander2024`: `references/alexander2024/text.md` (9 pages, Nature 641, 876-883, doi
10.1038/s41586-025-08820-7) and `supplement/text.md` (25 pages). Page-1 titles match the source row; neither part is a
correction or erratum (D397 / D409); no `garbled_text_layer`. Every metric row was checked at its locator. Renders read
(scratchpad crops of the cached PDFs): main p.3 Fig. 2(c), (d) at 400 dpi and the Fig. 2(e) inset at 1200-2400 dpi
(axis ticks and markers located on the pixel grid), p.6 Fig. 4, p.7 Fig. 5(a-c) at 300 dpi; SI p.9 Fig. S5, p.10
Fig. S6(a-f) at 300-450 dpi, p.17 Fig. S15. Locator convention checked: `p.N` = text.md page (Fig. 4 is on p.6,
Fig. 5 on p.7), `p.N Supp.` = SI text.md page (printed SI page + 1).

BATCH_REPORT counts (14 components, 27 metrics; 11 bench_01 ids replaced, 3 new) are correct. Two report statements are
wrong: "Wafer maps without printed values: splitter ratio, crossing extinction (Fig. S6(e,f))" and the matching
component notes: every die cell of Fig. S6(a-f) carries a printed value (misses below).

## Counts

| | ok | imprecise | wrong | miss (added) |
|---|---|---|---|---|
| metrics (27) | 21 | 6 | 0 | 4 |
| components (14) | 9 | 5 | 0 | 2 |

Additive notes on ok rows: sin_mm_wg (per-die range, resolution), edge_smf28 / edge_uhna4 (pointer to the added
connecting-waveguide rows).

## Findings

| row | finding | evidence (locator) | patch |
|---|---|---|---|
| hairpin_snspd-m6 (DCR 1.8e4 /s) | imprecise value: the inset's major ticks coincide with the printed labels (7.7 pt per decade); the last orange marker spans 10^4.0 to 10^4.44, centre 1.4e4 (triangle centroid) to 1.7e4 (box centre) | p.3 Fig. 2(e) inset, 2400 dpi render | value 15000, reading range in notes |
| baseline_mzi-m1, mzi_heater-m1, pump_filter-m1 | imprecise notes: 2 K entered while the note says not printed for this measurement; the circuit-level statements are p.3 (interferometer / heater paragraph: circuit cooled, about 2 K) and p.4 (packaged chips in cryostats, about 2 K base) | p.3, p.4, Fig. 2(c), (d) captions | notes re-anchored (Q4) |
| sin_pnrd-m1, -m2 | imprecise locator: Fig. 4(e) is on p.6, not p.5 | text.md p.6 (journal p.881) | locator |
| sin_pnrd (component) | same locator slip in core_material (Fig. 4(d)) | p.6 | core_material |
| grating_2d (component) | locator in notes: S8.5 design text is on p.21 Supp., not p.20 | SI text.md p.21 | notes |
| sin_sm_wg, sin_crossing, sin_splitter (components) | notes say the Fig. S6 wafer maps print no values; they print per-die values (SM 1.2-2.4 dB/m, crossing 0.52-2.04 mdB and extinction ratio -49 to -60 dB, splitter 0.16-0.88 mdB and ratio 0.475-0.515) | p.10 Supp. Fig. S6(a, c-f) | notes; misses added |

Verified ok (selection): SNSPD 93.4 % median / 88.9 +/- 3.5 % mean at 90 % I_sw, 2.1 K (p.3; p.12 Supp. S4.2; p.13
Fig. S10), geometry about 5 nm / about 90 nm (derived 0.09 um) / >= 80 um (p.2); MZI > 50 dB (p.3, Fig. 2(d) min at
about -50 dB); heater P_pi: Fig. 2(d) re-read, transmission minima about 2.9 and 23.2 mW, reflection minimum about
13.9 mW on a uniform 5 mW tick grid (the fifth label is a misprint), P_pi about 10.2 mW; pump rejection 99.1 +/- 1.2 dB
and about 1 dB (p.4); 2D grating about 3 dB (p.4), 15 deg design (p.21 Supp. S8.5); PNRD 98.9 % median / 96.2 +/-
4.3 % mean, 2.1 K, 6 devices x 2 power set points (p.5; p.12 Supp. S4.2; p.13 Fig. S11); SiN-process SNSPD IDE >= 99 %
for 80 devices / 20 dies by a model fit of own data (p.7 Supp. S3; p.9 Fig. S5); SiN loss values at 1560 nm, device-to-
device SD (p.17 Supp. S5): 1.8 dB/m = 0.018 dB/cm, 0.5 dB/m = 0.005 dB/cm, 1.2 mdB = 0.0012 dB, 0.5 mdB = 0.0005 dB,
all derived (D256); 350 nm SiN design_target (D402); edge couplers 127 +/- 18 and 52 +/- 12 mdB (p.6) = 0.127 / 0.052 dB,
mean of 10 / 9 repeated measurements (p.18 Supp. S6); cascaded rings FSR about 10 nm, spread about 2 nm by design
(p.7 Supp. S2.3).

Fig. 5 re-read (300 dpi, +/- 0.02 in the axis unit): SM mean 1.81 / median 1.83 dB/m; MM 0.52 / 0.53 dB/m; splitter
0.48 / 0.52 mdB; crossing 1.24 / 1.26 mdB; SMF-28 127 / 135 mdB; UHNA 52 / 45 mdB. Edge-coupler printed values are the
means (statistic mean correct). SiN rows: printed values round from either mark (crossing only weakly favours the
mean); statistic stays empty.

## Rulings requested (points 1-5)

1. fab_org_ids. Keep `org_globalfoundries` on the five baseline rows (hairpin_snspd, baseline_mzi, mzi_heater,
   pump_filter, grating_2d): p.2 states the baseline stack is fabricated in GF's 300 mm foundry and lists its process
   modules (SOI waveguides, NbN layer, heaters, grating couplers); the 2D grating sits on the baseline interconnect
   chips (p.4). The SI GF sentence (p.8 Supp. S3, wafer-scale BTO uniformity) names GF only as the source of the 300 mm
   SiN wafers onto which the BTO was oxide-bonded for the BTO switches (Fig. S7, p.10 Supp., calls the flow PsiQuantum's
   300mm SiN process): a wafer supplier for an EO device (rule 12: note), and none of the entered values comes from those
   wafers (the BTO VpiL wafer map is EO scope). The SiN loss figures are from several wafers and processes (p.17 Supp.
   S5); the SiN-process SNSPD set (p.7 Supp. S3) and the Fig. S6 maps name no org; the edge couplers name no process;
   the cascaded source is "our Si photonics platform" (p.7 Supp. S2.3) under the next-generation multi-flow section
   (p.5). Recommendation: no change; next-generation rows stay empty.
2. Scope and methods. Edge couplers: `loopback_half` is right: the SI divides the system-corrected two-coupler
   transmission by two, then subtracts the connecting waveguide (p.18 Supp. S6); method loopback, basis derived (mdB ->
   dB, D256), excludes lists system loss, drift and the waveguide. The benchmark edge_il row already admits
   loopback_half. Crossing and splitter: `per_component`, cutback with 50 / 200 / 350 / 500 copies, splitter outputs
   summed so the value is loss beyond the ideal split (`excess_loss_db`) (p.17 Supp. S5); derived (mdB -> dB). Waveguide
   dB/m -> dB/cm arithmetic correct, derived. Recommendation: keep.
3. Basis. (a) 2D grating about 3 dB: the sentence apportions part of the interconnect's system loss to grating-coupler
   coupling with no method and no per-coupler / per-link scope (p.4): loss-budget term of unstated origin ->
   `author_estimate`, scope unspecified; keep. The filter's about 1 dB (p.4) is the component's own stated transmission
   loss in the results paragraph: `measured`, method unspecified; keep (switch to author_estimate only if the
   coordinator wants the two treated alike; no benchmark row is affected). (b) P_pi about 10 mW, extracted_from_figure,
   confirmed (above). (c) SNSPD: median and mean are separate printed statistics, rows correct; N is 37 by S4.2
   arithmetic and twice in S4.3 (p.12, p.14-15 Supp.) but 38 in the Fig. S10 caption (p.13 Supp.): keep n_samples empty
   (paper inconsistent; note already says so). PNRD: statistics over 12 measurements of 6 devices; n_samples 6 (devices)
   with the 12 in condition; keep. (d) SNSPD DCR re-read to 1.5e4 (patched).
4. Temperatures. Stated per measurement: 2.1 K for both efficiency sets (p.12 Supp. S4.2); about 2 K for the Fig. 2(e)
   SNSPD curves incl. the DCR inset (p.2 sentence cites Fig. 2(e)). MZI extinction, heater P_pi and pump rejection
   carry no number of their own, but the paper states the operating temperature of these circuits in the same sections
   (p.3: the reconfigurable circuit is cooled, about 2 K; p.4: packaged chips in about 2 K cryostats) and the readout is
   by on-chip SNSPDs. Recommendation: keep 2 K on these three with the notes re-anchored to p.3 / p.4 (patched); this is
   a section-level statement, not an inference from physics. Strict alternative (clear them): the cryogenic, GF-fabbed
   about 10 mW heater P_pi would pass the D901 cryogenic filter and enter the gf.siph P_pi cell as if room temperature;
   not recommended. Not stated, empty (correct): SiN passives, edge couplers, SiN-process SNSPD set, filter loss,
   cascaded rings, 2D grating (liquid helium, no number; p.4).
5. Misses (registry parameter covers a stated number). Added: (a) sin_crossing-m3 `crosstalk_db` 49-60 dB, wafer_map, 51
   dies, measured (printed die labels, bayoumi2025 precedent), p.10 Supp. Fig. S6(f), printed as crossing extinction
   ratio -49 to -60 dB; sin_splitter-m3 `split_ratio_pct` 47.5-51.5 %, wafer_map, 49 dies, derived (fraction -> %),
   p.10 Supp. Fig. S6(e), port not stated. (b) Two connecting waveguides of the edge-coupler chips (p.18 Supp. S6):
   6.3 dB/m (4.56 mm) and 1.1 dB/m (3.3 mm) -> 0.063 / 0.011 dB/cm, `author_estimate` (origin not stated, rule 4),
   platform sin from the Fig. 5(a-c) caption; new components `cmp_lit_alexander2024_edge_smf28_link_wg` and
   `..._edge_uhna4_link_wg`. Recommendation: accept (a); (b) is optional (the distiller left them out as de-embedding
   inputs; author_estimate keeps them out of the benchmark). To reject (b), drop the two add_components, their -m1 rows
   and the edge_smf28 / edge_uhna4 notes ops. BTO metrics stay out (EO scope, rule 2); none entered.

## Other questions

6. Per-die loss ranges of Fig. S6(a-d) (SM 1.2-2.4, MM 0.04-1.08 dB/m, splitter 0.16-0.88, crossing 0.52-2.04 mdB):
   not added. Same population as the headline rows (they match the Fig. 5(a, b) whiskers), and several MM values are
   below the 0.2 dB/m single-cutback resolution the SI states (p.17 Supp. S5); a range row would surface 0.04 dB/m as a
   best value. Recommendation: keep out (noted on the components).
7. `crosstalk_db` for the crossing "extinction ratio": the SI does not define the ratio; read as through-to-cross
   suppression (only reading that fits a crossing). Recommendation: accept; fallback is to drop sin_crossing-m3.
8. Notes on seven metric rows quote the arXiv v1 values (e.g. "arXiv v1 printed 1.58 +/- 0.50"). They are provenance for the
   --replace, not values; rule 1 is not breached. Recommendation: keep (or strip in a later sweep).

## cache_list.csv and .gitignore (review only, not changed)

- `data/_staging/literature/cache_list.csv` row `alexander2024`: uid / doi / venue Nature / journal / year 2025 /
  oa_url / selection_reason / rationale updated, paper_id kept (D920): correct. The working-tree file has since been
  regenerated by another stream (+54 rows, 970 rank-only changes; this row now rank 954) and the edit survived because
  G7.yaml now carries the DOI. Defect: `last_author` is Matthew Wingert; the printed author list ends with Xinran Zhou
  (p.8), which HEAD had; first_author "PsiQuantum team" matches the byline. Minor: the selection_reason / G7 reason
  text "PsiQuantum / GlobalFoundries 300 mm SiN platform building blocks" over-states GF for SiN relative to the paper
  (ruling 1); pre-existing wording.
- `.gitignore`: the three new patterns ignore `_arxiv_v*/` PDFs, text.md and figures/ (the existing patterns are one
  level deep) and leave `_arxiv_v1/source.json` trackable; `git check-ignore` confirms. Correct. Not covered (absent
  today): `*.part`, `arxiv/`, `supplement/` inside `_arxiv_v*`. `_arxiv_v1/source.json` has no local paths.
- Dates: source.json, sources.csv `accessed_on` and the text.md headers carry 2026-11-08 (UTC) on a 2026-11-07 local
  run; the distiller reported it; no action from this audit.

## Effect on GlobalFoundries values

- fab_org_ids: no change (ruling 1). GF stays on the five baseline rows; benchmark-relevant among them only the heater
  P_pi, which stays out of gf.siph at 2 K (ruling 4).
- Benchmark overlay (working-tree `config/benchmark.yaml`, D925, owner): `org_psiquantum -> gf` by author affiliation,
  applied per component row when the row has no fab or facility org. All empty-fab alexander2024 rows (SiN passives,
  edge couplers, PNRD, SiN-process SNSPDs, cascaded rings, and the two added link waveguides) therefore resolve to GF
  as affiliation-marked cells; the added rows are author_estimate (link waveguides) or have no benchmark row
  (crosstalk, split ratio), so the patch adds no GF cell. Note that the paper itself ties GF to SiN only through the
  BTO-switch wafers (p.8 Supp. S3).

## Registry and orgs

- Orgs: org_globalfoundries and org_psiquantum exist; no missing org, no facility orgs.
- Registry gaps (confirmed from the report): SNSPD bias window (`bias_window_ua`, 0.7-2 uA per die, p.9 Supp. Fig.
  S5); PNRD resolved photon number (4+, p.6 Fig. 4(f)). New: grating-coupler die-level loss variability for
  fiber_chip_coupler (e.g. extend `il_nonuniformity_db`): 0.5 dB between adjacent SiN gratings (p.14 Supp. Fig. S12),
  Si gratings 2 % (p.14 Supp.); both are measurement-uncertainty inputs, low priority.
