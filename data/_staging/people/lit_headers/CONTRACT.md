# `lit` author affiliation batch contract (DevLog-011, 2026-10-23; audit fixes D359-D365 and batch fixes D366-D369 applied)

This is an addendum: everything in `data/_staging/people/ofc_headers/CONTRACT.md` applies (YAML format, never-invent
rules, markers, `dropped_markers`, campus, slots, no contacts / addresses), except where this file says otherwise.
Read `DevLog/DevLog-011-lit-author-affiliations.md` (D350-D369) and the worked examples in
`data/_staging/people/lit_headers/pilot/headers.yaml` first. Work from the repo root. No emoji, no git, no network.

## Your batch

`data/_staging/people/lit_headers/<batch>/papers.csv` lists the papers. Print one with

    uv run python scripts/ofc_headers.py show <batch> --corpus lit --codes <paper_id> [--pdf] [--pages 2 9]

Page 1 of `references/<paper_id>/text.md` is printed (plus `--pages`), then the ordered author list (the slots).
`--pdf` adds the same pages of the local `source.pdf` with superscripts as `^{...}`: use it whenever markers look lost.
Restricted corpus (D357): copy only names and the org / unit / city / country of each block; never quote text.

## Differences from the OFC contract

- `source_id: lit:<paper_id>`. Locators are exact pages of `text.md` (D353): `p.1 header` (default), `p.1 footnote`,
  `p.N affiliations` for blocks printed on a later page (the checker then also searches page N).
- Slots (D352, D359, D362): the ordered author list printed by `show` (literature cache: `merged.jsonl`, else
  `curator_adds.jsonl`); slot number = author-list position. Only when `show` prints "[no author list:
  slots_from_header]" set `slots_from_header: true` (the header order then defines the slots). A printed order that
  differs from the list is fine (the checker warns, D363); never reorder the authors in the YAML: list them in
  printed order.
- Prose affiliations (D354, `basis: prose`, grade A): footnote statements such as "K. A and L. B are with <block>",
  "X was with <block>" (the affiliation of the work), "X is also with <block>" (additional), "X is now with <block>" /
  "He / She / They are now with <block>" (`role: present_address`). Each statement is one block with a synthetic
  marker `P1`, `P2`, ... in printed order (never a printed marker); each author named in the statement carries it;
  "The authors are with ..." = every author. Two statements naming the same org are two blocks. Prose markers are not
  printed after names, so they never need `dropped_markers`.
- "<names> is with A, and (also) with B[, and with C]" (also ", also with", "and are also with") in one sentence:
  A is the statement block, each further "with" clause its own block with `clause: true` right after it (same
  subject, own unit / place, D366); the authors carry every block. A period after a name in the subject ("F.
  Ferraro. Y. Ban") is not a sentence end: list all names.
- An address-like span printed between the verb and the first field (a building or complex name: "are with Lee
  Maltings Complex, Tyndall National Institute") goes to `skip_prefix: "<span as printed>"`; it is verified and never
  recorded (D366).
- An unreadable author may still carry prose markers (so the statement stays consistent); no rows are derived.
- Record every statement that names an author (D361), including "is also with", "is now with", "was with" and
  pronoun statements ("He is now with ..."): the checker rejects a statement on the searched pages whose subject names
  an author but that no prose block records.
- A statement split across columns or blocks (D360): record the block with all fields printed in both parts and set
  `continued: "<first printed word(s) of the continuation>"` (e.g. "Corporation" when "... are with Intel" goes on
  "Corporation, ... Santa Clara, ..., USA" in the other column); mention the split in the note. The checker joins the
  verb's printed line with the continuation (found at a line start later on the page) and checks the fields there.
- Layouts without markers (D368, grade A): `per_author` = the block(s) printed under each author (IEEE conference
  style): one block per author with a synthetic marker `G1`, `G2`, ...; `grouped` = an author group printed above
  its own block(s) ("A, B and C \n Org1 \n D \n Org2"): one block per printed org, marker `G<n>`, carried by every
  author of the group. List authors in printed reading order. The checker verifies the position (block after its
  authors, no other author between). A single unmarked block next to marked blocks stays `layout` (grade B).
- Cover pages (D366): when page 1 is a cover and the marked author line is on page N, set `locator: "p.N header"` on
  every block; the checker then searches from page N. `show` prints page separators with text.md page numbers.
- Joint-printed orgs with their own unit / place (D367): `more_orgs: [{org: "Ghent University", unit: "Photonics
  Research Group, Department of Information Technology", locality: "Ghent", country: "BE"}]`; plain strings keep the
  block's place.
- A letter marker glued to its cue ("aPresent address:") is a marker plus a present-address block (D366).
- Locality (D366 / D288): the city as printed ("Atsugi-shi", "Yokohama-shi" kept); postal designations ("Cedex")
  dropped; a district printed before the city goes to the note.
- Slots (D369): a printed full name and an abbreviated list form must agree on every initial ("Siyuan Yu" vs "S. F.
  Yu" is not a match: `slot: 0` + `author_list_differs`). A distinctive (non-common) family name whose only
  difference is a missing middle initial may take an explicit name-part `slot:` (D287).
- Footnote markers that point to a contact line (e-mail) or an equal-contribution note go to `dropped_markers`
  (reason "contact footnote" / "equal contribution"). A printed block that no author carries is not recorded (note
  it).
- Membership designations ("Member, IEEE", "Senior Member, IEEE, Fellow, OSA") are not part of names; the checker
  ignores them in the author line.
- A statement or block truncated in both the text and the PDF layer (no continuation anywhere on the searched pages):
  record only what is printed (e.g. org without a city) and say so in the note; never complete it from elsewhere.
- No per-author metadata org exists, so `compare.csv` outcomes are `recorded` / `no_header` (D356).

## Check (until 0 errors)

    uv run python scripts/ofc_headers.py check <batch> --corpus lit

Same rules and derived files as OFC (written only at 0 errors, with `check_stamp.txt`). The coordinator runs
`uv run python scripts/ofc_headers.py aggregate --corpus lit` after the batches (`lit_headers/org_requests.csv`,
local `data/_local/lit_headers_conflicts.csv` (always empty: no metadata orgs) and `lit_headers_extra_authors.csv`).

## Final message (the coordinator saves it as the batch report)

Per batch: papers ok / partial / unreadable (with the reason), the check summary line, papers with
`slots_from_header` or `author_list_differs`, prose papers, truncated statements, unmapped org strings, judgment calls.

## Boundaries

Write only `headers.yaml` in your batch directory. Never edit `papers.csv`, other batches, `references/`,
`data/people/`, `data/registry/`, `data/crosswalk/`, `data/schema/`, scripts, `app/` or any sibling repo.
