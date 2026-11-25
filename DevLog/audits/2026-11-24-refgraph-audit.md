---
title: Fresh-context audit of the reference graph (DevLog-020, run_20261124)
date: 2026-11-24
mode: read-only audit subagent; no script, data or registry file modified; helper scripts kept in the session scratchpad (refgraph_audit/), not in the repo
inputs: cache/literature/refgraph/run_20261124/{refs.jsonl, missing.csv, summary.json}, scripts/lit_refgraph.py, data/registry/sources.csv, data/_staging/literature/cache_list.csv, cache/literature/merged.jsonl, references/<id>/text.md
---

# Reference-graph audit (2026-11-24)

## Summary

| Check | Result |
|---|---|
| Precision, DOI | 20/20 (95% CI 84-100%) |
| Precision, arXiv | 10/10 (72-100%) |
| Precision, title (exact, score 1.0) | 54/55 = 98% (90-100%) (main sample 34/35 + 20/20 extra on 30-40 character titles) |
| Precision, title (partial, 0.90 <= score < 1.0; 546 rows) | 15/20 = 75% (53-89%) strict; 16/20 counting a conference version |
| Precision, title_short | 43/45 = 96% (85-99%) |
| Precision, title_author | 20/40 = 50% (35-65%) same work; 25/40 = 62.5% counting conference / journal versions |
| Weighted precision of all 23,352 accepted rows | about 97.3% strict (about 620 wrong rows), 97.5% lenient |
| Recall sample (100 unmatched) | 8 are not references (body text, fragments); of 92 real references 12 (13%, CI 8-21%) are works present in the corpus (3) or pool (9), plus 2 unsure |
| Recall estimate | about 3,000 (1,700-5,200) unmatched entries are present works; recall of present works about 87-88% (81-93%) |
| Entry splitting | 9 / 12 sampled papers correct entry count; 3 zero-entry papers have 47, 25 and 9+ printed references; population: 1,400 body-text entries in 369 papers (section headings "1. Introduction" chained into Optica-style lists) |
| Dedup (40 clusters, n_citing >= 3) | 40/40 internally the same work (one cluster also holds a same-title conference version) |
| Dedup (top 300 rows) | 5 work pairs split into a pool row and a titleless unresolved row; 25 of 83 unresolved rows are works already in the corpus (12) or pool (13), plus 1 blog registry row |
| Self-citations | 0 accepted rows target the citing paper (same id, same DOI or same title); 89 self hits suppressed |

The builder's statements "a sample of 22 by hand found no missed corpus paper" and D1232 "a `1.` section heading no
longer chains into a reference list" do not hold on the full run (sections 2 and 3).

## Samples and method

- Precision: 150 rows with `matched=true`, seed 20261124, allocation per method doi 20 / arxiv 10 / title 35 /
  title_short 45 / title_author 40, within a method at least 4 rows per kind (or all) and the rest proportional.
  Strata drawn: doi corpus 6 / pool 10 / queued 4; arxiv corpus 5 / pool 5; title corpus 10 / pool 16 / queued 5 /
  registry_uncached 4; title_short corpus 8 / pool 32 / queued 5; title_author corpus 12 / pool 22 / queued 6. Each
  entry read against the matched record (sources.csv, cache_list.csv or merged.jsonl by uid). Supplement (seed
  20261125): 20 title rows with score < 1.0 (A) and 20 title rows with a 30-40 character squashed title (B).
  Judgment classes: same work; version (same research, different publication: conference vs journal, preprint vs
  journal); different work.
- Recall: 100 rows with `matched=false`, seed 20261124. Independent search per entry: rare-unigram (IDF) overlap over
  every corpus and pool title, first-author surname + year over pool authors and cache_list first authors, then
  keyword / DOI greps for every plausible hit.
- Entry splitting: 12 papers chosen by style (seed 20261124 for the style pools): IEEE `[n]` yamaoka2024,
  nedeljkovic2014; APS-like `n.` biberman2012; Optics Express "References and links" fukuda2006, streshinsky2013;
  Optica `n.` with numbered sections xie2022; Nature without heading wang2018b, abel2019; OFC conference brusberg2025;
  zero entries shiue2015, zhang2026d, simpanen2017. Counts compared with the printed list in text.md. Population
  checks on all 1776 texts using the script's own `_starts` / `START_RE`.
- Dedup: union-find rebuilt from `cluster_keys` in refs.jsonl; 20 pool-resolved + 20 unresolved clusters with
  n_citing >= 3 (seed 20261124), every member entry read. Top 300 rows of missing.csv: pairwise title containment /
  ratio >= 0.85 and surname + year pairs with one titleless side; every unresolved top-300 row looked up by exact
  title or surname + year + venue in corpus and pool.

## 1. Precision

### Per stratum

| Method / kind | n | Same work | Version | Different work |
|---|---|---|---|---|
| doi / corpus, pool, queued | 6 / 10 / 4 | 20 | 0 | 0 |
| arxiv / corpus, pool | 5 / 5 | 10 | 0 | 0 |
| title / corpus | 10 | 10 | 0 | 0 |
| title / pool | 16 | 16 | 0 | 0 |
| title / queued | 5 | 5 | 0 | 0 |
| title / registry_uncached | 4 | 3 | 1 | 0 |
| title_short / corpus | 8 | 8 | 0 | 0 |
| title_short / pool | 32 | 30 | 0 | 2 |
| title_short / queued | 5 | 5 | 0 | 0 |
| title_author / corpus | 12 | 7 | 1 | 4 |
| title_author / pool | 22 | 9 | 4 | 9 |
| title_author / queued | 6 | 4 | 0 | 2 |
| Supplement A: title, score < 1.0 | 20 | 15 | 1 | 4 |
| Supplement B: title, 30-40 chars | 20 | 20 | 0 | 0 |

Counted as same work although borderline: chrysostomidis2025#30 (DOI of the Adv. Mater. paper
held by an arXiv pool record), jung2026#25 (Sci. Adv. 2025 cited, arXiv preprint jung2025 in corpus, retitled),
chen2023#18 (entry says "160-nm tuning range", corpus guo2022 "172-nm", same APL Photonics 7 066101), murray2015#16
(manuscript in preparation, now the PTL paper).

### Every wrong or version match in the samples

Different work:

| refs.jsonl citing#n | Method, score | Entry cites | Matched record | Why |
|---|---|---|---|---|
| salamin2018#3 | title_short 1.0 | Yao, "Microwave photonics", JLT 27, 314 (2009) | 10.1002/9780470744857, Wiley book "Microwave Photonics" 2009 (no authors) | generic title; authorless record passes the "no surname + exact year" branch |
| xiang2018#6 | title_short 1.0 | same Yao JLT 2009 | same Wiley book | same |
| dostart2020#16 | title_author 0.7727 | Poulton, "High-performance integrated optical phased arrays for chip-scale beam steering and LiDAR", CLEO 2018 | lit:poulton2018 "Optical Phased Arrays for Integrated Beam Steering" (GFP 2018) | same group, same year, different paper |
| ni2025#15 | title_author 0.7963 | Badri, "Multimode waveguide crossing based on a square Maxwell's fisheye lens", Appl. Opt. 2019 | lit:badri2019 "3x3 slot waveguide crossing based on Maxwell's fisheye lens" | same author, different paper |
| antelius2011#7 | title_author 0.7887 | Van Laere, "Compact grating couplers ... 69% coupling efficiency", OFC 2006 | lit:taillaert2006 "Grating couplers for coupling between optical fibers and nanophotonic waveguides" (JJAP) | surname check passes on the 4th author (any of the first 40 words) |
| olivares2021#16 | title_author 0.8462 | Song, "Silicon photonic integrated circuits with electrically programmable non-volatile memory functions", Opt. Express 24, 21744 | lit:song2016 "Integrated photonics with programmable non-volatile memory" (Sci. Rep.) | two papers of one group, 2016 |
| osorniomartinez2025#8 | title_author 0.8023 | Liu, "Temperature-dependent gain characteristics of InAs/InP QDash SOAs", Photonics North 2020 | 10.1364/iprsn.2020.itu2a.4 "Gain characteristics ... between S- and C-bands" | different conference paper |
| itoh2024a#16 | title_author 0.8025 | Itoh, "High-power single-mode operation of 1.3 um double-lattice PCSELs using InP-based regrowth", ISLC 2022 | 10.1364/oe.461048 "High-power CW oscillation of 1.3-um InP-based PCSELs" | different paper |
| itoh2024#6 | title_author 0.8025 | same ISLC 2022 paper | same OE record | same |
| wang2025#22 | title_author 0.75 | Ghods, "Polarization-stable single-mode multi-junction VCSELs with integrated anti-phase mode filter", J. Appl. Phys. 2023 | 10.1109/jlt.2023.3240123 "Design and fabrication of single-mode multi-junction 905 nm VCSEL ..." | different paper |
| liu2019#29 | title_author 0.7981 | Kotb, "2 Tb/s all-optical gates based on TPA in QD-SOAs", Opt. Laser Technol. 2019 | 10.1007/s11082-019-2142-z "All-optical NOR and XNOR logic gates at 2 Tb/s ..." (Opt. Quantum Electron.) | different paper |
| gentry2015#20 | title_author 0.8261 | Harada, "Generation of high-purity entangled photon pairs using silicon wire waveguide", OE 16, 20368 | 10.1364/oe.16.005721 "Generation of polarization entangled photon pairs ..." (Takesue first author) | different paper; surname check passes on a co-author |
| fu2020#6 | title_author 0.7571 | Liu, "Advanced development of 850 nm oxide-confined VCSELs with 57 Gb/s ...", GOMACTech 2016 | 10.1364/cleo_si.2016.sf1l.6 "850 nm oxide-confined VCSELs with 50 Gb/s ... up to 85 C" | different paper |
| lee2012#5 | title_author 0.8889 | Ilchenko & Matsko, "Optical resonators with whispering-gallery modes - part II: applications" | 10.1109/jstqe.2005.862952 "... part I: basics" | part I vs part II |
| akin2024#21 | title_author 0.8205 | Chopin, "Ultra-efficient generation of time-energy entangled photon pairs in an InGaP PhC cavity", Commun. Phys. 2023 | 10.1364/cleo_fs.2023.fm4e.4 "Generation of time-energy entangled photon pairs in bichromatic PhC cavities" | different paper |
| pospischil2013#5 | title_author 0.75 | Park, "A hybrid AlGaInAs-silicon evanescent waveguide photodetector", OE 15, 6044 | lit:park2007a "A hybrid AlGaInAs-silicon evanescent preamplifier and photodetector" | different paper |
| xie2026#11 | title_author 0.7875 | Shen, "Ultra-low-crosstalk silicon AWG with 1.6-nm channel spacing", LPR 2024 | lit:shen2024 "High-performance silicon AWG with 0.4-nm channel spacing" (Adv. Photon. Nexus) | different paper |
| bauters2011#6 (suppl. A) | title 0.9706 | Kippenberg, "Demonstration of ultra-high-Q small mode volume toroid microcavities on a chip", APL 2004 | lit:armani2003 "Ultra-high-Q toroid microcavity on a chip" | scattered-block containment of a short title inside a longer one |
| kashiwazaki2021#14 (A) | title 0.9865 | Myers, "Quasi-phase-matched 1.064-um-pumped OPO in bulk PPLN", Opt. Lett. 20, 52 | 10.1364/josab.12.002102 "Quasi-phase-matched optical parametric oscillators in bulk PPLN" | different paper |
| gasse2019#1 (A) | title 0.9362 | body text ("Introduction Silicon photonics is ...") | ofc2026:Tu3H.3 "Photonic Integrated Circuit for Optical Beam Steering" | not a reference (section 3) |
| otterstrom2019#34 (A) | title 0.9429 | Pant, "Photonic-chip-based tunable slow and fast light via SBS", Opt. Lett. | lit:pant2011 "On-chip stimulated Brillouin scattering" | different paper |

Version (same research, different publication):

| citing#n | Method, score | Entry | Matched record |
|---|---|---|---|
| wang2026g#17 | title 1.0 | Ahmed, "Universal photonic artificial intelligence acceleration", Nature 640 (2025) | ofc2026:W3C.6 same title, OFC 2026 talk |
| riedhauser2025#30 | title_author 0.75 | Wu, "OH absorption in on-chip high-Q resonators", NLO 2023 | lit:wu2023 "Hydroxyl ion absorption ..." (Opt. Lett.) |
| parra2020#29 | title_author 0.8028 | Li, "Ultracompact silicon-conductive oxide nanocavity modulator ...", Nano Lett. 2018 | CLEO 2018 abstract |
| fan2021a#2 | title_author 0.8148 | Fotiadis, "16x16 silicon photonic AWGR ...", SPIE 2020 | IEEE PTL 2020 |
| ono2016#11 | title_author 0.7531 | Nielsen, "Adiabatic nanofocusing in hybrid gap plasmon waveguides ...", Nano Lett. 2016 | CLEO 2016 abstract |
| billah2018#32 | title_author 0.7671 | Lucci, "Thermal management of monolithic and heterogeneous integrated lasers", CSW 2016 | IEEE JSTQE 2016 |
| yu2023a#6 (A) | title 0.9825 | Niwa, "Tipping point for the future scalable OXC ...", JOCN 2017 | OFC 2016 abstract, same title |

### Failure modes (precision)

1. `title_author` (0.75-0.90 with surname + exact year) mostly pairs two papers of one group in one year: 15 of 40
   different works, 5 versions. Score separates them partly: at score >= 0.85 the sample keeps 13 of 14 correct (one
   wrong: lee2012#5, part I / part II at 0.889); 7 correct rows lie below 0.85. Eight of the 20 correct rows differ
   from the record only by a trailing "[Invited]" in the OpenAlex title (kumar2025#10, li2024#19, yang2020a#37,
   hu2025a#5, xu2022a#46, kuznetsov2025#53, qi2025#11, bao2024#15).
2. The surname check accepts any author in the first 40 words (antelius2011#7: 4th author; gentry2015#20: 2nd).
3. Partial title containment (0.90 <= s < 1.0) sums SequenceMatcher blocks of >= 4 characters anywhere in an entry of up
   to 1200 characters, so a shorter title is "contained" in a longer different title (bauters2011#6,
   kashiwazaki2021#14, otterstrom2019#34). 546 rows, about 25% wrong.
4. Authorless and venue-named pool records: "Microwave Photonics" Wiley book (6 rows), Choice review
   10.5860/choice.45-0306 for "Fundamentals of photonics" (4), and records titled with a journal name:
   10.1109/jstqe.2017.2648419 and 10.1109/jstqe.2016.2559120 "IEEE Journal of Selected Topics in Quantum Electronics"
   (13 + 11 rows), 10.1109/jlt.2016.2529780 "Journal of Lightwave Technology" (9), 10.1109/jlt.2016.2635921
   "Proceedings of the IEEE" (1). These 34 venue-title rows put 3 bogus works in the top 300 of missing.csv (ranks
   145, 181 and one at n=8).
5. Body text treated as an entry (section 3) matched by title containment: 61 accepted rows, e.g. adya2024#1 ->
   lit "Large-scale photonic integrated circuits", castro2025#1 -> "Hybrid and heterogeneous photonic integration",
   ai2024#5 -> "LXXVI. Facts relating to optical science. No. IV".
6. Same title, different publication (conference vs journal) is accepted at 1.0 with no venue check (wang2026g#17,
   yu2023a#6).

## 2. Recall

### Sample outcome (100 unmatched rows)

| Class | Count |
|---|---|
| Not a reference: body text from a section heading (zhang2022c#1, zhou2020a#3, govdeli2025#3, rawat2023#1, zhong2021#2, moralesalvarado2026#3, ayan2023#4) | 7 |
| Not a reference: fragment ("M. Knoedler 'Observation Res. 17(12),", thai2018#7) | 1 |
| Real reference, work present in corpus | 3 |
| Real reference, work present in pool | 9 |
| Real reference, unsure presence | 2 |
| Real reference, absent (books, theses, patents, web pages, old or off-topic papers, works outside the pool) | 78 |

Two entries also carry page-footer text (a2017#11 Wiley footer, stanton2017#12 "Vol. 25, No. 24", yokokawa2022#7
"Authorized licensed use limited to ...", margaria2025#50 "Nature Communications| (2025) 16:7553"), and armani2003#19 /
#20 come from the neighbouring Nature article's list (section 3).

### Every missed match in the sample

| citing#n | Entry | Present as | Cause |
|---|---|---|---|
| beeck2021#7 | McKenna et al., Optica 7, 1737 (2020) | pool 10.1364/optica.397235 | titleless entry |
| wang2023a#30 | Shang et al., Light Sci. Appl. 11, 299 (2022) | pool 10.1038/s41377-022-00982-7 | titleless |
| ji2020#20 | Cherchi et al., Opt. Express 21, 17814 (2013) | corpus lit:cherchi2013 (DOI 10.1364/oe.21.017814 derivable) | titleless |
| tan2009#7 | Murphy, Hastings, Smith, J. Lightwave Technol. 19, 1938 (2001) | pool 10.1109/50.971688 | titleless |
| ji2026#35 | Huang et al., Phys. Rev. A 99, 061801 (2019) | pool 10.1103/physreva.99.061801 (derivable) | titleless |
| pu2016#33 | Xue et al., Nat. Photonics 9, 594 (2015) | pool 10.1038/nphoton.2015.137 | titleless |
| guo2023#5 | Ludlow et al., Rev. Mod. Phys. 87, 637 (2015) | pool 10.1103/revmodphys.87.637 (derivable) | titleless |
| fang2021#22 | Shen et al., Nature Photon 2017, 11, 441 | corpus lit:shen2017 (in-degree 46) | titleless |
| raja2019#6 | Leo et al., Nature Photonics 4, 471 (2010) | pool 10.1038/nphoton.2010.120 | titleless |
| ren2025#7 | Cheng et al., Laser Photonics Rev. 2025, 19, 2401491 | corpus lit:cheng2024 (DOI 10.1002/lpor.202401491 derivable) | titleless |
| isichenko2023#10 | Blumenthal, "Silicon Nitride in Silicon Photonics", Proc. IEEE 106 (2018) | pool 10.1109/jproc.2018.2861576 | candidate generation: every title bigram is common ("silicon nitride", "silicon photonics" over BIGRAM_DF_MAX), one bigram left, candidates need >= 2 |
| li2025b#9 | Zhu, "Integrated photonics on thin-film lithium niobate", AOP 13 (2021) | pool 10.1364/aop.411024 | candidate generation, same cause |
| jasion2020#2 (unsure) | Bradley et al., Proc. ECOC 2019, PDP Th3F.1 | pool 10.1049/cp.2019.1028 (Bradley, ECOC 2019, 0.65 dB/km AR fibre) | titleless; postdeadline id not checkable offline |
| pitris2018#11 (unsure) | Grani, "Flat-topology high-throughput compute node with AWGR-based optical interconnects", JLT 34 (2016) | pool openalex:W2745409210, Japanese-titled JST record, JLT | title only in Japanese in the pool |

10 of the 12 sure misses are titleless entries (APS / AIP / Optica short style and some Wiley / Nature citations
without a title); 2 are candidate-generation misses. Titleless real references in the sample: 19 of 92, of which 11
(58%) were present works.

### Population checks

- Unmatched entries whose quoted title squashes exactly to a corpus / pool title: 386 of 12,965 quoted unmatched.
  Of these, 240 also agree on the year (+/- 1) and are not self titles or generic short titles: 212 candidate
  generation misses (e.g. stone2026#31 and li2025b#9 Zhu TFLN, boust2020#10 / levy2012#15 Kippenberg 2011 "Microresonator-based
  optical frequency combs", fan2025#3 Blumenthal) and 28 entries with glued words ("Chip-integratedvisible-telecomentangledphotonpairsource",
  gundlapalli2022#19 -> lit:lu2019a; wilmart2020#27), where `words()` yields no bigrams. 58 exact-title hits fail the
  year check and are correctly rejected (e.g. poletti2014#43 Heiblum 1975 vs a 2025 JQE paper of the same title).
- Extrapolation: about 8% of the 24,734 unmatched rows are not references (direct count in section 3: about 1,400
  body-text entries) and 12-14% are works present in corpus or pool: about 3,000 rows (CI 1,700-5,200). With about
  22,730 correct accepted rows, recall of present works is about 87-88% (CI 81-93%).

## 3. Entry splitting

### 12 papers

| Paper | Style | Printed | refs.jsonl | Notes |
|---|---|---|---|---|
| yamaoka2024 | IEEE `[n]` | 26 | 26 | entry 3 ends with the running header "JOURNAL OF LIGHTWAVE TECHNOLOGY, VOL. 42, NO. 24, DECEMBER 15, 2024" (adds the citing year 2024 to the entry's years); last entry cut at "Paper Th." |
| nedeljkovic2014 | IEEE `[n]` | 18 | 18 | clean |
| biberman2012 | `n.` without titles | 22 | 22 | clean split; every entry titleless (matching relies on DOI only) |
| fukuda2006 | OE "References and links" at top | 12 | 12 | clean |
| streshinsky2013 | OE top | 29 | 29 | clean (two URL-only entries) |
| xie2022 | Optica `n.` with numbered sections | 25 | 25 | entry 1 is body text from "1. Thanks to the bending waveguide ..." (line 353); the real ref 1 (Martinod et al., line 380) is lost |
| wang2018b | Nature, no heading | 48 | 48 | entry 32 runs into the acknowledgements (clipped at 500); entry 34 carries "Springer Nature Limited. All rights reserved. Letter RESEARCH" |
| abel2019 | Nature Materials | 53 | 53 | entry 3 carries a page footer ("Nature Materials"), entry 52 runs into the acknowledgements |
| brusberg2025 | OFC `[n]` | 7 | 7 | clean |
| shiue2015 | AIP superscript ("1M. Hochberg ...") | 47 | 0 | number glued to the initial: no START_RE form matches |
| zhang2026d | Wiley "1 . W. Bogaerts" | 25 | 0 | space before the dot: neither `n.` nor bare form matches |
| simpanen2017 | IET, number alone on its line | >= 9 | 0 | bare form needs `\s+[A-Z]` on the same line; entries carry DOIs that would match |

### Population checks

- Section-heading capture (contradicts D1232): `split_references` keeps the longest run and, on equal length, the first
  `1`. An Optica-style paper with "1. Introduction", "2. Design", ... and an `n.` reference list yields a run that takes
  sections 1..k and continues into the reference list at k+1, same length as the true run. Counted: 1,400 entries
  in 369 papers start with a section word, are >= 300 characters and have n <= 12 (n=1: 368, 2: 265, 3: 276, 4: 273,
  5: 151). Twelve random ones read: all body text. Re-running the script's own run search: 452 papers have a tie
  between runs of equal length. Effect: the first 1-6 real references of these papers are dropped, the body text is
  matched (61 accepted rows, section 1) or clustered into missing.csv.
- Zero-entry papers (203): 70 with no heading and no numbered run and 54 with a heading but no numbered run (mostly
  pre-1990 footnote or author-year papers, some conference papers); 36 with lone-number lines (run >= 5: du2018 60,
  jinguji1995 22, chen2024c 11, haus1976 8), 26 with glued superscript numbers (gehring2019 38, hickstein2019 37,
  jiang2018 29, lake2016 23), 2 with "n ." (sun2026 34, zhang2026d 25), 14 with a `[n]` / `n.` run of 5+ rejected by the
  length or year rules (bino2018 37, reck1994 10), 1 almost empty text (okai1990).
- Second lists: 37 papers hold a disjoint second run of >= 10 entries. Most are supplementary or Methods lists that
  restart at 1 and are dropped (kramnik2024: 74 main + 70 supplementary; tian2021 115 + 34). In armani2003 the chosen
  28-entry run is the neighbouring Nature article's list (Greene "The Elegant Universe", Moody and Wilczek); the
  paper's own 23 references start at line 344 and are dropped. Equal-length ties between two lists: chatterjee2019
  19/19, nie2019 23/23, sun2022 14/14.
- Footer / header text inside entries: 421 entries contain rights / licence / publisher footers (233 of them
  matched), 56 entries in 55 papers carry an IEEE running header with the citing paper's volume and date.

## 4. Dedup

### 40 sampled clusters (n_citing >= 3)

- Pool-resolved, 20 clusters (e.g. Siew 2021 review n=28, Chrostowski / Hochberg book n=40, Justice 2012 n=12, Shi
  2015 isolators n=9): every member entry is the same work. One cluster (Frey 2006, zhong2021#28) lists the SPIE editors
  first; same work.
- Unresolved, 20 clusters: every member is the same work. Surname + year + page keys merged a titled and a titleless
  citation correctly (Griffith 2012: liu2021a#72 "Opt. Express 20, 21341 (2012)") and a citation with a variant title
  (Rho 2004, hwang2007#3 "Low-crosstalk and high-efficiency ..." with JLT 22, 2128). The Taubenblatt cluster also holds
  tossoun2024#5, the 2011 IEEE Photonics Society meeting talk of the same title.
- 3 of the 20 unresolved clusters are corpus works cited without titles: bib:delhaye|2007|1214 (lit:delhaye2007, n=9),
  bib:raja|2019|680 (lit:raja2019, n=7), bib:miller|2017|346 (lit:miller2017a, n=3).

### Top 300 rows (216 pool, 83 unresolved, 1 registry; n_citing >= 8)

Same work in two rows (pool row + titleless unresolved row):

| Pool row (rank, n) | Unresolved row (rank, n) | Work |
|---|---|---|
| #20, 25, 10.1038/nphoton.2013.183 | #107, 13, bib:moss\|2013\|597 | Moss 2013, Nat. Photonics 7, 597 |
| #70, 14, 10.1038/s41566-019-0358-x | #161, 11, bib:gaeta\|2019\|158 | Gaeta 2019, Nat. Photonics 13, 158 |
| #78, 14, 10.1126/science.aao3924 | #249, 9, bib:trocha\|2018\|887 | Trocha 2018, Science 359, 887 |
| #97, 13, 10.1126/science.aao1968 | #248, 9, bib:suh\|2018\|884 | Suh 2018, Science 359, 884 |
| #116, 12, 10.1038/ncomms8957 | #246, 9, bib:liang\|2015\|7957 | Liang 2015, Nat. Commun. 6, 7957 |

Further pairs across the whole list (pool row below the top 300): Zhu TFLN review unresolved #8 (n=31) + pool row
10.1364/aop.411024 (n=3); Kippenberg 2011 #9 (29) + 10.1126/science.1193968 (1); Blumenthal 2018 #31 (21) +
10.1109/jproc.2018.2861576 (3); Roelkens 2010 #84 (14) + 10.1002/lpor.200900033 (5); Cheben 2018 #86 (14) +
10.1038/s41586-018-0421-7 (3).

Unresolved top-300 rows that are already in the corpus (should not be in missing.csv): #133 Herr 2014 Nat. Photonics
8, 145 (lit:herr2014), #162 Ji 2017 Optica 4, 619 (lit:ji2017), #163 Wang 2018 Nature 562, 101 (lit:wang2018b),
#164 Xuan 2016 Optica 3, 1171 (lit:xuan2016), #165 Zhang 2017 Optica 4, 1536 (lit:zhang2017a), #166 Zhang 2019
Nature 568, 373 (lit:zhang2019b), #167 Spencer 2018 Nature 557, 81 (lit:spencer2018, key raw:dtspencer...), #192
Chang 2016 Optica 3, 531 (lit:chang2016), #193 Marin-Palomo 2017 Nature 546, 274 (lit:marinpalomo2017; bib key
surname "marin" vs corpus "palomo"), #245 Del'Haye 2007 (lit:delhaye2007), #247 Stern 2018 Nature 562, 401
(lit:stern2018), #250 Wang 2018 Optica 5, 1438 (lit:wang2018). Present in the pool: #8, #9, #25 Hochberg 2010, #31,
#45 Rickman 2014, #84, #86, #107, #161, #197 Coddington 2016, #246, #248, #249. In the blog registry: #16 Jalali
2006 "Silicon photonics" (n=26; blog:jalali2006_silicon_photonics has no year or surname, so the title_short rule
cannot accept it). Total 26 of 83 unresolved top-300 rows (31%) are resolvable offline.

Not duplicates although similar: "Integrated microwave photonics" Marpaung 2019 Nat. Photonics (#21) vs Marpaung 2013
LPR (#114); Watts 2005 splitter (#125) vs rotators (#238); Herr 2014 Nat. Photonics (#133) vs Herr 2014 PRL (#295).

## 5. Self-citations

- 0 accepted rows where the target is the citing paper, checked by id, by the citing paper's DOI and by its squashed
  title (so no self match through an eo / pk / pool duplicate of the same paper).
- 380 rows have the citing paper as best candidate, 89 of them above threshold and suppressed. A random 12 of the 89:
  5 cite an earlier conference version or dataset with a near-identical title (jean2019#15, snyder2018#6, suzuki2018#11,
  rombouts2024#38, iseghem2022#27), 5 are body text (zhang2020#2, zhou2020a#3, wang2026e#5, pita2023#4, and the
  horiguchi1976#5 glued page), 2 are glued entries that contain the paper's own title (akahane2003#16, bakonyi2003#6).
  Because the pool is skipped when the corpus result is accepted, the conference versions (e.g. notaros2019#3 ->
  10.1364/cleo_si.2019.stu3o.4, same title) are not resolved and go to missing.csv as unresolved rows.

## Recommendations to the coordinator

1. Run selection: on equal or near-equal run length prefer the run whose `1` is closest to its `2` (the latest `1`),
   and reject a start whose entry has no year and is over about 300 characters or begins with a section word.
   Expected: about 1,400 real first references recovered in 369-452 papers, about 1,400 body-text rows and 61 false
   matches removed.
2. START_RE: add glued superscript (`^\d{1,3}(?=[A-Z][a-z]?\. )`), "n ." (`^\d{1,3} \.\s`) and a lone number line
   followed by an author line. Expected: about 64 of the 203 zero-entry papers gain lists (shiue2015 47, du2018 60,
   gehring2019 38, zhang2026d 25, sun2026 34); entries in IET lists carry DOIs.
3. Titleless entries: (a) build DOIs from venue + volume + page where the pattern is fixed: Optica legacy journals
   (10.1364/oe.VV.PPPPPP etc. for OE, OL, AO, JOSA B, OME, BOE, Optica up to about 2018), APS
   (10.1103/physreva.VV.PPPPPP, physrevlett, revmodphys), Wiley article numbers (10.1002/lpor.NNNNNNNNN); (b) else
   first-author surname + year + venue, accepted when the page / article number appears in the candidate DOI or the
   candidate is unique after the venue check. A prototype on the 6,157 unmatched titleless entries with a bib key
   matched 1,098 (75 corpus, 1,023 pool); 19 of 20 sampled correct (the wrong one, sun2024#36, had an unquoted title,
   so apply the unique-venue branch only to entries with no title text). Expected: covers the 10 titleless
   recall-sample misses (not verified one by one), the 5 duplicate pairs and 12 corpus works listed as missing in the top 300.
4. Candidate generation: add an exact squashed-title lookup (dict of corpus + pool squashed titles, with year check)
   for the first quoted title, and for titles with at most one indexable bigram accept one shared bigram (or fall
   back to rare unigrams). Expected: about 240 more matches, including unresolved top rows #8 (31 citing), #9 (29),
   #25 (23), #31 (21), #45, #84, #86, #197 and their pool duplicates; also catches glued-word entries if the lookup
   slides over the squashed entry.
5. Strip "[Invited]", "(Invited)" and "Invited paper" from record titles before squashing. Expected: 8 of the 20
   correct title_author rows in the sample become exact title matches, so rule 6 loses little.
6. title_author: raise AUTHOR_MIN from 0.75 to 0.85 and require the record surname to be the entry's first author
   (`first_surname(entry)`), not any of the first 40 words. Expected: precision of the rule from 50% to about 90%
   (13/14 in the sample at >= 0.85), about 80 of the 168 rows dropped, most of them wrong.
7. Partial title containment (0.90-1.0): require the longest single block to cover >= 0.6 of the title, or score
   against the quoted title when one exists with a symmetric ratio >= 0.90. Expected: removes most of the about 135
   wrong rows among the 546 (bauters2011#6, kashiwazaki2021#14, otterstrom2019#34 type).
8. Pool hygiene: drop records whose squashed title equals a venue name or front matter (4 records, 34 rows, three of
   them in the top 300) and do not accept authorless records through the title_short "exact year, no surname" branch
   (21 rows: Wiley "Microwave Photonics", Choice review, JLT / Proc. IEEE venue titles).
9. Venue check for same-title matches: when the entry names a clearly different venue type (journal vs conference,
   Nature vs OFC) prefer a candidate whose venue agrees, otherwise mark the row "version" (wang2026g#17, yu2023a#6,
   and the 5 title_author versions). Parse "Surname Year, " from blog titles for surname and year (Jalali 2006, n=26).
10. Self hits: when the best corpus candidate is the citing paper, still run the pool, and label the remaining rows
    "self_version" instead of adding them to missing.csv (89 rows).
11. Second lists: when a disjoint run of >= 10 exists, keep the run nearest the end of the paper's own text (Nature
    pages that carry a neighbouring article's references) and keep supplementary runs as extra entries numbered
    separately; at least flag the 37 papers. armani2003 currently has the wrong list.
12. Entry cleanup: remove IEEE running headers (journal, VOL., NO., date line), "Authorized licensed use limited to ...
    Downloaded on ..." lines, Nature "Letter RESEARCH" / Springer rights lines and acknowledgement paragraphs before
    year extraction; they add the citing paper's year to the entry's years (421 + 56 entries).
13. DevLog-020: correct D1232 (section headings still chain into `n.` lists) and the unmatched-sample claim (this
    sample: 3 corpus misses in 92 real references; 12 corpus works among the 83 unresolved top-300 rows).
