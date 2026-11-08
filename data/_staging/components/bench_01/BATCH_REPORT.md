# bench_01 batch report (2026-11-07)

Purpose: Tower and GlobalFoundries values for the foundry PDK benchmark (DevLog-014). Two sources, 13 components,
20 metric rows. `merge_component_staging.py --dry-run`: +13 components, +20 metrics, 0 errors. Not merged.

## Source ingest (outside this directory)

- `lit:alexander2024` = arXiv 2404.17570 v1 (2024-04-26), the preprint of PsiQuantum, Nature 641, 876-883 (2025),
  doi 10.1038/s41586-025-08820-7. Added as a coordinator curator add through the lit pipeline (D511 rule, as for
  xu2025a): zip backup `cache/literature/backup/s5_before_psiquantum_add_20261107T225610Z.zip`; G7 `adds` entry
  (arXiv id, class waveguide_platform); `lit_curator_adds.py --offline` (113 -> 114 adds, other rows unchanged);
  `lit_select.py --delta` (1 curator add beyond budget, 0 swaps, 0 paper_id changes; one label-only relabel:
  kurczveil2013 `rank` -> `reserve: best remaining`; list 1001 -> 1002); `increment_delta.md` history restored from the
  backup with the new section appended; `lit_build_queue.py --delta` (1001 rows verbatim, +1 row day 10, route arxiv);
  `lit_fetch_oa.py --paper-ids alexander2024` (1 arXiv PDF request, 13.8 MB, ok); `lit_extract.py` (8 pages, no
  garbled text, no correction); `lit_register_sources.py` (+1 lit row); `validate_db.py` 0 errors.
- Paper id: the DOI record's first author is the collective "PsiQuantum team", so the pipeline would have produced
  `team2025`; the add uses the arXiv record (first author Koen Alexander) -> `alexander2024` (no collision;
  `alexander2026` is a different paper). Consequence: the source row is the arXiv preprint (year 2024, doi empty,
  `same_as` empty).
- arXiv license lookup (OAI-PMH) timed out once; not retried; `license` empty, `redistribution: unknown`. The pool
  lists the Nature version as cc-by. No text quoted in the rows.
- Supplement: this arXiv v1 has no supplement; reference [20] says the supplementary material will be published later
  (p.8). The supplement exists only with the Nature version (a different, revised version: rule 1). No request was made
  to nature.com (earlier plain-client requests there armed a breaker, `logs/.lit_blocked_www.nature.com.json`, and the
  lit pipeline routes Nature through `publisher_browser`). See question 1.

## Paper 1: ofc2026:M1E.4 (Columbia; programmable MZI Fourier synthesizer)

Text: owner OFC corpus (`ofc_text_dir`, M1E.4 .md). 2 components, 3 metric rows.

| component | class | metrics |
|---|---|---|
| cmp_ofc2026_m1e4_folded_heater_ps | phase_shifter.thermo_optic | p_pi_mw 8.8 (per pi), tuning_power_mw 1.15 (trim for 0.13 pi mismatch) |
| cmp_ofc2026_m1e4_4tap_fourier_filter | wdm.cascaded_mzi | power_uniformity_db 1.8 derived (+/-0.9 dB, 1525.2-1553.9 nm, comb after filter) |

Fab attribution: Sec. 3 (p.~2) says the PIC with the 4-tap filter was fabricated through TowerJazz foundry ->
`org_tower_semiconductor` (registry org; precedent cmp_lit_munk2019_* for Tower-Jazz). The printed name TowerJazz is
not in `org_aliases.csv` (aliases: Tower Semiconductor (Tower)); alias row needed. Platform: only a commercial 300 mm
silicon photonics platform (pNA Sec. 1); entered `soi`, layer stack not stated (question 3). P_pi measured on a
reference test MZI in bare-die testing (Fig. 2(b)); the paper prints P_pi (per pi). No wavelength with the value:
C band inferred from the comb band of the same chip.

Not entered: MZI and coupler losses (none reported in this paper); filter insertion loss, Delta L, FSR (not stated);
phase mismatch across the six MZIs 0.12-0.42 pi (no registry parameter for an MZI arm phase error; `phase_error_deg`
is a 90-degree-hybrid parameter); >= 16 dB receiver dynamic-range reduction (system figure); 18 dB original comb
disparity (in condition only); programmed passband shapes (qualitative). Packaging org Optelligent (packaged and
wirebonded) is a note, not a fab org.

## Paper 2: lit:alexander2024 (PsiQuantum, arXiv v1)

11 components, 17 metric rows.

| component | class | platform | fab | metrics (locator) |
|---|---|---|---|---|
| hairpin_snspd | photodetector.snspd | soi | GF | QE on-chip 93.4 % median, 88.9 % mean (+/-3.1); NbN ~5 nm, width ~90 nm, length >= 80 um (p.2 Sec. II, Fig. 2(e)) |
| baseline_mzi | switch_fabric.other | soi | GF | extinction > 50 dB (p.2 Sec. II, p.3 Fig. 2(d)) |
| mzi_heater | phase_shifter.thermo_optic | soi | GF | p_pi ~10 mW, figure read, cryogenic (p.3 Fig. 2(d)) |
| pump_filter | wdm.other | soi | GF | pump rejection 99.1 dB (+/-1.2); IL ~1 dB device_total (p.3 Sec. III, Fig. 2(c)) |
| sin_pnrd | photodetector.snspd | sin | - | QE on-chip 98.9 % median, 96.3 % mean n=6 (p.5 Sec. IV, Fig. 4(e)) |
| sin_sm_wg | waveguide_platform.straight | sin | - | 0.0158 dB/cm (1.58 +/- 0.50 dB/m) (p.6, Fig. 5(a)) |
| sin_mm_wg | waveguide_platform.straight | sin | - | 0.0039 dB/cm (0.39 +/- 0.12 dB/m) (p.6, Fig. 5(a)) |
| sin_crossing | crossing.other | sin | - | 0.0016 dB per crossing (p.6, Fig. 5(b)) |
| sin_splitter | splitter.directional_coupler | sin | - | excess loss 0.0005 dB per_component (p.6, Fig. 5(b)) |
| edge_smf28 | fiber_chip_coupler.edge | sin | - | 0.120 dB per_coupler, SMF-28, 2 devices (p.6, Fig. 5(c)) |
| edge_uhna4 | fiber_chip_coupler.edge | sin | - | 0.053 dB per_coupler, UHNA4, 1 device (p.6, Fig. 5(c)) |

Fab attribution evidence:
- Baseline -> `org_globalfoundries`: p.1 Sec. II states the baseline quantum-photonic stack was developed in
  partnership with GlobalFoundries and is fabricated in their 300 mm foundry; its modules are SOI waveguides, NbN
  SNSPD layer, metal-filled trenches, resistive heaters, grating couplers, Cu BEOL, Al RDL. p.1 Sec. I separately says
  the components are made in a commercial foundry [14] with a 300 mm flow (org not named in that sentence). Rows from
  Sec. II / III building blocks (SNSPD, MZI, its heater, pump filter) take GF.
- Next generation -> fab empty: p.5 Sec. IV says the next-generation devices come from multiple process flows; no org
  is named for them, and all authors are PsiQuantum (not enough under D80b). SiN waveguides, crossings, splitters,
  edge couplers (Fig. 5 caption: a-c are SiN-based components), PNRDs, cascaded resonator source, BTO.
- Benchmark consequence: none of the GF rows is a benchmark row value at room temperature. The GF-attributed values
  are SNSPD efficiency, MZI extinction, pump-filter rejection / IL (no benchmark rows) and a cryogenic heater P_pi
  (temperature_k 2, excluded by the T >= 250 K filter). The low SiN / edge-coupler / crossing values would enter the
  SiN columns only if the coordinator attributes the next-generation flows to an org; this source does not.

Conditions: no value in this source carries a wavelength; all rows use `band: c_band`, `wavelength_inferred: true`
(the paper states the platform operates at telecom C-band wavelengths, p.1 Sec. I). Temperature 2 K on the SNSPD row
(stated about 2 K), and on the MZI / heater / filter rows because they were read out by the co-integrated SNSPDs
(note on each). PNRD temperature not stated (left empty).

Basis notes: mdB -> dB and dB/m -> dB/cm conversions are `derived` (D80). Edge couplers `statistic: best` (the paper
calls them two of the best coupler designs; the printed number is an average of repeated measurements, mean vs median
not stated). SiN waveguide / component values: Fig. 5 marks mean and median; which one the printed value is, and the
meaning of +/-, not stated (no statistic entered).

Not entered (registry gap or out of scope):
- BTO electro-optic phase shifter (rule 2, EO-atlas metrics; paper is an EO-atlas candidate `psiquantum2025`, not
  ingested there): VpiL 0.62 V cm DC non-push-pull (Fig. 5(g), Vpi 3.1 V, L = 2 mm), phase-shifter propagation loss
  53 +/- 3 dB/m (cutback, Fig. 5(f), 1520-1580 nm), phase-shifter IL about 100 mdB, VpiL alpha 0.33 +/- 0.02 V dB;
  BTO film Pockels > 1000 pm/V (free-space, Fig. 5(d)), 3 sigma thickness uniformity < 3 % over 300 mm (p.6). The
  registry `phase_shifter` class is non-EO.
- Photon-pair sources (no registry class for SFWM heralded sources): spectral purity 99.5 +/- 0.1 % (interferometrically
  coupled resonator, p.2 / Fig. 2(b)); cascaded 24-resonator source purity up to 99.7 % (upper bound, flat-phase
  assumption), > 99 % indistinguishability over +/-400 pm vs < +/-40 pm single ring (p.5, Fig. 4(b,c)); CAR up to
  3000, CAR 929 +/- 4, heralded g2(0) 0.00358 +/- 0.00024, Klyshko efficiency ~26 % (p.3-5).
- System / qubit metrics: SPAM 99.98 / 99.996 %, chip-to-chip 99.72 %, HOM 99.50 %, Bell fusion 99.22 % (Table I);
  about 115 dB pump suppression incl. scattered-light shield (p.3).
- Grating couplers and the 2D-grating path-to-polarization converter (baseline): no number (only "high loss", p.4).
- SNSPD dark count rate: log-scale inset only (Fig. 2(e)).
- Baseline thermal phase shifters / undercut: no stated P_pi; only the figure-read MZI value above.

## Questions for the coordinator

1. Version: the cached text is arXiv v1 (2024) without supplement; the Nature version (2025, CC BY, revised, with
   Methods and SI) may print different numbers and more fab detail. Keep v1, or fetch the Nature PDF + SI through the
   `publisher_browser` session / manual inbox as a separate source (or replace this one)?
2. Source identity: `lit:alexander2024` is registered as an arXiv preprint (doi empty). Should the registry row carry
   the Nature DOI (would need a pipeline change: the DOI record's collective first author yields `team2025`)?
3. M1E.4 platform: the paper says only "commercial 300 mm silicon photonics platform"; `soi` entered for the heater and
   filter. Keep, or leave platform empty under D422 (then the Tower P_pi drops out of the SiPh column)?
4. TowerJazz: add alias row `org_tower_semiconductor, TowerJazz, printed_variant, ofc2026` (evidence ofc2026:M1E.4 p.~2
   Sec. 3)?
5. Cryogenic figure-read P_pi (~10 mW, GF baseline, 2 K): keep (excluded from the benchmark by temperature) or drop as
   a low-value figure reading with non-uniform fringe spacing?
6. Temperature 2 K on rows read out by co-integrated SNSPDs (MZI, heater, filter): the temperature is stated for the
   detectors and cryostat, not for each measurement. Keep or move to condition text only?
7. SiN splitter subtype: `directional_coupler` (section heading) vs `other` (text says waveguide splitters)?

## Registry gaps (proposals)

- `phase_error_pi` (unit pi, classes splitter, wdm, switch_fabric): as-fabricated arm phase mismatch of an
  interferometer (M1E.4: 0.13 pi reference MZI; 0.12-0.42 pi across six MZIs).
- Quantum photon-pair source class (e.g. `quantum_source.sfwm`) with `spectral_purity_pct`, `car`,
  `heralded_g2`, `indistinguishability_pct` (alexander2024 p.2-5).
- `rejection_db` for filters (pump / band rejection) if `extinction_db` is judged too generic for a multi-stage
  pump filter.

## Missing orgs

- None missing from the registry. Alias missing: TowerJazz (ofc2026:M1E.4 p.~2 Sec. 3). Optelligent (packaging,
  p.~2 Sec. 3) is not in the registry; not needed (packaging only, note in the component rows).
