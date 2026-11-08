# cov_psiq: PsiQuantum, Nature 641, 876-883 (2025) + Supplementary Information (DevLog-015 D920)

Date: 2026-11-07. Source `lit:alexander2024` (paper id kept; the published version and its SI replace the arXiv v1,
which is kept under `references/alexander2024/_arxiv_v1/`). Page-1 title check: main PDF (9 pages) and SI (25 pages)
are this paper, Nature 641, 876 (2025), doi 10.1038/s41586-025-08820-7; licence printed on p.8: CC BY 4.0.
Re-distilled from both texts; bench_01 rows were the starting point and every value was re-checked at the new
locators. Locators: `p.N` = page of `references/alexander2024/text.md` (p.1 = journal page 876), `p.N Supp. <label>` =
page of `references/alexander2024/supplement/text.md`.

Result: 14 components (11 bench_01 ids replaced, 3 new, 0 dropped), 27 metric rows.
`merge_component_staging.py --dry-run`: 0 errors (11 existing ids skipped as expected; with `--replace` also 0 errors,
+14 / +27). Merge with `--replace` swaps all bench_01 rows of this paper.

## Source-level changes (outside this batch)

| file | change | how |
|---|---|---|
| `references/alexander2024/` | arXiv v1 `source.pdf`, `text.md`, `figures/`, `source.json` moved to `_arxiv_v1/`; Nature PDF + SI ingested, `text.md`, `figures/`, `supplement/` extracted, new `source.json` | `lit_ingest_inbox.py` (dry run first), which runs `lit_extract.py` |
| `.gitignore` | `references/*/_arxiv_v*/` pdf, `text.md`, `figures/` ignored (the old patterns are one level deep); `_arxiv_v1/source.json` stays trackable like every other `source.json` | hand edit |
| `config/literature/curation/G7.yaml` | the coordinator add now points at doi 10.1038/s41586-025-08820-7 (arXiv id kept), year 2025 | hand edit (curation config) |
| `cache/literature/curator_adds.jsonl` (git-ignored) | add resolved to the Nature record of the local pool (115 adds, 114 accepted, same as before) | `lit_curator_adds.py --offline` |
| `data/_staging/literature/cache_list.csv` | row 909 (`alexander2024`): uid / doi / venue Nature / journal / 2025 / oa_url / authors | hand edit (one-off script): no script swaps a uid while keeping the paper_id. `lit_select.py --delta --dry-run` afterwards: 1002 / 1002 paper_ids pinned by uid, 0 curator adds beyond budget (its `increment_delta.md` was restored byte-identical) |
| `data/registry/sources.csv` | `lit:alexander2024`: year 2025, published 2025-02-26, venue Nature, doi, url doi.org, source_type journal, access open_access, license cc-by, redistribution restricted_local_only, accessed_on 2026-11-08 | `lit_register_sources.py` (1 updated, 709 unchanged); `validate_db.py` 0 errors |

Notes: redistribution follows the script convention for manual copies (restricted_local_only) although p.8 prints CC BY
4.0; relaxing it is a coordinator call. `retrieved_on` / `accessed_on` are UTC dates (2026-11-08). The registry has no
volume / page column (Nature 641, 876-883 is in the doi). `retrieval_queue.csv` still lists the arXiv route for
`alexander2024` (schedule history, not changed).

## Per component: change vs bench_01

| component (`cmp_lit_alexander2024_*`) | status | change |
|---|---|---|
| hairpin_snspd | changed conditions, +1 metric | 93.4 % median / 88.9 % mean unchanged (+/- now 3.5, v1 3.1); temperature 2 -> 2.1 K (p.12 Supp. S4.2); band c_band -> 1550 nm (inferred from the normalization, p.12 Supp. S4.1); method reference_structure; condition 90 % I_sw; locators p.2 -> p.3 / Supp.; new m6 dark count rate about 1.8e4 /s at about 0.9 I_sw (read off Fig. 2(e) inset) |
| baseline_mzi | same value | > 50 dB; locator p.2 -> p.3 |
| mzi_heater | same value | P_pi about 10 mW re-read on the Nature Fig. 2(d) (minima 2.8 / 23.2 mW); the published x-axis labels read 0, 5, 10, 15, 25, 25 (noted) |
| pump_filter | same values | 99.1 dB, about 1 dB; locator p.3 -> p.4 |
| grating_2d | new | 2D grating coupler of the qubit interconnect: about 3 dB (author_estimate, scope unspecified), 15 deg design |
| sin_pnrd | changed value | median 98.9 % same; mean 96.3 -> 96.2 % (+/- 4.3); n 6 devices; 2.1 K; design 5 unit cells x 20 nanowires (SI) |
| sin_process_snspd | new | SiN-process SNSPD wafer set: internal detection efficiency >= 99 % for 80 devices / 20 dies (fit) |
| sin_sm_wg | changed value | 1.58 -> 1.8 dB/m (0.018 dB/cm); 1560 nm stated; cutback; + core_thickness_nm 350 |
| sin_mm_wg | changed value | 0.39 -> 0.5 dB/m (0.005 dB/cm); 1560 nm; cutback; + thickness 350 |
| sin_crossing | changed value | 1.6 -> 1.2 mdB (0.0012 dB); scope per_component; cutback 50-500; 1560 nm; + thickness 350 |
| sin_splitter | same value | 0.5 mdB; subtype directional_coupler confirmed by the SI; cutback, both outputs summed; 1560 nm; + thickness 350 |
| edge_smf28 | changed value + scope | 120 -> 127 mdB (0.127 dB); scope per_coupler -> loopback_half (SI: two-coupler transmission divided by two); n 2 devices -> 10 measurements (mean) |
| edge_uhna4 | changed value + scope | 53 -> 52 mdB (0.052 dB); scope per_coupler -> loopback_half; n 9 measurements (mean) |
| cascaded_source_rings | new | rings of the 24-resonator source: FSR about 10 nm, resonance spread about 2 nm (author_estimate) |

## Fab attribution (fab_org_ids)

- `org_globalfoundries` for hairpin_snspd, baseline_mzi, mzi_heater, pump_filter, grating_2d: p.2 baseline stack
  'developed in partnership with GlobalFoundries', 'fabricated in their 300-mm' foundry; process modules include NbN,
  heaters, grating couplers (p.2); p.1: the benchmarked components incl. chip-to-chip interconnects are 'fabricated in
  a commercial semiconductor foundry' (ref. 14 = a GF 300 mm paper). SI calls it the Gen1 (Si) process (p.8 Supp. S3).
- Empty for all SiN rows (sin_sm_wg, sin_mm_wg, sin_crossing, sin_splitter): the SiN loss figures are 'not all from the
  same wafer', nor from one process (p.17 Supp. S5); no org named. The only GF statement for SiN is '300mm silicon
  nitride from GlobalFoundries' for the BTO switch wafers (p.8 Supp. S3; Fig. S7 calls it PsiQuantum's 300mm SiN
  process). Reading that as covering the passive SiN components would be an inference, not entered.
- Empty for sin_pnrd and sin_process_snspd ('our SiN-based 300mm process', p.7 Supp. S3, no org), the edge couplers
  (no process or org stated), cascaded_source_rings ('our Si photonics platform', p.7 Supp. S2.3, no org).
- No facility orgs.

## Temperatures

2.1 K stated for the hairpin SNSPD and PNRD efficiency (p.12 Supp. S4.2); about 2 K for the SNSPD-read baseline
circuits (MZI, heater, pump-filter rejection, DCR; p.2 / p.4 cryostats). Not stated: SiN passives, edge couplers (lab
with environmental control), SiN-process SNSPD set, pump-filter loss, cascaded rings. 2D grating: liquid helium
temperature (p.4), no number entered.

## Not entered

- EO atlas (rule 2, D250; candidate `psiquantum2025` in the EO atlas candidates): BTO-on-SiN phase shifter / 2x2 MZ
  switch: propagation loss 53 +/- 3 dB/m, d.c. VpiL 0.62 V.cm non-push-pull, Vpi 3.1 V at L = 2 mm, insertion loss
  about 100 mdB, alpha VpiL 0.33 +/- 0.02 dB.V (p.6-7, Fig. 5(f,g)); wafer VpiL 0.77 +/- 0.04 V.cm average, 0.84
  worst, 95 % functional yield (p.8, p.10 Supp. S3, Fig. S7); 3-dB EO bandwidth 6.9 GHz (3 mm device), > 5 GHz for
  bias > 20 V (p.19 Supp. S7); film r_eff > 1,000 pm/V free-space, BTO 112 / 135 nm, gap 7 / 10 um, poling 40 V
  (p.6, p.18-19 Supp. S7); 3-sigma thickness uniformity < 3 % (p.6). Fab: BTO by MBE (PsiQuantum process), oxide
  bonded to 300 mm SiN from GlobalFoundries (p.8 Supp. S3).
- Photon-pair and quantum metrics (no registry parameters, D250): purity 99.5 +/- 0.1 % (SI 0.99516), 99.35 %
  (cascaded), indistinguishability > 99 % over +/- 400 pm, CAR up to 3,000 / 929 +/- 4, g2(0) 0.00358, Klyshko about
  26 %, HOM 99.50 %, SPAM / Bell / interconnect fidelities, 5 % pair probability at about 100 pJ.
- System figures: about 115 dB pump suppression and > 115 dB scatter rejection (shield + filter, p.4, p.20 Supp. S8.3);
  80 ps total jitter of the JSI setup (off-chip detectors and time tagger, equipment, rule 13; p.2 Supp. S2.1); cryostat
  > 10 W at 2.2 K.
- Process statistics: NbN width 1-sigma 1.6 nm and thickness < 0.1 nm wafer-to-wafer (Gen1), SiN thickness 1-sigma
  < 0.7 nm and index 0.01 % (Gen2) (p.8 Supp. S3).
- Measurement-uncertainty inputs: SiN grating-coupler variability 0.5 dB between adjacent gratings (p.14 Supp. Fig.
  S12), Si GC 2 %, loopback IL difference std about 0.1 dB (p.17 Supp. Fig. S15).
- Edge-coupler connecting waveguides 6.3 dB/m (4.56 mm) and 1.1 dB/m (3.3 mm) (p.18 Supp. S6): de-embedding inputs of
  unstated origin and unstated cross-section.
- Wafer maps without printed values: splitter ratio, crossing extinction (Fig. S6(e,f)).
- SNSPD bias window 0.7-2 uA per die and the 80 cps dark-count criterion (definitions / no registry parameter).
- PNRD designs with 4 unit cells (Fig. 4(f) readout) and 10 unit cells (number-resolution test, p.15 Supp. S4.4): no
  efficiency value; 0-4+ photon resolution has no registry parameter.

## Judgment calls and questions for the coordinator

1. Edge couplers: scope `loopback_half` (SI p.18: through-chip two-coupler transmission divided by two, connecting
   waveguide subtracted), not `per_coupler` as in bench_01. If the benchmark cell filters on per_coupler, the cell
   rule needs to admit loopback_half for these rows (recommendation: admit; the de-embedding is stated).
2. Hairpin SNSPD population: 37 (p.12 / p.14 Supp.) vs 38 (Fig. S10 caption); n_samples empty.
3. SNSPD / PNRD efficiency wavelength 1550 nm entered as inferred (photon energy in the normalization only).
4. Dark count rate 1.8e4 /s read off a log-scale inset (+/- 0.1 decade); drop it if figure reads of log insets are
   unwanted.
5. cascaded_source_rings: platform empty because the SI (Si photonics platform) and the main text (SiN n2) disagree.
6. GF for SiN passives: not entered (see Fab attribution); decide whether the BTO-wafer statement plus "PsiQuantum's
   300mm SiN process" is enough to call the SiN flow GF (current rule says no).

## Registry gaps (proposals, no value skipped that a row could not hold)

- `bias_window_ua` (photodetector, SNSPD high-efficiency bias plateau width, criterion in condition): 0.7-2 uA per die,
  p.9 Supp. Fig. S5.
- `photon_number_max` (photodetector, highest resolved photon number of a PNRD): 4+ (p.5 Fig. 4(f)).

## Benchmark-relevant values

| parameter | value | scope | basis | temperature | fab_org_ids | locator |
|---|---|---|---|---|---|---|
| SiN SM prop loss | 0.018 dB/cm (1.8 dB/m) | - | derived | not stated | - | p.5; p.15-17 Supp. S5 |
| SiN MM prop loss | 0.005 dB/cm (0.5 dB/m) | - | derived | not stated | - | p.5; p.15-17 Supp. S5 |
| SiN crossing loss | 0.0012 dB | per_component | derived | not stated | - | p.6; p.17 Supp. S5 |
| SiN DC excess loss | 0.0005 dB | per_component | derived | not stated | - | p.6; p.17 Supp. S5 |
| edge coupler SMF-28 | 0.127 dB | loopback_half | derived | not stated | - | p.6; p.17-18 Supp. S6 |
| edge coupler UHNA4 | 0.052 dB | loopback_half | derived | not stated | - | p.6; p.17-18 Supp. S6 |
| 2D grating coupler IL | about 3 dB | unspecified | author_estimate | LHe (no number) | org_globalfoundries | p.4 |
| Si hairpin SNSPD OCDE | 93.4 % median / 88.9 % mean | on_chip | measured | 2.1 K | org_globalfoundries | p.3; p.12-13 Supp. |
| thermo-optic P_pi (MZI) | about 10 mW | - | extracted_from_figure | about 2 K | org_globalfoundries | p.3 Fig. 2(d) |
| MZI extinction | > 50 dB | - | measured | about 2 K | org_globalfoundries | p.3 |
| pump filter rejection / IL | 99.1 dB / about 1 dB | - / device_total | measured | about 2 K / not stated | org_globalfoundries | p.4 |
| SiN PNRD OCDE | 98.9 % median / 96.2 % mean | on_chip | measured | 2.1 K | - | p.5; p.12-13 Supp. |

Values tied to GlobalFoundries by the paper: only the baseline (Gen1, Si) rows; none of the SiN, edge-coupler or PNRD
values.
