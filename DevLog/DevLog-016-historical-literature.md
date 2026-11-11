# DevLog-016: Historical literature layer (1842-2020): eras, threads, institutes, DRIs, ~300 papers to cache and ingest

| | |
|---|---|
| Date | 2026-11-11 |
| Status | Proposal delivered (list + plan, two fresh-context audits applied); waiting on Q1-Q3 before retrieval (inspection point D959) |
| Scope | Candidate research (14 subagent streams), central DOI verification, selection, DRI resolution, retrieval and ingest plan; list in `data/_staging/literature/history_candidates.csv` |
| Decisions | D950-D979 reserved for this DevLog |

## Request (2026-11-10, Wentao)

"Currently the caching/ingestion focus is on recent progress, and the historic progressions are lacking. Take my own
historic blog for example (fiber2chip history, cover image: references from early light guiding in water to the PLC era).
Dispatch research agents, expand on the eras and topics and institutes that are historically important (Bell Labs,
laser invention, nonlinear optics discovery, fiber discovery, integrated optics era, PLC era, EDFA etc.), and propose
~100 historically important papers to cache and ingest. You compose the list; I can help with the licensed download.
Ask questions after research; if all clear, deliver a DevLog."

Follow-ups (2026-11-11): "Does not need to be exactly 300, 100 or 200, totally fine. Make sure you have the DOIs [typed
DRIs], and cover the timeline up to ~2020." Then: "Having historic figures distilled is also good. Keep it as in
scope." Both are covered: every paper with a DOI has it (D961), and each row carries its directly responsible
individual(s) (DRI, D953).

## Starting point (2026-11-10)

- Registry: 2711 sources (lit 880, ofc2026 830, pk 299, lin 282, eo 235, blog 128, web 57). Sources with a year
  before 2000: 3 (two theses, one proxy statement). Oldest `lit` paper: 2000. DevLog-006 D121 restricted enumeration
  to 2016-2026; landmarks entered only via seeds.
- The `blog` corpus (128 PDFs in the blog repo, `text_cached = false`, no DOI / year in the registry) already holds the
  cover-image set and other classics (Colladon 1842, Maxwell 1865, Hopkins 1954, Schawlow 1958, Kao 1966, Tien 1969 /
  1971 / 1977, Smit 1988, Soref 1986, Waldhausl 1997, Ilchenko 1999, Cai 2000, Roelkens 2005, Doerr 2006 / 2008):
  14 core rows ingest from disk without a download.

## Method

1. Shared brief: primary paper over reviews; every field from a retrieved record; an `evidence_url` per significance
   claim; priority disputes recorded; international labs; no PDFs downloaded; no personal identifiers in requests; no
   repo edits.
2. Wave 1 (9 streams, 2026-11-11 07:40-08:02 UTC): foundations (1842-1960), maser / laser, semiconductor
   optoelectronics, nonlinear optics, optical fiber, integrated optics, PLC / WDM / EDFA / systems, silicon photonics
   and microcavities to ~2010, institute sweep (`DevLog/research/2026-11-11-history-institutes-map.md`).
3. Wave 2 (5 streams, 08:10-08:42 UTC): Si photonics industrialization 2006-2020, new platforms and integrated
   nonlinear / microcombs, InP PICs / transceivers / SDM / hollow core, nanophotonics / programmable / quantum /
   nonreciprocal, pre-2008 gap fill.
4. Central verification (coordinator, no subagent): every DOI fetched from Crossref (title, year, first author) and
   OpenAlex (OA status, best OA copy, citations) through `litfetch` (per-host lock, breaker, generic User-Agent); the
   wave-2 streams and audits used the same client through a small helper. 549 rows, 506 with a DOI: every DOI
   resolved; mismatches are only online-vs-print year (print year kept) and 3 Crossref section titles (Faraday 1846,
   Purcell 1946 APS meeting abstract, Woodbury 1962 Proc. IRE "Correspondence"; DOIs correct). OpenAlex cost 0 USD.
5. Merge: dedupe by DOI, then DOI-less rows by title and by hand; selection (D951); two fresh-context audits (D960);
   DRI resolution by 4 subagents from evidence pages (D953).

Wave-1 agents were throttled by Crossref (429 via WebFetch) and the session web-search cap; bibliographic fields were
re-checked in step 4, but some `evidence_url` values stay thin (Known gaps).

## Eras and threads

| era | years | what changed |
|---|---|---|
| E0 | 1842-1959 | light guided in water jets and glass, field theory, dielectric-rod and metal waveguides at Bell Labs, coupled-wave theory, fiberscopes, maser |
| E1 | 1960-1969 | ruby / HeNe / Nd lasers, resonator and Gaussian-beam theory, SHG and parametric optics, diode lasers (four 1962 groups), heterostructure proposal, Kao-Hockham, Bell Labs integrated-optics program (Miller, Marcatili, Tien, Kogelnik) |
| E2 | 1970-1979 | 20 dB/km then 0.2 dB/km fiber, MCVD / OVD / VAD, CW room-temperature DH lasers, DFB, Ti:LiNbO3, switched couplers, COBRA, MMI self-imaging, FBG, VCSEL concept, Si V-groove fiber arrays, first field systems |
| E3 | 1980-1989 | long-wavelength single-mode systems, QW / QD / strained lasers, QW electroabsorption, silica PLC at NTT, MT connector, phasar, EDFA, photonic bandgap, Si and SiN as waveguide materials |
| E4 | 1990-1999 | AWG and PLC products, QPM / PPLN, Tb/s WDM, MMI theory, thick-SOI ribs, Smart Cut, flip-chip MQW-on-CMOS I/O, microrings, PCF, photonic-crystal cavities and lasers, UTC-PD, Ge-on-Si |
| E5 | 2000-2009 | GHz Si modulators, Si Raman and hybrid lasers, grating couplers and tapers, CMOS photonics (Luxtera, imec), LN-on-insulator, frequency combs and microcombs, coherent DSP, waveguide quantum circuits |
| E6 | 2010-2020 | foundry Si photonics and PDKs, Ge lasers / detectors, QD lasers on Si, ultra-low-loss SiN, TFLN, soliton microcombs, PWB and printed micro-optics, MZI meshes, OPAs, nonreciprocal / Brillouin, parallel optical modules and CPO origins (TeraPHY, 45CLO) |

Core papers by thread and era (reserve in the last row). `core_reason`: priority A 230, override 31, cached tag 23,
owner seed 11; E6 holds 36 cached tags (free), so use `core_reason != cached_tag` when a timeline should show only
selected landmarks.

| thread | E0 | E1 | E2 | E3 | E4 | E5 | E6 | core |
|---|---|---|---|---|---|---|---|---|
| guided-wave and EM foundations | 12 | | | | | | | 12 |
| lasers | 3 | 7 | | | 1 | | | 11 |
| semiconductor optoelectronics | | 6 | 9 | 7 | 4 | | | 26 |
| nonlinear optics and combs | | 3 | 3 | 2 | 3 | 6 | | 17 |
| optical fiber | | 5 | 14 | 5 | 4 | | 3 | 31 |
| integrated optics (dielectric, LiNbO3, III-V) | | 5 | 16 | 3 | 3 | | | 27 |
| PLC, WDM, EDFA, systems | | | 1 | 9 | 9 | 5 | | 24 |
| InP PICs, transceivers, systems | | | | 3 | 5 | 2 | 6 | 16 |
| silicon photonics and microcavities | | | | 6 | 8 | 20 | 27 | 61 |
| new platforms and integrated nonlinear | | | | 2 | 1 | 4 | 29 | 36 |
| nanophotonics, programmable, quantum, nonreciprocal | | | | 2 | 4 | 7 | 21 | 34 |
| total core | 15 | 26 | 43 | 39 | 42 | 44 | 86 | 295 |
| reserve | 18 | 29 | 29 | 28 | 23 | 46 | 55 | 228 |

## Institutes

Counts are core papers whose `institutions` field names the institute: a lower bound (the field is empty for 134 core
rows until header extraction fills it, DevLog-011, and some multi-institution papers list one lab). Notes and sources:
`DevLog/research/2026-11-11-history-institutes-map.md`.

| institute | core | span | examples |
|---|---|---|---|
| Bell Labs, AT&T, Lucent, Bellcore | 36 | 1936-2018 | southworth1936, miller1954, fox1961, javan1961, miller1969, marcatili1969, hayashi1970, kogelnik1971, macchesney1974, henry1982, miller1984, desurvire1987, dragone1991a, faist1994, ranka2000 |
| NTT | 10 | 1977-2015 | izawa1977, miya1979, kawachi1983, takato1988, takahashi1990, jinguji1995, inoue1997, ishibashi1997 |
| Caltech, JPL | 10 | 1973-2020 | somekh1973, ilchenko1999, painter1999, cai2000, armani2003, eichenfield2009 |
| MIT (incl. Lincoln Lab) | 9 | 1962-2017 | quist1962, hsieh1976, little1998, liu2010, sun2013, sun2015 |
| KIT | 8 | 2009-2018 | koos2009, lindenmann2012, melikyan2014, haffner2015, billah2018 |
| IBM | 7 | 1962-2019 | nathan1962, dakss1970, assefa2010, barwicz2015, abel2019 |
| Univ. Southampton | 7 | 1975-2020 | payne1975, poole1985, mears1987, knight1996, poletti2014, jasion2020 |
| Stanford, Cornell | 5 each | 1984-2019 | goodman1984, fejer1992, kuo2005, xu2005, levy2010 |
| EPFL, Harvard, UCSB, Yale, Intel, Infinera, Max Planck, Columbia, CRC Canada, American Optical, Tokyo Tech, Ghent / imec | 3-4 each | 1954-2020 | herr2014, wang2018b, spencer2018, liu2004, nagarajan2005, delhaye2007, gordon1954, hill1978, koester1964, soda1979, acoleyen2009 |
| Hughes, GE, UCL, JILA / NIST, Corning, STL, NEC / Nippon Sheet Glass, Ioffe, Lebedev, Fujitsu, KDD, Kyoto, Surrey, Polaroid, Thomson-CSF, Delft, Luxtera, Acacia, Ayar Labs | 1-2 each | 1954-2020 | maiman1960, hall1962, kapron1970, kao1966, uchida1970, alferov1970, basov1954, onaka1996, suzuki1987, akahane2003, adams1986, snitzer1988, papuchon1975, smit1988, gunn2006, doerr2014, wade2020 |

Additions from audit B also reach Delft (vellekoop1991), imec (bogaerts2005), CEA-LETI (bruel1995), TU Berlin
(kirstaedter1994), Corning OVD (schultz1980), ETH Zurich (rabiei2004); their institutions are filled at header
extraction. Still under-served (no confirmed primary record): BTRL beyond doran1988, HHI, IBM Zurich, CNET, CSELT,
Philips, Tohoku (Nishizawa), Hitachi (aoki1991 to verify).

## Decisions (D950-D964)

| id | decision | reason |
|---|---|---|
| D950 | Window 1842-2020 (three 2021 cached papers are reserve); core 295, reserve 228; list `data/_staging/literature/history_candidates.csv`, one row per paper: era, year, paper_id, tier, core_reason, priority, thread, topic, component_class, has_device_metrics, paper_type, title, authors, dri, dri_basis, dri_source, institutions, venue, volume, pages, doi, url, route, oa_pdf, cited_by_openalex, already_in_repo, significance, evidence_url, streams, notes | follow-ups: size flexible, timeline to ~2020 |
| D951 | Core = priority A in any stream, the 11 owner cover-image seeds, cached papers (free tag), plus overrides. To reserve: rayleigh1897, pierce1954, snitzer1961b, nelson1963, patel1964, schafer1966, sorokin1966, marcatili1964, nakamura1994, boyraz2004 (coordinator); glauber1963a, geusic1964, mcclung1962, moulton1986, kogelnik2000, morioka1996, miller2000, yu2011, wang2009, chan2011, rakich2012, yi2015, doerr2006 (audit B). To core: holonyak1962, quist1962, kogelnik1972, izutsu1977, tien1977, marcatili1969a, shirasaki1982, alferness1982, kato1973, hill1993, dragone1989, henry1989, giles1991, koch1991, lo1991, inoue1997, jinguji1995, birks1997, john1987, absil2015, pinguet2018, poulton2017a, atabaki2018 (coordinator); vivien2007, barwicz2015, schwartz1978, mason1999, aoki1991, hocker1977, payne1975 (audit B). berreman1965 stays core as an owner seed (audit B suggested reserve); chan2011 (optomechanics ground state) is reserve and is the owner's call | PIC / fiber / transceiver lineage over adjacent physics |
| D952 | `paper_id` = `firstauthorYEAR[a-z]`, unique against `references/`, `cache_list.csv` and all registry native ids; cached papers keep their id (`lit:wang2018` is the PPLN Optica paper; the TFLN Nature modulator is `wang2018b`) | one id per paper |
| D953 | DRI = the person(s) credited with the result (inventor / PI and, where credited, the person who did the work); never inferred from byline position (audit A: the first + last author proxy was wrong in 12 of 18 sampled pre-1998 rows, e.g. Sumski for Panish, Atkin for Russell). `dri_basis`: `evidence` (a fetched milestone / award / history / bio page or the row's own evidence names them; `dri_source` gives it), `group_lead` (a bio states they led the group that did the work), `byline_single`, `byline` (senior / corresponding author, wave-2 streams), `audit` (set by audit A from byline order plus row evidence, no fetched page names the lead: hayashi1970, hall1962, goodman1984, somekh1973, little1997), `unresolved` (candidates in `notes`). Core: evidence 111, byline 89, byline_single 38, group_lead 19, audit 5, unresolved 33. People rows link to `data/people/` by DevLog-011 rules, never by name alone | owner: historic figures in scope |
| D954 | Historical papers join the `lit` corpus (same fetchers, extraction, header and distill pipeline) with a history tag; core rows are appended to `cache_list.csv` with `selection_reason = history` so `lit_ingest_inbox.py` and the fetchers accept their ids | no new corpus or pipeline |
| D955 | `blog:` duplicates (14 core rows) are ingested by copying the PDF from the blog repo (read-only) into `references/<paper_id>/`; the `blog:` row gets `same_as = lit:<paper_id>` | no re-download; one canonical source row |
| D956 | Retrieval as DevLog-006: BSTJ from archive.org (single owner, >= 5 s spacing, pilot 3 first); IEEE / IET through the IEEE browser route at its usual pacing; Optica browser route only for OE / Optica / OME; arXiv single owner >= 3.5 s; APS, AIP, Nature, Science, non-OA Optica, Wiley, Elsevier, Royal Society and no-DOI rows go to an owner list `references/_inbox/<paper_id>.pdf`. Licensed copies stay `restricted_local_only`; only `source.json` is committed | rate limits; rights |
| D957 | Ingest outputs per paper: text + figures (lit_extract), header affiliations (DevLog-011) for the people / org layer, DRI linked as people rows, component and metric rows only when the paper reports a measured device value (pic-component-distill rules unchanged), and a milestone row (proposed `data/history/milestones.csv`: date, era, thread, event <= 25 words, DRI, orgs, source_id) | proposal; Q1 |
| D958 | Old papers: OCR fallback for scans; units and terms kept as printed (dB/km, Angstrom, "optical maser"); German / French / Russian originals cached as-is, an English translation (e.g. Soviet Physics JETP) cached as a supplement when it exists | faithful values |
| D959 | Inspection point: no bulk retrieval before Q1-Q3; pilot = 3 BSTJ + 3 IEEE + 3 blog copies | ask before rate-limited runs |
| D960 | Fresh-context audits. A (facts, 47 core rows): every sampled DOI correct; 25 row fixes applied (DRI 13, institutions 4, authors 2 incl. Crossref typos Zeigler -> Zeiger and Larenzo -> Lorenzo, significance 2 incl. kapron1970 "7 dB/km" unsupported -> "about 20 dB/km", page ranges from Crossref, marcuse1977 DOI, liu2010 Optics Letters moved to the owner list). B (coverage): 29 confirmed additions (kogelnik1966, personick1973, cohen1974, horiguchi1976, dupuis1978, miller1978, schultz1980, wood1984, satake1986, henry1987, bowers1987, vellekoop1991, soref1991, rickman1994, kirstaedter1994, goossen1995, bruel1995, mekis1996, luan1999, lee2000, yariv2000, notomi2001, taillaert2003, rabiei2004, bogaerts2005, liao2005, barwicz2007, green2007, rylyakov2010) + 3 cached papers added as tags (goh2001, weigel2018, roeloffzen2018); 20 tier changes (D951); 20 thread fixes (e.g. maiman1960 / schawlow1958 to lasers; hollow-core and SDM fiber to optical fiber; photonic crystals to nanophotonics) | audit rule |
| D961 | DOIs: 497 of 523 rows carry a DOI (core 287 of 295). 11 DOIs found by Crossref for rows the agents left without one (BSTJ via Wiley for schwartz1978, boyd1962, marcatili1964, kaiser1973; tsukada1974, utaka1981, murata1987, suzuki1986, colace1998, izawa1980, iga2000). Core rows with no DOI found: colladon1842, pockels1894, fabry1899, einstein1917, basov1954, alferov1970, izawa1977 (conference), onaka1996 (OFC 1996 PD19) | owner: "make sure you have the DOIs" |
| D962 | `core_reason` separates selected landmarks (priority_a, owner_seed, override) from cached tags, so a timeline is not dominated by recent cached papers (audit B balance note) | balance |

## Retrieval plan (core, 295)

| route | core | who |
|---|---|---|
| already cached (`lit` 44, `eo` 2) | 46 | none (tag) |
| blog repo PDF on disk | 14 | coordinator (copy) |
| archive.org BSTJ | 11 | coordinator |
| IEEE / IET browser (Electron. Lett. 17, JQE 14, JLT 14, PTL 7, Proc. IEEE 6, JSTQE 1, other 10) | 69 | coordinator, owner session |
| Optica OA browser | 11 | coordinator |
| arXiv | 16 | coordinator |
| open publisher copy | 8 | coordinator |
| owner download: AIP 36, Optica non-OA 28, Nature 21, APS 16, Science 4, Wiley 3, Elsevier 2, Royal Society 1, other 2 | 113 | owner |
| owner download, no DOI | 7 | owner |

120 owner downloads in total, 67 of them in E0-E3. Electronics Letters (IET) rows go through IEEE Xplore; the pilot
checks this, otherwise they move to the owner list.

## Known gaps and weak points

- Thin or missing `evidence_url`: 37 core rows have none (mostly audit-B additions confirmed by Crossref only, plus
  records where the stream found no narrative source); others rest on a record page or a general review (flagged in
  `notes`, e.g. taylor2004, savory2008, schmidt1974, kogelnik1976, yariv1973, little1997, akahane2003, huang2019,
  watts2011, miller2009).
- DRI: 33 core rows unresolved (e.g. dakss1970, burns1975, papuchon1975, miya1979, miller1984, soref1985, meltz1989,
  fejer1992, yamada1993, soldano1995, ranka2000, goh2001); several `dri_source` pages were seen only as search
  summaries (goodman1984, takato1988, lo1991, kawachi1983, lygagnon2006, kippenberg2004, ahn2007, savchenkov2004,
  spence1991) and are re-checked at header extraction; patent inventor lists back uchida1970, schmidt1974,
  shirasaki1982, lin1980, yu2009.
- Not confirmed, left out: Iogansen 1962/1967 prism coupler, Akhmanov 1965, Nishizawa p-i-n / APD primary records,
  Knox-Toulios 1970, Dorset 1973 and NTT 1981 systems, Babinet 1842, Tyndall 1854, Lamm 1930.
- Priority disputes recorded in `notes`: Gould vs Townes / Schawlow; four 1962 diode groups; Alferov vs Hayashi /
  Panish; first EML (kawamura1986 vs suzuki1987 vs wood1984 modulator); first GHz Si modulator (liu2004 vs xu2005);
  taper coupling to WGM (knight1997 vs cai2000); PCSEL (imada1999 vs Meier 1999); waveguide SNSPD (pernice2012 vs
  Sprengers 2011); boson sampling (spring2013 vs three 2013 groups); AWG (smit1988 / vellekoop1991 vs takahashi1990
  vs dragone1991a).
- Companion versions to ingest once: kogelnik1966 (Applied Optics and Proc. IEEE), wood1984 (IEDM 1983 version),
  rylyakov2010 (OFC and NFOEC DOIs). bogaerts2005 has no authors in Crossref (byline from the PDF header).
- `murakowski2024` (cover image) is not historical and stays in the `blog` corpus; `oif2020` (400ZR) is a standard,
  reserve.

## Questions for Wentao

- Q1. Ingest output: (a, proposed) text + header affiliations + DRI people rows + component / metric rows where a
  measured device value exists + a milestone row per paper feeding a timeline view; or (b) text + milestones + DRI
  only, no component distill?
- Q2. Downloads: core needs 120 owner downloads (113 with DOI, 7 without). All at once, or a first batch (E0-E3, 67)?
  And is the IEEE browser route through your session OK for the 69 IEEE / IET rows at the usual pacing?
- Q3. Reserve (228): list only, or ingest after the core?

## Answers (2026-11-11, Wentao)

- Q1: proposal (a) accepted. Also pick one core figure per paper when the paper has figures (for a later timeline view).
- Q2: use the IEEE session the same way as the existing script; Wentao logs in.
- Q3: ingest the reserve after the core.

| id | decision | reason |
|---|---|---|
| D963 | Milestone table `data/history/milestones.csv`, one row per paper: paper_id, source_id, date (publication date, else year), era, thread, event (<= 25 words, from the paper), dri, orgs (registry org ids from header extraction), key_figure_file (`references/<paper_id>/figures/...`, local), key_figure_label (as printed, e.g. "Fig. 2"), key_figure_page, key_figure_caption (<= 30 words, paraphrase), key_figure_reason (<= 15 words); figure fields empty when the paper has no figure. Figures stay local (rights); only the pointer and caption paraphrase are committed | timeline view (Q1) |
| D964 | Pipeline plumbing: `scripts/hist_prepare.py` appends the selected tier of `history_candidates.csv` to `cache_list.csv` (`selection_reason = history`, uid = DOI or `hist:<paper_id>`) and to `retrieval_queue.csv` as day 101 (core; reserve later as day 102), writes author records to `cache/literature/history_adds.jsonl` (read by `people.py` and `ofc_headers.py` next to `curator_adds.jsonl`), copies the blog-repo PDFs into `references/_inbox/`, resolves archive.org BSTJ PDF URLs, and writes `data/_staging/literature/history_manual_downloads.md`. Backups of both CSVs before the first write; idempotent; `--dry-run`. Routes: 10.1109 -> `ieee_browser`, 10.1049 (Electronics Letters, IET DOIs resolve outside Xplore) -> `ieee_search` (Xplore title search, existing route), OE / Optica / OME -> `optica_browser`, BSTJ -> `oa_publisher` with the archive.org URL, arXiv -> `arxiv`, open copies -> `oa_publisher`, others -> `manual`; cached papers get no queue row | reuse the existing fetchers unchanged |

| D965 | OCR (`scripts/lit_ocr.py`): papers whose `source.json` flags `low_text` / `garbled_text_layer` get macOS Vision OCR (accurate, en-US, 200 dpi renders in git-ignored `cache/literature/ocr/`), the approach of the blog repo's `ofc2026_ocr.py`; `text.md` is rewritten with page markers, an existing PyMuPDF text layer is kept as `text_pymupdf.md`, `source.json` gets `ocr_on` / `ocr_method`. Superscripts and Greek letters are unreliable in OCR text, so distillers read numbers from page renders. Only history papers are OCR'd here; 23 older `lit` papers with garbled layers (e.g. a2017, barwicz2017, kittlaus2018) are out of scope and untouched | archive.org BSTJ and pre-1990 publisher PDFs are image-only scans (0 chars) |
| D966 | Identity check on page 1-2: the blog copy for `colladon1842` is a Geneva Musee d'histoire des sciences booklet about Colladon, not the 1842 Comptes rendus note; it is kept in git-ignored `cache/literature/secondary/colladon1842_museum_booklet/` and `colladon1842` is on the owner list (Comptes rendus 15, 1842; archive.org `comptesrendusheb15acad`). All other 14 blog copies match their titles | wrong PDF never registered |
| D967 | `access` of the 13 paywalled blog copies corrected from `oa` to `paywalled` in `cache_list.csv` (backup `cache/literature/backup/hist_access_*.zip`) and re-extracted, so the registry says `paywalled` / `restricted_local_only`; the history rows in `cache_list.csv` (appended by the owner's run, 250 rows, CRLF) are otherwise kept as written | registry access must reflect the original publication |
| D968 | Routing fixes after the pilot: IOP (JJAP, Semicond. Sci. Technol.) answers HTML to non-browser clients (breaker 30 min) -> `publisher_browser`; PNAS / Science author copies -> owner list. `hist_prepare.py queue` re-routes uncached rows of the day when the rule changes. The existing `lit_fetch_browser.py --site ieee` session (owner login) serves 10.1109 rows; Electronics Letters (10.1049) via its `ieee_search` route | reuse the existing fetchers |
| D970 | (owner correction 2026-11-11 01:36) Browser fetching for this DevLog is the IEEE session only. An Optica session (route `optica_browser`, session 31) was started without approval inside the open-route script and was stopped after 5 attempts (4 ok: gardes2005, liu2007, vivien2007, sun2008; savory2008 `no_access`) when Optica answered "This IP address is subject to a downloading timeout based on heavy usage"; the queued publisher-browser session (IOP, 4 rows) never ran. The 6 remaining Optica OA rows and the 4 IOP rows stay in the queue and wait for an explicit go | owner instruction: "ieee only" |
| D971 | Pilot `hist_01` rulings: kao1966 (PDF = IEE Proc. J 1986 reprint; locators are reprint pages, date 1966-07 from its footnote) and delhaye2007 (arXiv v1 copy; date empty) kept with notes; smit1988 fab Delft kept ("We realised", D80b own-process statement); tien1969 prism coupler kept as `fiber_chip_coupler.other` (couples into an on-chip thin-film guide; not a D411 bulk resonator); delhaye2007 comb rows stay `laser.comb` (precedent); registry gaps noted, no new parameters (comb span, dispersion per FSR, comb-line uniformity, coupler spacer thickness); subagents cannot write `.md` files, so batch reports are `report.txt`; `lit_ocr.py --figures-only` adds 150 dpi page renders for OCR caption pages (scans had no figure files, e.g. maiman1960) | pilot hand-back |
| D972 | No-DOI papers (research agent, page images checked): colladon1842 (Comptes rendus 15, pp. 800-802, archive.org `comptesrendusheb15acad` leaves 813-815; p. 802 header OCR-misread as 803, Babinet's note starts there), pockels1894 (Abh. Ges. Wiss. Goettingen 39, memoir pp. 1-204, `abhandlungenderk3940knig` leaves 12-215), fabry1899 (Ann. Chim. Phys. (7) 16, pp. 115-144, `annalesdechimie47lusgoog` leaves 121-150; start page inferred, scan has no text layer), einstein1917 (Phys. Z. 18, pp. 121-128, Heft 6 item leaves 4-11) cut from the archive.org volume PDFs (`scripts/hist_ia_extract.py`, volumes in git-ignored `cache/literature/ia_volumes/`); basov1954 Russian original from jetp.ras.ru through `lit_fetch_oa.py`; alferov1970 = pp. 132-139 (English and Russian, bilingual reprint) of "Beginning of the Laser Era in the USSR" (FIAN / LPI 2010 collected papers, owner download), cut to 8 pages; its `garbled_text_layer` flag comes from the Russian pages, the text layer is born-digital and is not OCR'd. The five archive / jetp scans are public domain: `access` set to `oa` in cache_list. OCR languages: fr-FR (colladon1842, fabry1899), de-DE (pockels1894, einstein1917), ru-RU (basov1954) | owner: cache them |
| D973 | TBA: izawa1977 (IOOC 1977 technical digest p. 375) and onaka1996 (OFC 1996 PD19, record only on Optica, not on Xplore) were not found in the first retrieval round (Crossref, archive.org, publisher sites, IEEE Xplore title search); queue `status = tba`, candidate-list notes prefixed "TBA"; they stay in core | owner instruction |
| D974 | (owner 2026-11-11) Batch 1 = `hist_01`-`hist_09` (72 papers). With the weekly quota low, batch 1 gets one fresh-context audit of its milestone rows only (the timeline input); its 33 staged component rows wait for a full audit. Then a new app tab `/history` for a general audience: a meandering top-down timeline (serpentine path, era sections with short intros), color modes by topic (thread), institution, material / platform (from the paper's component rows, else "theory / no device") and era; technical details in a hover tooltip and a click popup (event, DRI, institutions, venue, DOI, key figure with caption, linked component rows). Data `app/static/data/history.json` from `scripts/build_history_view.py` (hooked into `build_views.py`). Key figures come from licensed PDFs: thumbnails are generated only for local builds into a git-ignored folder; the public build shows the caption and a note | timeline view (Q1) |
| D969 | Milestone and key-figure batches `hist_NN` (<= 8 papers) under `data/_staging/history/CONTRACT.md`: one distiller per batch writes `milestones.csv` (event from the paper, DRI confirmed or changed with page evidence, affiliations as printed, one key figure: the paper's own label, page, an existing file under `references/<id>/figures/`, caption paraphrase) and component rows only for measured device values (pic-component-distill skill, staging `data/_staging/components/hist_NN/`); one fresh-context audit per batch; `scripts/hist_merge_milestones.py` validates and merges into `data/history/milestones.csv`; component merges as DevLog-007. Pilot `hist_01` (miller1969, maiman1960, kogelnik1969, tien1969, kao1966, smit1988, roelkens2005, delhaye2007) before scaling | timeline view (Q1) |

## TODO

- [x] Research waves 1-2 (14 streams), central verification, merge, selection, list CSV, this DevLog.
- [x] Fresh-context audits A and B; corrections applied (D960); DRI resolution (D953); DOI gap fill (D961).
- [x] Q1-Q3 answered (above).
- [x] `hist_prepare.py` (D964): cache_list + queue day 101, author records, blog copies, BSTJ URLs, owner download list.
- [x] Pilot retrieval (D959), then the rest of blog / BSTJ / arXiv / OA (Optica / IOP browser rows wait for an owner go, D970).
- [ ] IEEE day 101 sessions (Wentao logs in); owner inbox ingest as downloads arrive.
- [ ] Extraction (OCR check on pre-1980 scans), registry rows (`lit_register_sources.py`), `same_as` on `blog:` duplicates.
- [ ] Header batches (affiliations, DRI people links), milestone rows with key figure (D963), distill batches `hist_NN` with audits.
- [ ] Reserve (228) as day 102 after the core.

## Progress

- 2026-11-11 07:40 UTC: repo inspected (registry decade counts, blog corpus, DevLog-006 pipeline, skill); shared brief;
  wave 1 (9 streams) dispatched.
- 07:54-08:02 UTC: wave 1 done, 292 rows; central Crossref + OpenAlex verification: all 255 DOIs resolve.
- 08:10 UTC: follow-up (timeline to ~2020, DOIs, size flexible); wave 2 (5 streams) with a shared rate-limited Crossref
  helper.
- 08:33-08:42 UTC: wave 2 done, 225 rows; verification 517 rows / 474 DOIs; merge 491; selection; first DevLog draft.
- ~09:00-09:30 UTC: audits A and B; DRI resolution (4 agents; paused when the owner clarified DOI, resumed when the
  owner put historic figures in scope); 29 + 3 additions verified; 11 DOIs filled; final list 523 rows (core 295);
  this DevLog rewritten from the final CSV.
- 2026-11-11 09:15-09:50 UTC (owner answered Q1-Q3): `hist_prepare.py` queued day 101 (249 rows; cache_list rows were
  already appended by the owner's run), author records, BSTJ archive.org URLs (13/13 resolved, titles match), blog
  copies (14 ingested; colladon1842 set aside, D966), owner list `history_manual_downloads.md` (118). Open routes:
  pilot 5/6 ok (IOP blocked non-browser clients, D968), then 26 ok + 5 cached. IEEE session (owner login) running in
  tmux `hist-fetch`. Optica session stopped on owner correction (D970). OCR of 17 scans (D965). 94 history papers
  registered (`lit_register_sources.py`), validate_db 0 errors.
- 09:40-09:47 UTC: pilot `hist_01` distilled, audited (GO; 0 wrong, 6 imprecise, 1 missing), patched
  (`hist_apply_patch.py`, 18 changes, re-run 0), merged: `data/history/milestones.csv` 8 rows; components +8 / metrics
  +25 (backup `cache/components_backup/components_before_hist_01_*.zip`). Batches `hist_02`-`hist_18` cut by
  `hist_make_batches.py` (130 ready papers: 11 full batches, 6 milestone-only); distillers `hist_02`-`hist_09`
  dispatched.
- 10:02 UTC PAUSED (owner: weekly usage limit, resumes in ~20 h). Handoff:
  - Distilled, validated (dry-run 0 errors), NOT audited, NOT merged: `hist_02`-`hist_09` (64 milestone rows;
    components hist_04 +4/+13, hist_06 +4/+16, hist_07 +2/+4, hist_08 +5/+11, hist_09 +18/+74; hist_02/03/05 none).
    Next: one fresh-context audit per batch (same prompt as hist_01: write only `audit_patch.csv` + `audit.txt`),
    coordinator rulings below, `hist_apply_patch.py <batch>` (re-run 0 changes), `hist_merge_milestones.py`
    dry-run then merge, components zip backup then `merge_component_staging.py` per batch, serialized.
  - Open rulings from the distillers (each batch's `report.txt` has details): microwave devices (southworth1936,
    miller1954, gordon1954) and bulk / gas / fiber lasers and fiber amplifiers get no component rows (proposed: yes,
    D411 analogue); `author_estimate` loss rows (schmidt1974, kaminow1975, papuchon1975: keep, the skill allows
    them); fab from own-work wording ("we grew / have built": hayashi1970, kogelnik1971, kaminow1975; D80b as smit1988);
    hayashi1970 threshold current derived from density x area; free-space grating / prism / sphere couplers as
    `fiber_chip_coupler.other` (dakss1970, kato1973, waldhausl1997, ilchenko1999; tien1969 precedent) and microsphere
    scope (D411); registry gaps (threshold current density, laser spectral FWHM, quantum efficiency, coupling
    coefficient K, coupling ratio); two-month BSTJ issues dated year only; DRI changes in hist_09 (vellekoop1991,
    ilchenko1999) need evidence check by the audit; significance claims in `history_candidates.csv` that the papers do
    not make (hopkins1954 "over 10,000 fibers", hondros1910 / vanheel1954 / franken1961 / snitzer1961a "first") are
    candidates for a CSV correction; missing orgs: Thomson-CSF, Western Electric ERC, RADC, JPL, Fraunhofer IOF
    (org round); kogelnik1966 venue empty in papers.csv (Applied Optics 1966-10).
  - Cut, not dispatched: `hist_10`-`hist_12` (full) and `hist_13`-`hist_18` (milestone_only). 157 core papers not
    ready yet (owner downloads, IEEE sessions 12-13, Optica / IOP rows waiting for an owner go, D970).
  - Fetching: IEEE session 11 done (19 ok, 11 `no_ieee_copy`: Electronics Letters titles not found by the Xplore
    search; regenerate the owner list with `lit_manual_list.py` so they appear there); sessions 12-13 running in tmux
    `hist-fetch` (no token cost). After it ends: `lit_extract.py --pending`, `lit_ocr.py` on flagged history scans
    (history ids only, D965), `lit_register_sources.py`, `validate_db.py`, then `hist_make_batches.py`.
  - Not done yet: header batches (DevLog-011) for the new `lit` history papers, `same_as` on `blog:` duplicates,
    reserve (day 102). Nothing committed.

## Lists
### Core list

Route: `blog` PDF on disk in the blog repo; `repo` already cached here or in the EO atlas; `bstj` archive.org; `ieee` IEEE / IET browser route; `optica` Optica OA journals; `arxiv`; `oa` open publisher copy; `manual` owner download; `manual*` owner download, no DOI. DRI marks: none = evidence page or single author; (g) group lead; (b) senior byline author; (a) set by audit; `-` unresolved (candidates in the CSV notes).

#### E0 1842-1959 foundations: guided light, field theory, waveguides, maser (15)

| year | paper_id | DRI | title | venue | DOI or URL | route |
|---|---|---|---|---|---|---|
| 1842 | colladon1842 | Jean-Daniel Colladon | Sur les réflexions d'un rayon de lumière à l'intérieur d'une veine liquide para~ | Comptes rendus hebdomadaires de~ | https://archive.org/details/comptesrendusheb15acad | blog |
| 1846 | faraday1846 | Michael Faraday | I. Experimental researches in electricity.—Nineteenth series | Philosophical Transactions of t~ | 10.1098/rstl.1846.0001 | manual |
| 1865 | maxwell1865 | James Clerk Maxwell | VIII. A dynamical theory of the electromagnetic field | Philosophical Transactions of t~ | 10.1098/rstl.1865.0008 | blog |
| 1894 | pockels1894 | Friedrich Pockels | Ueber den Einfluss des elektrostatischen Feldes auf das optische Verhalten piëz~ | Abhandlungen der Königlichen Ge~ | https://archive.org/details/abhandlungenderk3940knig | manual* |
| 1899 | fabry1899 | C. Fabry; A. Pérot | Théorie et applications d'une nouvelle méthode de spectroscopie interférentielle | Annales de Chimie et de Physiqu~ | (no DOI, no URL) | manual* |
| 1910 | hondros1910 | - | Elektromagnetische Wellen an dielektrischen Drähten | Annalen der Physik | 10.1002/andp.19103370802 | manual |
| 1910 | rayleigh1910 | Lord Rayleigh | CXII. The problem of the whispering gallery | Philosophical Magazine (Series ~ | 10.1080/14786441008636993 | manual |
| 1917 | einstein1917 | Albert Einstein | Zur Quantentheorie der Strahlung | Physikalische Zeitschrift | (no DOI, no URL) | manual* |
| 1936 | southworth1936 | George C. Southworth | Hyper-Frequency Wave Guides-General Considerations and Experimental Results* | Bell System Technical Journal | 10.1002/j.1538-7305.1936.tb00733.x | bstj |
| 1954 | basov1954 | Nikolay G. Basov; Alexander M. Prokhorov | Application of molecular beams for radiospectroscopic study of molecular rotati~ | Zhurnal Eksperimental'noi i Teo~ | https://www.jetp.ras.ru/cgi-bin/index2/gf-view/en/basov | manual* |
| 1954 | gordon1954 | Charles H. Townes; James P. Gordon; H. J.~ | Molecular Microwave Oscillator and New Hyperfine Structure in the Microwave Spe~ | Physical Review | 10.1103/physrev.95.282 | manual |
| 1954 | hopkins1954 | Harold H. Hopkins; Narinder S. Kapany | A Flexible Fibrescope, using Static Scanning | Nature | 10.1038/173039b0 | blog |
| 1954 | miller1954 | Stewart E. Miller | Coupled Wave Theory and Waveguide Applications | Bell System Technical Journal | 10.1002/j.1538-7305.1954.tb02359.x | bstj |
| 1954 | vanheel1954 | A. C. S. van Heel | A New Method of transporting Optical Images without Aberrations | Nature | 10.1038/173039a0 | manual |
| 1958 | schawlow1958 | Arthur L. Schawlow; Charles H. Townes | Infrared and Optical Masers | Physical Review | 10.1103/physrev.112.1940 | blog |

#### E1 1960-1969 laser, nonlinear optics, integrated-optics idea (26)

| year | paper_id | DRI | title | venue | DOI or URL | route |
|---|---|---|---|---|---|---|
| 1960 | maiman1960 | Theodore H. Maiman | Stimulated Optical Radiation in Ruby | Nature | 10.1038/187493a0 | manual |
| 1961 | boyd1961 | G. D. Boyd; James P. Gordon | Confocal Multimode Resonator for Millimeter Through Optical Wavelength Masers | Bell System Technical Journal | 10.1002/j.1538-7305.1961.tb01626.x | bstj |
| 1961 | fox1961 | A. Gardner Fox; Tingye Li | Resonant Modes in a Maser Interferometer | Bell System Technical Journal | 10.1002/j.1538-7305.1961.tb01625.x | bstj |
| 1961 | franken1961 | Peter A. Franken | Generation of Optical Harmonics | Physical Review Letters | 10.1103/physrevlett.7.118 | manual |
| 1961 | javan1961 | A. Javan; W. R. Bennett; D. R. Herriott | Population Inversion and Continuous Optical Maser Oscillation in a Gas Discharg~ | Physical Review Letters | 10.1103/physrevlett.6.106 | manual |
| 1961 | snitzer1961 | Elias Snitzer | Cylindrical Dielectric Waveguide Modes* | Journal of the Optical Society ~ | 10.1364/josa.51.000491 | manual |
| 1961 | snitzer1961a | Elias Snitzer | Observed Dielectric Waveguide Modes in the Visible Spectrum* | Journal of the Optical Society ~ | 10.1364/josa.51.000499 | manual |
| 1962 | armstrong1962 | Nicolaas Bloembergen (g) | Interactions between Light Waves in a Nonlinear Dielectric | Physical Review | 10.1103/physrev.127.1918 | manual |
| 1962 | hall1962 | R. N. Hall (a) | Coherent Light Emission From GaAs Junctions | Physical Review Letters | 10.1103/physrevlett.9.366 | manual |
| 1962 | holonyak1962 | Nick Holonyak Jr. | COHERENT (VISIBLE) LIGHT EMISSION FROM Ga(As1− x P x ) JUNCTIONS | Applied Physics Letters | 10.1063/1.1753706 | manual |
| 1962 | nathan1962 | - | STIMULATED EMISSION OF RADIATION FROM GaAs p-n JUNCTIONS | Applied Physics Letters | 10.1063/1.1777371 | manual |
| 1962 | quist1962 | T. M. Quist; R. H. Rediker | SEMICONDUCTOR MASER OF GaAs | Applied Physics Letters | 10.1063/1.1753710 | manual |
| 1963 | kroemer1963 | Herbert Kroemer | A proposed class of hetero-junction injection lasers | Proceedings of the IEEE | 10.1109/proc.1963.2706 | ieee |
| 1964 | hargrove1964 | Logan E. Hargrove Jr. | LOCKING OF He–Ne LASER MODES INDUCED BY SYNCHRONOUS INTRACAVITY MODULATION | Applied Physics Letters | 10.1063/1.1754025 | manual |
| 1964 | koester1964 | Elias Snitzer | Amplification in a Fiber Laser | Applied Optics | 10.1364/ao.3.001182 | manual |
| 1965 | berreman1965 | D. W. Berreman | Convective Gas Light Guides or Lens Trains for Optical Beam Transmission | Journal of the Optical Society ~ | 10.1364/josa.55.000239 | manual |
| 1965 | giordmaine1965 | Joseph A. Giordmaine; Robert C. Miller | Tunable Coherent Parametric Oscillation in LiNb O 3 at Optical Frequencies | Physical Review Letters | 10.1103/physrevlett.14.973 | manual |
| 1966 | kao1966 | K. C. Kao; George A. Hockham | Dielectric-fibre surface waveguides for optical frequencies | Proceedings of the Institution ~ | 10.1049/piee.1966.0189 | ieee |
| 1966 | kogelnik1966 | Herwig Kogelnik; Tingye Li | Laser Beams and Resonators |  | 10.1364/ao.5.001550 | manual |
| 1966 | mcintyre1966 | R. J. McIntyre (b) | Multiplication noise in uniform avalanche diodes | IEEE Transactions on Electron D~ | 10.1109/t-ed.1966.15651 | ieee |
| 1968 | kawakami1968 | Jun-ichi Nishizawa | An Optical Waveguide with the Optimum Distribution of the Refractive Index with~ | IEEE Transactions on Microwave ~ | 10.1109/tmtt.1968.1126797 | ieee |
| 1969 | kogelnik1969 | Herwig Kogelnik | Coupled Wave Theory for Thick Hologram Gratings | Bell System Technical Journal | 10.1002/j.1538-7305.1969.tb01198.x | bstj |
| 1969 | marcatili1969 | E. A. J. Marcatili | Dielectric Rectangular Waveguide and Directional Coupler for Integrated Optics | Bell System Technical Journal | 10.1002/j.1538-7305.1969.tb01166.x | bstj |
| 1969 | marcatili1969a | E. A. J. Marcatili | Bends in Optical Dielectric Guides | Bell System Technical Journal | 10.1002/j.1538-7305.1969.tb01167.x | bstj |
| 1969 | miller1969 | Stewart E. Miller | Integrated Optics: An Introduction | Bell System Technical Journal | 10.1002/j.1538-7305.1969.tb01165.x | bstj |
| 1969 | tien1969 | P. K. Tien | MODES OF PROPAGATING LIGHT WAVES IN THIN DEPOSITED SEMICONDUCTOR FILMS | Applied Physics Letters | 10.1063/1.1652820 | blog |

#### E2 1970-1979 low-loss fiber, heterostructure lasers, LiNbO3 integrated optics (43)

| year | paper_id | DRI | title | venue | DOI or URL | route |
|---|---|---|---|---|---|---|
| 1970 | alfano1970 | R. R. Alfano; S. L. Shapiro | Emission in the Region 4000 to 7000 Å Via Four-Photon Coupling in Glass | Physical Review Letters | 10.1103/physrevlett.24.584 | manual |
| 1970 | alferov1970 | Zhores I. Alferov; Dmitri Z. Garbuzov | Investigation of the influence of the AlAs-GaAs heterostructure parameters on t~ | Soviet Physics Semiconductors (~ | (no DOI, no URL) | manual* |
| 1970 | dakss1970 | - | GRATING COUPLER FOR EFFICIENT EXCITATION OF OPTICAL GUIDED WAVES IN THIN FILMS | Applied Physics Letters | 10.1063/1.1653091 | manual |
| 1970 | hayashi1970 | I. Hayashi; M. B. Panish (a) | JUNCTION LASERS WHICH OPERATE CONTINUOUSLY AT ROOM TEMPERATURE | Applied Physics Letters | 10.1063/1.1653326 | manual |
| 1970 | kapron1970 | D. B. Keck; R. D. Maurer; F. P. Kapron | RADIATION LOSSES IN GLASS OPTICAL WAVEGUIDES | Applied Physics Letters | 10.1063/1.1653255 | manual |
| 1970 | uchida1970 | Teiji Uchida | Optical characteristics of a light-focusing fiber guide and its applications | IEEE Journal of Quantum Electro~ | 10.1109/jqe.1970.1076326 | ieee |
| 1971 | gloge1971 | D. Gloge | Weakly Guiding Fibers | Applied Optics | 10.1364/ao.10.002252 | manual |
| 1971 | kogelnik1971 | Herwig Kogelnik; Charles V. Shank | STIMULATED EMISSION IN A PERIODIC STRUCTURE | Applied Physics Letters | 10.1063/1.1653605 | manual |
| 1971 | tien1971 | P. K. Tien | Light Waves in Thin Films and Integrated Optics | Applied Optics | 10.1364/ao.10.002395 | blog |
| 1972 | kogelnik1972 | Herwig Kogelnik; C. V. Shank | Coupled-Wave Theory of Distributed Feedback Lasers | Journal of Applied Physics | 10.1063/1.1661499 | manual |
| 1972 | stolen1972 | Roger H. Stolen | Raman Oscillation in Glass Optical Waveguide | Applied Physics Letters | 10.1063/1.1654046 | manual |
| 1973 | gloge1973 | D. Gloge; E. A. J. Marcatili | Multimode Theory of Graded-Core Fibers | Bell System Technical Journal | 10.1002/j.1538-7305.1973.tb02033.x | bstj |
| 1973 | hasegawa1973 | Akira Hasegawa; Fred Tappert | Transmission of stationary nonlinear optical pulses in dispersive dielectric fi~ | Applied Physics Letters | 10.1063/1.1654836 | manual |
| 1973 | kato1973 | Daisuke Kato | Light coupling from a stripe-geometry GaAs diode laser into an optical fiber wi~ | Journal of Applied Physics | 10.1063/1.1662645 | manual |
| 1973 | personick1973 | S. D. Personick | Receiver Design for Digital Fiber Optic Communication Systems, I |  | 10.1002/j.1538-7305.1973.tb01993.x | manual |
| 1973 | somekh1973 | A. Yariv; E. Garmire; S. Somekh (a) | Channel optical waveguide directional couplers | Applied Physics Letters | 10.1063/1.1654468 | manual |
| 1973 | yariv1973 | Amnon Yariv | Coupled-mode theory for guided-wave optics | IEEE Journal of Quantum Electro~ | 10.1109/jqe.1973.1077767 | ieee |
| 1974 | dingle1974 | Raymond Dingle; Charles H. Henry | Quantum States of Confined Carriers in Very ThinAlxGa1−xAs-GaAs-AlxGa1−xAsHeter~ | Physical Review Letters | 10.1103/physrevlett.33.827 | manual |
| 1974 | macchesney1974 | John B. MacChesney; P. B. O'Connor | A new technique for the preparation of low-loss and graded-index optical fibers | Proceedings of the IEEE | 10.1109/proc.1974.9608 | ieee |
| 1974 | schmidt1974 | Ronald V. Schmidt; Ivan P. Kaminow | Metal-diffused optical waveguides in LiNbO3 | Applied Physics Letters | 10.1063/1.1655547 | manual |
| 1975 | burns1975 | - | Mode conversion in planar-dielectric separating waveguides | IEEE Journal of Quantum Electro~ | 10.1109/jqe.1975.1068511 | ieee |
| 1975 | kaminow1975 | Ivan P. Kaminow | Efficient strip-waveguide modulator | Applied Physics Letters | 10.1063/1.88284 | manual |
| 1975 | martin1975 | W. E. Martin | A new waveguide switch/modulator for integrated optics | Applied Physics Letters | 10.1063/1.87992 | manual |
| 1975 | papuchon1975 | - | Electrically switched optical directional coupler: Cobra | Applied Physics Letters | 10.1063/1.88449 | manual |
| 1975 | payne1975 | W. A. Gambling; D. N. Payne | Zero material dispersion in optical fibres | Electronics Letters | 10.1049/el:19750135 | ieee |
| 1975 | ulrich1975 | R. Ulrich | Image formation by phase coincidences in optical waveguides | Optics Communications | 10.1016/0030-4018(75)90095-4 | manual |
| 1976 | haus1976 | - | Antisymmetric taper of distributed feedback lasers | IEEE Journal of Quantum Electro~ | 10.1109/jqe.1976.1069214 | ieee |
| 1976 | horiguchi1976 | - | Spectral losses of low-OH-content optical fibres |  | 10.1049/el:19760239 | ieee |
| 1976 | hsieh1976 | J. J. Hsieh | Room-temperature cw operation of GaInAsP/InP double-heterostructure diode laser~ | Applied Physics Letters | 10.1063/1.88645 | manual |
| 1976 | kogelnik1976 | Herwig Kogelnik; R. V. Schmidt | Switched directional couplers with alternating ΔΒ | IEEE Journal of Quantum Electro~ | 10.1109/jqe.1976.1069190 | ieee |
| 1977 | hocker1977 | G. B. Hocker; W. K. Burns (b) | Mode dispersion in diffused channel waveguides by the effective index method | Applied Optics | 10.1364/ao.16.000113 | manual |
| 1977 | izawa1977 | Tatsuo Izawa | Continuous fabrication of high silica fiber preform | International Conference on Int~ | https://ieeemilestones.ethw.org/Milestones:Invention_and_development_of_vapor-phase_axial_deposition_(VAD)_method_for_mass_production_of_high-quality_optical_fiber_for_telecommunication | manual* |
| 1977 | izutsu1977 | T. Sueta (g) | Broad-band traveling-wave modulator using a LiNbO&lt;inf&gt;3&lt;/inf&gt;optica~ | IEEE Journal of Quantum Electro~ | 10.1109/jqe.1977.1069310 | ieee |
| 1977 | marcuse1977 | Dietrich Marcuse | Loss Analysis of Single-Mode Fiber Splices | Bell System Technical Journal | 10.1002/j.1538-7305.1977.tb00534.x | bstj |
| 1977 | tien1977 | P. K. Tien | Integrated optics and new wave phenomena in optical waveguides | Reviews of Modern Physics | 10.1103/revmodphys.49.361 | blog |
| 1978 | dupuis1978 | Russell D. Dupuis; P. D. Dapkus | Room-temperature laser operation of quantum-well Ga(1−x)AlxAs-GaAs laser diodes~ |  | 10.1063/1.90026 | manual |
| 1978 | feit1978 | - | Light propagation in graded-index optical fibers | Applied Optics | 10.1364/ao.17.003990 | manual |
| 1978 | hill1978 | Kenneth O. Hill | Photosensitivity in optical fiber waveguides: Application to reflection filter ~ | Applied Physics Letters | 10.1063/1.89881 | manual |
| 1978 | kawanishi1978 | Yasuharu Suematsu (g) | GaxIn1-xAsyP1-y–InP Injection Laser Partially Loaded with Distributed Bragg Ref~ | Japanese Journal of Applied Phy~ | 10.1143/jjap.17.1439 | oa |
| 1978 | miller1978 | C. M. Miller | Fiber-Optic Array Splicing with Etched Silicon Chips |  | 10.1002/j.1538-7305.1978.tb02075.x | manual |
| 1978 | schwartz1978 | - | Atlanta Fiber System Experiment: The Chicago Lightwave Communications Project | Bell System Technical Journal | 10.1002/j.1538-7305.1978.tb02132.x | bstj |
| 1979 | miya1979 | - | Ultimate low-loss single-mode fibre at 1.55 μm | Electronics Letters | 10.1049/el:19790077 | ieee |
| 1979 | soda1979 | Kenichi Iga; Yasuharu Suematsu | GaInAsP/InP Surface Emitting Injection Lasers | Japanese Journal of Applied Phy~ | 10.1143/jjap.18.2329 | oa |

#### E3 1980-1989 long-wavelength systems, InP, silica PLC, EDFA (39)

| year | paper_id | DRI | title | venue | DOI or URL | route |
|---|---|---|---|---|---|---|
| 1980 | mollenauer1980 | Linn F. Mollenauer | Experimental Observation of Picosecond Pulse Narrowing and Solitons in Optical ~ | Physical Review Letters | 10.1103/physrevlett.45.1095 | manual |
| 1980 | schultz1980 | P. C. Schultz | Fabrication of optical waveguides by the outside vapor deposition process |  | 10.1109/proc.1980.11828 | ieee |
| 1981 | kawasaki1981 | Kenneth O. Hill | Biconical-taper single-mode fiber coupler | Optics Letters | 10.1364/ol.6.000327 | manual |
| 1982 | alferness1982 | - | Efficient single-mode fiber to titanium diffused lithium niobate waveguide coup~ | IEEE Journal of Quantum Electro~ | 10.1109/jqe.1982.1071390 | ieee |
| 1982 | arakawa1982 | Yasuhiko Arakawa | Multidimensional quantum well laser and temperature dependence of its threshold~ | Applied Physics Letters | 10.1063/1.92959 | manual |
| 1982 | henry1982 | Charles H. Henry | Theory of the linewidth of semiconductor lasers | IEEE Journal of Quantum Electro~ | 10.1109/jqe.1982.1071522 | ieee |
| 1982 | jackel1982 | - | Proton exchange for high-index waveguides in LiNbO3 | Applied Physics Letters | 10.1063/1.93615 | manual |
| 1982 | shirasaki1982 | Masataka Shirasaki | Compact optical isolator for fibers using birefringent wedges | Applied Optics | 10.1364/ao.21.004296 | manual |
| 1983 | campbell1983 | J. C. Campbell | High-performance avalanche photodiode with separate absorption ‘grading’ and mu~ | Electronics Letters | 10.1049/el:19830558 | ieee |
| 1983 | kawachi1983 | Masao Kawachi | Fabrication of SiO 2 -TiO 2 glass planar optical waveguides by flame hydrolysis~ | Electronics Letters | 10.1049/el:19830398 | ieee |
| 1984 | goodman1984 | J. W. Goodman (a) | Optical interconnections for VLSI systems | Proceedings of the IEEE | 10.1109/proc.1984.12943 | ieee |
| 1984 | luryi1984 | - | New infrared detector on a silicon chip | IEEE Transactions on Electron D~ | 10.1109/t-ed.1984.21676 | ieee |
| 1984 | miller1984 | - | Band-Edge Electroabsorption in Quantum Well Structures: The Quantum-Confined St~ | Physical Review Letters | 10.1103/physrevlett.53.2173 | manual |
| 1984 | sekartedjo1984 | Yasuharu Suematsu; K. Sekartedjo | 1.5 μm phase-shifted DFB lasers for single-mode operation | Electronics Letters | 10.1049/el:19840055 | ieee |
| 1984 | wood1984 | - | High-speed optical modulation with GaAs/GaAlAs quantum wells in a p-i-n diode s~ |  | 10.1063/1.94586 | manual |
| 1985 | poole1985 | S. B. Poole; D. N. Payne | Fabrication of low-loss optical fibres containing rare-earth ions | Electronics Letters | 10.1049/el:19850520 | ieee |
| 1985 | soref1985 | - | Single-crystal silicon: a new material for 1.3 and 1.6 μm integrated-optical co~ | Electronics Letters | 10.1049/el:19850673 | ieee |
| 1986 | adams1986 | A. R. Adams | Band-structure engineering for low-threshold high-efficiency semiconductor lase~ | Electronics Letters | 10.1049/el:19860171 | ieee |
| 1986 | kawamura1986 | Y. Kawamura (b) | Monolithic integration of InGaAs/InP DFB lasers and InGaAs/InAlAs MQW optical m~ | Electronics Letters | 10.1049/el:19860166 | ieee |
| 1986 | satake1986 | Toshiaki Satake | A new type of demountable plastic-molded single-mode multifiber connector |  | 10.1109/jlt.1986.1074860 | ieee |
| 1986 | soref1986 | R. A. Soref; J. P. Lorenzo (b) | All-silicon active and passive guided-wave components for λ = 1.3 and 1.6 µm | IEEE Journal of Quantum Electro~ | 10.1109/jqe.1986.1073057 | blog |
| 1987 | desurvire1987 | Emmanuel Desurvire | High-gain erbium-doped traveling-wave fiber amplifier | Optics Letters | 10.1364/ol.12.000888 | manual |
| 1987 | henry1987 | Charles H. Henry; R. F. Kazarinov | Low loss Si_3N_4–SiO_2 optical waveguides on Si |  | 10.1364/ao.26.002621 | manual |
| 1987 | john1987 | Sajeev John | Strong localization of photons in certain disordered dielectric superlattices | Physical Review Letters | 10.1103/physrevlett.58.2486 | manual |
| 1987 | lugiato1987 | L. A. Lugiato; R. Lefever | Spatial Dissipative Structures in Passive Optical Systems | Physical Review Letters | 10.1103/physrevlett.58.2209 | manual |
| 1987 | mears1987 | David N. Payne | Low-noise erbium-doped fibre amplifier operating at 1.54μm | Electronics Letters | 10.1049/el:19870719 | ieee |
| 1987 | soref1987 | Richard A. Soref; Brian R. Bennett | Electrooptical effects in silicon | IEEE Journal of Quantum Electro~ | 10.1109/jqe.1987.1073206 | ieee |
| 1987 | suzuki1987 | M. Suzuki | Monolithic integration of InGaAsP/InP distributed feedback laser and electroabs~ | Journal of Lightwave Technology | 10.1109/jlt.1987.1075650 | ieee |
| 1987 | yablonovitch1987 | Eli Yablonovitch | Inhibited Spontaneous Emission in Solid-State Physics and Electronics | Physical Review Letters | 10.1103/physrevlett.58.2059 | manual |
| 1988 | smit1988 | Meint K. Smit | New focusing and dispersive planar component based on an optical phased array | Electronics Letters | 10.1049/el:19880260 | blog |
| 1988 | snitzer1988 | E. Snitzer (b) | DOUBLE CLAD, OFFSET CORE Nd FIBER LASER | Optical Fiber Sensors 1988, pos~ | 10.1364/ofs.1988.pd5 | manual |
| 1988 | takato1988 | Masao Kawachi | Silica-based single-mode waveguides on silicon and their application to guided-~ | Journal of Lightwave Technology | 10.1109/50.4091 | ieee |
| 1989 | braginsky1989 | V. B. Braginsky | Quality-factor and nonlinear properties of optical whispering-gallery modes | Physics Letters A | 10.1016/0375-9601(89)90912-2 | manual |
| 1989 | dragone1989 | Corrado Dragone | Efficient N*N star couplers using Fourier optics | Journal of Lightwave Technology | 10.1109/50.16884 | ieee |
| 1989 | henry1989 | - | Glass waveguides on silicon for hybrid optical packaging | Journal of Lightwave Technology | 10.1109/50.39094 | ieee |
| 1989 | koren1989 | T. L. Koch; U. Koren | Wavelength division multiplexing light source with integrated quantum well tuna~ | Applied Physics Letters | 10.1063/1.101164 | manual |
| 1989 | lim1989 | Martin M. Fejer; Robert L. Byer | Second-harmonic generation of green light in periodically poled planar lithium ~ | Electronics Letters | 10.1049/el:19890127 | ieee |
| 1989 | meltz1989 | - | Formation of Bragg gratings in optical fibers by a transverse holographic method | Optics Letters | 10.1364/ol.14.000823 | manual |
| 1989 | nakazawa1989 | Masataka Nakazawa | Efficient Er3+-doped optical fiber amplifier pumped by a 1.48 μm InGaAsP laser ~ | Applied Physics Letters | 10.1063/1.101448 | manual |

#### E4 1990-1999 WDM, AWG, QPM, photonic crystals, microcavities (42)

| year | paper_id | DRI | title | venue | DOI or URL | route |
|---|---|---|---|---|---|---|
| 1990 | liau1990 | Z. L. Liau | Wafer fusion: A novel technique for optoelectronic device fabrication and monol~ | Applied Physics Letters | 10.1063/1.102697 | manual |
| 1990 | takahashi1990 | Hiroshi Takahashi | Arrayed-waveguide grating for wavelength division multi/demultiplexer with nano~ | Electronics Letters | 10.1049/el:19900058 | ieee |
| 1991 | aoki1991 | M. Aoki (b) | Novel structure MQW electroabsorption modulator/DFB-laser integrated device fab~ | Electronics Letters | 10.1049/el:19911324 | ieee |
| 1991 | dragone1991a | Corrado Dragone | An N*N optical multiplexer using a planar arrangement of two star couplers | IEEE Photonics Technology Lette~ | 10.1109/68.84502 | ieee |
| 1991 | giles1991 | C. R. Giles; E. Desurvire (b) | Modeling erbium-doped fiber amplifiers | Journal of Lightwave Technology | 10.1109/50.65886 | ieee |
| 1991 | koch1991 | T. L. Koch | Semiconductor photonic integrated circuits | IEEE Journal of Quantum Electro~ | 10.1109/3.81373 | ieee |
| 1991 | lo1991 | Yu-Hwa Lo; Rajaram Bhat | Bonding by atomic rearrangement of InP/InGaAsP 1.5 μm wavelength lasers on GaAs~ | Applied Physics Letters | 10.1063/1.105032 | manual |
| 1991 | soref1991 | - | Large single-mode rib waveguides in GeSi-Si and Si-on-SiO/sub 2/ |  | 10.1109/3.83406 | ieee |
| 1991 | spence1991 | Wilson Sibbett (g) | 60-fsec pulse generation from a self-mode-locked Ti:sapphire laser | Optics Letters | 10.1364/ol.16.000042 | manual |
| 1991 | vellekoop1991 | Meint K. Smit | Four-channel integrated-optic wavelength demultiplexer with weak polarization d~ |  | 10.1109/50.70004 | oa |
| 1992 | fejer1992 | - | Quasi-phase-matched second harmonic generation: tuning and tolerances | IEEE Journal of Quantum Electro~ | 10.1109/3.161322 | ieee |
| 1993 | hill1993 | Kenneth O. Hill | Bragg gratings fabricated in monomode photosensitive optical fiber by UV exposu~ | Applied Physics Letters | 10.1063/1.108786 | manual |
| 1993 | jayaraman1993 | L. A. Coldren | Theory, design, and performance of extended tuning range semiconductor lasers w~ | IEEE Journal of Quantum Electro~ | 10.1109/3.234440 | ieee |
| 1993 | yamada1993 | - | First-order quasi-phase matched LiNbO3 waveguide periodically poled by applying~ | Applied Physics Letters | 10.1063/1.108925 | manual |
| 1994 | faist1994 | Federico Capasso | Quantum Cascade Laser | Science | 10.1126/science.264.5158.553 | manual |
| 1994 | huffaker1994 | D. G. Deppe | Native-oxide defined ring contact for low threshold vertical-cavity lasers | Applied Physics Letters | 10.1063/1.113087 | manual |
| 1994 | kirstaedter1994 | Dieter Bimberg (g) | Low threshold, large T o injectionlaser emissionfrom (InGa)As quantum dots |  | 10.1049/el:19940939 | ieee |
| 1994 | reck1994 | Michael Reck; Anton Zeilinger (b) | Experimental realization of any discrete unitary operator | Physical Review Letters | 10.1103/physrevlett.73.58 | manual |
| 1994 | rickman1994 | Graham T. Reed; Andrew G. Rickman (g) | Silicon-on-insulator optical rib waveguide loss and mode characteristics |  | 10.1109/50.337489 | ieee |
| 1995 | bruel1995 | Michel Bruel | Silicon on insulator material technology |  | 10.1049/el:19950805 | ieee |
| 1995 | goossen1995 | D. A. B. Miller (g) | GaAs MQW modulators integrated with silicon CMOS |  | 10.1109/68.376802 | ieee |
| 1995 | jinguji1995 | - | Synthesis of coherent two-port lattice-form optical delay-line circuit | Journal of Lightwave Technology | 10.1109/50.350643 | ieee |
| 1995 | soldano1995 | - | Optical multi-mode interference devices based on self-imaging: principles and a~ | Journal of Lightwave Technology | 10.1109/50.372474 | ieee |
| 1996 | chraplyvy1996 | Andrew R. Chraplyvy | 1-Tb/s transmission experiment | IEEE Photonics Technology Lette~ | 10.1109/68.531857 | ieee |
| 1996 | knight1996 | J. C. Knight; P. St. J. Russell | All-silica single-mode optical fiber with photonic crystal cladding | Optics Letters | 10.1364/ol.21.001547 | manual |
| 1996 | krauss1996 | Thomas F. Krauss | Two-dimensional photonic-bandgap structures operating at near-infrared waveleng~ | Nature | 10.1038/383699a0 | manual |
| 1996 | onaka1996 | H. Onaka | 1.1 Tb/s WDM Transmission over a 150 km 1.3 um Zero-Dispersion Single-Mode Fiber | Optical Fiber Communication Con~ | https://opg.optica.org/abstract.cfm?uri=OFC-1996-PD19 | manual* |
| 1996 | vengsarkar1996 | A. M. Vengsarkar | Long-period fiber gratings as band-rejection filters | Journal of Lightwave Technology | 10.1109/50.476137 | ieee |
| 1997 | birks1997 | Philip St. J. Russell (g) | Endlessly single-mode photonic crystal fiber | Optics Letters | 10.1364/ol.22.000961 | manual |
| 1997 | inoue1997 | - | Athermal silica-based arrayed-waveguide gratingmultiplexer | Electronics Letters | 10.1049/el:19971317 | ieee |
| 1997 | ishibashi1997 | T. Ishibashi (b) | High-Speed Response of Uni-Traveling-Carrier Photodiodes | Japanese Journal of Applied Phy~ | 10.1143/jjap.36.6263 | oa |
| 1997 | little1997 | B. E. Little; H. A. Haus (a) | Microring resonator channel dropping filters | Journal of Lightwave Technology | 10.1109/50.588673 | ieee |
| 1997 | waldhausl1997 | - | Efficient Coupling into Polymer Waveguides by Gratings | Applied Optics | 10.1364/ao.36.009383 | blog |
| 1998 | levy1998 | M. Levy | Fabrication of single-crystal lithium niobate films by crystal ion slicing | Applied Physics Letters | 10.1063/1.121801 | manual |
| 1998 | little1998 | B. E. Little; J. S. Foresi | Ultra-compact Si-SiO2 microring resonator optical channel dropping filters | IEEE Photonics Technology Lette~ | 10.1109/68.662590 | ieee |
| 1999 | cregan1999 | Philip St. J. Russell (g) | Single-Mode Photonic Band Gap Guidance of Light in Air | Science | 10.1126/science.285.5433.1537 | manual |
| 1999 | ilchenko1999 | - | Pigtailing the high-Q microsphere cavity:?a simple fiber coupler for optical wh~ | Optics Letters | 10.1364/ol.24.000723 | blog |
| 1999 | imada1999 | Susumu Noda | Coherent two-dimensional lasing action in surface-emitting laser with triangula~ | Applied Physics Letters | 10.1063/1.124361 | manual |
| 1999 | luan1999 | Hsin-Chiao Luan; Lionel C. Kimerling | High-quality Ge epilayers on Si with low threading-dislocation densities |  | 10.1063/1.125187 | manual |
| 1999 | mason1999 | L. A. Coldren | Widely tunable sampled grating DBR laser with integrated electroabsorption modu~ | IEEE Photonics Technology Lette~ | 10.1109/68.766769 | ieee |
| 1999 | painter1999 | Oskar Painter; Axel Scherer (b) | Two-Dimensional Photonic Band-Gap Defect Mode Laser | Science | 10.1126/science.284.5421.1819 | manual |
| 1999 | udem1999 | Theodor W. Hänsch (g) | Absolute Optical Frequency Measurement of the CesiumD1Line with a Mode-Locked L~ | Physical Review Letters | 10.1103/physrevlett.82.3568 | manual |

#### E5 2000-2009 silicon photonics, frequency combs, coherent DSP (44)

| year | paper_id | DRI | title | venue | DOI or URL | route |
|---|---|---|---|---|---|---|
| 2000 | cai2000 | Kerry J. Vahala (g) | Observation of Critical Coupling in a Fiber Taper to a Silica-Microsphere Whisp~ | Physical Review Letters | 10.1103/physrevlett.85.74 | blog |
| 2000 | jones2000 | John L. Hall | Carrier-Envelope Phase Control of Femtosecond Mode-Locked Lasers and Direct Opt~ | Science | 10.1126/science.288.5466.635 | manual |
| 2000 | ranka2000 | - | Visible continuum generation in air–silica microstructure optical fibers with a~ | Optics Letters | 10.1364/ol.25.000025 | manual |
| 2001 | goh2001 | - | Low loss and high extinction ratio strictly nonblocking 16×16 thermooptic matri~ | Journal of Lightwave Technology | 10.1109/50.918890 | repo |
| 2001 | goltsman2001 | Grigory N. Gol'tsman; Roman Sobolewski | Picosecond superconducting single-photon optical detector | Applied Physics Letters | 10.1063/1.1388868 | manual |
| 2002 | shoji2002 | T. Shoji (b) | Low loss mode size converter from 0.3 µm square Si wire waveguides to singlemod~ | Electronics Letters | 10.1049/el:20021185 | repo |
| 2002 | taillaert2002 | Roel Baets (g) | An out-of-plane grating coupler for efficient butt-coupling between compact pla~ | IEEE Journal of Quantum Electro~ | 10.1109/jqe.2002.1017613 | ieee |
| 2003 | akahane2003 | Susumu Noda (g) | High-Q photonic nanocavity in a two-dimensional photonic crystal | Nature | 10.1038/nature02063 | manual |
| 2003 | almeida2003 | Michal Lipson (g) | Nanotaper for compact mode conversion | Optics Letters | 10.1364/ol.28.001302 | repo |
| 2003 | armani2003 | Kerry J. Vahala; Deniz K. Armani | Ultra-high-Q toroid microcavity on a chip | Nature | 10.1038/nature01371 | manual |
| 2004 | almeida2004 | Vilson R. Almeida; Carlos A. Barrios; Mic~ | Guiding and confining light in void nanostructure | Optics Letters | 10.1364/ol.29.001209 | manual |
| 2004 | dumon2004 | Roel Baets (b) | Low-Loss SOI Photonic Wires and Ring Resonators Fabricated With Deep UV Lithogr~ | IEEE Photonics Technology Lette~ | 10.1109/lpt.2004.826025 | repo |
| 2004 | kippenberg2004 | Tobias J. Kippenberg; Kerry J. Vahala | Kerr-Nonlinearity Optical Parametric Oscillation in an Ultrahigh- Q Toroid Micr~ | Physical Review Letters | 10.1103/physrevlett.93.083904 | manual |
| 2004 | liu2004 | Mario Paniccia (g) | A high-speed silicon optical modulator based on a metal–oxide–semiconductor cap~ | Nature | 10.1038/nature02310 | manual |
| 2004 | rabiei2004 | - | Optical and electro-optical properties of submicrometer lithium niobate slab wa~ |  | 10.1063/1.1819527 | manual |
| 2004 | taylor2004 | M. G. Taylor | Coherent Detection Method Using DSP for Demodulation of Signal and Subsequent E~ | IEEE Photonics Technology Lette~ | 10.1109/lpt.2003.823106 | ieee |
| 2004 | vlasov2004 | Yurii A. Vlasov (b) | Losses in single-mode silicon-on-insulator strip waveguides and bends | Optics Express | 10.1364/opex.12.001622 | repo |
| 2005 | bogaerts2005 | Wim Bogaerts | Nanophotonic waveguides in silicon-on-insulator fabricated with CMOS technology |  | 10.1109/jlt.2004.834471 | ieee |
| 2005 | gardes2005 | Graham T. Reed | A sub-micron depletion-type photonic modulator in Silicon On Insulator | Optics Express | 10.1364/opex.13.008845 | optica |
| 2005 | kuo2005 | David A. B. Miller; James S. Harris | Strong quantum-confined Stark effect in germanium quantum-well structures on si~ | Nature | 10.1038/nature04204 | manual |
| 2005 | nagarajan2005 | D. F. Welch; F. A. Kish | Large-scale photonic integrated circuits | IEEE Journal of Selected Topics~ | 10.1109/jstqe.2004.841721 | ieee |
| 2005 | roelkens2005 | Roel Baets (g) | Efficient silicon-on-insulator fiber coupler fabricated using 248-nm-deep UV li~ | IEEE Photonics Technology Lette~ | 10.1109/lpt.2005.859132 | blog |
| 2005 | rong2005 | Mario Paniccia (g) | A continuous-wave Raman silicon laser | Nature | 10.1038/nature03346 | manual |
| 2005 | xu2005 | Michal Lipson (g) | Micrometre-scale silicon electro-optic modulator | Nature | 10.1038/nature03569 | manual |
| 2006 | analui2006 | Behnam Analui; Adithyaram Narasimha (b) | A Fully Integrated 20-Gb/s Optoelectronic Transceiver Implemented in a Standard~ | IEEE Journal of Solid-State Cir~ | 10.1109/jssc.2006.884388 | ieee |
| 2006 | fang2006 | John E. Bowers; Mario J. Paniccia (g) | Electrically pumped hybrid AlGaInAs-silicon evanescent laser | Optics Express | 10.1364/oe.14.009203 | repo |
| 2006 | foster2006 | Alexander L. Gaeta; Michal Lipson | Broad-band optical parametric gain on a silicon photonic chip | Nature | 10.1038/nature04932 | repo |
| 2006 | gunn2006 | C. Gunn | CMOS Photonics for High-Speed Interconnects | IEEE Micro | 10.1109/mm.2006.32 | ieee |
| 2006 | lygagnon2006 | Kazuro Kikuchi | Coherent detection of optical quadrature phase-shift keying signals with carrie~ | Journal of Lightwave Technology | 10.1109/jlt.2005.860477 | ieee |
| 2007 | delhaye2007 | Tobias J. Kippenberg; Pascal Del'Haye | Optical frequency comb generation from a monolithic microresonator | Nature | 10.1038/nature06401 | arxiv |
| 2007 | liu2007 | Mario Paniccia (b) | High-speed optical modulation based on carrier depletion in a silicon waveguide | Optics Express | 10.1364/oe.15.000660 | optica |
| 2007 | vivien2007 | Laurent Vivien (b) | High speed and high responsivity germanium photodetector integrated in a Silico~ | Optics Express | 10.1364/oe.15.009843 | optica |
| 2008 | doerr2008 | - | Planar lightwave circuits in fiber-optic communications | Optical Fiber Telecommunication~ | 10.1016/b978-0-12-374171-4.00009-5 | blog |
| 2008 | kang2008a | Yimin Kang; Mike Morse (b) | Monolithic germanium/silicon avalanche photodiodes with 340 GHz gain–bandwidth ~ | Nature Photonics | 10.1038/nphoton.2008.247 | repo |
| 2008 | li2008 | Hong X. Tang | Harnessing optical forces in integrated photonic circuits | Nature | 10.1038/nature07545 | manual |
| 2008 | politi2008 | Jeremy L. O'Brien (b) | Silica-on-Silicon Waveguide Quantum Circuits | Science | 10.1126/science.1155441 | arxiv |
| 2008 | savory2008 | Seb J. Savory | Digital filters for coherent optical receivers | Optics Express | 10.1364/oe.16.000804 | optica |
| 2008 | shoji2008 | Tetsuya Mizumoto (b) | Magneto-optical isolator with silicon waveguides fabricated by direct bonding | Applied Physics Letters | 10.1063/1.2884855 | repo |
| 2008 | sun2008 | K. Roberts | Real-time measurements of a 40 Gb/s coherent system | Optics Express | 10.1364/oe.16.000873 | optica |
| 2009 | acoleyen2009 | Roel Baets (b) | Off-chip beam steering with a one-dimensional optical phased array on silicon-o~ | Optics Letters | 10.1364/ol.34.001477 | repo |
| 2009 | eichenfield2009 | Oskar Painter (b) | Optomechanical crystals | Nature | 10.1038/nature08524 | arxiv |
| 2009 | koos2009 | J. Leuthold; W. Freude; C. Koos (b) | All-optical high-speed signal processing with silicon–organic hybrid slot waveg~ | Nature Photonics | 10.1038/nphoton.2009.25 | manual |
| 2009 | miller2009 | David A. B. Miller | Device Requirements for Optical Interconnects to Silicon Chips | Proceedings of the IEEE | 10.1109/jproc.2009.2014298 | ieee |
| 2009 | xia2009 | Phaedon Avouris (b) | Ultrafast graphene photodetector | Nature Nanotechnology | 10.1038/nnano.2009.292 | arxiv |

#### E6 2010-2020 industrial SiPh, new platforms, solitons, programmable and quantum (86)

| year | paper_id | DRI | title | venue | DOI or URL | route |
|---|---|---|---|---|---|---|
| 2010 | alduino2010 | Mario Paniccia (b) | Demonstration of a High Speed 4-Channel Integrated Silicon Photonics WDM Link w~ | Integrated Photonics Research, ~ | 10.1364/iprsn.2010.pdiwi5 | manual |
| 2010 | assefa2010 | Solomon Assefa; Yurii A. Vlasov | Reinventing germanium avalanche photodetector for nanophotonic on-chip optical ~ | Nature | 10.1038/nature08813 | manual |
| 2010 | essiambre2010 | R.-J. Essiambre; P. J. Winzer (b) | Capacity Limits of Optical Fiber Networks | Journal of Lightwave Technology | 10.1109/jlt.2009.2039464 | ieee |
| 2010 | levy2010 | Michal Lipson; Alexander L. Gaeta (b) | CMOS-compatible multiple-wavelength oscillator for on-chip optical interconnects | Nature Photonics | 10.1038/nphoton.2009.259 | arxiv |
| 2010 | liu2010 | Jurgen Michel; Lionel C. Kimerling | Ge-on-Si laser operating at room temperature | Optics Letters | 10.1364/ol.35.000679 | manual |
| 2010 | razzari2010 | D. J. Moss; R. Morandotti (b) | CMOS-compatible integrated optical hyper-parametric oscillator | Nature Photonics | 10.1038/nphoton.2009.236 | manual |
| 2010 | rylyakov2010 | - | A 24-Channel 300 Gb/s 8.2 pJ/bit Full-Duplex Fiber-Coupled Optical Transceiver ~ |  | 10.1364/ofc.2010.pdpa8 | manual |
| 2010 | vermeulen2010 | Gunther Roelkens (b) | High-efficiency fiber-to-chip grating couplers realized using an advanced CMOS-~ | Optics Express | 10.1364/oe.18.018278 | repo |
| 2011 | bauters2011 | John E. Bowers; Daniel J. Blumenthal (b) | Planar waveguides with less than 01 dB/m propagation loss fabricated with wafer~ | Optics Express | 10.1364/oe.19.024090 | repo |
| 2011 | bi2011 | Caroline A. Ross (b) | On-chip optical isolation in monolithically integrated non-reciprocal optical r~ | Nature Photonics | 10.1038/nphoton.2011.270 | repo |
| 2011 | liu2011a | Xiang Zhang (b) | A graphene-based broadband optical modulator | Nature | 10.1038/nature10067 | manual |
| 2011 | nagarajan2011 | D. F. Welch; F. A. Kish | 10 Channel, 100Gbit/s per Channel, Dual Polarization, Coherent QPSK, Monolithic~ | Optical Fiber Communication Con~ | 10.1364/ofc.2011.oml7 | manual |
| 2011 | pant2011 | Benjamin J. Eggleton (b) | On-chip stimulated Brillouin scattering | Optics Express | 10.1364/oe.19.008285 | optica |
| 2012 | assefa2012 | Yurii A. Vlasov; Solomon Assefa | A 90nm CMOS integrated Nano-Photonics technology for 25Gbps WDM optical communi~ | 2012 International Electron Dev~ | 10.1109/iedm.2012.6479162 | ieee |
| 2012 | camachoaguilera2012 | Jurgen Michel; Lionel C. Kimerling (b) | An electrically pumped germanium laser | Optics Express | 10.1364/oe.20.011316 | optica |
| 2012 | lee2012 | Kerry J. Vahala (b) | Chemically etched ultrahigh-Q wedge-resonator on a silicon chip | Nature Photonics | 10.1038/nphoton.2012.109 | repo |
| 2012 | lindenmann2012 | Christian Koos | Photonic wire bonding: a novel concept for chip-scale interconnects | Optics Express | 10.1364/oe.20.017667 | repo |
| 2012 | lira2012 | Michal Lipson; Shanhui Fan (b) | Electrically Driven Nonreciprocity Induced by Interband Photonic Transition on ~ | Physical Review Letters | 10.1103/physrevlett.109.033901 | repo |
| 2012 | pernice2012 | Wolfram H. P. Pernice; Hong X. Tang | High-speed and high-efficiency travelling wave single-photon detectors embedded~ | Nature Communications | 10.1038/ncomms2307 | repo |
| 2012 | takara2012 | H. Takara (b) | 1.01-Pb/s (12 SDM/222 WDM/456 Gb/s) Crosstalk-managed Transmission with 91.4-b/~ | European Conference and Exhibit~ | 10.1364/eceoc.2012.th.3.c.1 | manual |
| 2012 | thomson2012 | Graham T. Reed | 50-Gb/s Silicon Optical Modulator | IEEE Photonics Technology Lette~ | 10.1109/lpt.2011.2177081 | ieee |
| 2013 | hafezi2013 | Mohammad Hafezi; Jacob M. Taylor (b) | Imaging topological edge states in silicon photonics | Nature Photonics | 10.1038/nphoton.2013.274 | arxiv |
| 2013 | pospischil2013 | Thomas Mueller (b) | CMOS-compatible graphene photodetector covering all optical communication bands | Nature Photonics | 10.1038/nphoton.2013.240 | repo |
| 2013 | rechtsman2013 | Mordechai Segev; Alexander Szameit (b) | Photonic Floquet topological insulators | Nature | 10.1038/nature12066 | arxiv |
| 2013 | richardson2013 | D. J. Richardson | Space-division multiplexing in optical fibres | Nature Photonics | 10.1038/nphoton.2013.94 | arxiv |
| 2013 | sun2013 | Michael R. Watts | Large-scale nanophotonic phased array | Nature | 10.1038/nature11727 | repo |
| 2014 | ding2014 | Haiyan Ou; Kresten Yvind (b) | Fully etched apodized grating coupler on the SOI platform with −058 dB coupling~ | Optics Letters | 10.1364/ol.39.005348 | repo |
| 2014 | doerr2014 | C. Doerr | Single-Chip Silicon Photonics 100-Gb/s Coherent Transceiver | Optical Fiber Communication Con~ | 10.1364/ofc.2014.th5c.1 | manual |
| 2014 | hausmann2014 | M. Loncar (b) | Diamond nonlinear photonics | Nature Photonics | 10.1038/nphoton.2014.72 | repo |
| 2014 | herr2014 | T. J. Kippenberg; M. L. Gorodetsky (b) | Temporal solitons in optical microresonators | Nature Photonics | 10.1038/nphoton.2013.343 | arxiv |
| 2014 | hirose2014 | Susumu Noda | Watt-class high-power, high-beam-quality photonic-crystal lasers | Nature Photonics | 10.1038/nphoton.2014.75 | manual |
| 2014 | liu2014 | John E. Bowers; Arthur C. Gossard (b) | High performance continuous wave 1.3 μ m quantum dot lasers on silicon | Applied Physics Letters | 10.1063/1.4863223 | manual |
| 2014 | melikyan2014 | J. Leuthold (b) | High-speed plasmonic phase modulators | Nature Photonics | 10.1038/nphoton.2014.9 | manual |
| 2014 | poletti2014 | F. Poletti (b) | Nested antiresonant nodeless hollow core fiber | Optics Express | 10.1364/oe.22.023807 | optica |
| 2014 | santis2014 | Amnon Yariv | High-coherence semiconductor lasers based on integral high- Q resonators in hyb~ | Proceedings of the National Aca~ | 10.1073/pnas.1400184111 | oa |
| 2014 | smit2014 | M. Smit | An introduction to InP-based generic integration technology | Semiconductor Science and Techn~ | 10.1088/0268-1242/29/8/083001 | oa |
| 2014 | spencer2014 | John E. Bowers (b) | Integrated waveguide coupled Si_3N_4 resonators in the ultrahigh-Q regime | Optica | 10.1364/optica.1.000153 | repo |
| 2014 | zaoui2014 | Manfred Berroth (b) | Bridging the gap between optical fibers and silicon photonic integrated circuits | Optics Express | 10.1364/oe.22.001277 | repo |
| 2015 | absil2015 | Philippe P. Absil; Joris Van Campenhout (b) | Imec iSiPP25G silicon photonics: a robust CMOS-based photonics technology platf~ | Proceedings of SPIE | 10.1117/12.2076262 | manual |
| 2015 | barwicz2015 | Tymon Barwicz (b) | Automated, self-aligned assembly of 12 fibers per nanophotonic chip with standa~ | 2015 IEEE 65th Electronic Compo~ | 10.1109/ectc.2015.7159680 | ieee |
| 2015 | carolan2015 | Jeremy L. O'Brien; Anthony Laing (b) | Universal linear optics | Science | 10.1126/science.aab3642 | arxiv |
| 2015 | haffner2015 | J. Leuthold (b) | All-plasmonic Mach–Zehnder modulator enabling optical high-speed communication ~ | Nature Photonics | 10.1038/nphoton.2015.127 | manual |
| 2015 | piggott2015 | Jelena Vuckovic (b) | Inverse design and demonstration of a compact and broadband on-chip wavelength ~ | Nature Photonics | 10.1038/nphoton.2015.69 | repo |
| 2015 | rios2015 | Harish Bhaskaran; Wolfram H. P. Pernice (b) | Integrated all-photonic non-volatile multi-level memory | Nature Photonics | 10.1038/nphoton.2015.182 | oa |
| 2015 | shen2015 | Rajesh Menon (b) | An integrated-nanophotonics polarization beamsplitter with 2.4 × 2.4 μm2 footpr~ | Nature Photonics | 10.1038/nphoton.2015.80 | repo |
| 2015 | sun2015 | Vladimir M. Stojanovic; Milos A. Popovic;~ | Single-chip microprocessor that communicates directly using light | Nature | 10.1038/nature16454 | manual |
| 2016 | brasch2016 | T. J. Kippenberg (b) | Photonic chip–based optical frequency comb using soliton Cherenkov radiation | Science | 10.1126/science.aad4811 | arxiv |
| 2016 | chen2016 | Huiyun Liu; Alwyn J. Seeds | Electrically pumped continuous-wave III–V quantum dot lasers on silicon | Nature Photonics | 10.1038/nphoton.2016.21 | repo |
| 2016 | clements2016 | Ian A. Walmsley (b) | Optimal design for universal multiport interferometers | Optica | 10.1364/optica.3.001460 | optica |
| 2016 | pfeiffer2016 | Tobias J. Kippenberg (b) | Photonic Damascene process for integrated high-Q microresonator based nonlinear~ | Optica | 10.1364/optica.3.000020 | optica |
| 2016 | pu2016 | Kresten Yvind (b) | Efficient frequency comb generation in AlGaAs-on-insulator | Optica | 10.1364/optica.3.000823 | optica |
| 2017 | ji2017 | Michal Lipson; Alexander L. Gaeta (b) | Ultra-low-loss on-chip resonators with sub-milliwatt parametric oscillation thr~ | Optica | 10.1364/optica.4.000619 | repo |
| 2017 | marinpalomo2017 | Christian Koos; Tobias J. Kippenberg (b) | Microresonator-based solitons for massively parallel coherent optical communica~ | Nature | 10.1038/nature22387 | arxiv |
| 2017 | miller2017a | David A. B. Miller | Attojoule Optoelectronics for Low-Energy Information Processing and Communicati~ | Journal of Lightwave Technology | 10.1109/jlt.2017.2647779 | arxiv |
| 2017 | perez2017 | Jose Capmany (b) | Multipurpose silicon photonics signal processor core | Nature Communications | 10.1038/s41467-017-00714-1 | repo |
| 2017 | poulton2017a | Michael R. Watts (b) | Coherent solid-state LIDAR with silicon photonic optical phased arrays | Optics Letters | 10.1364/ol.42.004091 | manual |
| 2017 | shen2017 | Dirk Englund; Marin Soljacic (b) | Deep learning with coherent nanophotonic circuits | Nature Photonics | 10.1038/nphoton.2017.93 | arxiv |
| 2017 | zhang2017a | Marko Loncar (b) | Monolithic ultra-high-Q lithium niobate microring resonator | Optica | 10.1364/optica.4.001536 | repo |
| 2018 | atabaki2018 | Rajeev J. Ram (b) | Integrating photonics with silicon nanoelectronics for the next generation of s~ | Nature | 10.1038/s41586-018-0028-z | manual |
| 2018 | billah2018 | Christian Koos (b) | Hybrid integration of silicon photonics circuits and InP lasers by photonic wir~ | Optica | 10.1364/optica.5.000876 | repo |
| 2018 | dietrich2018 | Christian Koos (b) | In situ 3D nanoprinting of free-form coupling elements for hybrid photonic inte~ | Nature Photonics | 10.1038/s41566-018-0133-4 | repo |
| 2018 | gundavarapu2018 | Daniel J. Blumenthal (b) | Sub-hertz fundamental linewidth photonic integrated Brillouin laser | Nature Photonics | 10.1038/s41566-018-0313-2 | repo |
| 2018 | kittlaus2018 | Peter T. Rakich (b) | Non-reciprocal interband Brillouin modulation | Nature Photonics | 10.1038/s41566-018-0254-9 | repo |
| 2018 | otterstrom2018 | Peter T. Rakich (b) | A silicon Brillouin laser | Science | 10.1126/science.aar6113 | arxiv |
| 2018 | pinguet2018 | Peter De Dobbelaere (b) | High-Volume Manufacturing Platform for Silicon Photonics | Proceedings of the IEEE | 10.1109/jproc.2018.2859198 | ieee |
| 2018 | roeloffzen2018 | - | Low-Loss Si3N4 TriPleX Optical Waveguides: Technology and Applications Overview | IEEE Journal of Selected Topics~ | 10.1109/jstqe.2018.2793945 | repo |
| 2018 | sohn2018 | Gaurav Bahl (b) | Time-reversal symmetry breaking with acoustic pumping of nanophotonic circuits | Nature Photonics | 10.1038/s41566-017-0075-2 | repo |
| 2018 | spencer2018 | Scott B. Papp; Scott A. Diddams (b) | An optical-frequency synthesizer using integrated photonics | Nature | 10.1038/s41586-018-0065-7 | arxiv |
| 2018 | stern2018 | Michal Lipson; Alexander L. Gaeta (b) | Battery-operated integrated frequency comb generator | Nature | 10.1038/s41586-018-0598-9 | repo |
| 2018 | wang2018 | Marko Loncar; Martin M. Fejer (b) | Ultrahigh-efficiency wavelength conversion in nanophotonic periodically poled l~ | Optica | 10.1364/optica.5.001438 | repo |
| 2018 | wang2018a | Jianwei Wang; Mark G. Thompson (b) | Multidimensional quantum entanglement with large-scale integrated optics | Science | 10.1126/science.aar7053 | oa |
| 2018 | wang2018b | Marko Loncar (b) | Integrated lithium niobate electro-optic modulators operating at CMOS-compatibl~ | Nature | 10.1038/s41586-018-0551-y | manual |
| 2018 | weigel2018 | - | Bonded thin film lithium niobate modulator on a silicon photonics platform exce~ | Optics Express 26(18), 23728 | 10.1364/oe.26.023728 | repo |
| 2019 | abel2019 | Jean Fompeyrine (b) | Large Pockels effect in micro- and nanostructured barium titanate integrated on~ | Nature Materials | 10.1038/s41563-018-0208-0 | manual |
| 2019 | fahrenkopf2019 | Douglas D. Coolbaugh (b) | The AIM Photonics MPW: A Highly Accessible Cutting Edge Technology for Rapid Pr~ | IEEE Journal of Selected Topics~ | 10.1109/jstqe.2019.2935698 | repo |
| 2019 | giewont2019 | Ken Giewont; Thomas Houghton (b) | 300-mm Monolithic Silicon Photonics Foundry Technology | IEEE Journal of Selected Topics~ | 10.1109/jstqe.2019.2908790 | repo |
| 2019 | he2019 | Xinlun Cai (b) | High-performance hybrid silicon and lithium niobate Mach–Zehnder modulators for~ | Nature Photonics | 10.1038/s41566-019-0378-6 | repo |
| 2019 | huang2019 | John E. Bowers (b) | High-power sub-kHz linewidth lasers fully integrated on silicon | Optica | 10.1364/optica.6.000745 | repo |
| 2019 | jones2019 | Richard Jones (b) | Heterogeneously Integrated InP\/Silicon Photonics: Fabricating Fully Functional~ | IEEE Nanotechnology Magazine | 10.1109/mnano.2019.2891369 | ieee |
| 2019 | wilson2019 | Paul Seidler (b) | Integrated gallium phosphide nonlinear photonics | Nature Photonics | 10.1038/s41566-019-0537-9 | repo |
| 2019 | zhang2019b | Marko Loncar (b) | Broadband electro-optic frequency comb generation in a lithium niobate microrin~ | Nature | 10.1038/s41586-019-1008-7 | repo |
| 2020 | jasion2020 | F. Poletti; D. J. Richardson (b) | Hollow Core NANF with 0.28 dB/km Attenuation in the C and L Bands | Optical Fiber Communication Con~ | 10.1364/ofc.2020.th4b.4 | manual |
| 2020 | kittlaus2020a | Peter T. Rakich; Mina Rais-Zadeh (b) | Electrically driven acousto-optics and broadband non-reciprocity in silicon pho~ | Nature Photonics | 10.1038/s41566-020-00711-9 | repo |
| 2020 | rakowski2020 | Michal Rakowski; John Pellerin (b) | 45nm CMOS - Silicon Photonics Monolithic Technology (45CLO) for next-generation~ | Optical Fiber Communication Con~ | 10.1364/ofc.2020.t3h.3 | manual |
| 2020 | shen2020 | Kerry Vahala; John E. Bowers (b) | Integrated turnkey soliton microcombs | Nature | 10.1038/s41586-020-2358-x | repo |
| 2020 | wade2020 | Mark Wade | TeraPHY: A Chiplet Technology for Low-Power, High-Bandwidth In-Package Optical ~ | IEEE Micro | 10.1109/mm.2020.2976067 | ieee |

### Reserve list (ids; details in the CSV)

- E0 (18): kerr1875, bell1880, rayleigh1897, mie1908, debye1909, bragg1913, baird1928, hansell1930, barrow1936, carson1936, purcell1946, goos1947, weber1953, pierce1954, gordon1955, bloembergen1956, franz1958, hirschowitz1958
- E1 (29): schawlow1960, sorokin1960, basov1961, snitzer1961b, snitzer1961c, boyd1962, giordmaine1962, maker1962, mcclung1962, woodbury1962, glauber1963, glauber1963a, nelson1963, chiao1964, geusic1964, marcatili1964, patel1964, ashkin1966, schafer1966, sorokin1966, werts1966, kao1968, shubert1968, alferov1969, goell1969, harris1969, kressel1969, marcuse1969, snyder1969
- E2 (29): hall1970, tien1970, curtiss1971, kazarinov1971, ippen1972, ippen1972a, tien1972, zeldovich1972, bryngdahl1973, kaiser1973, keck1973, pinnow1973, chandross1974, cohen1974, stolen1974, tsukada1974, auracher1975, haus1975, nakamura1975, ohmachi1975, vanderziel1975, kuppers1976, epworth1977, gould1977, tamir1977, eckstein1978, stolen1978, arai1979, cohen1979
- E3 (28): alferness1980, bergh1980, izawa1980, lin1980, okoshi1980, fork1981, hosaka1981, utaka1981, birch1982, tohmori1983, mollenauer1984, runge1984, hardy1985, mears1985, moulton1986, suzuki1986, yablonovitch1986, bowers1987, murata1987, saitoh1987, doran1988, grover1988, koyama1988, kurdi1988, amano1989, jewell1989, laming1989, po1989
- E4 (23): coldren1990, kawachi1990, magel1990, saleh1990, adar1991, brinkmann1991, dragone1991b, schmidtchen1991, tachibana1991, weiss1991, ishii1993, nakamura1994, babic1995, myers1995, mekis1996, morioka1996, okamoto1996, vandenhoven1996, bestwick1997, knight1997, colace1998, shimizu1998, vernooy1998
- E5 (46): diddams2000, holzwarth2000, iga2000, ito2000, kogelnik2000, lee2000, miller2000, yariv2000, bigo2001, fukuchi2001, notomi2001, nagayama2002, spillane2002, taillaert2003, borel2004, boyraz2004, coldren2004, dehlinger2004, jensen2004, li2004, savchenkov2004, liao2005, park2005, song2005, vlasov2005, doerr2006, jacobsen2006, kuramochi2006, nagarajan2006, ahn2007, barwicz2007, green2007, guarino2007, liao2007, vanlaere2007, xu2007, fang2008a, ferrera2008, haldane2008, narasimha2008, stolen2008, matthews2009, pelusi2009, roberts2009, wang2009, yu2009
- E6 (55): bradley2010, doerr2010, kucharski2010, leo2010, mueller2010, reed2010, bauters2011a, bradley2011, chan2011, evans2011, gardes2011, qian2011, safavinaeini2011, sakaguchi2011, smit2011, tien2011, watts2011, yu2011, lee2012a, rakich2012, ryf2012, sakaguchi2012, xiong2012, abel2013, coen2013, gan2013, jung2013, koch2013, lalaukeraly2013, miller2013, shin2013, silverstone2013, spring2013, wang2013, alloatti2014, kuchta2014, phare2015, vanlaer2015, xue2015, yi2015, khorasaninejad2016, kittlaus2016, xuan2016, li2017, augustin2018, kippenberg2018, stojanovic2018, yoshida2018, feldmann2019, bogaerts2020, chang2020, oif2020, jung2021, liu2021a, puckett2021
