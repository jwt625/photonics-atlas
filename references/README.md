# references/

Local literature cache for the `lit` registry corpus (DevLog-006 S7, D127). One directory per selected paper,
named by its `paper_id` from `data/_staging/literature/cache_list.csv` (`<firstauthor><year>[a-z]`, e.g. `nan2025`);
the registry row is `lit:<paper_id>` in `data/registry/sources.csv`.

## Layout

```
references/
  README.md                  this file (committed)
  _inbox/                    manual downloads waiting for ingest (local only)
  <paper_id>/
    source.json              metadata, provenance, license, extraction statistics (committed)
    source.pdf               the retrieved PDF (local only)
    text.md                  YAML header + text per page with <!-- page N --> markers (local only)
    figures/                 page_NN.png (150 dpi, pages with a figure / table caption), img_pNN_k.png
                             (embedded rasters >= 150 px), figures.json (local only)
    supplement/              source.pdf, text.md, figures/ of the supplement, when ingested (local only)
```

## What is committed

| Path | Committed | Why |
|---|---|---|
| `<paper_id>/source.json` | yes | identifiers, URLs, route, license, redistribution, sha256, page / text / figure counts, dates, quality flags; no publisher text |
| `<paper_id>/source.pdf`, `*.pdf` | no (`references/*/*.pdf`) | rights are source-specific; even `open_license_ok` copies stay local |
| `<paper_id>/text.md`, `figures/` | no | derived from the PDF |
| `<paper_id>/supplement/`, `arxiv/` | no | as above |
| `_inbox/*` | no | user downloads |

Unfinished downloads never land here: they are written to `cache/literature/fetch_part/<paper_id>.pdf.part` and moved
to `source.pdf` only after the `%PDF` magic, size and Content-Length checks.

## source.json

Written by the fetchers (`scripts/lit_fetch_oa.py`, `scripts/lit_fetch_browser.py`, `scripts/lit_ingest_inbox.py`)
and completed by `scripts/lit_extract.py`. Main fields: `paper_id`, `uid`, `doi`, `arxiv_id`, `title`, `url` (the URL
the PDF came from), `landing_url`, `route` (arxiv / oa_publisher / optica_browser / ieee_browser / manual), `access`
(registry enum: arxiv / open_access / paywalled), `license` (normalized, e.g. `cc-by-4.0`,
`arxiv-nonexclusive-distrib-1.0`), `license_source`, `redistribution`, `sha256`, `bytes`, `pages`, `text_chars`,
`n_figure_files`, `retrieved_on` (UTC), `extracted_on` (UTC date), `garbled_text_layer`, `garbled_pages`, `low_text`,
`institutional_stamp`, `ocr_available`, `ocr_run`.

Redistribution rule: `open_license_ok` only for a cc-* license of the fetched version (arXiv copies: the arXiv license
of the latest version from the OAI-PMH arXivRaw record; publisher / repository copies: the OpenAlex best-location
license); bronze, paywalled, manual or institution-stamped copies and known non-CC licenses: `restricted_local_only`;
no license known: `unknown`. A value set by the acquiring script is never relaxed.

## Inbox (manual downloads)

The list of papers to download by hand is `data/_staging/literature/manual_downloads.md`.

- Save the main PDF as `references/_inbox/<paper_id>.pdf`, a supplement as `references/_inbox/<paper_id>_supplement.pdf`.
- Run `uv run python scripts/lit_ingest_inbox.py --dry-run`, then without `--dry-run`. Files that fail the `%PDF` /
  size check, have an unknown `paper_id`, or whose target already exists stay in the inbox and are reported; nothing
  in the inbox is deleted.

## Pipeline

```
uv run python scripts/lit_fetch_oa.py --day N            # arxiv + oa_publisher rows of queue day N
uv run python scripts/lit_fetch_browser.py ...           # optica_browser / ieee_browser rows
uv run python scripts/lit_ingest_inbox.py                # manual downloads
uv run python scripts/lit_extract.py --pending           # text.md, figures/, source.json
uv run python scripts/lit_register_sources.py            # lit:<paper_id> rows in data/registry/sources.csv
uv run python scripts/validate_db.py
```

Fetch status per attempt: `logs/lit_fetch_status.jsonl` (append-only). Host breakers: `logs/.lit_blocked_<host>.json`.
