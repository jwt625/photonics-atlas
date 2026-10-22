"""Select the component-literature cache list from LLM scores + curation (DevLog-006 S5, D120-D125). No network.

Inputs:  cache/literature/prefiltered.jsonl (metadata, kept records), cache/literature/scoring/out_*.jsonl (S3 scores),
         config/literature/selection.yaml (rules, per-class budget), config/literature/curation/*.yaml (S4 overrides:
         `picks: [{uid, class, reason}]`, `drops: [{uid, reason}]`, `reclass: [{uid, class, subtype?, reason}]`).
Steps:   1. eligibility: scored, prefilter-kept, not known, not review / out_of_scope / EO-modulator-main;
         2. version families: works whose normalized titles nearly match (token Jaccard >= 0.6 and difflib >= 0.85) and
            share the first- or last-author surname are one family; the best member stays (journal > conference >
            preprint, then OA, then score);
         3. per class (primary = first LLM class, or the curator reclass): curator picks, then subtype floors, then
            platform floors, then greedy fill by rank, under the per-senior-author cap and the paywalled share cap;
            paywalled rule picks need paywalled_min_score;
         4. reserve = reserve_curator_picks + unfilled class budget: curator picks beyond class budgets first, then the
            best remaining eligible works across classes (fill_reserve_with_best).
Outputs: data/_staging/literature/cache_list.csv, data/_staging/literature/triage_report.md,
         data/_staging/literature/eo_atlas_candidates.csv (EO-modulator-main works for the EO atlas, not selected).

Usage: uv run python scripts/lit_select.py [--dry-run]
"""

from __future__ import annotations

import argparse
import ast
import csv
import difflib
import json
import math
import re
import unicodedata
from collections import Counter, defaultdict
from typing import Any

import yaml

from photonics_atlas.paths import CACHE, ROOT, STAGING
from photonics_atlas.runlog import RunLog

LIT = CACHE / "literature"
OUT = STAGING / "literature"
CFG = ROOT / "config" / "literature"
VENUE_RANK = {"journal": 0, "conference": 1, "other": 2, "repository": 3}
FIELDS = [
    "rank", "primary_class", "subtype", "classes", "uid", "doi", "arxiv_id", "paper_id", "title", "first_author",
    "last_author", "venue", "venue_type", "year", "score", "platform", "band", "access", "oa_url", "industrial",
    "record_claim", "selection_reason", "family_size", "rationale",
]  # fmt: skip


def as_list(v: Any) -> list[Any]:
    if isinstance(v, list):
        return v
    if isinstance(v, str) and v.startswith("["):
        try:
            out = ast.literal_eval(v)
            return out if isinstance(out, list) else []
        except (ValueError, SyntaxError):
            return []
    return [v] if v else []


def as_bool(v: Any) -> bool:
    return v is True or str(v).lower() == "true"


def ascii_slug(s: str) -> str:
    return re.sub(r"[^a-z]", "", unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower())


def surname(name: str) -> str:
    parts = [p for p in re.split(r"\s+", name.strip()) if p]
    return ascii_slug(parts[-1]) if parts else ""


def tokens(title: str) -> set[str]:
    return {t for t in re.findall(r"[a-z0-9]+", title.lower()) if len(t) > 2}


def same_work(a: dict[str, Any], b: dict[str, Any]) -> bool:
    ta, tb = a["_tok"], b["_tok"]
    if not ta or not tb or len(ta & tb) / len(ta | tb) < 0.7:
        return False
    ya, yb = int(a.get("year") or 0), int(b.get("year") or 0)
    if ya and yb and abs(ya - yb) > 2:
        return False
    if difflib.SequenceMatcher(None, a["title"].lower(), b["title"].lower()).ratio() < 0.9:
        return False
    return bool({a["_fa"], a["_la"]} - {""} & {b["_fa"], b["_la"]} - {""})


def is_oa(r: dict[str, Any]) -> bool:
    return as_bool(r.get("is_oa")) or bool(r.get("arxiv_id")) or bool(r.get("preprint_oa_url"))


def rank_key(r: dict[str, Any]) -> tuple[Any, ...]:
    s = r["_s"]
    year = int(r.get("year") or 0)
    cites = float(r.get("cited_by_count") or 0) / max(1, 2027 - year) if year else 0.0
    return (-s["score"], not is_oa(r), not s.get("industrial"), not s.get("record_claim"), -year, -cites)


def family_key(r: dict[str, Any]) -> tuple[Any, ...]:
    return (VENUE_RANK.get(r.get("venue_type") or "other", 2), not is_oa(r), -r["_s"]["score"])


class ClassFill:
    """Per-class fill state: count, paywalled share cap and per-senior-author cap (D124, D125)."""

    def __init__(self, budget: int, cfg: dict[str, Any], selected: dict[str, dict[str, Any]]) -> None:
        self.budget = budget
        self.cfg = cfg
        self.selected = selected
        self.pw_cap = math.ceil((1 - cfg["oa_target_fraction"]) * budget)
        self.n = self.pw = 0
        self.per_author: Counter[str] = Counter()

    def full(self) -> bool:
        return self.n >= self.budget

    def ok(self, r: dict[str, Any], min_score: int) -> bool:
        if r["uid"] in self.selected or r["_s"]["score"] < min_score:
            return False
        if not is_oa(r) and (r["_s"]["score"] < self.cfg["paywalled_min_score"] or self.pw >= self.pw_cap):
            return False
        return not (r["_la"] and self.per_author[r["_la"]] >= self.cfg["max_per_senior_author"])

    def add(self, r: dict[str, Any], reason: str) -> None:
        self.selected[r["uid"]] = {**r, "_reason": reason}
        self.n += 1
        self.pw += not is_oa(r)
        if r["_la"]:
            self.per_author[r["_la"]] += 1


def paper_id(r: dict[str, Any], used: set[str]) -> str:
    authors = as_list(r.get("authors"))
    base = (surname(str(authors[0])) if authors else "") or "anon"
    base += str(r.get("year") or "")
    pid, i = base, 0
    while pid in used:
        pid = base + "abcdefghijklmnopqrstuvwxyz"[i % 26] * (1 + i // 26)
        i += 1
    used.add(pid)
    return pid


def load_curation() -> dict[str, list[dict[str, Any]]]:
    cur: dict[str, list[dict[str, Any]]] = {"picks": [], "drops": [], "reclass": []}
    d = CFG / "curation"
    for p in sorted(d.glob("*.yaml")) if d.exists() else []:
        y = yaml.safe_load(p.read_text()) or {}
        for k in cur:
            for item in y.get(k) or []:
                cur[k].append({**item, "_file": p.name})
    return cur


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    cfg = yaml.safe_load((CFG / "selection.yaml").read_text())
    budget: dict[str, int] = cfg["budget"]
    with RunLog("lit_select", dry_run=args.dry_run) as log:
        scores: dict[str, dict[str, Any]] = {}
        for p in sorted((LIT / "scoring").glob("out_G*_b*.jsonl")):
            for line in p.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    s = json.loads(line)
                    scores[s["uid"]] = s
        # metadata of every kept or scored record (G9 rescue rows are scored but not score_keep, D135)
        meta = {}
        with (LIT / "prefiltered.jsonl").open(encoding="utf-8") as f:
            for line in f:
                r = json.loads(line)
                if as_bool(r.get("score_keep")) or r["uid"] in scores:
                    meta[r["uid"]] = r
        log.info(f"kept records {len(meta)}, scored {len(scores)}, unscored {len(set(meta) - set(scores))}")
        cur = load_curation()
        drops = {d["uid"]: d for d in cur["drops"]}
        reclass = {d["uid"]: d for d in cur["reclass"]}
        stats: Counter[str] = Counter()
        adds_path = LIT / "curator_adds.jsonl"  # scripts/lit_curator_adds.py
        for line in adds_path.read_text(encoding="utf-8").splitlines() if adds_path.exists() else []:
            rec = json.loads(line)
            ca, uid = rec["curator_add"], rec["uid"]
            if uid not in scores:
                meta[uid] = {**rec, "score_keep": True}
                scores[uid] = {
                    "uid": uid, "classes": [ca["class"]], "subtypes": [ca["subtype"]] if ca["subtype"] else [],
                    "platform": "unstated", "band": "unstated", "score": 8, "c": {}, "industrial": False,
                    "record_claim": None, "is_review": False, "eo_modulator_main": False,
                    "rationale": f"curator add ({ca['group']}): {ca['reason']}"[:160],
                }  # fmt: skip
            cur["picks"].append(
                {"uid": uid, "class": ca["class"], "reason": f"add: {ca['reason']}", "_file": ca["group"]}
            )
            reclass.setdefault(uid, {"class": ca["class"], "subtype": ca["subtype"]})
            stats["curator_add"] += 1
        elig: list[dict[str, Any]] = []
        eo_rows: list[dict[str, Any]] = []
        excluded: list[tuple[dict[str, Any], dict[str, Any], str]] = []
        pick_cls = {p["uid"]: p.get("class") for p in cur["picks"]}
        pick_uids = set(pick_cls)
        for uid, s in scores.items():
            r = meta.get(uid)
            if r is None:
                stats["scored_not_kept"] += 1
                continue
            # EO-atlas candidates that the EO atlas has not ingested are not "known" (D139)
            if set(map(str, as_list(r.get("known_in")))) - {"eo_candidates"}:
                stats["known"] += 1
                continue
            picked = uid in pick_uids
            if uid in drops:
                stats["curator_drop"] += 1
                excluded.append((r, s, f"curator_drop: {drops[uid].get('reason', '')}"))
                continue
            if s.get("eo_modulator_main") and not picked:
                eo_rows.append({**r, "_s": s})
                stats["eo_modulator_main"] += 1
                excluded.append((r, s, "eo_modulator_main"))
                continue
            if not picked and (
                s.get("is_review") or s["c"].get("review") or s["c"].get("out_of_scope") or not s.get("classes")
            ):
                stats["review_or_out_of_scope"] += 1
                excluded.append((r, s, "out_of_scope" if s["c"].get("out_of_scope") else "review"))
                continue
            rc = reclass.get(uid)
            cls = rc["class"] if rc else (s.get("classes") or [pick_cls.get(uid)])[0]
            if picked and pick_cls.get(uid) and not rc:
                cls = pick_cls[uid] or cls
            sub = rc.get("subtype", "") if rc else ""
            if not sub:
                sub = next((x for x in s.get("subtypes") or [] if str(x).startswith(cls + ".")), f"{cls}.other")
            authors = as_list(r.get("authors"))
            elig.append({
                **r, "_s": s, "_cls": cls, "_sub": sub, "_tok": tokens(r.get("title") or ""),
                "_fa": surname(str(authors[0])) if authors else "", "_la": ascii_slug(str(r.get("last_author") or "")),
            })  # fmt: skip
        # 2. version families (within a class)
        by_cls: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for r in elig:
            by_cls[r["_cls"]].append(r)
        fams: list[list[dict[str, Any]]] = []
        for rows in by_cls.values():
            cls_fams: list[list[dict[str, Any]]] = []
            for r in rows:
                fam = next((fm for fm in cls_fams if any(same_work(r, o) for o in fm)), None)
                if fam is None:
                    cls_fams.append([r])
                else:
                    fam.append(r)
            fams.extend(cls_fams)
        best: list[dict[str, Any]] = []
        for fam in fams:
            fam.sort(key=lambda o: (o["uid"] not in pick_uids, *family_key(o)))
            head = fam[0]
            head["_family"] = len(fam)
            head["_alts"] = [o["uid"] for o in fam[1:]]
            best.append(head)
            stats["family_merged"] += len(fam) - 1
        threshold, pw_min = cfg["threshold"], cfg["paywalled_min_score"]
        picks_by_uid = {p["uid"]: p for p in cur["picks"]}
        selected: dict[str, dict[str, Any]] = {}
        alt_owner = {a: h["uid"] for h in best for a in h["_alts"]}

        reserve = cfg["reserve_curator_picks"]
        best_by_cls: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for r in best:
            best_by_cls[r["_cls"]].append(r)
        overflow_picks: list[dict[str, Any]] = []
        fills: dict[str, ClassFill] = {}
        for cls in sorted(budget):
            rows = sorted(best_by_cls.get(cls, []), key=rank_key)
            fill = fills[cls] = ClassFill(budget[cls], cfg, selected)
            for r in rows:
                cp = picks_by_uid.get(r["uid"]) or picks_by_uid.get(alt_owner.get(r["uid"], ""))
                if cp and r["uid"] not in selected:
                    if fill.n < fill.budget:
                        fill.add(r, f"curator: {cp.get('reason', '')}")
                    else:
                        overflow_picks.append({**r, "_cp": cp})
            subs = Counter(r["_sub"] for r in rows if r["_s"]["score"] >= cfg["floor_min_score"])
            for sub in sorted(subs):
                need = min(cfg["subtype_floor"], subs[sub]) - sum(1 for x in selected.values() if x["_sub"] == sub)
                for r in rows:
                    if need <= 0 or fill.full():
                        break
                    if r["_sub"] == sub and fill.ok(r, cfg["floor_min_score"]):
                        fill.add(r, f"subtype floor {sub}")
                        need -= 1
            have_pf = {x["_s"].get("platform") for x in selected.values() if x["_cls"] == cls}
            for r in rows:
                if len(have_pf - {"unstated", "other"}) >= cfg["min_platforms"] or fill.full():
                    break
                pf = r["_s"].get("platform")
                if pf not in have_pf and pf not in ("unstated", "other") and fill.ok(r, threshold):
                    fill.add(r, f"platform floor {pf}")
                    have_pf.add(pf)
            for r in rows:
                if fill.full():
                    break
                if fill.ok(r, threshold):
                    fill.add(r, "rank")
            stats[f"class_unfilled:{cls}"] = fill.budget - fill.n
            reserve += fill.budget - fill.n
        for r in overflow_picks:
            if reserve <= 0:
                break
            if r["uid"] not in selected:
                selected[r["uid"]] = {**r, "_reason": f"curator (reserve): {r['_cp'].get('reason', '')}"}
                reserve -= 1
        if cfg.get("fill_reserve_with_best", True):
            rest = sorted((r for r in best if r["uid"] not in selected), key=rank_key)
            extra: Counter[str] = Counter()
            frac = cfg.get("reserve_max_per_class_fraction", 0.5)
            for r in rest:
                if reserve <= 0:
                    break
                if extra[r["_cls"]] >= math.ceil(frac * budget[r["_cls"]]):
                    continue
                fl = fills[r["_cls"]]
                if r["_la"] and fl.per_author[r["_la"]] >= cfg["max_per_senior_author"]:
                    continue
                if r["_s"]["score"] >= threshold and (is_oa(r) or r["_s"]["score"] >= pw_min):
                    extra[r["_cls"]] += 1
                    if r["_la"]:
                        fl.per_author[r["_la"]] += 1
                    selected[r["uid"]] = {**r, "_reason": "reserve: best remaining"}
                    reserve -= 1
        missing_picks = [
            p for p in cur["picks"] if p["uid"] not in selected and alt_owner.get(p["uid"]) not in selected
        ]
        # outputs
        used: set[str] = set()
        rows_out = []
        for i, r in enumerate(sorted(selected.values(), key=lambda x: (x["_cls"], rank_key(x))), 1):
            s = r["_s"]
            authors = as_list(r.get("authors"))
            rows_out.append({
                "rank": i, "primary_class": r["_cls"], "subtype": r["_sub"], "classes": "|".join(s["classes"]),
                "uid": r["uid"], "doi": r.get("doi", ""), "arxiv_id": r.get("arxiv_id", ""),
                "paper_id": paper_id(r, used), "title": r.get("title", ""),
                "first_author": authors[0] if authors else "", "last_author": r.get("last_author", ""),
                "venue": r.get("venue", ""), "venue_type": r.get("venue_type", ""), "year": r.get("year", ""),
                "score": s["score"], "platform": s.get("platform", ""), "band": s.get("band", ""),
                "access": "oa" if is_oa(r) else "paywalled",
                "oa_url": r.get("preprint_oa_url") or r.get("oa_url") or "", "industrial": bool(s.get("industrial")),
                "record_claim": s.get("record_claim") or "", "selection_reason": r["_reason"],
                "family_size": r.get("_family", 1), "rationale": s.get("rationale", ""),
            })  # fmt: skip
        n_sel = len(rows_out)
        cls_n = Counter(x["primary_class"] for x in rows_out)
        oa_n = sum(x["access"] == "oa" for x in rows_out)
        log.info(f"selected {n_sel} (oa {oa_n}), stats {dict(stats)}")
        log.event("select", selected=n_sel, oa=oa_n, per_class=dict(cls_n), stats=dict(stats))
        if args.dry_run:
            for c in sorted(budget):
                log.info(f"  {c:22s} {cls_n.get(c, 0):4d} / {budget[c]}")
            return 0
        OUT.mkdir(parents=True, exist_ok=True)
        with (OUT / "cache_list.csv").open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS)
            w.writeheader()
            w.writerows(rows_out)
        with (OUT / "eo_atlas_candidates.csv").open("w", newline="", encoding="utf-8") as f:
            ew = csv.writer(f)
            ew.writerow(["uid", "title", "venue", "year", "score", "rationale"])
            for r in sorted(eo_rows, key=lambda x: -x["_s"]["score"]):
                ew.writerow([r["uid"], r.get("title", ""), r.get("venue", ""), r.get("year", ""), r["_s"]["score"],
                            r["_s"].get("rationale", "")])  # fmt: skip
        write_report(rows_out, budget, stats, len(meta), len(scores), missing_picks)
        write_review_files(elig, selected, excluded, alt_owner)
    return 0


def write_report(
    rows: list[dict[str, Any]],
    budget: dict[str, int],
    stats: Counter[str],
    n_kept: int,
    n_scored: int,
    missing_picks: list[dict[str, Any]],
) -> None:
    by = defaultdict(list)
    for x in rows:
        by[x["primary_class"]].append(x)
    lines = [
        "# Component-literature triage report (DevLog-006 S5)",
        "",
        "Generated by `scripts/lit_select.py` from LLM scores, curation overrides and `config/literature/selection.yaml`.",
        "",
        f"- prefilter-kept records: {n_kept}; scored: {n_scored}; selected: {len(rows)}; "
        f"OA: {sum(x['access'] == 'oa' for x in rows)}; paywalled: {sum(x['access'] != 'oa' for x in rows)}",
        "- exclusions and merges: "
        + ", ".join(f"{k} {v}" for k, v in sorted(stats.items()) if not k.startswith("class_")),
        "",
        "| class | budget | selected | OA | paywalled | subtypes | platforms | years | senior authors | median score |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for c in sorted(budget):
        xs = by.get(c, [])
        sc = sorted(x["score"] for x in xs)
        lines.append(
            f"| {c} | {budget[c]} | {len(xs)} | {sum(x['access'] == 'oa' for x in xs)} | "
            f"{sum(x['access'] != 'oa' for x in xs)} | {len({x['subtype'] for x in xs})} | "
            f"{len({x['platform'] for x in xs})} | {len({x['year'] for x in xs})} | "
            f"{len({x['last_author'] for x in xs})} | {sc[len(sc) // 2] if sc else ''} |"
        )
    reasons = Counter(x["selection_reason"].split(":")[0].split(" floor")[0] for x in rows)
    lines += ["", "Selection reasons: " + ", ".join(f"{k} {v}" for k, v in reasons.most_common()), ""]
    if missing_picks:
        lines += ["Curator picks not selected (not eligible or not scored):", ""]
        lines += [f"- {p['uid']} ({p['_file']}): {p.get('reason', '')}" for p in missing_picks]
    (OUT / "triage_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


REVIEW_FIELDS = [
    "status", "uid", "score", "subtype", "platform", "band", "access", "venue", "year", "first_author", "last_author",
    "institutions", "title", "rationale", "record_claim", "industrial", "selection_reason",
]  # fmt: skip


def write_review_files(
    elig: list[dict[str, Any]],
    selected: dict[str, dict[str, Any]],
    excluded: list[tuple[dict[str, Any], dict[str, Any], str]],
    alt_owner: dict[str, str],
) -> None:
    """Per-class curation inputs (S4): cache/literature/curation_inputs/<class>.csv (git-ignored, has no abstracts)."""
    d = LIT / "curation_inputs"
    d.mkdir(parents=True, exist_ok=True)
    rows: dict[str, list[dict[str, Any]]] = defaultdict(list)

    def row(r: dict[str, Any], s: dict[str, Any], status: str, sub: str, reason: str) -> dict[str, Any]:
        authors = as_list(r.get("authors"))
        return {
            "status": status, "uid": r["uid"], "score": s["score"], "subtype": sub, "platform": s.get("platform", ""),
            "band": s.get("band", ""), "access": "oa" if is_oa(r) else "paywalled", "venue": r.get("venue", ""),
            "year": r.get("year", ""), "first_author": authors[0] if authors else "",
            "last_author": r.get("last_author", ""), "institutions": "; ".join(map(str, as_list(r.get("institutions")))),
            "title": r.get("title", ""), "rationale": s.get("rationale", ""), "record_claim": s.get("record_claim") or "",
            "industrial": bool(s.get("industrial")), "selection_reason": reason,
        }  # fmt: skip

    for r in elig:
        if r["uid"] in selected:
            st, reason = "selected", selected[r["uid"]]["_reason"]
        elif r["uid"] in alt_owner:
            st, reason = "version_of", alt_owner[r["uid"]]
        else:
            st, reason = "not_selected", ""
        rows[r["_cls"]].append(row(r, r["_s"], st, r["_sub"], reason))
    for r, s, why in excluded:
        cls = (s.get("classes") or [r.get("best_class") or "unclassified"])[0]
        rows[cls].append(row(r, s, "excluded", "", why))
    order = {"selected": 0, "not_selected": 1, "version_of": 2, "excluded": 3}
    for cls, xs in rows.items():
        xs.sort(key=lambda x: (order[x["status"]], -x["score"]))
        with (d / f"{cls}.csv").open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=REVIEW_FIELDS)
            w.writeheader()
            w.writerows(xs)


if __name__ == "__main__":
    raise SystemExit(main())
