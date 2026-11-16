"""B1 of DevLog-019: find comparison tables / trend plots that cite other works, write one packet per paper.

Scans the lit corpus (references/<id>/text.md), the EO atlas cache and the OFC 2026 Marker texts (read-only inputs).
A candidate region is a table caption or figure caption (or a Markdown table / caption-less "this work" cluster)
whose neighbourhood carries reference tags. Each paper with >= 1 candidate gets a packet (Markdown) holding the
regions, the page renders to look at, and the parsed reference entries the regions cite (or the whole reference
section when the tags cannot be read from text, e.g. a plot legend).

Outputs (git-ignored): cache/literature/bench/candidates.jsonl, cache/literature/bench/packets/<corpus>__<id>.md,
log logs/bench_prefilter_<ts>.log. Pure local reads; no network.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
GH = ROOT.parent
OUT = ROOT / "cache" / "literature" / "bench"

PAGE_RE = re.compile(r"<!-- page (\d+) -->")
TABLE_CAP_RE = re.compile(r"^\s*(?:\|\s*)?(?:\*\*)?(TABLE|Table)\s+([0-9]+|[IVX]+|S[0-9]+)\b")
FIG_CAP_RE = re.compile(r"^\s*(?:\*\*)?(Fig\.|FIG\.|Figure|FIGURE)\s*([0-9]+)\b")
KEY_RE = re.compile(
    r"compar|state[- ]of[- ]the[- ]art|\bsota\b|reported|previous|prior (?:work|art)|literature|benchmark|summar|"
    r"evolution|progress|over the (?:past|years|last)|timeline|histor|record|other (?:work|group|device|platform)s?|"
    r"recent (?:work|result|demonstration)s?|survey|this work|our work|published",
    re.I,
)
# Caption style: "Fig. 3." / "Fig. 3:" / "Fig. 3 |" / "Figure 3 Comparison" (capitalised); not "Fig. 3 shows".
FIG_STYLE_RE = re.compile(r"^\s*(?:[.:|\-–]|\*\*|\s+[A-Z(])")
# A figure counts only when its caption points at other works.
FIG_OTHERS_RE = re.compile(
    r"state[- ]of[- ]the[- ]art|\bSOTA\b|reported|previous (?:work|stud|result|demonstr|record|report)|literature|"
    r"other (?:work|group|report|device|platform|technolog|approach|demonstr|design|modulator|laser|detector)s?|"
    r"prior (?:work|art)|benchmark|published|over the (?:past|years|last)|timeline|historical|"
    r"(?:by|per|versus|vs\.?) (?:the )?(?:publication )?year|since (?:19|20)\d\d|"
    r"(?:various|different|existing|recent|typical|representative|selected) (?:[\w-]+ ){0,3}"
    r"(?:devices|modulators|lasers|(?:photo)?detectors|couplers|platforms|technologies|demonstrations|works|results|"
    r"resonators|amplifiers|filters|isolators|switches|waveguides|splitters|sources|combs|transceivers|PDs|MRRs|"
    r"approaches|implementations|reports)",
    re.I,
)
THISWORK_RE = re.compile(r"\b(this|our|present|proposed) (work|device|paper|design)\b", re.I)
# [12], [3,4], [5-7], [5–7], [ 12 ], Ref. 12, ref. 3
TAG_RE = re.compile(r"\[\s*(\d{1,3}(?:\s*[,–\-]\s*\d{1,3})*)\s*\]|\b[Rr]efs?\.\s*(\d{1,3}(?:\s*[,–\-]\s*\d{1,3})*)")
REFHEAD_RE = re.compile(
    r"^\s*(?:#+\s*)?(?:[0-9]{1,2}\.?\s*)?(R\s?EFERENCES?|References?(?: and (?:links|Links|Notes|notes))?|"
    r"REFERENCES AND NOTES|Bibliography)\s*:?\s*$"
)
REF_ENTRY_RE = re.compile(r"^\s*(?:[-*]\s*)?(?:\[(\d{1,3})\]|(\d{1,3})\.(?:\s|$))\s*(.*)$")
NOISE_RE = re.compile(r"<span[^>]*>\s*</span>|\*\*")


def clean(ln: str) -> str:
    return NOISE_RE.sub("", ln)


@dataclass
class Paper:
    corpus: str
    pid: str
    text_path: Path
    fig_dir: Path | None
    lines: list[str] = field(default_factory=list)
    pages: list[int] = field(default_factory=list)


def expand_tags(s: str) -> set[int]:
    out: set[int] = set()
    for m in TAG_RE.finditer(s):
        body = m.group(1) or m.group(2) or ""
        for part in re.split(r"\s*,\s*", body):
            rng = re.split(r"\s*[–\-]\s*", part)
            try:
                if len(rng) == 2:
                    a, b = int(rng[0]), int(rng[1])
                    if 0 < a <= b and b - a < 40:
                        out.update(range(a, b + 1))
                elif rng[0]:
                    out.add(int(rng[0]))
            except ValueError:
                continue
    return {n for n in out if 0 < n < 400}


def load(p: Paper) -> None:
    page = 1
    for ln in p.text_path.read_text(errors="replace").splitlines():
        m = PAGE_RE.search(ln)
        if m:
            page = int(m.group(1))
        p.lines.append(ln)
        p.pages.append(page)


def ref_section(p: Paper) -> tuple[int, int] | None:
    """Line range of the reference section (last heading wins unless it leaves < 3 entries)."""
    heads = [i for i, ln in enumerate(p.lines) if REFHEAD_RE.match(clean(ln))]
    for h in reversed(heads):
        n = sum(1 for ln in p.lines[h + 1 : h + 400] if REF_ENTRY_RE.match(clean(ln)))
        if n >= 3:
            return h, min(len(p.lines), h + 1 + 900)
    # no heading (e.g. Nature layouts): first "1." in the back half followed by "2." and "3." within 40 lines
    for i in range(len(p.lines) // 2, len(p.lines)):
        m = REF_ENTRY_RE.match(clean(p.lines[i]))
        if m and int(m.group(1) or m.group(2)) == 1:
            nums = []
            for ln in p.lines[i + 1 : i + 40]:
                m2 = REF_ENTRY_RE.match(clean(ln))
                if m2:
                    nums.append(int(m2.group(1) or m2.group(2)))
            # bibliographic entries carry a year; numbered appendix headings ("1. Mean-field analysis") do not
            if 2 in nums and 3 in nums and YEAR_RE.search(" ".join(p.lines[i : i + 12])):
                return i - 1, min(len(p.lines), i + 900)
    if heads:
        return heads[-1], min(len(p.lines), heads[-1] + 1 + 900)
    return None


def parse_refs(p: Paper, sec: tuple[int, int] | None) -> dict[int, str]:
    """Numbered entries in the reference section; keeps only a monotone run (1, 2, 3, ...) to avoid stray numbers."""
    if sec is None:
        return {}
    refs: dict[int, str] = {}
    cur: int | None = None
    expect = 1
    for ln in p.lines[sec[0] + 1 : sec[1]]:
        if PAGE_RE.search(ln):
            continue
        ln = clean(ln)
        m = REF_ENTRY_RE.match(ln)
        num = int(m.group(1) or m.group(2)) if m else None
        if m and num is not None and num in (expect, expect + 1):
            cur = num
            refs[cur] = (m.group(3) or "").strip()
            expect = cur + 1
        elif cur is not None and ln.strip():
            if len(refs[cur]) < 700:
                refs[cur] += " " + ln.strip()
    # a run of numbered prose (appendix sections) is not a bibliography: most entries must carry a year
    if len(refs) < 3 or sum(bool(YEAR_RE.search(v)) for v in refs.values()) < 0.5 * len(refs):
        return {}
    return refs


YEAR_RE = re.compile(r"\b(19[5-9]\d|20[0-3]\d)\b")
# A "Ref." / "References" column header: the table cites other works by plain numbers (e.g. review summary tables).
REFCOL_RE = re.compile(r"^\s*\|?\s*(Refs?\.?|References?|Reference No\.?)\s*\|?\s*$", re.I)
SECTION_RE = re.compile(r"^\s*(?:#+\s*)?(?:[0-9]{1,2}|[IVX]{1,5})\.\s+[A-Z][A-Za-z ,-]{3,60}\s*$")


# A caption that itself says the table compares other works (tags may be superscripts lost in the text layer).
STRONG_CAP_RE = re.compile(
    r"compar\w* (?:of|with|between|among)? ?(?:the )?(?:\w+ ){0,4}(?:reported|previous|recent|state|published|"
    r"literature|other|existing|various|different)|state[- ]of[- ]the[- ]art|reported in (?:the )?literature|"
    r"benchmark|summary of (?:\w+ ){0,3}(?:reported|published|recent|demonstrat)|"
    r"\bcompara?\w*|\bsummary\b|\boverview\b|\bsurvey\b",
    re.I,
)


def table_end(lines: list[str], i: int, stop: int, max_lines: int = 170) -> int:
    """End of a table window: next table caption, next section heading or the reference section, at most max_lines."""
    for j in range(i + 1, min(stop, i + max_lines)):
        if TABLE_CAP_RE.match(lines[j]) or SECTION_RE.match(clean(lines[j])):
            return j + 1 if j - i > 8 else min(stop, i + max_lines)
    return min(stop, i + max_lines)


def caption_text(lines: list[str], i: int, n: int = 6) -> str:
    out: list[str] = []
    for ln in lines[i : i + n]:
        if not ln.strip() and out:
            break
        out.append(ln.strip())
    return " ".join(out)[:600]


def candidates(p: Paper) -> list[dict[str, Any]]:
    L = p.lines
    regions: list[dict[str, Any]] = []
    sec = ref_section(p)
    stop = sec[0] if sec else len(L)
    for i, ln in enumerate(L[:stop]):
        kind = None
        if TABLE_CAP_RE.match(ln):
            kind = "table"
        elif FIG_CAP_RE.match(ln):
            kind = "figure"
        if not kind:
            continue
        cap = caption_text(L, i)
        if kind == "table":
            lo, hi = max(0, i - 25), table_end(L, i, stop)
            win = "\n".join(L[lo:hi])
            tags = expand_tags(win)
            refcol = any(REFCOL_RE.match(x) for x in L[i : min(hi, i + 25)])
            if (
                ((KEY_RE.search(cap) or THISWORK_RE.search(win)) and len(tags) >= 2)
                or refcol
                or STRONG_CAP_RE.search(cap)
            ):
                regions.append(
                    {
                        "kind": "table",
                        "line": i + 1,
                        "lo": lo + 1,
                        "hi": hi,
                        "page": p.pages[i],
                        "caption": cap,
                        "tags": sorted(tags),
                    }
                )
        else:
            ctags = expand_tags(cap)
            body = FIG_CAP_RE.sub("", clean(ln), count=1)
            if not FIG_STYLE_RE.match(body):  # "Fig. 6 shows ..." is body text, not a caption
                continue
            if FIG_OTHERS_RE.search(cap) or (len(ctags) >= 2 and re.search(r"compar|versus|\bvs\.?\b", cap, re.I)):
                regions.append(
                    {
                        "kind": "figure",
                        "line": i + 1,
                        "lo": i + 1,
                        "hi": min(stop, i + 8),
                        "page": p.pages[i],
                        "caption": cap,
                        "tags": sorted(ctags),
                    }
                )
    # Markdown tables (OFC Marker output) and caption-less flattened tables: "this work" near >= 3 tags
    for i, ln in enumerate(L[:stop]):
        if THISWORK_RE.search(ln) and (ln.lstrip().startswith("|") or len(ln.strip()) < 40):
            lo, hi = max(0, i - 40), min(stop, i + 30)
            if any(r["lo"] - 1 <= i < r["hi"] for r in regions):
                continue
            tags = expand_tags("\n".join(L[lo:hi]))
            if len(tags) >= 3:
                regions.append(
                    {
                        "kind": "table_nocap",
                        "line": i + 1,
                        "lo": lo + 1,
                        "hi": hi,
                        "page": p.pages[i],
                        "caption": "",
                        "tags": sorted(tags),
                    }
                )
    # de-overlap: keep first region per overlapping span
    regions.sort(key=lambda r: r["lo"])
    kept: list[dict[str, Any]] = []
    for r in regions:
        if kept and r["lo"] <= kept[-1]["hi"] and r["kind"] == kept[-1]["kind"] == "table_nocap":
            kept[-1]["hi"] = max(kept[-1]["hi"], r["hi"])
            kept[-1]["tags"] = sorted(set(kept[-1]["tags"]) | set(r["tags"]))
            continue
        kept.append(r)
    return kept


def write_packet(p: Paper, regs: list[dict[str, Any]], refs: dict[int, str], sec: tuple[int, int] | None) -> Path:
    path = OUT / "packets" / f"{p.corpus}__{p.pid}.md"
    out = [f"# packet {p.corpus}:{p.pid}", f"text: {p.text_path}", ""]
    need_full = False
    cited: set[int] = set()
    for k, r in enumerate(regs, 1):
        img = ""
        if p.fig_dir is not None:
            pg = p.fig_dir / f"page_{r['page']:02d}.png"
            img = str(pg) if pg.exists() else ""
        out.append(
            f"## region {k}: {r['kind']} (text lines {r['lo']}-{r['hi']}, page {r['page']})"
            + (f" image: {img}" if img else "")
        )
        out.append("```")
        out.extend(p.lines[r["lo"] - 1 : r["hi"]])
        out.append("```")
        cited |= set(r["tags"])
        if r["kind"] == "figure" and len(r["tags"]) < 2:
            need_full = True
    out.append("")
    if refs and not need_full and all(n in refs for n in cited):
        out.append("## cited reference entries (parsed)")
        out.extend(f"[{n}] {refs[n]}" for n in sorted(cited))
    elif sec is not None:
        out.append(f"## reference section (text lines {sec[0] + 1}-{sec[1]})")
        out.append("```")
        out.extend(ln for ln in p.lines[sec[0] : sec[1]] if not PAGE_RE.search(ln))
        out.append("```")
    else:
        out.append("## reference section: not found by the parser; search the text file")
    path.write_text("\n".join(out) + "\n")
    return path


def iter_papers(corpora: set[str]) -> list[Paper]:
    papers: list[Paper] = []
    if "lit" in corpora:
        lit_ids = set()
        with open(ROOT / "data" / "registry" / "sources.csv", newline="") as f:
            for row in csv.DictReader(f):
                if row["corpus"] == "lit":
                    lit_ids.add(row["native_id"])
        for pid in sorted(lit_ids):
            t = ROOT / "references" / pid / "text.md"
            if t.exists():
                papers.append(Paper("lit", pid, t, ROOT / "references" / pid / "figures"))
    if "eo" in corpora:
        for d in sorted((GH / "eo-modulator-atlas" / "references").iterdir()):
            t = d / "text.md"
            if t.exists():
                papers.append(Paper("eo", d.name, t, d / "figures"))
    if "ofc2026" in corpora:
        for t in sorted((GH / "PlayGround" / "20260320_OFC" / "extracted_text").glob("*.md")):
            papers.append(Paper("ofc2026", t.name.split("-")[0], t, None))
    return papers


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--corpora", default="lit,eo,ofc2026")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--dry-run", action="store_true", help="count only, write nothing")
    ap.add_argument(
        "--only-new",
        default="",
        help="earlier candidates.jsonl: write packets only for papers not in it, to candidates_delta_<ts>.jsonl",
    )
    a = ap.parse_args()
    ts = datetime.now().strftime("%Y%m%dT%H%M%S")
    (OUT / "packets").mkdir(parents=True, exist_ok=True)
    log = open(ROOT / "logs" / f"bench_prefilter_{ts}.log", "w")
    papers = iter_papers(set(a.corpora.split(",")))
    if a.limit:
        papers = papers[: a.limit]
    known: set[str] = set()
    if a.only_new:
        for line in open(a.only_new):
            r = json.loads(line)
            known.add(f"{r['corpus']}:{r['paper_id']}")
    stats: dict[str, dict[str, int]] = {}
    rows: list[dict[str, Any]] = []
    for p in papers:
        load(p)
        sec = ref_section(p)
        refs = parse_refs(p, sec)
        regs = candidates(p)
        s = stats.setdefault(p.corpus, {"papers": 0, "with_cand": 0, "regions": 0, "refs_parsed": 0, "no_refsec": 0})
        s["papers"] += 1
        s["refs_parsed"] += bool(refs)
        s["no_refsec"] += sec is None
        if not regs or f"{p.corpus}:{p.pid}" in known:
            continue
        s["with_cand"] += 1
        s["regions"] += len(regs)
        pk = "" if a.dry_run else str(write_packet(p, regs, refs, sec).relative_to(ROOT))
        rows.append(
            {
                "corpus": p.corpus,
                "paper_id": p.pid,
                "text": str(p.text_path),
                "packet": pk,
                "n_regions": len(regs),
                "n_refs_parsed": len(refs),
                "regions": [
                    {k: r[k] for k in ("kind", "lo", "hi", "page", "caption")} | {"n_tags": len(r["tags"])}
                    for r in regs
                ],
            }
        )
        print(f"{p.corpus}:{p.pid} regions={len(regs)} refs={len(refs)}", file=log)
    if not a.dry_run:
        name = f"candidates_delta_{ts}.jsonl" if a.only_new else "candidates.jsonl"
        with open(OUT / name, "w") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(json.dumps(stats, indent=1), file=log)
    print(json.dumps(stats, indent=1))
    log.close()


if __name__ == "__main__":
    main()
