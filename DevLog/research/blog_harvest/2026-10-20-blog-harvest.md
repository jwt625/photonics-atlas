# Blog harvest: candidate papers for new photonics atlases (2026-10-20)

Inventory only. Nothing downloaded, no web fetches, no source files modified. Every identifier below was taken literally from a blog file (verified: all 1990 identifiers in `candidates.csv` occur in their `post_file`, modulo URL percent-encoding).

## Outputs

| file | content |
|---|---|
| `candidates.csv` | 1990 unique scholarly identifiers (doi 1386, arxiv 338, url 183, ieee_doc 50, optica_uri 33) from 144 blog files, post dates 2018-01-03 to 2026-10-14 |
| `local_pdfs.csv` | 128 photonics-relevant PDFs out of 202 under `jwt625.github.io/assets/` (title_source: filename 84, pdf_page1 36, pdf_metadata 8) |
| this file | counts, atlas overlap, top-40 OA seeding list, method, limitations |

## Counts: topic_guess x access_class (unique identifiers)

OA = arxiv + optica_oa_journal + nature_comms_or_lsa + other_oa_journal + other_oa_repository. "via heading" = topic came from the section heading because the link text matched no rule (merged into the topic row here; kept as `topic(heading)` in the CSV).

| topic | arxiv | optica_oa_journal | nature_comms_or_lsa | other_oa_journal | other_oa_repository | other_publisher | ieee | total | OA subtotal | via heading |
|---|---|---|---|---|---|---|---|---|---|---|
| eo_modulator | 14 | 11 | 3 | 1 | 0 | 14 | 9 | 52 | 29 | 4 |
| coupler | 9 | 3 | 1 | 0 | 1 | 15 | 5 | 34 | 14 | 5 |
| passive | 18 | 15 | 7 | 2 | 2 | 42 | 16 | 102 | 44 | 15 |
| laser/source | 34 | 53 | 12 | 5 | 7 | 138 | 12 | 261 | 111 | 26 |
| detector | 8 | 4 | 0 | 0 | 0 | 10 | 0 | 22 | 12 | 2 |
| platform/material/wafer | 34 | 11 | 5 | 6 | 6 | 111 | 12 | 185 | 62 | 24 |
| packaging/CPO | 8 | 6 | 0 | 2 | 2 | 35 | 18 | 71 | 18 | 7 |
| AMO/quantum photonics | 66 | 12 | 7 | 13 | 7 | 88 | 11 | 204 | 105 | 24 |
| systems/interconnect | 12 | 5 | 1 | 2 | 0 | 28 | 18 | 66 | 20 | 4 |
| photonics_unclassified | 63 | 32 | 27 | 12 | 14 | 203 | 30 | 381 | 148 | 55 |
| other/non-photonics | 72 | 15 | 20 | 21 | 27 | 410 | 47 | 612 | 155 | 0 |
| total | 338 | 167 | 83 | 64 | 66 | 1094 | 178 | 1990 | 718 | 166 |

- OA rows with a photonics topic (all except other/non-photonics) and in neither atlas: 534.
- Truncated identifiers kept and flagged in `context` ("[truncated URL in source, identifier may be incomplete]"): 48. Rows present only in secondary sources: 37 (35 from `_posts/scraping/`, 2 from `old/_includes/publications.html` (a publication list page); `post_date` empty).

## Overlap with existing atlases

| check | Y |
|---|---|
| in_eo_atlas (eo-modulator-atlas `data/papers.csv` + `data/candidates.csv`) | 44 (eo_modulator 34 incl. 1 via heading; platform 4; AMO 3; photonics_unclassified 2; packaging 1) |
| in_packaging_atlas (advanced-packaging-atlas `data/papers.csv` + `outputs/candidates.csv`) | 19 (packaging/CPO 6, platform 3, photonics_unclassified 3, coupler 2, systems 2, other 2, passive 1) |

Of 52 eo_modulator-tagged rows, 18 are not in the EO atlas (see below); the remaining blog EO links are already covered.

## Top 40 OA candidates for component / supply-chain atlas seeding (non-EO-modulator, in neither atlas)

Selection: hand-picked from the OA rows for PIC-component or packaging relevance; title is the blog link text. Access class is journal/repository-level, not verified per article.

| # | identifier | title (blog link text) | topic | access | post_date |
|---|---|---|---|---|---|
| 1 | doi:10.1364/oe.541701 | Fabrication of a 3D mode size converter for efficient edge coupling in photonic integrated circuits | coupler | optica_oa_journal | 2025-03-09 |
| 2 | arxiv:2412.17941 | High-efficiency, cryogenic-compatible grating couplers on an AlN-on-sapphire platform through bottom-side coupling | coupler | arxiv | 2025-08-10 |
| 3 | arxiv:2510.15622 | Ultracompact Inverse-Designed Silicon-on-Insulator Couplers with Sub-Decibel Coupling Efficiency | coupler | arxiv | 2025-10-26 |
| 4 | arxiv:2510.02089 | Fiber-to-chip grating couplers for Lithium Niobate on Sapphire | coupler | arxiv | 2026-01-25 |
| 5 | arxiv:2607.01477 | High-Beam-Quality Meta-Grating Couplers for Large Collimated Free-Space Beams on Silicon-on-Insulator | coupler | arxiv | 2026-07-07 |
| 6 | arxiv:2608.00833 | Efficient Mode Conversion at 1064 nm via Bilayer Inverse Taper on Thin-Film Lithium Niobate | coupler | arxiv | 2026-08-23 |
| 7 | doi:10.1364/oe.603256 | SAFELOC: self-aligned fiber entry low-loss optical coupler | coupler | optica_oa_journal | 2026-08-31 |
| 8 | doi:10.1038/s41598-024-79945-4 | Microresonator photonic wire bond integration for Kerr-microcomb generation | coupler (PWB) | nature_comms_or_lsa (Sci Rep) | 2024-11-30 |
| 9 | optica_uri:optica-11-10-1397 | Efficient mass manufacturing of high-density, ultra-low-loss Si3N4 photonic integrated circuits | passive / platform | optica_oa_journal | 2024-11-03 |
| 10 | arxiv:2404.06117 | Low-Loss Silicon Directional Coupler with Arbitrary Coupling Ratios for Broadband Wavelength Operation Based on Bent Waveguides | passive | arxiv | 2025-01-12 |
| 11 | doi:10.1038/s41467-024-55528-9 | Silicon photonic MEMS switches based on split waveguide crossings | passive | nature_comms_or_lsa | 2025-01-26 |
| 12 | arxiv:2504.12917 | Arrayed waveguide gratings in lithium tantalate integrated photonics | passive | arxiv | 2025-04-27 |
| 13 | arxiv:2512.04886 | Near-Zero Crosstalk and Ultra-Low Loss Waveguide Crossings Enabled by three-dimensional Ta2O5-on-LNOI Integrated Photonics | passive | arxiv | 2025-12-07 |
| 14 | arxiv:2602.15250 | Systematic Design and Demonstration of Multipole, Coupled-Cavity Integrated Photonic Bandpass Filters with High FSR | passive | arxiv | 2026-02-22 |
| 15 | arxiv:2608.03146 | Zero-change foundry compatible silicon photonics MEMS optical switch | passive | arxiv | 2026-08-23 |
| 16 | arxiv:2411.19264 | Monolithic piezoelectrically tunable hybrid integrated laser with sub-fiber laser coherence | laser/source | arxiv | 2024-12-15 |
| 17 | arxiv:2501.06936 | Full C- and L-band tunable erbium-doped integrated lasers via scalable manufacturing | laser/source | arxiv | 2025-01-26 |
| 18 | doi:10.1364/oe.561111 | Widely tunable narrow-linewidth lasers with booster amplification on silicon photonics | laser/source | optica_oa_journal | 2025-05-26 |
| 19 | doi:10.1364/oe.412839 | Back-side-on-BOX heterogeneously integrated III-V-on-silicon O-band discrete-mode lasers | laser/source | optica_oa_journal | 2025-09-15 |
| 20 | doi:10.1364/oe.580766 | Compact hybrid-integrated multi-port multi-wavelength laser source based on high-power DFB laser array for optical I/O | laser/source | optica_oa_journal | 2025-12-22 |
| 21 | arxiv:2510.16699 | Hybrid integration of InGaN lasers in a foundry-fabricated visible-light photonics platform | laser/source | arxiv | 2025-10-26 |
| 22 | arxiv:2412.07627 | Terabit-class coherent communications enabled by an integrated photonics erbium doped amplifier | laser/source (amplifier) | arxiv | 2024-12-22 |
| 23 | doi:10.1364/optica.572859 | 100 GHz bandwidth ultra-thin germanium photodetectors with high responsivity on a 300 mm silicon photonics process | detector | optica_oa_journal | 2026-01-25 |
| 24 | arxiv:2607.03008 | Heterogeneously Integrated Balanced Photodetector on an Ultra-Low Loss Silicon Nitride Delay Line Interferometer | detector | arxiv | 2026-07-15 |
| 25 | arxiv:2507.19269 | Waveguide-Coupled Mid-Infrared GeSn Membrane Photodetectors on Silicon-on-Insulator | detector | arxiv | 2025-08-05 |
| 26 | doi:10.1364/optica.554862 | Heterogeneous tantala photonic integrated circuits for sub-micron wavelength applications | platform | optica_oa_journal | 2025-04-27 |
| 27 | arxiv:2509.08092 | Monolithic 3D integration of tantalum pentoxide photonics on arbitrary substrates | platform | arxiv | 2025-09-15 |
| 28 | arxiv:2604.12889 | Building reliable 3D photonic integrated circuits and cavities at the wafer scale | platform | arxiv | 2026-04-20 |
| 29 | doi:10.1364/optica.589726 | Transparent and mechanically flexible wafer-scale silicon-photonics fabrication platform | platform | optica_oa_journal | 2026-09-27 |
| 30 | doi:10.1038/s41467-024-44750-0 | Roadmapping the next generation of silicon photonics | platform (review) | nature_comms_or_lsa | 2025-01-19 |
| 31 | arxiv:2412.06570 | Next generation Co-Packaged Optics Technology to Train & Run Generative AI Models in Data Centers and Other Computing Applications | packaging/CPO | arxiv | 2024-12-29 |
| 32 | arxiv:2505.21168 | Ultra-Broadband plug-and-play photonic circuit packaging with sub-dB loss | packaging/CPO | arxiv | 2025-06-01 |
| 33 | url:hal.science/hal-04665935 (2024-Boucaud-APL-Photonic-Glass-Interposer) | Glass interposer for heterogeneous integration of flip-chipped photonic and electronic integrated circuits | packaging/CPO | other_oa_repository | 2025-10-13 |
| 34 | doi:10.3390/photonics12080821 | Photonic Integrated Circuits: Research Advances and Challenges in Interconnection and Packaging Technologies | packaging/CPO (review) | other_oa_journal (MDPI) | 2025-12-29 |
| 35 | doi:10.1364/oe.576420 | Silicon nitride photonic platform on glass for scalable, high-density optical redistribution layers in panel-level packaging | packaging/CPO | optica_oa_journal | 2026-10-14 |
| 36 | doi:10.1364/oe.555476 | 1.6-Tbps low-power linear-drive high-density optical interface for machine learning/artificial intelligence | systems/interconnect | optica_oa_journal | 2025-04-06 |
| 37 | doi:10.1038/s41467-024-55423-3 | An integrated photonic engine for programmable atomic control | AMO/quantum | nature_comms_or_lsa | 2025-12-01 |
| 38 | arxiv:2509.03279 | Silicon nitride photonic integrated circuit for controlling chip-based cold-atom inertial sensors | AMO/quantum | arxiv | 2025-09-08 |
| 39 | doi:10.1364/opticaq.532260 | Enabling photonic integrated 3D magneto-optical traps for quantum sciences and applications | AMO/quantum | optica_oa_journal (Optica Quantum) | 2025-03-09 |
| 40 | arxiv:2505.07445 | Integrated Multi-Wavelength Photonic Architectures for Future Scalable Trapped Ion Quantum Devices | AMO/quantum | arxiv | 2025-05-18 |

Further OA rows of similar relevance, not ranked into the 40: arxiv:2504.19465 (slow-light tunable microrings), arxiv:2601.15753 (Ta2O5 microrings), arxiv:2601.02842 (AlN microresonators), arxiv:2501.15010 (coil-stabilized ECL), doi:10.1364/oe.558707 (sputtered Er waveguide amplifier), doi:10.1364/oe.600656 (QCL on Ge-on-Si), doi:10.1364/oe.607675 (transfer-printed magneto-optic on SiPh), arxiv:2508.06079 (panel-scale photonic interconnects), arxiv:2503.14704 (cryogenic PIC packaging), arxiv:2604.03229 (Sr clocks with integrated photonics), arxiv:2512.19852 (atom-clad waveguide vapor PIC), arxiv:2605.17738 (III-V-on-SiN quantum platform), arxiv:2512.07535 (QD arrays edge-coupled to SiN), doi:10.1364/oe.25.018288 (printed freeform lenses on multi-core fiber), doi:10.1364/oe.601126 (laser-welded multi-core fiber interfaces).

## EO-modulator-tagged rows not in the EO atlas (18)

Keyword-tagged; several are not EO modulators (LED, SLM, laser).

| identifier | link text / context | access |
|---|---|---|
| ieee_doc:10225255 | Millimeter-Wave and Sub-THz Phased-Array Imaging Systems Based on Electro-Optic Up-Conversion and Optical Beam... | ieee |
| doi:10.1038/s41378-020-00198-y | Directly addressable GaN-based nano-LED arrays (not EO modulator) | other_publisher |
| doi:10.1117/12.580527 | KTN optical waveguide devices with an extremely large electro-optic effect | other_publisher |
| doi:10.1038/s41566-025-01687-0 | Ultrafast tunable photonic-integrated extended-DBR Pockels laser | other_publisher |
| ieee_doc:10727517 | Hybrid Integration of Silicon Slot Photonics with Ferroelectric Nematic Liquid Crystal for Poling-Free Pockels... | ieee |
| doi:10.1063/5.0088842 | Visible light modulator by sputter-deposited lithium niobate | other_publisher |
| doi:10.1038/s41467-025-62635-8 | Integrated lithium niobate photonic computing circuit based on efficient and high-speed electro-optic conversion | nature_comms_or_lsa |
| doi:10.1038/s41467-025-66718-4 | Piezoelectrically actuated silicon-nitride-based high-speed spatial light modulator | nature_comms_or_lsa |
| doi:10.1364/oe.26.032388 | Model and experimental validation of a unidirectional phase modulator | optica_oa_journal |
| doi:10.1364/opticaq.582412 | CMOS-fabricated ultraviolet light modulator using low-loss alumina piezo-optomechanical photonics | optica_oa_journal |
| doi:10.15479/at:ista:13175 | Cavity quantum electrooptics (ISTA thesis) | other_publisher |
| arxiv:2601.08906 | A 10 Megahertz Spatial Light Modulator | arxiv |
| doi:10.1117/12.2514483 | Adapting Texas Instruments DLP technology to demonstrate a phase spatial light modulator | other_publisher |
| url:ieeexplore (truncated) | Broadband and turnkey Pockels micro-comb with Monolithic Microwave Resonator (URL truncated in post) | ieee |
| doi:10.1364/oe.26 (truncated) | duplicate of the unidirectional phase modulator row (truncated in source) | optica_oa_journal |
| 3 x url:rdcu.be | Nature share links with link text "also"/"see also" (DOI not in URL) | other_publisher |

Local PDFs tagged eo_modulator not represented as blog links: SPIE 133650T (W-band up-conversion with folded TFLN modulators), SPIE 1336917 + poster (BTO EO modulation), `wang-et-al-2025-thin-film-lithium-tantalate-modulator-operating-at-high-optical-power.pdf`, Khurgin 2024 LPR, Soref 1986. Not checked against the EO atlas by title.

## Local PDFs (`local_pdfs.csv`)

128 rows: platform/material/wafer 26 (includes EBL/nanofab and Soitec wafer-supply docs), laser/source 20, photonics_unclassified 19, packaging/CPO 15 (OIF CPO framework, OIF ELSFP 02.0, ECTC 2015 micro-transfer printing, IBM assembly, CPO folder), systems/interconnect 13, AMO/quantum 11, passive 9, coupler 8 (incl. SPIE photonic wire bond reliability and power-handling papers, RAM Photonics Medusa), eo_modulator 6, detector 1. Excluded: superconducting-circuit, RF/mm-wave hardware, MEMS, biomedical, AI/market reports, and general non-photonics PDFs. Several are publisher PDFs or company slides: local reference copies, not OA-redistributable by default.

## OFC 2026 corpus (not OA)

`PlayGround/20260320_OFC`: 599 MB; `extracted_text/` holds 677 papers as paired `.md` + `.txt` (1354 files); no paper PDFs locally (source zip was on a remote host per README); plus TF-IDF/term/bigram/trigram CSVs, word maps, `output/` (metadata, institution-topic analysis, scrape runs), `ofc_browser/`.

## Method

1. Sources: `_posts/*.md` (173 files incl. OFS weekly posts and long-form posts), `_pages/*.md`, `_posts/scraping/*` (raw X-thread JSON/MD used to build posts) and `old/**/*.html`, the last two kept only for identifiers absent from rendered posts. `_site/` skipped (generated duplicate); `_site/` and `old/` contain no PDFs absent from `assets/`.
2. Regex URL extraction per line; context = the source line (or a 200-char window around the URL), whitespace-collapsed, truncated to 200 chars; markdown link text captured as the title.
3. Normalization: arXiv abs/pdf/html (any version) -> arXiv ID without version; `nature.com/articles/<suffix>` -> `10.1038/<suffix>` (lowercased; `_reference`/`MOESM` suffixes stripped); any URL with a literal `10.NNNN/...` DOI (doi.org, dx.doi.org, science.org/doi, pubs.acs.org/doi, Wiley, APS, Springer, IOP, ...) -> DOI (lowercased, trailing `/full`, `/abstract`, `.pdf` etc. stripped); `ieeexplore .../document/N` and `stamp.jsp?arnumber=N` -> ieee_doc N; `opg.optica.org ...?uri=<code>` -> optica_uri; other URLs kept only for an allowlist of publisher/repository domains (id_type url). News sites, company sites, GitHub, YouTube, X, Wikipedia excluded.
4. Dedupe by (id_type, identifier); earliest rendered post kept as `post_file`/`post_date`. The same paper can appear twice as arXiv ID and DOI (no metadata lookup was done to merge them).
5. Topic: first-match keyword rules over the link text(s) of all mentions, in order eo_modulator, passive (MMI/DC/AWG), coupler, packaging/CPO, AMO/quantum, detector, laser/source, passive (rings, filters, switches, ...), platform/material/wafer, systems/interconnect, photonics_unclassified; fallback to the section heading (`topic(heading)`), else other/non-photonics.
6. Access class by DOI prefix or domain: arxiv; optica_oa_journal (10.1364/ oe, optica, osac, optcon, boe, ome, opticaq; same journal codes for optica_uri); nature_comms_or_lsa (10.1038/ s41467, ncomms, s41377, lsa, plus Sci Rep s41598/srep and Commun Phys s42005); ieee (10.1109, ieeexplore); added classes: other_oa_journal (Science Advances, Advanced Photonics / AP Nexus, PRX, PRX Quantum, eLight, OEA, Light Adv Manuf, MDPI, Frontiers, PLOS, eLife, APL Photonics and AIP Advances by URL) and other_oa_repository (theses, DSpace, HAL, OSTI, NTRS, DTIC, PMC, Optica Open, Zenodo, etc.); everything else other_publisher. OL, PRJ, JLT, AO, JOSA, Nature Photonics, Nature, Science, APL, ACS fall in other_publisher or ieee.
7. Atlas dedupe: exact match on DOI / arXiv ID / normalized URL from the atlas `doi`, `arxiv_id`, `url` columns, plus exact normalized-title match (alphanumerics only, >= 25 chars) between blog link text and atlas `title`.
8. Truncation handling: X display URLs ending in an ellipsis were stripped and merged into the full identifier when the same ID occurs elsewhere; short DOI stems (e.g. `10.1063/5.0281`, `10.1038/s41467`, `10.1021/ac`) and stub IEEE URLs are flagged, not dropped.

## Limitations

- Access class is a journal-level heuristic, not per-article license verification. Hybrid journals (Nature Photonics, Science, APL, ACS Photonics, LPR, OL, PRJ) may have OA articles counted as other_publisher. Optica OA journals before their OA start date (if any) are not distinguished.
- Topic tagging is keyword-based and noisy: acoustic/BAW/microwave resonators land in passive, LED/SLM/laser rows in eo_modulator, microwave parametric amplifiers in laser/source. 166 rows were tagged only from a section heading. Treat `topic_guess` as a sort key, not a label.
- Atlas overlap is a lower bound: an arXiv preprint of an atlas DOI (or vice versa) is not detected without a metadata lookup; title matching needs the blog link text to equal the atlas title exactly.
- Rows whose link text is "also", "arxiv", "source" or empty have little classification signal; context column shows the raw line.
- 48 identifiers are flagged as possibly truncated; they need lookup before use. 3 `rdcu.be` and other share links have no DOI in the URL.
- Not every scholarly domain is in the allowlist; links on publisher sites without a DOI in the URL (e.g. pubs.aip.org article paths, sciencedirect pii) are kept as url rows without DOI resolution.
- Local PDF list is curated by hand from filenames plus PDF metadata/page-1 text (PDFKit, offline); topic for local PDFs is a guess. Scripts live in the session scratchpad, not in this repo.
