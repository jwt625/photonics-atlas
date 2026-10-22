---
title: Literature lane L2 (conferences) - venue routes, counts, abstract coverage
date: 2026-10-21
status: S1 harvest complete (2026-10-22 00:15 UTC)
scope: DevLog-006 S1 lane L2
authors: Claude (lane L2 subagent)
---

# Lane L2: conference papers 2016-2025

Config `config/literature/venues_conferences.yaml`; harvesters `scripts/lit_harvest_openalex.py` (journals lane, run
with `--only`) and `scripts/lit_harvest_crossref.py` (this lane). Pool: `cache/literature/pool/conferences_<key>_<year>.jsonl`.
All facts below come from Crossref / OpenAlex responses on 2026-10-21/22 (probe commands in the lane report to the
coordinator). OFC 2026 excluded (local corpus); DOI-year filter drops `ofc.2026.*`.

## Result

49,295 records, 49,294 unique DOIs (1 OFC 2021 paper also dated 2017 by OpenAlex), abstract 98.8 %,
first/last-author affiliation 58.9 % (0 % on Optica 2020-2025 Crossref records: Optica deposits no affiliations),
OA flag 5.2 %. Conference papers are paywalled by default (Optica, IEEE, IET); `is_oa` true only from an OpenAlex OA
location or a Creative Commons license in Crossref.

## Venue routes

| venue | years | route | source id / filter | records | abstract | notes |
|---|---|---|---|---|---|---|
| OFC | 2016-2019 | OpenAlex | S4306420648 | 2,801 | 100 % | Crossref has no Optica abstracts before 2020 |
| OFC | 2020-2025 | Crossref | prefix:10.1364,type:proceedings-article + DOI `^10.1364/ofc.` | 4,022 | 100 % | incl. postdeadline; DOI pattern `10.1364/ofc.<year>.<code>` in all years |
| CLEO | 2016-2019 | OpenAlex | S4306418073 | 8,567 | 99 % | codes cleo_si / cleo_at / cleo_qels |
| CLEO | 2020-2025 | Crossref | same Optica pass, DOI `^10.1364/cleo_(si\|at\|qels\|fs)\.` | 10,677 | 100 % | CLEO 2023+ works have no OpenAlex source |
| ECOC | 2016-2021, 2025 | OpenAlex | S4306418339 | 2,444 | 92 % | 2016 only 32 works; 2019 (IET cp.2019) abstracts 36 % |
| ECOC 2023 | 2023 | Crossref + OpenAlex DOI enrich | container-title:IET Conference Proceedings, pub 2023-11-13, vol 2023 issue 34 | 451 | 100 % | 10 DOIs read icp.2024.* |
| ECOC 2022, 2024 | - | none | - | 0 | - | not found in Crossref (IEEE, IET, Optica prefixes) or OpenAlex sources |
| GFP | 2016-2019, 2021 | OpenAlex | S7407086434 | 469 | 97 % | no 2020 / 2022 container in Crossref |
| IEEE Silicon Photonics Conf. (GFP successor) | 2023-2025 | OpenAlex | S7407089019 | 290 | 97 % | |
| IPC | 2016-2025 | OpenAlex | S4306418808 | 2,965 | 99 % | |
| Advanced Photonics Congress (IPR + NOMA, NP, Networks, SPPCom, ...) | 2016-2019 | OpenAlex | S4306500759 | 1,687 | 99 % | whole congress; IPR = DOI code iprsn |
| same | 2020-2025 | Crossref | Optica pass, container `Advanced Photonics` | 2,199 | 100 % | |
| ACP | 2016-2018 | OpenAlex | S4363608265 | 1,785 | 100 % | 2016-2017 Optica, 2018 IEEE |
| ACP | 2020-2021 | Crossref | Optica pass, DOI `^10.1364/acpc\.` | 1,021 | 100 % | |
| ACP | 2022, 2025 | OpenAlex | S4363608265 | 1,231 | 100 % | |
| ACP | 2023-2024 | Crossref + OpenAlex DOI enrich | IEEE container titles (config) | 1,253 | 100 % | |
| ACP 2019 | - | none | - | 0 | - | not found in Crossref or OpenAlex |
| CLEO-PR | 2017, 2022, 2024 | OpenAlex | S7407089323 | 2,537 | 100 % | 2022 = IEEE 811 + Optica 654 (Crossref containers); likely title duplicates, dedupe in S2 |
| CLEO-PR | 2018, 2020 | Crossref (+ enrich 2018) | Optica pass, container `Pacific Rim\|CLEO PR` | 1,224 | 100 % | |
| IEDM | 2016-2025 | OpenAlex | S4210168112 | 2,431 | 99 % | whole program, prefilter selects photonics |
| VLSI Symposium | 2016-2024 | OpenAlex | S4306421008\|S7407086820\|S4363605407 | 1,241 | 97 % | 2025 not in these sources |
| ECIO | - | dropped | - | 0 | - | no Crossref container, no OpenAlex source |
| ECTC | - | not harvested | - | - | - | packaging atlas covers it |

Cost: Crossref free (474 Crossref requests logged 2026-10-21/22, all agents; most from this lane). OpenAlex for this lane (from `logs/litfetch_*.jsonl`): 2026-10-21 176 requests
$0.029 (incl. 11 source searches $0.011), 2026-10-22 105 requests $0.011; ~179 list pages + ~30 DOI-batch enrich pages.

## Venue-year table

| unit key | year | records | abstract % | affiliation % | OA % | route | venue string (most common) |
|---|---|---|---|---|---|---|---|
| acp | 2016 | 575 | 100 | 97 | 5 | openalex | Asia Communications and Photonics Conference |
| acp | 2017 | 615 | 100 | 95 | 5 | openalex | Asia Communications and Photonics Conference |
| acp | 2018 | 595 | 100 | 98 | 3 | openalex | Asia Communications and Photonics Conference |
| acp_cr | 2020 | 524 | 100 | 0 | 0 | crossref | Asia Communications and Photonics Conference/International Conference  |
| acp_cr | 2021 | 497 | 100 | 0 | 0 | crossref | Asia Communications and Photonics Conference 2021 |
| acp_ieee | 2022 | 562 | 100 | 98 | 3 | openalex | Asia Communications and Photonics Conference |
| acp_ieee | 2025 | 669 | 100 | 95 | 1 | openalex | Asia Communications and Photonics Conference |
| acp_ieee_cr | 2023 | 616 | 100 | 100 | 2 | crossref | 2023 Asia Communications and Photonics Conference/2023 International P |
| acp_ieee_cr | 2024 | 637 | 100 | 100 | 2 | crossref | 2024 Asia Communications and Photonics Conference (ACP) and Internatio |
| apc | 2016 | 384 | 98 | 94 | 7 | openalex | OSA Advanced Photonics Congress |
| apc | 2017 | 329 | 97 | 94 | 9 | openalex | OSA Advanced Photonics Congress |
| apc | 2018 | 806 | 99 | 96 | 12 | openalex | OSA Advanced Photonics Congress |
| apc | 2019 | 168 | 100 | 99 | 9 | openalex | OSA Advanced Photonics Congress |
| apc_cr | 2020 | 465 | 100 | 0 | 0 | crossref | OSA Advanced Photonics Congress (AP) 2020 (IPR, NP, NOMA, Networks, PV |
| apc_cr | 2021 | 261 | 100 | 0 | 0 | crossref | OSA Advanced Photonics Congress 2021 |
| apc_cr | 2022 | 693 | 100 | 0 | 0 | crossref | Optica Advanced Photonics Congress 2022 |
| apc_cr | 2023 | 155 | 100 | 0 | 0 | crossref | Advanced Photonics Congress 2023 |
| apc_cr | 2024 | 361 | 100 | 0 | 0 | crossref | Advanced Photonics Congress 2024 |
| apc_cr | 2025 | 264 | 100 | 0 | 0 | crossref | Advanced Photonics Congress (IPR, Networks, NOMA, SOLITH, SPPCom) |
| cleo | 2016 | 2108 | 100 | 98 | 9 | openalex | Conference on Lasers and Electro-Optics |
| cleo | 2017 | 1736 | 100 | 97 | 8 | openalex | Conference on Lasers and Electro-Optics |
| cleo | 2018 | 2011 | 100 | 97 | 10 | openalex | Conference on Lasers and Electro-Optics |
| cleo | 2019 | 2712 | 94 | 93 | 5 | openalex | Conference on Lasers and Electro-Optics |
| cleo_cr | 2020 | 1844 | 100 | 0 | 0 | crossref | Conference on Lasers and Electro-Optics |
| cleo_cr | 2021 | 1770 | 100 | 0 | 0 | crossref | Conference on Lasers and Electro-Optics |
| cleo_cr | 2022 | 1899 | 100 | 0 | 0 | crossref | Conference on Lasers and Electro-Optics |
| cleo_cr | 2023 | 1704 | 100 | 0 | 0 | crossref | CLEO 2023 |
| cleo_cr | 2024 | 1907 | 100 | 0 | 0 | crossref | CLEO 2024 |
| cleo_cr | 2025 | 1553 | 100 | 0 | 0 | crossref | CLEO 2025 |
| cleopr | 2017 | 525 | 100 | 99 | 5 | openalex | Conference on Lasers and Electro-Optics Pacific Rim (CLEO-PR) |
| cleopr | 2022 | 1465 | 100 | 99 | 2 | openalex | Conference on Lasers and Electro-Optics Pacific Rim (CLEO-PR) |
| cleopr | 2024 | 547 | 99 | 97 | 1 | openalex | Conference on Lasers and Electro-Optics Pacific Rim (CLEO-PR) |
| cleopr_cr | 2018 | 737 | 100 | 98 | 5 | crossref | CLEO Pacific Rim Conference |
| cleopr_cr | 2019 | 0 |  |  |  |  |  |
| cleopr_cr | 2020 | 487 | 100 | 0 | 0 | crossref | 14th Pacific Rim Conference on Lasers and Electro-Optics (CLEO PR 2020 |
| ecoc | 2016 | 32 | 41 | 78 | 0 | openalex | European Conference on Optical Communication |
| ecoc | 2017 | 420 | 100 | 91 | 20 | openalex | European Conference on Optical Communication |
| ecoc | 2018 | 475 | 100 | 92 | 21 | openalex | European Conference on Optical Communication |
| ecoc | 2019 | 403 | 36 | 25 | 18 | openalex | European Conference on Optical Communication |
| ecoc | 2020 | 303 | 99 | 87 | 18 | openalex | European Conference on Optical Communication |
| ecoc | 2021 | 278 | 100 | 88 | 19 | openalex | European Conference on Optical Communication |
| ecoc | 2025 | 533 | 100 | 90 | 15 | openalex | European Conference on Optical Communication |
| ecoc_iet2023 | 2023 | 451 | 100 | 100 | 20 | crossref | IET Conference Proceedings |
| gfp | 2016 | 91 | 97 | 93 | 11 | openalex | IEEE International Conference on Group IV Photonics (GFP) |
| gfp | 2017 | 90 | 98 | 96 | 12 | openalex | IEEE International Conference on Group IV Photonics (GFP) |
| gfp | 2018 | 61 | 98 | 97 | 7 | openalex | IEEE International Conference on Group IV Photonics (GFP) |
| gfp | 2019 | 134 | 96 | 91 | 8 | openalex | IEEE International Conference on Group IV Photonics (GFP) |
| gfp | 2021 | 93 | 96 | 90 | 17 | openalex | IEEE International Conference on Group IV Photonics (GFP) |
| iedm | 2016 | 235 | 99 | 93 | 7 | openalex | Technical digest - International Electron Devices Meeting/Technical di |
| iedm | 2017 | 228 | 99 | 94 | 9 | openalex | Technical digest - International Electron Devices Meeting/Technical di |
| iedm | 2018 | 235 | 99 | 95 | 11 | openalex | Technical digest - International Electron Devices Meeting/Technical di |
| iedm | 2019 | 243 | 99 | 97 | 13 | openalex | Technical digest - International Electron Devices Meeting/Technical di |
| iedm | 2020 | 232 | 100 | 96 | 6 | openalex | Technical digest - International Electron Devices Meeting/Technical di |
| iedm | 2021 | 223 | 99 | 93 | 9 | openalex | Technical digest - International Electron Devices Meeting/Technical di |
| iedm | 2022 | 229 | 100 | 93 | 11 | openalex | Technical digest - International Electron Devices Meeting/Technical di |
| iedm | 2023 | 231 | 100 | 97 | 3 | openalex | Technical digest - International Electron Devices Meeting/Technical di |
| iedm | 2024 | 277 | 100 | 94 | 4 | openalex | Technical digest - International Electron Devices Meeting/Technical di |
| iedm | 2025 | 298 | 100 | 95 | 3 | openalex | Technical digest - International Electron Devices Meeting/Technical di |
| ipc | 2016 | 369 | 99 | 96 | 6 | openalex | IEEE Photonics Conference |
| ipc | 2017 | 303 | 98 | 95 | 16 | openalex | IEEE Photonics Conference |
| ipc | 2018 | 253 | 97 | 92 | 12 | openalex | IEEE Photonics Conference |
| ipc | 2019 | 204 | 100 | 96 | 8 | openalex | IEEE Photonics Conference |
| ipc | 2020 | 340 | 99 | 96 | 10 | openalex | IEEE Photonics Conference |
| ipc | 2021 | 254 | 98 | 96 | 11 | openalex | IEEE Photonics Conference |
| ipc | 2022 | 297 | 100 | 97 | 11 | openalex | IEEE Photonics Conference |
| ipc | 2023 | 295 | 99 | 97 | 11 | openalex | IEEE Photonics Conference |
| ipc | 2024 | 305 | 99 | 96 | 18 | openalex | IEEE Photonics Conference |
| ipc | 2025 | 345 | 99 | 95 | 9 | openalex | IEEE Photonics Conference |
| ofc | 2016 | 679 | 100 | 92 | 11 | openalex | Optical Fiber Communication Conference |
| ofc | 2017 | 739 | 100 | 90 | 13 | openalex | Optical Fiber Communication Conference |
| ofc | 2018 | 735 | 100 | 82 | 13 | openalex | Optical Fiber Communication Conference |
| ofc | 2019 | 648 | 100 | 82 | 11 | openalex | Optical Fiber Communication Conference |
| ofc_cr | 2020 | 666 | 100 | 0 | 0 | crossref | Optical Fiber Communication Conference (OFC) 2020 |
| ofc_cr | 2021 | 624 | 100 | 0 | 0 | crossref | Optical Fiber Communication Conference (OFC) 2021 |
| ofc_cr | 2022 | 531 | 100 | 0 | 0 | crossref | Optical Fiber Communication Conference (OFC) 2022 |
| ofc_cr | 2023 | 651 | 100 | 0 | 0 | crossref | Optical Fiber Communication Conference (OFC) 2023 |
| ofc_cr | 2024 | 765 | 100 | 0 | 0 | crossref | Optical Fiber Communication Conference (OFC) 2024 |
| ofc_cr | 2025 | 785 | 100 | 0 | 0 | crossref | Optical Fiber Communication Conference (OFC) 2025 |
| siphotonics | 2023 | 77 | 96 | 84 | 13 | openalex | IEEE Silicon Photonics Conference (SiPhotonics) |
| siphotonics | 2024 | 129 | 99 | 96 | 10 | openalex | IEEE Silicon Photonics Conference (SiPhotonics) |
| siphotonics | 2025 | 84 | 96 | 95 | 10 | openalex | IEEE Silicon Photonics Conference (SiPhotonics) |
| vlsi | 2016 | 98 | 98 | 93 | 4 | openalex | IEEE Symposium on VLSI Technology |
| vlsi | 2017 | 94 | 90 | 86 | 3 | openalex | Symposium on VLSI Technology |
| vlsi | 2018 | 90 | 99 | 92 | 2 | openalex | IEEE Symposium on VLSI Technology |
| vlsi | 2019 | 100 | 91 | 87 | 11 | openalex | Symposium on VLSI Technology |
| vlsi | 2020 | 104 | 98 | 78 | 7 | openalex | IEEE Symposium on VLSI Technology |
| vlsi | 2021 | 53 | 100 | 94 | 0 | openalex | Symposium on VLSI Technology |
| vlsi | 2022 | 214 | 99 | 97 | 6 | openalex | IEEE Symposium on VLSI Technology and Circuits (VLSI Technology and Ci |
| vlsi | 2023 | 239 | 97 | 93 | 9 | openalex | IEEE Symposium on VLSI Technology and Circuits (VLSI Technology and Ci |
| vlsi | 2024 | 249 | 100 | 95 | 2 | openalex | IEEE Symposium on VLSI Technology and Circuits (VLSI Technology and Ci |

Crossref cross-check (rows=0 / facet counts, 2026-10-21): Optica proceedings per publication year 2016-2025 = 8211,
6164, 7399, 5450, 6403, 6134, 6798, 5113, 5538, 4906 (abstracts 0-146 per year 2016-2019, >= 95 % 2020-2025);
OpenAlex OFC 2016-2019 (679-739/yr) matches Crossref OFC + postdeadline containers within 1 %.

## Not harvested, candidates (outside the lane's venue list)

Optica: Photonics in Switching and Computing 2021 (64, Crossref), Frontiers in Optics (~450-950/yr), OECC 2021
(371). IEEE: CLEO/Europe-EQEC (OpenAlex S7407086093 / S4363607729), OECC/PGC. All visible in the same Crossref
Optica pass or as OpenAlex sources.

## Known gaps / follow-ups

- Optica 2020-2025 Crossref records have no affiliations (18,419 records; 20,268 pool records in total lack one). Fill after the S2 prefilter by OpenAlex
  DOI-batch lists (100 DOIs per $0.0001) or free singleton gets, not for the whole pool.
- Crossref abstracts lose superscripts at source (e.g. "8 x 104" for 8e4 in Optica deposits); the harvester joins
  inline tags (Si<sub>3</sub>N<sub>4</sub> -> Si3N4) and writes <sup> as ^ where present.
- OpenAlex returned HTTP 200 with truncated JSON twice on 2026-10-22 00:01-00:03 UTC; lit_harvest_crossref.py retries
  (3 attempts); lit_harvest_openalex.py crashed and was resumed by rerun (no data loss: units are atomic).
