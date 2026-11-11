"""Validate and merge historical milestone rows (DevLog-016 D963) from data/_staging/history/<batch>/milestones.csv into
data/history/milestones.csv (one row per paper_id; a re-merge of the same batch replaces that batch's rows).

Checks per row: required columns; paper_id in the batch papers.csv; source_id `lit:<paper_id>` present in
data/registry/sources.csv; date ISO (YYYY, YYYY-MM or YYYY-MM-DD) or empty; event <= 25 words, caption <= 30 words,
reason <= 15 words; key figure fields all set or all empty; key_figure_file exists under references/<paper_id>/figures/
(local check, skipped with a warning when the references are not on this machine); the figure label (e.g. "Fig. 2",
"2") appears in the paper's text.md; no emoji. A paper already merged from another batch is an error unless --replace.

Usage: uv run python scripts/hist_merge_milestones.py data/_staging/history/hist_NN [--dry-run] [--replace]
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
import zipfile
from pathlib import Path

from photonics_atlas.paths import ROOT
from photonics_atlas.runlog import RunLog

OUT = ROOT / "data" / "history" / "milestones.csv"
SOURCES = ROOT / "data" / "registry" / "sources.csv"
COLUMNS = [
    "paper_id", "source_id", "batch", "date", "era", "thread", "event", "event_locator", "dri", "dri_locator",
    "orgs_printed", "key_figure_label", "key_figure_page", "key_figure_file", "key_figure_caption",
    "key_figure_reason", "notes",
]  # fmt: skip
DATE = re.compile(r"^\d{4}(-\d{2}(-\d{2})?)?$")
EMOJI = re.compile("[\U0001f300-\U0001faff☀-➿]")
FIG = ("key_figure_label", "key_figure_page", "key_figure_file", "key_figure_caption", "key_figure_reason")


def words(s: str) -> int:
    return len(s.split())


def read(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return [dict(r) for r in csv.DictReader(f)]


def check(batch: Path, rows: list[dict[str, str]]) -> tuple[list[str], list[str]]:
    errs: list[str] = []
    warns: list[str] = []
    papers = {r["paper_id"] for r in read(batch / "papers.csv")}
    sources = {r["source_id"] for r in read(SOURCES)}
    seen: set[str] = set()
    for i, r in enumerate(rows, 2):
        pid = r.get("paper_id", "")
        at = f"line {i} {pid}"
        missing = [c for c in COLUMNS if c != "batch" and c not in r]
        if missing:
            errs.append(f"{at}: missing columns {missing}")
            continue
        if pid not in papers:
            errs.append(f"{at}: paper_id not in papers.csv")
        if pid in seen:
            errs.append(f"{at}: duplicate paper_id")
        seen.add(pid)
        if r["source_id"] != f"lit:{pid}" or r["source_id"] not in sources:
            errs.append(f"{at}: source_id {r['source_id']!r} is not a registered lit:<paper_id>")
        if r["date"] and not DATE.match(r["date"]):
            errs.append(f"{at}: date {r['date']!r} not ISO")
        if not r["event"].strip():
            errs.append(f"{at}: empty event")
        for col, cap in (("event", 25), ("key_figure_caption", 30), ("key_figure_reason", 15)):
            if words(r[col]) > cap:
                errs.append(f"{at}: {col} has {words(r[col])} words (cap {cap})")
        for col, val in r.items():
            if val and EMOJI.search(val):
                errs.append(f"{at}: emoji in {col}")
        filled = [c for c in FIG if r[c].strip()]
        if filled and len(filled) != len(FIG):
            errs.append(f"{at}: key figure fields partly filled ({filled})")
        if len(filled) == len(FIG):
            d = ROOT / "references" / pid
            f = d / "figures" / r["key_figure_file"]
            if not (ROOT / "references").exists() or not d.exists():
                warns.append(f"{at}: references not on this machine, figure file not checked")
            elif "/" in r["key_figure_file"] or not f.is_file():
                errs.append(f"{at}: key_figure_file {r['key_figure_file']!r} not in references/{pid}/figures/")
            if not r["key_figure_page"].isdigit():
                errs.append(f"{at}: key_figure_page {r['key_figure_page']!r} not a page number")
            text = (d / "text.md").read_text(encoding="utf-8", errors="ignore") if (d / "text.md").exists() else ""
            num = re.sub(r"(?i)^(fig(ure)?\.?|fig\.)\s*", "", r["key_figure_label"]).strip()
            if text and num and not re.search(rf"(?i)\bfig(ure|\.)?\s*{re.escape(num)}\b", text):
                warns.append(f"{at}: figure label {r['key_figure_label']!r} not found in text.md (OCR?)")
    return errs, warns


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("batch", type=Path)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--replace", action="store_true")
    a = ap.parse_args()
    batch = a.batch if a.batch.is_absolute() else ROOT / a.batch
    name = batch.name
    with RunLog("hist_merge_milestones", a.dry_run) as log:
        rows = read(batch / "milestones.csv")
        errs, warns = check(batch, rows)
        old = read(OUT) if OUT.exists() else []
        other = {r["paper_id"]: r["batch"] for r in old if r["batch"] != name}
        for r in rows:
            if r["paper_id"] in other and not a.replace:
                errs.append(f"{r['paper_id']}: already merged from {other[r['paper_id']]} (use --replace)")
        for wmsg in warns:
            log.info(f"WARN {wmsg}")
        for e in errs:
            log.info(f"ERROR {e}")
        log.info(f"{name}: {len(rows)} rows, {len(errs)} errors, {len(warns)} warnings")
        if errs or a.dry_run:
            return 1 if errs else 0
        keep = [
            r for r in old if r["batch"] != name and not (a.replace and r["paper_id"] in {x["paper_id"] for x in rows})
        ]
        new = keep + [{c: (name if c == "batch" else r.get(c, "")) for c in COLUMNS} for r in rows]
        new.sort(key=lambda r: (r["date"] or "9999", r["paper_id"]))
        OUT.parent.mkdir(parents=True, exist_ok=True)
        if OUT.exists():
            bak = ROOT / "cache" / "history_backup"
            bak.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(bak / f"milestones_before_{name}.zip", "w", zipfile.ZIP_DEFLATED) as z:
                z.write(OUT, OUT.relative_to(ROOT))
        with OUT.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=COLUMNS)
            w.writeheader()
            w.writerows(new)
        log.info(f"merged {len(rows)} rows from {name}; {len(new)} rows in {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
