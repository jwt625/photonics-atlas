"""Build data/registry/org_events.csv + org_event_participants.csv and the web: rows of sources.csv.

Inputs: LIN canonical events (imported, basis imported_lineage, D22) and the researched events staged in
data/_staging/org_events/{A,B,C}/ (basis stated_in_source), with participants resolved only through
config/event_participant_map.yaml (no name matching). Orgs the map marks `create` are appended to organizations.csv
when their id does not exist (append-only). Event tables and web: source rows are regenerated on every run.

Usage: uv run python scripts/merge_org_events.py [--dry-run]
"""

from __future__ import annotations

import argparse
import sys
from typing import Any

import yaml

from photonics_atlas.adapters import lineage
from photonics_atlas.csvio import read_csv, split_list, write_csv
from photonics_atlas.paths import REGISTRY, ROOT, STAGING
from photonics_atlas.runlog import RunLog
from photonics_atlas.schema import columns
from photonics_atlas.textnorm import norm_key

LIN_ROLE = {
    "target": "target",
    "acquirer": "acquirer",
    "acquired_company": "target",
    "acquirer_parent": "acquirer",
    "predecessor_program": "predecessor",
    "successor_program": "successor",
    "parent_and_renamed_company": "merging",
    "merged_subsidiary": "merging",
    "resulting_name": "resulting",
}
GRADE_STATUS = {"A": "validated", "B": "validated", "C": "asserted", "D": "asserted", "X": "inferred"}
SOURCE_TYPE = {
    "regulatory_filing",
    "acquisition_filing",
    "official_press_release",
    "official_company_page",
    "reputable_technical_media",
    "news_media",
    "other",
}


def lin_events(log: RunLog) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    evs, parts = [], []
    names = {o.id: o.name for o in lineage.orgs()}
    for e in lineage.events():
        evs.append(
            {
                "event_id": e.id,
                "event_type": e.event_type,
                "name": e.name,
                "announced_on": e.announced_date or "",
                "effective_on": e.effective_date or "",
                "grade": e.grade,
                "status": GRADE_STATUS[e.grade],
                "basis": "imported_lineage",
                "source_ids": ";".join(f"lin:{s.source_id}" for s in e.sources),
                "locator": f"lin:canonical/events.yaml#{e.id}",
                "notes": e.notes or "",
            }
        )
        for p in e.participants:
            role = LIN_ROLE.get(p.role)
            if role is None:
                log.event("lin_role", "unknown", event=e.id, role=p.role)
                continue
            parts.append(
                {"event_id": e.id, "org_id": p.entity_id, "role": role, "printed_name": names.get(p.entity_id, "")}
            )
    return evs, parts


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    with RunLog("merge_org_events", args.dry_run) as log:
        with (ROOT / "config" / "event_participant_map.yaml").open() as f:
            cfg: dict[str, Any] = yaml.safe_load(f)
        pmap: dict[str, dict[str, Any]] = cfg["participants"]
        drop = {(a, b) for a, b in cfg.get("drop_participants", [])}
        exclude: dict[str, str] = cfg.get("exclude_events", {})
        dates: dict[str, dict[str, str]] = cfg.get("date_overrides", {})
        role_ov: dict[str, dict[str, str]] = cfg.get("role_overrides", {})
        specs = {m["org"]: m["create"] for m in pmap.values() if m.get("create")}
        orgs = read_csv(REGISTRY / "organizations.csv")
        have = {o["org_id"] for o in orgs}
        name2id = {norm_key(o["name"]): o["org_id"] for o in orgs if o["no_name_match"] != "true"}
        created: dict[str, dict[str, str]] = {}
        evs, parts = lin_events(log)
        web_sources: dict[str, dict[str, str]] = {}
        for g in ("A", "B", "C"):
            d = STAGING / "org_events" / g
            for s in read_csv(d / "sources_proposed.csv"):
                sid = s["source_key"] if s["source_key"].startswith("web:") else f"web:{s['source_key']}"
                if sid in web_sources and web_sources[sid]["url"] != s["url"]:
                    raise SystemExit(f"source key collision {sid} between groups")
                st = s["source_type"] if s["source_type"] in SOURCE_TYPE else "other"
                web_sources[sid] = {
                    "source_id": sid,
                    "corpus": "web",
                    "native_id": sid.removeprefix("web:"),
                    "title": s["title"],
                    "published_on": s["published_on"],
                    "year": s["published_on"][:4],
                    "venue": s["publisher"],
                    "url": s["url"],
                    "source_type": st,
                    "access": "public_web",
                    "redistribution": "unknown",
                    "evidence_grade": s["evidence_grade"],
                    "accessed_on": s["accessed_on"],
                    "notes": "; ".join(x for x in (s["notes"], f"researched by org-events group {g}") if x),
                }
            for e in read_csv(d / "events_proposed.csv"):
                key = e["event_key"]
                if key in exclude:
                    log.event("event", "excluded", key=key, reason=exclude[key])
                    continue
                eid = f"event_{key}"
                ov = dates.get(key, {})
                note = e["notes"]
                if ov:
                    note = "; ".join(x for x in (note, f"date override (config/event_participant_map.yaml): {ov}") if x)
                evs.append(
                    {
                        "event_id": eid,
                        "event_type": e["event_type"],
                        "name": key.replace("_", " "),
                        "announced_on": ov.get("announced_on", e["announced_on"]),
                        "effective_on": ov.get("effective_on", e["effective_on"]),
                        "grade": e["grade"],
                        "status": e["status"],
                        "basis": "stated_in_source",
                        "source_ids": ";".join(
                            s if s.startswith("web:") else f"web:{s}" for s in split_list(e["source_keys"])
                        ),
                        "locator": e["locator"],
                        "notes": note,
                    }
                )
                for p in split_list(e["participants"]):
                    name, role = p.rsplit("|", 1)
                    if (key, name) in drop:
                        continue
                    if e["event_type"] == "merger" and role in ("acquirer", "target"):
                        role = "merging"
                    role = role_ov.get(key, {}).get(name, role)
                    m = pmap.get(name)
                    if m is None:
                        raise SystemExit(
                            f"participant {name!r} of {key} missing from config/event_participant_map.yaml"
                        )
                    oid = m["org"]
                    spec = specs.get(oid)
                    if oid not in have and oid not in created and spec and not spec.get("no_name_match"):
                        # The org may already exist under another id (e.g. created by OFC curation): exact name key only.
                        same = name2id.get(norm_key(spec["name"]))
                        if same:
                            log.event("participant", "reused_existing", name=name, planned=oid, existing=same)
                            oid = same
                    if oid not in have and oid not in created:
                        c = specs.get(oid)
                        if not c:
                            raise SystemExit(f"{oid} for {name!r} does not exist and has no create spec")
                        created[oid] = {
                            "org_id": oid,
                            "name": c["name"],
                            "name_basis": "cited_source",
                            "name_source": e["source_keys"].split(";")[0],
                            "org_type": c["org_type"],
                            "status": c["status"],
                            "origin": "web",
                            "no_name_match": "true" if c.get("no_name_match") else "",
                            "notes": f"created from org event {eid} (config/event_participant_map.yaml)",
                        }
                        log.event("org", "new", org_id=oid, name=c["name"], event=eid)
                    dup = next((q for q in parts if (q["event_id"], q["org_id"], q["role"]) == (eid, oid, role)), None)
                    if dup:
                        dup["printed_name"] += f" | {name}"
                        continue
                    parts.append({"event_id": eid, "org_id": oid, "role": role, "printed_name": name})
        # Give each staged event a readable name from its participants.
        by_ev: dict[str, list[dict[str, str]]] = {}
        for pp in parts:
            by_ev.setdefault(pp["event_id"], []).append(pp)
        for e in evs:
            if e["basis"] == "stated_in_source":
                ps = by_ev.get(e["event_id"], [])
                e["name"] = f"{e['event_type'].replace('_', ' ')}: " + "; ".join(
                    f"{q['printed_name']} ({q['role']})" for q in ps
                )
        log.info(
            f"events {len(evs)} (lin {sum(e['basis'] == 'imported_lineage' for e in evs)}), participants {len(parts)}, "
            f"new orgs {len(created)}, web sources {len(web_sources)}"
        )
        # Keep only web sources an event cites (uncited staged sources stay in staging, e.g. P2 product evidence).
        cited = {sid for e in evs for sid in split_list(e["source_ids"])}
        dropped = sorted(set(web_sources) - cited)
        web_sources = {k: v for k, v in web_sources.items() if k in cited}
        log.info(f"web sources cited {len(web_sources)}, uncited dropped {len(dropped)}: {dropped}")
        # Preserve events added to the registry by hand (ids produced by neither LIN nor staging) with participants.
        produced = {e["event_id"] for e in evs}
        old_ev = read_csv(REGISTRY / "org_events.csv") if (REGISTRY / "org_events.csv").exists() else []
        old_pa = (
            read_csv(REGISTRY / "org_event_participants.csv")
            if (REGISTRY / "org_event_participants.csv").exists()
            else []
        )
        kept = [e for e in old_ev if e["event_id"] not in produced]
        kept_ids = {e["event_id"] for e in kept}
        evs += kept
        parts += [p for p in old_pa if p["event_id"] in kept_ids]
        if kept:
            log.info(f"hand-added events preserved: {sorted(kept_ids)}")
        if args.dry_run:
            return 0
        evs.sort(key=lambda r: r["event_id"])
        parts.sort(key=lambda r: (r["event_id"], r["role"], r["org_id"]))
        write_csv(REGISTRY / "org_events.csv", columns("org_events"), evs)
        write_csv(REGISTRY / "org_event_participants.csv", columns("org_event_participants"), parts)
        if created:
            write_csv(
                REGISTRY / "organizations.csv",
                columns("organizations"),
                [*orgs, *sorted(created.values(), key=lambda r: r["org_id"])],
            )
        if not (REGISTRY / "sources.csv").exists():
            raise SystemExit("data/registry/sources.csv missing: run scripts/build_sources.py first (README order)")
        src = read_csv(REGISTRY / "sources.csv")
        write_csv(
            REGISTRY / "sources.csv",
            columns("sources"),
            [*(s for s in src if s["corpus"] != "web"), *web_sources.values()],
        )
        log.info(
            "wrote org_events.csv, org_event_participants.csv, organizations.csv (+created), sources.csv (web rows)"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
