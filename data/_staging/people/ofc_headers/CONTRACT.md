# OFC 2026 header extraction batch contract (DevLog-008, 2026-10-22; D240-D249, D282-D285 and D286-D288 applied 2026-10-22; D300-D305 2026-10-23)

You extract the author / affiliation header of OFC 2026 papers into one `headers.yaml` per batch. Work from the repo
root. No emoji. Never invent: what the text does not show is not entered. No git. No network requests of any kind.

## Read first

1. `DevLog/DevLog-008-ofc-header-extraction.md` (decisions D170-D179, coordinator rulings D240-D245, audit fixes D246-D249, batch-1 fixes D282-D285, cleanup D286-D288, batch audit D300-D305).
2. `data/_staging/people/ofc_headers/pilot/headers.yaml` (worked examples: lost markers, PDF-read markers, joint
   blocks, present addresses, a header author missing from the metadata, single-block papers, 50-author papers).

## Your batch

The task message names `data/_staging/people/ofc_headers/<batch>/`; `papers.csv` lists its papers. Print each paper's
header and the metadata author slots with

    uv run python scripts/ofc_headers.py show <batch>            # all papers of the batch
    uv run python scripts/ofc_headers.py show <batch> --codes Th3F.1 --pdf   # one paper, with the local PDF page 1

Contacts are masked in this output. Use `--pdf` whenever `local_pdf` is true and the text lost markers or looks
garbled; the PDF view marks superscripts as `^{...}`. Do not open the source files in other ways. Restricted corpus
(D244): copy only names and the organization / unit / city / country of each block; never a street address, postal
code, block or building number, title, abstract or any other text.

## headers.yaml (one list item per paper, in `papers.csv` order)

```yaml
- source_id: ofc2026:<code>
  status: ok                 # ok (every author readable) | partial (>= 1 author unreadable: true) | unreadable
  note: ""                   # required for unreadable / author_list_differs; short, factual
  author_list_differs: false # true when header and metadata author lists differ (explain in note)
  affiliations:              # one item per printed affiliation block, in printed order
    - marker: "1"            # printed symbol without superscript markup or parentheses: "1", "a", "†"; "" for a single unmarked block
      basis: printed         # printed | single | listing_order | pdf | layout   (D173)
      role: affiliation      # affiliation (default) | present_address ("Now with", "now at", "Present address")
      org: "<organization name as printed>"
      more_orgs: []          # further organizations printed in the same block ("University X and CNIT")
      # org_from_prefix: true  # org printed once before several marked blocks ("Org: 1 City, 2 City"), D283
      # marker_trailing: true  # the block's marker is printed after it ("Org, City, Country (1)"), D286e
      # campus: "Shenzhen"     # printed place that with the org names a distinct campus / institution, D301
      unit: "<department / lab as printed>"
      locality: "<city as printed, nothing else: no region, no postal code>"
      country: "JP"          # quoted ISO 3166-1 alpha-2 code of the place printed in this block; "" when none is printed
  authors:                   # in header order
    - name: "<name as printed, no markers, no asterisks>"
      markers: ["1", "2"]    # affiliation markers in printed order; [] when the paper has one unmarked block
      # dropped_markers: [{marker: "3", reason: "equal contribution"}]  # printed, not an affiliation (D286d)
      # slot: N              # only when the script cannot match the metadata slot; slot: 0 = not in the metadata
      # unreadable: true     # this author's markers cannot be read (paper status partial); no rows are derived;
      #                      # the name is not checked against the text, but the slot must still resolve (D284)
```

Rules:

- Names and fields must be copied as printed. The checker (D246) compares against the header text or the local PDF
  after removing markup, accents, case and punctuation: each author name must be printed directly followed by exactly
  the recorded markers; each block must be found after the author line, in printed order, starting with its unit or
  org (preceded by its marker for `printed` blocks, and on the PDF for `pdf` blocks); org, unit, city and more_orgs
  must lie inside that block (up to the next block); unit and org must be one contiguous printed segment (copy the
  whole sub-unit chain, e.g. "State Key Laboratory X, Department Y"); a present-address cue ("Now with", "now at",
  "Present address", "currently with") must be in the block exactly when `role: present_address`; the country must
  be printed in the block. Keep parenthesized acronyms as printed ("Institute of Microelectronics (IME)"). A parent named after the
  institute in the same block (", A*STAR") is not copied unless it is part of the institute's printed name
  ("Institute of Semiconductors, Chinese Academy of Sciences").
- No street address, postal code, block / building / room number in any field or note: the checker rejects postal-code
  and street patterns in every YAML / CSV file of the batch and in every field (D244).
- Country (D249, D288): the ISO 3166-1 alpha-2 code of the place printed in that block, quoted ("NO" for Norway;
  all 249 codes are known to the checker). Hong Kong, Macau and Taiwan get HK, MO, TW when the block prints them as
  the place (also "Hong Kong SAR, China" -> "HK"); "Hong Kong" inside an organization name is not the place
  ("HKUST (Guangzhou), Guangzhou, PR China" -> "CN"). No inference: a block that prints no country gets "" even when
  the city or org makes it obvious; a code whose name is not printed is an error.
- Locality (D288): the first printed city only; a block that prints only a province / prefecture / state gets
  `locality: ""`; a block that prints two places gets strictly the first printed one ("Theale" when Theale is
  printed first) and the other place goes to the note.
- Campus (D301): when the place printed right after a multi-campus or homonym organization names a distinct
  institution or campus ("the Chinese University of Hong Kong, Shenzhen", "University of California, ... Davis",
  "Indian Institute of Technology, Delhi", "University of Maryland, College Park"), record `org` as printed without
  the place and the place in `campus` (and the city in `locality` as usual). The row's org name becomes "org,
  campus", and org matching never falls back to the parent or homonym org (an unmapped row is correct until the
  registry has the campus). A campus printed in parentheses ("HKUST (Guangzhou)") stays inside `org`; the matcher
  never drops a parenthesized place.
- Leading articles (D288) are copied as printed ("the Zhejiang Lab"); org matching normalizes them. A department
  printed between a joint institute and a second organization is dropped (note it).
- Markers (D286d): the markers recorded for an author plus the author's `dropped_markers` must be exactly the printed
  run of markers after the name. Numeric or letter markers that point to a non-affiliation footnote (equal
  contribution, corresponding author, "no longer affiliated") go to `dropped_markers` with the reason. Symbol marks
  (`*`, dagger, pilcrow, section) that no block uses are ignored and need no entry. Lookalikes are not folded: an "l"
  or a stray digit printed where a marker should be is not marker 1; such authors are `unreadable` (paper `partial`).
- Trailing markers (D286e): blocks printed as "Org, City, Country (1)" are `printed` with `marker_trailing: true`;
  the checker requires the marker right after the block's last field.
- Mixed layout (D286f): one unmarked block next to marked blocks (authors without a marker belong to it) is recorded
  with `marker: ""`, `basis: layout` and a paper note (grade B); the marked blocks keep their own basis.
- Blocks without markers (`listing_order`, `layout`, `single`) are located by their unit first (the org may be
  printed directly before it), as whole words, each after the previous block's last field (D286c): so record the unit
  exactly as printed, especially when several blocks share one org.
- Non-affiliation footnotes (D249) are not blocks: "no longer affiliated with ...", deceased, visiting, on leave,
  retired. Drop their marker from the author and mention it in the paper note; the checker rejects such wording in
  org / unit fields.
- Two printed organizations in one block ("University X and CNIT", "Institute X, State Key Laboratory Y" when the
  laboratory is not a department of the institute) go to `org` + `more_orgs`, not `unit`. French joint research
  units (UMR, e.g. IRISA, Institut FOTON) are treated like state key laboratories (D285): `more_orgs` when printed as
  a separate organization, `unit` only when printed as a sub-unit of the org. A block that prints two places: record
  the first place as `locality` and mention the second in the note.
- Shared organization prefix (D283): when the org is printed once and followed by marked blocks that print only a
  place or unit ("U.S. Geological Survey: 1 Vancouver, WA, 2 Golden, CO"), give each of those blocks the org with
  `org_from_prefix: true` and its own `locality` / `unit`. The checker requires the org to be printed directly before
  the first block of the run.
- Single block (D285): a single block printed with a marker ("1" on the block and on the authors) is `printed` with
  that marker and the authors carry `["1"]`; an unmarked single block is `single` (authors `[]`, a `1` printed only on
  the authors is dropped).
- Text-extraction artefacts (D282): write names with the intended letters ("Luís" for an extracted "Lu´ıs");
  the checker folds dotless i and detached accents.
- Markers that are not affiliations are not recorded: corresponding author (`*`), equal contribution (`†`, `¶`,
  `#` when the footnote says so), contact markers. A marker that points to a present address IS an affiliation marker
  (`role: present_address`).
- `basis` (D173; grades D240): `printed` = block marker visible in the text; `single` = one block, no markers needed (authors carry
  `markers: []`; a printed `1` on every author with an unmarked block is dropped); `pdf` = marker read in the local PDF
  because the text lost it; `listing_order` = text lost the block markers, no local PDF, blocks are listed 1..N in
  order and N equals the largest author marker (these rows get grade B, "affiliation marker inferred from block
  order"; all other bases grade A); `layout` = no markers, grouping read from the printed layout (requires a paper
  note describing the layout; grade B, D246).
  Prefer `pdf` over `listing_order` whenever a local PDF exists. If none of these applies, the paper is `unreadable` or the authors concerned are `unreadable`.
- `status: unreadable` when the author line or the blocks are garbled, truncated or missing, or the blocks are printed
  after the abstract in the extraction (the checker searches only the header): no affiliations, no authors, a note
  saying what is wrong. Never guess. `status: partial` (D249) when only some authors' markers cannot be read: those
  authors carry `unreadable: true` (no rows); `ok` papers have no unreadable author.
- Author to metadata slot (D247): the checker matches by name only (exact name first, then compatible forms: initials,
  family-name initial first, dropped middle or second family name); different full given names never match ("Yi" vs
  "Yu"), and nothing is matched by position. When a name matches 0 or several metadata slots, set `slot: N` after
  checking the `show` metadata list, or `slot: 0` (not in the metadata, with `author_list_differs`).
- `slot: N` is allowed only (D287) for plain misspellings or transliteration variants (Naoto / Nato, Kyosuke /
  Kyousuke), name-part variants (Seyed Morteza / Morteza, Muhammad Rosdi B. Abu Hassan / Rosdi Hassan), nicknames or
  alternate names whose initials agree, plus the listed cases (Avi / Avraham, Drew / Andrew, Doutje / Dora, Chun-Kit
  / Calvin C. K., D. Pavitra Varsha / Pavitra Diddi), or a printed parenthetical name (Ming (Richard)). A different
  name or a differing first initial (Qing / Wing, R. M. / Mark, J. I. / Iwan, Sheng-Fu / Vincent, Ziawei / Jiawei) is
  `slot: 0` with `author_list_differs: true` and a note. The checker rejects `slot: 0` for a name that is compatible
  with a metadata author left unmatched (D302).
- Never type an e-mail address, phone number or URL anywhere, not even masked; never write the word e-mail in notes.
- Locator defaults to `p.~1 header`; set `locator: "p.~1 footnote"` on a block printed as a first-page footnote.

## Check (until 0 errors)

    uv run python scripts/ofc_headers.py check <batch>

It validates the YAML, scans every file of the batch for contact data, verifies texts against the source, checks
markers and slot coverage. Only at 0 errors does it write the derived `header_rows.csv`, `compare.csv`,
`unmapped_orgs.csv` and `check_stamp.txt` (hash of `headers.yaml`) into the batch directory (never edit those by
hand). It writes nothing outside the batch, so batches can be checked in parallel (D248). The log is
`logs/ofc_headers_check_<batch>_<pid>_<timestamp>.log`. The coordinator runs `uv run python scripts/ofc_headers.py
aggregate` after the batches: it writes `data/_staging/people/ofc_headers/org_requests.csv` (alias requests for the
org-curation stream, D242) and the local review lists `data/_local/ofc_headers_conflicts.csv` (D241) and
`data/_local/ofc_headers_extra_authors.csv` (D243) from every batch whose stamp matches its YAML. `org_requests.csv`
has one row per (printed org, city, country) with the printed units, locators, a proposed id when the registry has
that exact name, and a curation note for requests that need more than an alias (D303, D305). Subagents do not run
`aggregate`.

## Final message (the coordinator saves it as the batch report; do not write report files)

Per batch: papers ok / partial / unreadable (with the reason), the check summary line (outcome counts agree / extra /
conflict / present_address / unmapped / no_header), every `conflict` slot (paper, slot, metadata org vs header org),
papers with `author_list_differs`, the unmapped org strings, and judgment calls.

## Boundaries

Write only `headers.yaml` in your batch directory (the checker writes the derived files). Never edit `papers.csv`,
other batches, `data/people/`, `data/registry/`, `data/crosswalk/`, `data/schema/`, scripts or any sibling repo.
