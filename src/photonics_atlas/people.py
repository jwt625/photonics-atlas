"""People atlas core (DevLog-004, D61-D70): author slots, identity merge, review queue, observations, person ids.

Identity unit = one author slot (EO paper_authors row, PK paper x author_index, OFC authors_json element) or one LIN
person (D62). Slots join only under D63 (ORCID; exact name + shared org; compatible name + shared org + shared
coauthor) with D62 constraints (never two EO persons, two LIN persons, two ORCIDs or two slots of one source in one
person). Everything else that looks like the same name goes to the local review queue (D64).
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from .adapters import ofc, pk
from .csvio import read_csv, split_list
from .paths import CROSSWALK, REGISTRY, ROOT, input_path
from .textnorm import ascii_fold, strip_emails

# Family names too common for a name match alone: eo-modulator-atlas scripts/build_people.py COMMON (68 names, DevLog-020
# decision 2), extended by data (D63, D91): COMMON_MIN_KEYS distinct full-name keys, or COMMON_MIN_SLOTS author slots,
# across all inputs.
EO_COMMON = set(
    """zhang wang li liu chen yang huang zhao wu zhou xu sun ma zhu hu guo he lin gao luo zheng liang xie song tang han
    feng deng cao peng zeng xiao tian dong pan yuan cai jiang yu du ye cheng wei su lu ding ren shen yao jin
    kim lee park choi jung kang cho yoon jang lim nguyen tran le pham singh kumar sharma patel""".split()
)
COMMON_MIN_KEYS = 8
COMMON_MIN_SLOTS = 10  # D91; 0 = off
COMMON_SLOT_MIN_KEYS = 3  # D96: the slot rule also needs >= 3 distinct full-name keys
HUB_MIN_SOURCES = 10  # D92; 0 = off
DENSE_COUNTRIES = {"CN", "TW", "HK", "MO", "JP", "KR", "SG"}
DENSE_SHARE = 0.5  # D91; 0 = off
DENSE_FAM_KEYS = 2  # D96: ambiguity in the data (distinct full-name keys per family name)
DENSE_GIVEN_KEYS = 2  # D96: ... and per given name
SUFFIXES = {"jr", "sr", "ii", "iii", "iv"}
# eo-modulator-atlas scripts/build_people.py DUPLICATE_ORCID (one person registered twice in ORCID, reviewed in EO
# DevLog-022): duplicate -> kept iD. tests/test_people.py checks this copy against the EO file.
EO_DUPLICATE_ORCID = {"0009-0007-1328-1082": "0000-0003-3859-1558"}
# Spelled-out e-mail addresses ("x at y dot edu", "x [at] y [dot] edu"), beyond textnorm.EMAIL_RE (C2).
_AT = r"(?:\s+at\s+|\s*\[\s*at\s*\]\s*|\s*\(\s*at\s*\)\s*|\s*<\s*at\s*>\s*|\s*\uff20\s*)"
_DOT = r"(?:\s+dot\s+|\s*\[\s*dot\s*\]\s*|\s*\(\s*dot\s*\)\s*|\s*<\s*dot\s*>\s*|\.)"
# Spelled-out or full-width e-mail addresses ("x at y dot edu", "x [at] y.edu", "x at y.edu", full-width at sign),
# beyond textnorm.EMAIL_RE (C2, D97).
SPELLED_EMAIL_RE = re.compile(rf"[\w.+-]+{_AT}[\w-]+(?:{_DOT}[\w-]+)*{_DOT}[a-z]{{2,24}}\b", re.IGNORECASE)
BASIS_RANK = {"origin": 0, "orcid": 1, "exact_name_shared_org": 2, "compatible_name_shared_org_coauthor": 3}
UNI_TYPES = {"university", "academic_lab"}


# ---------------------------------------------------------------- names


def fold(name: str) -> str:
    """ASCII lower case; parenthesized nicknames dropped; hyphen inside a name joins (Safavi-Naeini), between
    initials it separates (K.-Y.); every other non-letter becomes a space (EO build_people.fold + D63)."""
    s = re.sub(r"\([^)]*\)", " ", strip_emails(name))
    s = ascii_fold(s).lower()
    s = re.sub(r"(?<=[a-z]{2})-(?=[a-z]{2})", "", s)
    return " ".join(re.sub(r"[^a-z\s]", " ", s).split())


@dataclass(frozen=True)
class Name:
    """A parsed printed name (D63 as amended by D90).

    given: folded given tokens (hyphenated syllables joined, the key form); capital runs of 2-3 letters in a name that
    has lower-case letters ("QT", "XY") are initials, one token per letter. inits: one initial per syllable of a full
    given name and per initial ("Qai-Tun" and "Q. T." both give q, t). lead: the full given syllables before the
    first initial ("Xo-Ya" -> xo, ya; "Jon E." -> jon). Examples are fictitious."""

    given: tuple[str, ...]
    fam: str
    inits: tuple[str, ...] = ()
    lead: tuple[str, ...] = ()
    fulls: tuple[str, ...] = ()  # every full given name (joined form), lead or not
    tail: tuple[str, ...] = ()  # full given names printed after an initial ("J. Y. Gene" -> gene)

    @property
    def abbreviated(self) -> bool:
        return not self.lead

    @property
    def mono(self) -> bool:
        """One full given name of one syllable and nothing else ("Qing")."""
        return len(self.given) == 1 and len(self.lead) == 1


def parse(name: str) -> Name:
    s = ascii_fold(re.sub(r"\([^)]*\)", " ", strip_emails(name)))
    has_lower = any(c.islower() for c in s)
    raw = [t for t in re.sub(r"[^A-Za-z\s-]", " ", s).split() if t.strip("-").lower() not in SUFFIXES]
    raw = [t for t in raw if t.strip("-")]
    if not raw:
        return Name((), "")
    fam = "".join(p.lower() for p in raw[-1].split("-") if p)
    given: list[str] = []
    inits: list[str] = []
    lead: list[str] = []
    fulls: list[str] = []
    tail: list[str] = []
    open_lead = True
    for tok in raw[:-1]:
        parts = [p for p in tok.split("-") if p]
        units: list[list[str]] = []  # each unit: syllables (len 1 and 1 letter = an initial)
        if len(parts) > 1 and all(len(p) >= 2 for p in parts):
            units.append(parts)
        else:
            for p in parts:
                if has_lower and p.isupper() and 2 <= len(p) <= 3:
                    units.extend([[c] for c in p])
                else:
                    units.append([p])
        for u in units:
            syl = [x.lower() for x in u]
            given.append("".join(syl))
            inits.extend(x[0] for x in syl)
            if len(syl) == 1 and len(syl[0]) == 1:
                open_lead = False
                continue
            fulls.append("".join(syl))
            if open_lead:
                lead.extend(syl)
            else:
                tail.append("".join(syl))
    return Name(tuple(given), fam, tuple(inits), tuple(lead), tuple(fulls), tuple(tail))


def tokens(name: str) -> tuple[tuple[str, ...], str]:
    n = parse(name)
    return n.given, n.fam


def _lead_ok(a: tuple[str, ...], b: tuple[str, ...]) -> bool:
    """Leading full given names agree: same letters, or the shorter ends on a syllable boundary of the longer
    ("Jon" ~ "Jon Edgar", "Qaitun" ~ "Qai-Tun"; not "Hiro" ~ "Hirotaka", not "Qeng-Qi" ~ "Qeng-Qieh"; fictitious)."""
    sa, sb = "".join(a), "".join(b)
    if sa == sb:
        return True
    (s, _), (lng, lt) = sorted([(sa, a), (sb, b)], key=lambda x: len(x[0]))
    bounds = {sum(len(x) for x in lt[: k + 1]) for k in range(len(lt))}
    return lng.startswith(s) and len(s) in bounds


def compatible(a: Name, b: Name, common: bool = False) -> bool:
    """Same family name; the full initials sequences agree (one a prefix of the other); leading full given names agree
    where both have one (D90); a full given name printed after an initial must be one of the other side's full given
    names when it has any (D95: "J. Y. Gene" !~ "Jon"); for common family names a one-syllable full given name is not
    compatible with two or more initials (D95: "Qing" !~ "Q. T."). Two non-abbreviated names whose given names join to
    the same letters (hyphen, camel-case or spacing variants: "Qaitun" ~ "Qai-Tun" ~ "QaiTun" ~ "Qai Tun") are
    compatible before the D95 checks (D211). Examples are fictitious."""
    if a.fam != b.fam or not a.inits or not b.inits:
        return False
    # D211: one spelling of the same full given names (no initials on either side); D95 is about initials
    if a.given == a.fulls and b.given == b.fulls and "".join(a.given) == "".join(b.given):
        return True
    if any(x != y for x, y in zip(a.inits, b.inits, strict=False)):
        return False
    for x, y in ((a, b), (b, a)):
        if x.tail and y.fulls and not set(x.tail) <= set(y.fulls):
            return False
        if common and x.mono and len(y.inits) >= 2:
            return False
    return not (a.lead and b.lead) or _lead_ok(a.lead, b.lead)


def names_compatible(xs: Iterable[Name], ys: Iterable[Name], common: Iterable[str] = ()) -> bool:
    """Two records' name sets agree: every family name they share has a compatible variant pair."""
    xs, ys, cs = list(xs), list(ys), set(common)
    for f in {x.fam for x in xs} & {y.fam for y in ys}:
        if not any(compatible(x, y, f in cs) for x in xs if x.fam == f for y in ys if y.fam == f):
            return False
    return True


def full_key(n: Name) -> str:
    """Exact full-name key; empty for initial-abbreviated or single-token names."""
    return "" if n.abbreviated or not n.fam else " ".join((*n.given, n.fam))


def name_key(name: str) -> str:
    n = parse(name)
    return " ".join((*n.given, n.fam))


def completeness(name: str) -> tuple[int, int]:
    return sum(len(t) > 1 for t in fold(name).split()), len(name)


# ---------------------------------------------------------------- slots


@dataclass
class Aff:
    """One affiliation row of a slot (EO/PK row or the OFC element). OFC header rows (D214) carry their own obs id,
    printed name, kind and grade; the slot's identity fields are not taken from them (D217)."""

    order: int
    printed_org: str
    org_ids: list[str]
    unit: str
    country: str
    role: str
    locator: str
    oid: str = ""  # D214: explicit obs id (OFC header rows); empty = derived from source, author index and order
    printed_name: str = ""  # D218: header printed form (observation and alias only)
    kind: str = ""
    grade: str = ""


@dataclass
class Slot:
    sid: str  # <source_id>#<author_index>, or lin:<person_id>
    corpus: str  # eo | pk | ofc2026 | lin
    source_id: str  # canonical source id ('' for lin)
    index: int
    names: list[str]  # printed name first; LIN: name + romanized aliases
    variants: list[Name] = field(default_factory=list)
    roots: frozenset[str] = frozenset()
    lineages: frozenset[str] = frozenset()  # identity org keys: roots + direct org-event links (D63)
    coauthor_names: list[str] = field(default_factory=list)
    coauthors: frozenset[str] = frozenset()
    selfkeys: frozenset[str] = frozenset()
    orcid: str = ""
    eo_pid: str = ""
    lin_id: str = ""
    active_on: str = ""
    kind: str = ""  # publication | conference
    affs: list[Aff] = field(default_factory=list)
    lin: dict[str, Any] = field(default_factory=dict)
    hdr: list[Aff] = field(default_factory=list)  # D214: OFC header rows of this slot (observations only, D217)
    hdr_status: str = ""  # D215: confirmed | conflict | unmapped ('' = no header rows)

    @property
    def name(self) -> str:
        return self.names[0]


@dataclass
class Inputs:
    slots: list[Slot]
    orgs: dict[str, dict[str, str]]
    sources: dict[str, dict[str, str]]
    common: set[str]
    dropped: Counter[str]
    hubs: frozenset[str] = frozenset()
    dense: frozenset[str] = frozenset()
    headers: Counter[str] = field(default_factory=Counter)  # D214: header merge counts
    committed: dict[str, str] = field(default_factory=dict)  # D219d: slot id -> person id in data/people/ tables


def org_root(orgs: dict[str, dict[str, str]], oid: str) -> str:
    seen = {oid}
    cur = oid
    while orgs.get(cur, {}).get("parent_org_id"):
        nxt = orgs[cur]["parent_org_id"]
        if nxt in seen:
            break
        seen.add(nxt)
        cur = nxt
    return cur


def org_lineages(orgs: dict[str, dict[str, str]]) -> dict[str, frozenset[str]]:
    """Root org -> identity org keys: the root itself plus one key per org event (rename, merger, acquisition,
    spin-off, team formation) it takes part in. Two slots share an org when their keys intersect: same root, or
    roots that are direct participants of one event (no transitive chains). Identity support only (D63); transitions
    keep roots and label such pairs as continuations (D68)."""
    keys: dict[str, set[str]] = defaultdict(set)
    for o in orgs:
        r = org_root(orgs, o)
        keys[r].add(r)
    for p in read_csv(REGISTRY / "org_event_participants.csv"):
        if p["org_id"] in orgs:
            keys[org_root(orgs, p["org_id"])].add("event:" + p["event_id"])
    return {r: frozenset(k) for r, k in keys.items()}


def _crosswalk() -> dict[tuple[str, str], list[str]]:
    return {(r["corpus"], r["printed"]): split_list(r["org_ids"]) for r in read_csv(CROSSWALK / "org_crosswalk.csv")}


def clean_text(s: str) -> str:
    return " ".join(SPELLED_EMAIL_RE.sub(" ", strip_emails(s or "")).split())


def _eo_slots(
    sources: dict[str, dict[str, str]],
    xw: dict[tuple[str, str], list[str]],
    ofc_dates: dict[str, str],
    notes: Counter[str] | None = None,
) -> list[Slot]:
    root = input_path("eo_atlas")
    data = root / "data"
    people = {r["person_id"]: r for r in read_csv(data / "people.csv")}
    papers = {r["paper_id"]: r for r in read_csv(data / "papers.csv")}
    # OFC 2026 papers in EO: the ofc2026 duplicate row gives the session date (D67).
    dup_date = {
        s["same_as"][3:]: ofc_dates.get(s["native_id"], "")
        for s in sources.values()
        if s["corpus"] == "ofc2026" and s["same_as"].startswith("eo:")
    }
    affs: dict[tuple[str, int], list[dict[str, str]]] = defaultdict(list)
    for r in read_csv(data / "author_affiliations.csv"):
        affs[(r["paper_id"], int(r["author_index"]))].append(r)
    by_paper: dict[str, list[dict[str, str]]] = defaultdict(list)
    for r in read_csv(data / "paper_authors.csv"):
        by_paper[r["paper_id"]].append(r)
    out = []
    orcid_mismatch: list[str] = []
    for pid, rows in by_paper.items():
        p = papers[pid]
        names = split_list(p["authors"])
        cr: list[dict[str, Any]] = []
        crp = root / "references" / pid / "crossref.json"
        if crp.exists():
            m = json.loads(crp.read_text())
            cr = (m.get("message", m).get("author") or []) if isinstance(m, dict) else []
        date = p["published_on"] or dup_date.get(pid, "") or p["year"]
        allnames = [clean_text(r["author"]) for r in rows]
        for k_self, r in enumerate(rows):
            i = int(r["author_index"])
            person = people[r["person_id"]]
            orcid = ""
            if person["orcid"] and len(cr) == len(names) and 0 < i <= len(cr):
                a = cr[i - 1]
                if tokens(str(a.get("family", "")))[1] == tokens(names[i - 1])[1] and a.get("ORCID"):
                    got = str(a["ORCID"]).rsplit("/", 1)[-1]
                    if EO_DUPLICATE_ORCID.get(got, got) == person["orcid"]:  # I3: the slot's own iD, EO duplicate map
                        orcid = person["orcid"]
                    else:
                        orcid_mismatch.append(f"eo:{pid}#{i}")
            sl = Slot(
                sid=f"eo:{pid}#{i}",
                corpus="eo",
                source_id=f"eo:{pid}",
                index=i,
                names=[clean_text(r["author"])],
                coauthor_names=[n for k, n in enumerate(allnames) if k != k_self],
                orcid=orcid,
                eo_pid=r["person_id"],
                active_on=date,
                kind="publication",
            )
            for a in sorted(affs.get((pid, i), []), key=lambda x: int(x["aff_order"])):
                sl.affs.append(
                    Aff(
                        order=int(a["aff_order"]),
                        printed_org=clean_text(a["org_name"]),
                        org_ids=xw.get(("eo", a["org_name"]), []),
                        unit=clean_text(a["unit"]),
                        country=a["country"],
                        role=a["kind"],
                        locator=clean_text(a["locator"]),
                    )
                )
            out.append(sl)
    if notes is not None and orcid_mismatch:
        notes["eo: Crossref ORCID differs from the EO person iD (slot ORCID not set)"] += len(orcid_mismatch)
    return out


def _pk_slots(xw: dict[tuple[str, str], list[str]]) -> list[Slot]:
    years = {p.paper_id: str(p.year) for p in pk.papers()}
    by_slot: dict[tuple[str, int], list[pk.PkAffiliation]] = defaultdict(list)
    for a in pk.affiliations():
        by_slot[(a.paper_id, a.author_index)].append(a)
    authors: dict[str, dict[int, str]] = defaultdict(dict)
    for (pid, i), rows in by_slot.items():
        authors[pid][i] = clean_text(rows[0].author)
    out = []
    for (pid, i), rows in by_slot.items():
        sl = Slot(
            sid=f"pk:{pid}#{i}",
            corpus="pk",
            source_id=f"pk:{pid}",
            index=i,
            names=[authors[pid][i]],
            coauthor_names=[n for k, n in sorted(authors[pid].items()) if k != i],
            active_on=years[pid],
            kind="publication",
        )
        for a in sorted(rows, key=lambda x: x.aff_order):
            sl.affs.append(
                Aff(
                    order=a.aff_order,
                    printed_org=clean_text(a.org_name),
                    org_ids=xw.get(("pk", a.org_name), []),
                    unit=clean_text(a.unit),
                    country=a.country,
                    role=a.kind,
                    locator=clean_text(a.locator),
                )
            )
        out.append(sl)
    return out


def _ofc_slots(xw: dict[tuple[str, str], list[str]], pres: list[ofc.OfcPresentation]) -> list[Slot]:
    out = []
    for p in pres:
        names = [clean_text(a.name) for a in p.authors]
        for a in p.authors:
            out.append(
                Slot(
                    sid=f"ofc2026:{p.code}#{a.index}",
                    corpus="ofc2026",
                    source_id=f"ofc2026:{p.code}",
                    index=a.index,
                    names=[clean_text(a.name)],
                    coauthor_names=[n for k, n in enumerate(names) if k != a.index - 1],
                    active_on=p.session_date,
                    kind="conference",
                    affs=[
                        Aff(
                            order=1,
                            printed_org=clean_text(a.affiliation),
                            org_ids=xw.get(("ofc2026", a.affiliation), []),
                            unit="",
                            country="",
                            role="primary",
                            locator=f"program metadata authors_json #{a.index}",
                        )
                    ],
                )
            )
    return out


def _lin_slots() -> list[Slot]:
    root = input_path("lineage") / "canonical"
    with (root / "people.yaml").open() as f:
        people: list[dict[str, Any]] = yaml.safe_load(f)["people"]
    with (root / "edges.yaml").open() as f:
        edges: list[dict[str, Any]] = yaml.safe_load(f)["edges"]
    orgs_of: dict[str, set[str]] = defaultdict(set)
    for e in edges:
        if str(e["source_id"]).startswith("person_") and str(e["target_id"]).startswith("org_"):
            orgs_of[e["source_id"]].add(e["target_id"])
    out = []
    for p in people:
        names = [p["name"]] + [a["name"] for a in p.get("aliases") or [] if len(fold(a["name"]).split()) >= 2]
        lin_orgs = set(orgs_of[p["id"]])
        if p.get("current_organization_id"):
            lin_orgs.add(p["current_organization_id"])
        out.append(
            Slot(
                sid=f"lin:{p['id']}",
                corpus="lin",
                source_id="",
                index=0,
                names=names,
                lin_id=p["id"],
                lin=p,
                affs=[Aff(0, "", sorted(lin_orgs), "", "", "", "")],
            )
        )
    return out


# ---------------------------------------------------------------- OFC 2026 paper headers (DevLog-008, D214-D219)

HEADER_ALIAS_NOTE = "OFC paper header form; not used for identity (D218)"
HEADERS_REL = Path("data") / "_staging" / "people" / "ofc_headers"
HEADER_STAMP = "check_stamp.txt"
HEADER_GRADE_B = {"listing_order", "layout"}  # D240 / D246: grade B marker bases; every other basis is grade A
SLOT_OF_OBS_RE = re.compile(r"^(.+#a\d+)\.")  # obs id -> '<source_id>#a<author_index>'
HEADER_ID_RE = re.compile(r"#a(\d+)\.h(\d+)\.(\d+)\.m(\d+)$")  # D219e


def header_batches(root: Path = ROOT) -> tuple[list[Path], list[Path]]:
    """Batch directories whose derived files belong to the current headers.yaml (D248 stamp), and the stale ones."""
    base = root / HEADERS_REL
    ok: list[Path] = []
    stale: list[Path] = []
    for d in sorted(x for x in base.iterdir() if x.is_dir()) if base.exists() else []:
        st, yp = d / HEADER_STAMP, d / "headers.yaml"
        if not (d / "header_rows.csv").exists():
            continue
        good = st.exists() and yp.exists()
        good = good and st.read_text(encoding="utf-8").split()[-1] == hashlib.sha256(yp.read_bytes()).hexdigest()
        (ok if good else stale).append(d)
    return ok, stale


def header_rows(root: Path = ROOT) -> list[dict[str, str]]:
    """Staged OFC header rows of every current batch (DevLog-008 D171; one row per slot x affiliation x org)."""
    ok, _ = header_batches(root)
    return [r for d in ok for r in read_csv(d / "header_rows.csv")]


def header_obs_id(r: dict[str, str]) -> str:
    """D214: own namespace, so committed metadata ids keep their meaning (D10). Base id of a header row; each
    observation adds '.m<n>' (D219e: n = position of the registry org in the row's org list, always present, 1 for an
    unmapped or single org), so a later one-to-several mapping adds ids and never renames one."""
    return f"{r['source_id']}#a{r['author_index']}.h{r['aff_order']}.{r['org_k']}"


def header_status(
    meta_ids: Iterable[str],
    meta_printed: str,
    rows: list[dict[str, str]],
    orgs: dict[str, dict[str, str]],
) -> str:
    """D215: does the paper header confirm the metadata affiliation of a slot? Read from the rows (batch audit S4),
    on registry roots with the crosswalk current at build time. confirmed: every metadata root is among the header
    roots (present addresses and joint-printed orgs included), or the folded metadata string equals a printed header
    org ("org" or "unit, org") and the metadata org is unmapped or shares a root with a header row (D219a); conflict: both sides mapped, not confirmed, and every header org string mapped;
    unmapped: anything else (one side has no registry id)."""
    printed = {fold(r["org_name"]) for r in rows} | {fold(f"{r['unit']}, {r['org_name']}") for r in rows if r["unit"]}
    meta = set(meta_ids)
    hdr = {o for r in rows for o in split_list(r["org_ids"])}
    meta_roots, hdr_roots = {org_root(orgs, o) for o in meta}, {org_root(orgs, o) for o in hdr}
    if meta and hdr and meta_roots <= hdr_roots:
        return "confirmed"
    # D219a: a folded-name match confirms only when the metadata org is unmapped or a header row carries one of its
    # roots; fold() drops parenthesized text, so a mapped metadata org is never replaced by an unmapped header string
    if meta_printed and fold(meta_printed) in printed and (not meta or meta_roots & hdr_roots):
        return "confirmed"
    if meta and hdr and all(r["org_ids"] for r in rows):
        return "conflict"
    return "unmapped"


def committed_slots(root: Path = ROOT) -> dict[str, str]:
    """D219d: slot id -> person id in the committed people tables (observations by slot; LIN persons by lin_id)."""
    d = root / "data" / "people"
    out: dict[str, str] = {}
    obs, xref = d / "affiliation_observations.csv", d / "person_xref.csv"
    for r in read_csv(obs) if obs.exists() else []:
        m = SLOT_OF_OBS_RE.match(r["obs_id"])
        if m:
            src, i = m.group(1).rsplit("#a", 1)
            out.setdefault(f"{src}#{i}", r["person_id"])
    for x in read_csv(xref) if xref.exists() else []:
        if x["scheme"] == "lin_id":
            out[f"lin:{x['value']}"] = x["person_id"]
    return out


def attach_headers(slots: list[Slot], rows: list[dict[str, str]], orgs: dict[str, dict[str, str]]) -> Counter[str]:
    """D214-D218: header rows become extra observations of their OFC metadata slot (D62: the slot is the identity
    unit; identity names and org keys stay the metadata ones, D217)."""
    by_slot: dict[str, list[dict[str, str]]] = defaultdict(list)
    for r in rows:
        by_slot[f"{r['source_id']}#{r['author_index']}"].append(r)
    stats: Counter[str] = Counter()
    seen: set[str] = set()
    for s in slots:
        rs = by_slot.get(s.sid)
        if s.corpus != "ofc2026" or not rs:
            continue
        seen.add(s.sid)
        rs = sorted(rs, key=lambda r: (int(r["aff_order"]), int(r["org_k"])))
        for r in rs:
            s.hdr.append(
                Aff(
                    order=int(r["aff_order"]),
                    printed_org=r["org_name"],
                    org_ids=split_list(r["org_ids"]),
                    unit=r["unit"],
                    country=r["country"],
                    role=r["aff_role"],
                    locator=r["locator"],
                    oid=header_obs_id(r),
                    printed_name=clean_text(r["printed_name"]),
                    kind="publication",
                    grade=r["evidence_grade"],
                )
            )
        meta = s.affs[0]
        s.hdr_status = header_status(meta.org_ids, meta.printed_org, rs, orgs)
        stats[f"slots {s.hdr_status}"] += 1
        for r in rs:
            stats[f"rows grade {r['evidence_grade']}"] += 1
    stats["rows without a kept OFC slot (EO duplicate or not in the registry)"] = sum(
        len(v) for k, v in by_slot.items() if k not in seen
    )
    return +stats


def load_inputs() -> Inputs:
    orgs = {r["org_id"]: r for r in read_csv(REGISTRY / "organizations.csv")}
    sources = {r["source_id"]: r for r in read_csv(REGISTRY / "sources.csv")}
    xw = _crosswalk()
    pres = ofc.presentations()
    dropped: Counter[str] = Counter()
    eo = _eo_slots(sources, xw, {p.code: p.session_date for p in pres}, dropped)
    slots = eo + _pk_slots(xw) + _ofc_slots(xw, pres)
    kept = []
    for s in slots:
        src = sources.get(s.source_id)
        if src is None:
            dropped[f"{s.corpus}: source not in registry"] += 1
        elif src["same_as"]:
            dropped[f"{s.corpus}: duplicate source (same_as {src['same_as'].split(':')[0]})"] += 1
        else:
            kept.append(s)
    slots = kept + _lin_slots()
    lineage = org_lineages(orgs)
    for s in slots:
        s.variants = [v for v in dict.fromkeys(parse(n) for n in s.names) if v.fam]
        s.roots = frozenset(org_root(orgs, o) for a in s.affs for o in a.org_ids if o in orgs)
        s.lineages = frozenset(k for r in s.roots for k in lineage.get(r, {r}))
    headers = attach_headers(slots, header_rows(), orgs)  # after roots: header orgs are not identity keys (D217)
    common = common_families(slots)
    for s in slots:
        s.coauthors = frozenset(coauthor_key(n, common) for n in s.coauthor_names) - {""}
        s.selfkeys = frozenset(coauthor_key(n, common) for n in s.names)
    return Inputs(
        slots=slots,
        orgs=orgs,
        sources=sources,
        common=common,
        dropped=dropped,
        hubs=hub_keys(slots),
        dense=dense_keys(slots, orgs),
        headers=headers,
        committed=committed_slots(),
    )


def dense_keys(
    slots: list[Slot],
    orgs: dict[str, dict[str, str]],
    share: float | None = None,
    fam_keys: int | None = None,
    given_keys: int | None = None,
) -> frozenset[str]:
    """D91(b) as amended by D96: full-name keys for which rule (2) (exact name + same org) does not apply; rule (3)
    still does. A key is listed when (1) its family name is region-dense: >= DENSE_SHARE of the family's EO / PK /
    OFC slots with a known country are in DENSE_COUNTRIES (printed site country of the affiliation where the input
    has one, EO / PK; else the registry country of the mapped org; share 0 = no region condition), and (2) the name
    is ambiguous in the data: the family name is carried by >= DENSE_FAM_KEYS and the given names by
    >= DENSE_GIVEN_KEYS distinct full-name keys. Data-driven; no name list."""
    share = DENSE_SHARE if share is None else share
    fam_keys = DENSE_FAM_KEYS if fam_keys is None else fam_keys
    given_keys = DENSE_GIVEN_KEYS if given_keys is None else given_keys
    tot: Counter[str] = Counter()
    hit: Counter[str] = Counter()
    by_fam: dict[str, set[str]] = defaultdict(set)
    by_given: dict[tuple[str, ...], set[str]] = defaultdict(set)
    for s in slots:
        for v in s.variants:
            k = full_key(v)
            if k:
                by_fam[v.fam].add(k)
                by_given[v.given].add(k)
        if s.corpus == "lin":
            continue
        cs = {a.country for a in s.affs if a.country}
        if not cs:
            cs = {orgs.get(r, {}).get("country", "") for r in s.roots} - {""}
        if not cs:
            continue
        for f in {v.fam for v in s.variants}:
            tot[f] += 1
            hit[f] += bool(cs & DENSE_COUNTRIES)
    out = set()
    for s in slots:
        for v in s.variants:
            k = full_key(v)
            if not k or len(by_fam[v.fam]) < fam_keys or len(by_given[v.given]) < given_keys:
                continue
            if share and not (tot[v.fam] and hit[v.fam] / tot[v.fam] >= share):
                continue
            out.add(k)
    return frozenset(out)


def hub_keys(slots: list[Slot], min_sources: int | None = None) -> frozenset[str]:
    """D92: coauthor keys printed on >= HUB_MIN_SOURCES sources (prolific senior authors). A shared hub coauthor says
    little about identity inside one org, so it does not count as the shared-coauthor discriminator."""
    n = HUB_MIN_SOURCES if min_sources is None else min_sources
    srcs: dict[str, set[str]] = defaultdict(set)
    for s in slots:
        if s.source_id:
            for k in s.selfkeys - {""}:
                srcs[k].add(s.source_id)
    return frozenset(k for k, v in srcs.items() if len(v) >= n) if n else frozenset()


def common_families(slots: list[Slot], min_slots: int | None = None) -> set[str]:
    """D63/D91/D96: EO list + family names with >= COMMON_MIN_KEYS distinct full-name keys, or >= COMMON_MIN_SLOTS
    author slots (EO / PK / OFC slots; LIN records not counted) and >= COMMON_SLOT_MIN_KEYS distinct full-name keys."""
    min_slots = COMMON_MIN_SLOTS if min_slots is None else min_slots
    keys_by_fam: dict[str, set[str]] = defaultdict(set)
    slots_by_fam: Counter[str] = Counter()
    for s in slots:
        for f in {v.fam for v in s.variants}:
            if s.corpus != "lin":
                slots_by_fam[f] += 1
        for v in s.variants:
            k = full_key(v)
            if k:
                keys_by_fam[v.fam].add(k)
    out = EO_COMMON | {f for f, ks in keys_by_fam.items() if len(ks) >= COMMON_MIN_KEYS}
    if min_slots:  # D96: frequent AND carried by several different full names (not one prolific person)
        out |= {f for f, n in slots_by_fam.items() if n >= min_slots and len(keys_by_fam[f]) >= COMMON_SLOT_MIN_KEYS}
    return out


def coauthor_key(name: str, common: set[str]) -> str:
    n = parse(name)
    g, f = n.given, n.fam
    if not f:
        return ""
    if f in common:
        return full_key(n)
    return f"{g[0][0]} {f}" if g else f


# ---------------------------------------------------------------- identity


@dataclass
class Pair:
    a: int
    b: int
    basis: str  # merge basis, or '' for a review-only pair
    flags: tuple[str, ...]
    need: tuple[str, ...] = ()  # D219c: coauthor keys that must resolve to one person at union time (else review)


def shared_coauthors(a: Slot, b: Slot, hubs: frozenset[str] = frozenset()) -> set[str]:
    """Coauthor keys on both records other than the two slots themselves, minus hub coauthors (D92)."""
    return set((a.coauthors & b.coauthors) - a.selfkeys - b.selfkeys - hubs)


def pair_hubs(a: Slot, b: Slot, hubs: frozenset[str]) -> frozenset[str]:
    """D92 as amended (D96): no hub discount when one of the two slots is itself a hub (prolific authors share
    prolific coauthors; discounting them would split the hubs themselves)."""
    return frozenset() if (a.selfkeys | b.selfkeys) & hubs else hubs


def coauthor_support(a: Slot, b: Slot, hubs: frozenset[str] = frozenset(), common: bool = False) -> bool:
    """D92/D96: one shared non-hub coauthor; for non-common family names also >= 2 shared coauthors of any kind."""
    h = pair_hubs(a, b, hubs)
    return bool(shared_coauthors(a, b, h)) or (not common and len(shared_coauthors(a, b)) >= 2)


def key_family(key: str) -> str:
    return key.rsplit(" ", 1)[-1]


def _evidence(a: Slot, b: Slot, hubs: frozenset[str]) -> int:
    return len(shared_coauthors(a, b, pair_hubs(a, b, hubs)))


def evaluate(
    a: Slot, b: Slot, common: set[str], hubs: frozenset[str] = frozenset(), dense: frozenset[str] = frozenset()
) -> Pair | None:
    """D63 merge basis for two slots of one family block, a review-only pair (basis ''), or None (no relation).
    Rule (2) excludes common family names and ambiguous full names (D91, D96)."""
    if a.source_id and a.source_id == b.source_id:
        return None
    if a.orcid and a.orcid == b.orcid:
        return Pair(0, 0, "orcid", ())
    org = bool(a.lineages & b.lineages)
    exact_any = compat_any = common_any = dense_any = full_any = False
    for va in a.variants:
        for vb in b.variants:
            if va.fam != vb.fam:
                continue
            exact = va.given == vb.given and not va.abbreviated
            if not (exact or compatible(va, vb, va.fam in common)):
                continue
            if exact and org and va.fam not in common and full_key(va) not in dense:
                return Pair(0, 0, "exact_name_shared_org", ())
            exact_any |= exact
            compat_any = True
            common_any |= va.fam in common
            dense_any |= exact and full_key(va) in dense and va.fam not in common
            full_any |= not (va.abbreviated or vb.abbreviated)
    if not compat_any:
        return None
    co = coauthor_support(a, b, hubs, common_any)
    need: tuple[str, ...] = ()
    if co and common_any:
        # D219c: for common family names the supporting coauthor has a non-common family name, or its two slots
        # resolve to one person (checked at union time); a name-key match alone never supports the join
        keys = shared_coauthors(a, b, pair_hubs(a, b, hubs))
        if not any(key_family(k) not in common for k in keys):
            need = tuple(sorted(keys))
    if org and co and not need:
        return Pair(0, 0, "compatible_name_shared_org_coauthor", ())
    if need:
        co = False  # fallback flags if the coauthor never resolves to one person
    eo_split = bool(a.eo_pid and b.eo_pid and a.eo_pid != b.eo_pid and full_any)
    if not (exact_any or org or eo_split):
        return None
    flags = ["exact_name" if exact_any else "compatible_name"]
    flags += [
        f
        for f, on in (
            ("shared_org", org),
            ("shared_coauthor", co),
            ("common_family_name", common_any),
            ("ambiguous_full_name", dense_any),
            ("eo_split", eo_split),
        )
        if on
    ]
    if need and org:
        return Pair(0, 0, "compatible_name_shared_org_coauthor", (*flags, "coauthor_unresolved"), need)
    return Pair(0, 0, "", tuple(flags))


class Clusters:
    """Union-find with D62 cannot-link constraints."""

    def __init__(self, slots: list[Slot], common: Iterable[str] = ()) -> None:
        self.common = frozenset(common)
        self.p = list(range(len(slots)))
        self.eo = [{s.eo_pid} - {""} for s in slots]
        self.lin = [{s.lin_id} - {""} for s in slots]
        self.orcid = [{s.orcid} - {""} for s in slots]
        self.src = [{s.source_id} - {""} for s in slots]
        self.names: list[set[frozenset[Name]]] = [{frozenset(s.variants)} for s in slots]

    def find(self, x: int) -> int:
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def blocker(self, a: int, b: int) -> str:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return "same"
        if len(self.eo[ra] | self.eo[rb]) > 1:
            return "blocked_eo_split"
        if len(self.lin[ra] | self.lin[rb]) > 1:
            return "blocked_lin_split"
        if len(self.orcid[ra] | self.orcid[rb]) > 1:
            return "blocked_orcid"
        if self.src[ra] & self.src[rb]:
            return "blocked_same_source"
        return ""

    def name_conflict(self, a: int, b: int) -> bool:
        """D90: every record of one cluster must be name-compatible with every record of the other (no chaining of
        "Q. T." -> "Qai-Tun" -> "Q. J." or "Hiroki" -> "H." -> "Hirotaka"; fictitious)."""
        ra, rb = self.find(a), self.find(b)
        return not all(names_compatible(x, y, self.common) for x in self.names[ra] for y in self.names[rb])

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        lo, hi = min(ra, rb), max(ra, rb)
        self.p[hi] = lo
        for attr in (self.eo, self.lin, self.orcid, self.src):
            attr[lo] |= attr[hi]
        self.names[lo] |= self.names[hi]


@dataclass
class Identity:
    cluster_of: list[int]  # slot index -> cluster root
    join_basis: dict[int, str]  # slot index -> strongest accepted basis incident to it
    merges: Counter[str]
    review: list[Pair]  # review-only pairs and blocked merges (flags carry the reason)
    edges: list[tuple[int, int, str]]  # accepted joins (slot a, slot b, basis); the clusters' spanning forest


def resolve(inp: Inputs, blocks: set[str] | None = None) -> Identity:
    slots = inp.slots
    by_fam: dict[str, list[int]] = defaultdict(list)
    for i, s in enumerate(slots):
        for f in {v.fam for v in s.variants}:
            if blocks is None or f in blocks:
                by_fam[f].append(i)
    pairs: dict[tuple[int, int], Pair] = {}
    by_orcid: dict[str, list[int]] = defaultdict(list)
    for i, s in enumerate(slots):
        if s.orcid and (blocks is None or any(v.fam in blocks for v in s.variants)):
            by_orcid[s.orcid].append(i)
    for ks in by_orcid.values():
        for x in range(len(ks)):
            for y in range(x + 1, len(ks)):
                if slots[ks[x]].source_id != slots[ks[y]].source_id:
                    pairs[(ks[x], ks[y])] = Pair(ks[x], ks[y], "orcid", ())
    for f in sorted(by_fam):
        idx = by_fam[f]
        for x in range(len(idx)):
            for y in range(x + 1, len(idx)):
                a, b = idx[x], idx[y]
                if (a, b) in pairs:
                    continue
                pr = evaluate(slots[a], slots[b], inp.common, inp.hubs, inp.dense)
                if pr is not None:
                    pr.a, pr.b = a, b
                    pairs[(a, b)] = pr
    cl = Clusters(slots, inp.common)
    join: dict[int, str] = {}
    edges: list[tuple[int, int, str]] = []
    merges: Counter[str] = Counter()
    review: list[Pair] = [p for p in pairs.values() if not p.basis]
    ambiguous = ambiguous_slots(slots, pairs, inp.common)
    by_src: dict[str, list[int]] = defaultdict(list)
    for i, s in enumerate(slots):
        if s.source_id:
            by_src[s.source_id].append(i)

    def committed_pair(a: int, b: int) -> bool:
        pa = inp.committed.get(slots[a].sid)
        return bool(pa) and pa == inp.committed.get(slots[b].sid)

    def resolved(a: int, b: int, keys: tuple[str, ...]) -> bool:
        """D219c: a shared coauthor key whose slots on the two sources are already one person."""
        for k in keys:
            xa = [x for x in by_src[slots[a].source_id] if k in slots[x].selfkeys and x != a]
            xb = [x for x in by_src[slots[b].source_id] if k in slots[x].selfkeys and x != b]
            if any(cl.find(x) == cl.find(y) for x in xa for y in xb):
                return True
        return False

    for basis in ("orcid", "exact_name_shared_org", "compatible_name_shared_org_coauthor"):
        todo = [(k, pr) for k, pr in pairs.items() if pr.basis == basis]
        # strongest evidence first (D90): more shared coauthors, then deterministic slot order
        todo.sort(key=lambda kv: (-_evidence(slots[kv[0][0]], slots[kv[0][1]], inp.hubs), kv[0]))
        # D219c: pairs whose support needs a resolved coauthor wait until it is one person (fixpoint over passes, so
        # support is never circular: a coauthor counts only once it was joined by other evidence)
        # D219d: the stricter D219c evidence applies only to joins not already in the committed tables; committed
        # joins keep their place in the order (unchanged pending the owner's decision on D219c)
        pending = [kv for kv in todo if kv[1].need and not committed_pair(kv[0][0], kv[0][1])]
        todo = [kv for kv in todo if not kv[1].need or committed_pair(kv[0][0], kv[0][1])]
        while True:
            ready = [kv for kv in pending if resolved(kv[0][0], kv[0][1], kv[1].need)]
            done = {kv[0] for kv in ready}
            pending = [kv for kv in pending if kv[0] not in done]
            batch, todo = todo + ready, []
            if not batch:
                break
            for (a, b), _pr in batch:
                why = cl.blocker(a, b)
                if not why and basis != "orcid":
                    if a in ambiguous or b in ambiguous:
                        why = "blocked_name_ambiguous"
                    elif cl.name_conflict(a, b):
                        why = "blocked_name_conflict"
                if why == "same":
                    pass
                elif why:
                    review.append(Pair(a, b, "", (why, basis)))
                    continue
                else:
                    cl.union(a, b)
                    edges.append((a, b, basis))
                    merges[basis] += 1
                for k in (a, b):
                    if k not in join or BASIS_RANK[basis] < BASIS_RANK[join[k]]:
                        join[k] = basis
        review += [Pair(a, b, "", pr.flags) for (a, b), pr in pending]  # D219c: coauthor never resolved
    # Low/I5: one EO person split into several registry persons is always queued, whatever the evidence.
    by_eo: dict[str, dict[int, int]] = defaultdict(dict)
    for i, s in enumerate(slots):
        if s.eo_pid and (blocks is None or any(v.fam in blocks for v in s.variants)):
            by_eo[s.eo_pid].setdefault(cl.find(i), i)
    for reps in by_eo.values():
        firsts = sorted(reps.values())
        for x in range(len(firsts)):
            for y in range(x + 1, len(firsts)):
                review.append(Pair(firsts[x], firsts[y], "", ("eo_person_split",)))
    return Identity(
        cluster_of=[cl.find(i) for i in range(len(slots))], join_basis=join, merges=merges, review=review, edges=edges
    )


def ambiguous_slots(slots: list[Slot], pairs: dict[tuple[int, int], Pair], common: Iterable[str] = ()) -> set[int]:
    """D90: a record whose rule-based merge partners include two mutually name-incompatible records ("Q. Q." next to
    "Qeng-Qieh" and "Qeng-Qi", fictitious) cannot be assigned by name; none of its rule merges is applied (review queue)."""
    cs = frozenset(common)
    part: dict[int, set[int]] = defaultdict(set)
    for (a, b), pr in pairs.items():
        if pr.basis in ("exact_name_shared_org", "compatible_name_shared_org_coauthor"):
            part[a].add(b)
            part[b].add(a)
    out = set()
    for x, ps in part.items():
        ls = sorted(ps)
        if any(
            not names_compatible(slots[p].variants, slots[q].variants, cs)
            for i, p in enumerate(ls)
            for q in ls[i + 1 :]
        ):
            out.add(x)
    return out


def chain_basis(members: list[int], anchor: int, edges: list[tuple[int, int, str]]) -> dict[int, str]:
    """Per slot, the weakest join on the strongest chain from the anchor (accepted joins form a spanning forest, so
    the chain is unique): the basis by which the slot's record joined the person (D66)."""
    mem = set(members)
    adj: dict[int, list[tuple[int, str]]] = defaultdict(list)
    for a, b, basis in edges:
        if a in mem:
            adj[a].append((b, basis))
            adj[b].append((a, basis))
    out = {anchor: "origin"}
    stack = [anchor]
    while stack:
        x = stack.pop()
        for y, basis in adj[x]:
            if y not in out:
                out[y] = basis if BASIS_RANK[basis] > BASIS_RANK[out[x]] else out[x]
                stack.append(y)
    return out


# ---------------------------------------------------------------- persons, xref, aliases, observations


def obs_ids(s: Slot) -> list[tuple[str, Aff, str]]:
    """(obs_id, aff, org_id) per observation of a slot; one per org of a joint_printed string (D67)."""
    out: list[tuple[str, Aff, str]] = []
    if s.corpus == "lin":
        return out
    for a in ([] if s.hdr_status == "confirmed" else s.affs) + s.hdr:  # D215: a confirmed metadata row is dropped
        if a.oid:  # D219e: header rows always carry the org index
            out.extend((f"{a.oid}.m{n}", a, oid) for n, oid in enumerate(a.org_ids or [""], start=1))
            continue
        base = f"{s.source_id}#a{s.index}.{a.order}"
        if len(a.org_ids) <= 1:
            out.append((base, a, a.org_ids[0] if a.org_ids else ""))
        else:
            out.extend((f"{base}.{k}", a, oid) for k, oid in enumerate(a.org_ids, start=1))
    return out


def display_name(members: list[Slot]) -> str:
    for s in members:
        if s.lin_id:
            return str(s.lin["name"])
    spell = Counter(s.name for s in members if s.corpus != "lin")
    return max(sorted(spell), key=lambda n: (completeness(n)[0], n != n.lower(), spell[n], completeness(n)[1]))


def _anchor(members: list[Slot]) -> Slot:
    order = {"lin": 0, "eo": 1, "pk": 2, "ofc2026": 3}
    return min(members, key=lambda s: (order[s.corpus], s.sid))


def lin_sources(s: Slot, sources: dict[str, dict[str, str]]) -> list[str]:
    """Registry source ids of a LIN person's sources (recorded in the lin_id xref notes; the validator grades them)."""
    return sorted({f"lin:{x['source_id']}" for x in s.lin.get("sources") or []} & set(sources))


def lin_grade(s: Slot, sources: dict[str, dict[str, str]]) -> str:
    gs = [sources[x]["evidence_grade"] for x in lin_sources(s, sources) if sources[x]["evidence_grade"]]
    return min(gs) if gs else "X"


def xref_rows(pid: str, members: list[Slot], ident: Identity, idx: dict[str, int], inp: Inputs) -> list[dict[str, str]]:
    anchor = _anchor(members)
    chain = chain_basis([idx[s.sid] for s in members], idx[anchor.sid], ident.edges)
    groups: dict[tuple[str, str], list[Slot]] = defaultdict(list)
    for s in members:
        if s.corpus == "eo":
            groups[("eo_person_id", s.eo_pid)].append(s)
        elif s.corpus == "pk":
            groups[("pk_name_key", name_key(s.name))].append(s)
        elif s.corpus == "ofc2026":
            groups[("ofc_name", s.name)].append(s)
        else:
            groups[("lin_id", s.lin_id)].append(s)
    rows = []
    for (scheme, value), ss in sorted(groups.items()):
        if not value:
            continue
        basis = min((chain[idx[s.sid]] for s in ss), key=lambda b: BASIS_RANK[b])
        if basis == "origin":
            grade = {"eo": "A", "pk": "A", "ofc2026": "B"}.get(ss[0].corpus) or lin_grade(ss[0], inp.sources)
        elif basis == "orcid":
            grade = "A"
        else:
            grade = "X"
        row = {"person_id": pid, "scheme": scheme, "value": value, "basis": basis, "grade": grade}
        if scheme == "lin_id":
            row["notes"] = "lin sources: " + ";".join(lin_sources(ss[0], inp.sources))
        rows.append(row)
    for o in sorted({s.orcid for s in members if s.orcid}):
        rows.append({"person_id": pid, "scheme": "orcid", "value": o, "basis": "orcid", "grade": "A"})
    return rows


def alias_rows(pid: str, dname: str, members: list[Slot]) -> list[dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for s in members:
        if s.lin_id:
            for a in s.lin.get("aliases") or []:
                t = a.get("alias_type") or "alternate_spelling"
                out[a["name"]] = {
                    "person_id": pid,
                    "alias": a["name"],
                    "alias_type": t
                    if t in {"native_name", "transliteration", "alternate_spelling", "common_name", "former_name"}
                    else "alternate_spelling",
                    "lang": a.get("language") or "",
                    "origin": "lin",
                }
    prio = {"eo": 0, "pk": 1, "ofc2026": 2}
    for s in sorted((s for s in members if s.corpus in prio), key=lambda s: (prio[s.corpus], s.sid)):
        n = s.name
        if n == dname or n in out or not n:
            continue
        out[n] = {
            "person_id": pid,
            "alias": n,
            "alias_type": "abbreviated" if parse(n).abbreviated else "printed_variant",
            "lang": "",
            "origin": s.corpus,
        }
    for s in sorted((s for s in members if s.hdr), key=lambda s: s.sid):  # D218: header printed forms, last
        for n in dict.fromkeys(a.printed_name for a in s.hdr):
            if n == dname or n in out or not n:
                continue
            out[n] = {
                "person_id": pid,
                "alias": n,
                "alias_type": "abbreviated" if parse(n).abbreviated else "printed_variant",
                "lang": "",
                "origin": "ofc2026",
                "notes": HEADER_ALIAS_NOTE,
            }
    return [out[k] for k in sorted(out)]


def new_person_id(dname: str, taken: set[str]) -> str:
    base = "person_" + ("_".join(re.sub(r"[^a-z0-9]+", " ", ascii_fold(dname).lower()).split()) or "unnamed")
    pid, n = base, 1
    while pid in taken:
        n += 1
        pid = f"{base}_{n}"
    return pid


def assign_ids(
    clusters: dict[int, list[Slot]],
    names: dict[int, str],
    old_obs: dict[str, str],
    old_xref: Iterable[dict[str, str]],
    old_ids: set[str],
) -> dict[int, str]:
    """D65: LIN ids verbatim; reuse an old id of the cluster: its ORCID first (a split keeps the id on the ORCID-backed
    part, D90), then the id spelled like the cluster's display name (D96), then the most observations (or the EO
    person xref); never reassign an id; new ids in deterministic order."""
    eo_old: dict[str, set[str]] = defaultdict(set)
    orcid_old: dict[str, set[str]] = defaultdict(set)
    for x in old_xref:
        if x["scheme"] == "eo_person_id":
            eo_old[x["value"]].add(x["person_id"])
        elif x["scheme"] == "orcid":
            orcid_old[x["value"]].add(x["person_id"])
    by_slot: dict[str, Counter[str]] = defaultdict(Counter)  # D217: old ids looked up by slot, not by obs id
    for oid, pid in old_obs.items():
        m = SLOT_OF_OBS_RE.match(oid)
        if m:
            by_slot[m.group(1)][pid] += 1
    out: dict[int, str] = {}
    claimed: set[str] = set()
    for c, ms in clusters.items():
        lin = [s.lin_id for s in ms if s.lin_id]
        if lin:
            out[c] = lin[0]
            claimed.add(lin[0])
    cand: dict[int, Counter[str]] = {}
    for c, ms in clusters.items():
        if c in out:
            continue
        cnt: Counter[str] = Counter()
        for s in ms:
            for p, n in by_slot.get(f"{s.source_id}#a{s.index}", Counter()).items():
                cnt[p] += 2 * n
            for p in eo_old.get(s.eo_pid, set()):
                cnt[p] += 1
        for o in {s.orcid for s in ms if s.orcid}:
            for p in orcid_old.get(o, set()):
                cnt[p] += 100000
        slug = new_person_id(names[c], set())
        if slug in cnt:
            cnt[slug] += 10000  # D96: the id spelled like the display name outweighs observation counts
        cand[c] = cnt
    order = sorted(cand, key=lambda c: (-max(cand[c].values(), default=0), min(s.sid for s in clusters[c])))
    for c in order:
        for p, _ in sorted(cand[c].items(), key=lambda kv: (-kv[1], kv[0])):
            if p not in claimed and p in old_ids:
                out[c] = p
                claimed.add(p)
                break
    taken = old_ids | claimed
    rest = sorted((c for c in clusters if c not in out), key=lambda c: (names[c], min(s.sid for s in clusters[c])))
    for c in rest:
        pid = new_person_id(names[c], taken)
        out[c] = pid
        taken.add(pid)
    return out


def review_pairs(ident: Identity, slots: list[Slot], pid_of: dict[int, str]) -> list[dict[str, str]]:
    """One row per person pair: union of flags, an example name on each side (local file only, D64)."""
    agg: dict[tuple[str, str], dict[str, Any]] = {}
    for pr in ident.review:
        pa, pb = pid_of[ident.cluster_of[pr.a]], pid_of[ident.cluster_of[pr.b]]
        if pa == pb:
            continue
        (pa, sa), (pb, sb) = sorted([(pa, slots[pr.a]), (pb, slots[pr.b])])
        r = agg.setdefault(
            (pa, pb),
            {"flags": set(), "n_pairs": 0, "name_a": sa.name, "name_b": sb.name, "sid_a": sa.sid, "sid_b": sb.sid},
        )
        r["flags"] |= set(pr.flags)
        r["n_pairs"] += 1
    out = []
    for (pa, pb), r in sorted(agg.items()):
        flags = r["flags"]
        if any(f.startswith("blocked_") for f in flags):
            reason = sorted(f for f in flags if f.startswith("blocked_"))[0]
        elif "eo_person_split" in flags:
            reason = "eo_person_split"
        elif "exact_name" in flags and "shared_org" in flags:
            reason = "exact_name_shared_org_common_family_name"
        elif "exact_name" in flags and "shared_coauthor" in flags:
            reason = "exact_name_shared_coauthor_no_shared_org"
        elif "exact_name" in flags:
            reason = "name_only"
        elif "shared_org" not in flags and "eo_split" in flags:
            reason = "eo_split_compatible_name"
        else:
            reason = "compatible_name_shared_org_no_coauthor"
        out.append(
            {
                "person_id_a": pa,
                "person_id_b": pb,
                "reason": reason,
                "flags": ";".join(sorted(flags)),
                "n_slot_pairs": str(r["n_pairs"]),
                "name_a": r["name_a"],
                "name_b": r["name_b"],
                "example_a": r["sid_a"],
                "example_b": r["sid_b"],
            }
        )
    return out


def demoted_by_queue(queue: Iterable[dict[str, str]], n_obs: dict[str, int]) -> set[str]:
    """D64 ruling (2026-10-20): a person's observations are review when the person is in a queue pair whose partner
    has >= 1 observation; a partner without observations (a LIN-only record) keeps the pair queued but demotes
    nothing."""
    out = set()
    for q in queue:
        a, b = q["person_id_a"], q["person_id_b"]
        if n_obs.get(b, 0):
            out.add(a)
        if n_obs.get(a, 0):
            out.add(b)
    return out


def read_optional(path: Path) -> list[dict[str, str]]:
    return read_csv(path) if path.exists() else []


def same_as_redirects(
    people_rows: dict[str, dict[str, str]],
    orphans: list[str],
    old_obs: dict[str, str],
    new_obs: dict[str, str],
) -> dict[str, str]:
    """D212: an id kept without records (D65) that was absorbed by a merge redirects to the surviving person: the one
    person now holding all of its previous observations, else its existing same_as. Chains are followed to the end
    (the target is never itself redirected); an id that holds records again gets no redirect."""
    out: dict[str, str] = {}
    for pid in orphans:
        holders = {new_obs[o] for o, p in old_obs.items() if p == pid and o in new_obs}
        target = next(iter(holders)) if len(holders) == 1 else people_rows[pid].get("same_as", "")
        if target and target != pid:
            out[pid] = target
    final: dict[str, str] = {}
    for pid, t in out.items():
        seen = {pid}
        while t in out and t not in seen:
            seen.add(t)
            t = out[t]
        if t not in seen:  # a cycle cannot hold a surviving person
            final[pid] = t
    return final
