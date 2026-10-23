---
title: Fresh-context audit of the lit author-affiliation batches (pilot + lit_h01..lit_h04, D350-D369) before the people merge
date: 2026-10-23
auditor: Claude (fresh context, read-only except this file)
scope: DevLog-011 (D350-D369, totals, merge proposal), both header contracts, scripts/ofc_headers.py (show / check, lit corpus), data/_staging/people/lit_headers/ (all batches, org_requests.csv)
verdict: GO for the people merge (0 wrong slots in 342 sampled); 2 imprecise slots and 1 latent matcher loophole to fix, none blocking
---

# Lit header batches audit (2026-10-23)

## Method

- Sample: 39 papers / 342 author-list slots / 393 header rows, stratified over all five batches and every basis:
  - the 11 papers re-extracted in the D366-D369 cleanup (elsaeed2024, qi2024, sheng2012, shamsansari2022, mu2026,
    jahed2022, liang2025, koninck2025, maeda2023, mangal2020, wang2026);
  - every paper with prose / clause / grouped / per_author / continued / skip_prefix blocks (all 21 prose papers, all
    201 prose rows, all 29 grouped and 5 per_author rows);
  - every `slot: 0` / `author_list_differs` paper (garciablanco2025, koninck2025, liang2025, liu2022, meng2023,
    song2008, wang2026, wilson2019);
  - every present address (10 rows: kim2019, koninck2025, kuznetsov2025, shen2019);
  - the other explicit `slot:` overrides (tao2024, zhang2023a; song2021 and garciablanco2025 already in);
  - 4 random ok papers (seed 20261023): nevlacsil2020, ni2025a, lu2024, zhang2013a.
- Per slot: printed text (`show --corpus lit`, page separators, `--pdf` where markers could be lost) vs `headers.yaml`,
  `header_rows.csv` and `compare.csv`: slot assignment (D359 position, D369 initials rule, common-family tie-break),
  markers / dropped_markers, block mapping, org / unit / city / country, basis, grade, role.
- Whole staging tree: scan of every file under `data/_staging/people/lit_headers/` for contacts, URLs, postal codes,
  street / building terms and quoted text; address-word scan of every derived row; mapped-org country cross-check
  against `data/registry/organizations.csv`; family-name and swapped-order scan of all 973 recorded slot matches;
  probe of `strict_compatible`.

## Commands run (2026-10-23 11:11-11:13 log time)

| Command | Result |
|---|---|
| `uv run python scripts/ofc_headers.py check all --corpus lit` | 0 errors, 8 warnings (5 printed-order notices, 3 explicit `slot:` overrides); totals equal DevLog-011 Totals exactly |
| `uv run python scripts/ofc_headers.py check all` (OFC) | 0 errors, 48 warnings (unchanged) |
| `uv run pytest -q tests/test_lit_headers.py tests/test_ofc_headers.py` | 111 passed (7 third-party SWIG deprecation warnings) |
| hash snapshot of every file under `lit_headers/` and `ofc_headers/` before and after the two checks | 126 / 126 byte-identical (the checks rewrite the derived files; content unchanged, mtimes updated) |
| `git status` (read-only) | OFC staging files unmodified in git, so the current code reproduces the committed OFC derived files |

DevLog-011 Totals re-derived and confirmed: 116 papers (ok 115, unreadable 1: ma2026, no affiliation printed in text
or PDF, confirmed); 985 slots (973 recorded, 12 without rows, the 12 listed are exactly the `no_header` rows);
1312 rows all grade A (printed 1001, prose 201, single 76, grouped 29, per_author 5); 10 present addresses; 175
multi-affiliation slots; 5 order-differs papers; 5 header-only authors; 75 org-request strings (81 per-batch
unmapped strings before de-duplication).

## Counts (sample)

| batch | papers | slots | rows | ok | imprecise | wrong | of which correctly without rows |
|---|---|---|---|---|---|---|---|
| pilot | 3 | 25 | 28 | 25 | 0 | 0 | 0 |
| lit_h01 | 8 | 65 | 76 | 65 | 0 | 0 | 1 (garciablanco2025 #7) |
| lit_h02 | 14 | 130 | 151 | 129 | 1 | 0 | 3 (koninck2025 #7, liang2025 #6, liu2022 #4) |
| lit_h03 | 9 | 77 | 91 | 77 | 0 | 0 | 1 (song2008 #5) |
| lit_h04 | 5 | 45 | 47 | 45 | 0 | 0 | 4 (wang2026 #6 #9, wilson2019 #5 #6) |
| total | 39 | 342 | 393 | 341 | 1 | 0 | 9 |

Outside the sample, the full-tree scan found 1 more imprecise slot (sulway2023 #1, lit_h03), so the corpus-level
known non-ok total is 2 imprecise, 0 wrong.

Slots without rows were checked one by one: list authors not printed in the cached (preprint) header (koninck2025
Cenk Ibrahim Ozdemir: only in the reference list; liu2022 Anton Lukashchuk; wilson2019 Yannick Baumgartner and
Lukas Czornomaz; garciablanco2025 Marco Romanelli) and the D369 non-matches (below). All correct.

## Non-ok slots

| # | slot | rating | evidence | fix |
|---|---|---|---|---|
| 1 | lit:nakamura2020 #4 (Ken Tanizawa), P3 | imprecise | The statement prints AIST, then the Quantum ICT Research Institute, then Tamagawa University, then one place (Tokyo). Recorded `org: AIST`, `more_orgs: ["Tamagawa University"]`, `locality: Tokyo`: the AIST row takes the city printed for Tamagawa University (the postal district printed is Tamagawa's) and the Quantum ICT Research Institute unit is dropped, although D367 now allows a structured `more_orgs` entry with its own unit and place | Re-record as `org: "National Institute of Advanced Industrial Science and Technology (AIST)"`, `locality: ""`, `country: "JP"` and `more_orgs: [{org: "Tamagawa University", unit: "Quantum ICT Research Institute", locality: "Tokyo", country: "JP"}]` (needs the checker to accept the AIST field without a place; otherwise keep and add a note). Org ids unchanged |
| 2 | lit:sulway2023 #1 (Dominic A. Sulway), block 1 (outside the sample, found by the full scan) | imprecise | `unit` = "Quantum Engineering Centre for Doctoral Training, Nanoscience and Quantum Information Building": a building name (address component) copied into the unit field and into `header_rows.csv`; the restricted-text rule allows org / unit / city / country only, and jahed2022 treats a building complex the opposite way (`skip_prefix`, not recorded) | Record `unit: "Quantum Engineering Centre for Doctoral Training"`; the checker needs a printed-block analogue of `skip_prefix` (a verified, unrecorded span between unit and org), or an owner ruling that building names are acceptable in units |

No wrong slot (wrong org, wrong author, wrong marker, wrong role, wrong country) was found.

## Checked and correct (highlights)

- D369 initials rule: song2008 M. B. Yu vs Ming Yu, liang2025 Siyuan Yu vs S. F. Yu, wang2026 Hao Deng vs H T Deng
  and Junpeng Lu vs J. Y. Lu are `slot: 0` + `author_list_differs`; the checker's D302 test passes (no compatible
  unmatched slot). Each list author sits at the same position as the printed one, so these are probable metadata
  variants, but the rule is applied as written and no affiliation is attached on name evidence that does not hold.
  The 3 matches that rely on the letter-order rule are all legitimate (song2008 S. H. Tao ~ Shaohua, D. L. Kwong ~
  Dim-Lee; garciablanco2025 S. M. Garcia-Blanco, explicit distinctive-family override, D369).
- Common-family tie-break: common family names with an unexplained initial go to `slot: 0` (Yu, Deng, Lu); the
  distinctive ones take an explicit `slot:` (Garcia-Blanco, Osornio-Martinez). Consistent in the sample.
- Prose: every statement on the searched pages is recorded (D361 coverage holds in all 21 papers); clause blocks
  (qi2024, maeda2023, mangal2020, wang2026) carry the right subjects; the period after a name in elsaeed2024
  statement 2 is not a boundary (all 17 names carry P2); "was with" / "were with" = affiliation and "They / He ...
  now with" = present address (kim2019, jayatilleka2021); the jayatilleka2021 continuation (Corporation ... Santa
  Clara) is at a line start in the other column; jahed2022 `skip_prefix` verified and not in any derived row.
- grouped / per_author: mu2026 (6 groups incl. the two-org first author), shamsansari2022 (4 groups, Jankowski with
  two blocks, HyperLight with no printed country -> ""), liang2025 (6 per-author blocks) all match the printed
  layout.
- Present addresses (10): koninck2025 a-d (letter glued to the cue), kuznetsov2025 4, shen2019 6 (Currently with),
  kim2019 P3 / P6: role and carriers correct.
- dropped_markers: equal contribution (kuznetsov2025 5) and contact lines (zhang2023a 3-6, ni2025a 3-4) correct.
- Places: prefecture-only blocks get `locality: ""` (nakamura2020 Kanagawa / Ibaraki); printed `-shi` localities kept
  (maeda2023); HK for City University of Hong Kong; AE for UAE; campus orgs (song2021 UCSB, kim2019 Berkeley) map
  to the campus ids.
- Mapped-org countries: every mapped row's country equals the registry org country except 4 rows of multinationals
  at a foreign site (NVIDIA Roskilde, Microsoft Cambridge GB, Ciena Ottawa, STMicroelectronics Crolles): correct.
- Contacts / addresses / quotes: no e-mail, URL, ORCID, phone, postal code or street term in any file under
  `lit_headers/` (the only hits are the YAML header comments, the contract, the jahed2022 `skip_prefix` building
  name, the sulway2023 unit above, and the family name Van Gasse); notes are short factual phrases, no quoted
  sentences.

## Systematic issues

1. Latent loophole in `strict_compatible` (D369), not triggered by current data: an extra initial is accepted when
   its letter occurs anywhere later in the joined given name, not only at a syllable / hyphen boundary. Probes:
   "M. G. Li" ~ "Ming Li" -> True (D369 says "M. B." !~ "Ming"; G is accepted only because Ming contains g),
   "S. A. Yu" ~ "Siyuan Yu" -> True, "S. U. Yu" ~ "Siyuan Yu" -> True, "J. N. Smith" ~ "Johann Smith" -> True.
   Fix before `lit_h05`: an extra initial must start a pinyin syllable of the given name (or follow a hyphen / case
   boundary in the printed form), plus tests for these probes. Current batches: 0 affected slots (only 3 matches
   use the rule, all legitimate).
2. Swapped name order (5 slots, all recorded correctly): qi2024 #1 (list Xu Qi, printed Qi Xu), ni2025a #2 (Han Chen /
   CHEN HAN), nie2024 #11 (Li Mi / MI LI), tao2024 #4 (Yang Yu / YU YANG, explicit slot), zhang2023a #7 (Bo Fang /
   FANG BO, explicit slot). The affiliation rows are right, but the slot name comes from the author list (D359), whose
   given / family order is probably inverted in these 5 cases, so the family-name keys used by D63 / D219d are likely
   wrong for them. Merge caveat: flag these slots (`name_order_swapped`) and keep them out of new common-family
   rule-3 joins until reviewed. The matcher auto-accepts some swaps (qi2024, ni2025a, nie2024) but needs an explicit
   slot for others (tao2024, zhang2023a); harmless, but inconsistent.
3. Joint "Ghent University-imec" (and "Ghent University-Interuniversity Microelectronics Center") is recorded two
   ways: as one org string (koninck2025, keyvaninia2013, vaskasi2022, zhang2023; the matcher maps it to both orgs) or
   split into `org` + `more_orgs` (bogaerts2006, deng2026, deng2026a, elsaeed2024). The org ids are the same either
   way; cosmetic, no fix needed for the merge.
4. Address components inside fields: one building name in a unit (sulway2023, non-ok #2) vs `skip_prefix` for prose
   only (jahed2022). `skip_prefix` itself stores a building name in `headers.yaml` (staging only, never derived),
   as D366 allows; acceptable, but a printed-block equivalent is missing.
5. Printed line-split units are kept as printed: wang2026 P9 unit "Devices of Ministry of Education" is a fragment of
   the key-laboratory name split across two clauses (the paper note says so). It follows the as-printed rule; the
   people view will show a fragment-like unit (Southeast University, org ids right).
6. Printed names in capitals ("BIN SHEN", "S. M. GARCÍA-BLANCO") will go to `person_aliases` as `printed_variant`
   under merge item 3a; consider skipping variants that differ only in case or accents to avoid alias noise.

## Merge proposal review (DevLog-011 merge path)

- Items 1-8 match the people rules: slots = author-list positions (D359), header names only to `printed_name` /
  `person_aliases` (D217 / D218 analogue), D219e observation ids, header-only authors not merged, duplicate-paper
  check, grade A for all 1312 rows, preprint attribution.
- Wording: item 1 writes the slot as `lit:<paper_id>#a<i>`; the other corpora use `<source_id>#<i>` for the slot and
  `#a<i>.h...` only in observation ids (D219e). The uncommitted `people.py` in the working tree (a parallel people
  stream, D370-D372, not audited here) already uses `#<i>`. Align the DevLog wording.
- Add to the merge: the 5 swapped-order slots flag (issue 2). The 9 sampled (12 total) slots without rows stay
  without observations, as proposed.
- `strict_compatible` imports `photonics_atlas.people.parse`; people.py is being edited in parallel, so re-run
  `check all --corpus lit` after the people changes land, to confirm the slot assignments stay the same.

## Verdict

GO for the people merge. 342 / 342 sampled slots have the right slot and organization; 341 ok, 1 imprecise
(nakamura2020 #4 locality / dropped unit), 0 wrong; plus 1 imprecise slot from the full scan (sulway2023 #1,
building name in the unit). Neither changes an org id. Recommended before or with the merge: fix both imprecise slots,
flag the 5 swapped-order slots, and fix the `strict_compatible` loophole (with tests) before the next lit batch.
