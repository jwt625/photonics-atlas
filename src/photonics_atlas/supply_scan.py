"""Vendor / model candidate finder over cached paper texts (DevLog-003 D205). Proposes candidates only; a reviewer
decides which are product usage facts (D206, D207).

Dictionary: the gazetteer and model patterns of config/supply_scanner.yaml plus the registry orgs of vendor-like
org_type by name and alias (literal, case-sensitive, word-bounded). Text: page markers -> locators (`<!-- page N -->`
-> p.N; OFC `_page_k_` figure markers -> p.~(k+1), pNA before the first one, D4); reference lists are not scanned;
front matter, author-affiliation sentences and acknowledgements are flagged by zone. One candidate per sentence and
vendor entity (a vendor and a model of the same vendor, or of a lineage predecessor, in one sentence merge).
Amended 2026-10-22 after the pilot audit (D292-D295): whitespace / tail / acronym fixes, reference-list and inline
acknowledgement detection, OFC span anchors, parenthesis-aware sentences, gazetteer names resolved against the
registry, registry-independent candidate ids, and gazetteer-independent `unlisted` candidates.
"""

from __future__ import annotations

import bisect
import hashlib
import re
import unicodedata
from collections.abc import Iterator
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from .csvio import read_csv
from .orgmatch import load_matcher
from .paths import REGISTRY, ROOT, input_path
from .textnorm import norm_key

CONFIG = ROOT / "config" / "supply_scanner.yaml"
CONTEXT_MAX = 300

PAGE_MD = re.compile(r"<!-- page (\d+) -->")
PAGE_OFC = re.compile(r"_page_(\d+)_|<span id=\"page-(\d+)-\d+\">")
# Known section headings on a line of their own (pymupdf text wraps lines, so free-form heading detection is not used).
# Prefixes seen in the corpora: markdown #, bold **, <span id="page-N-M"></span> anchors (OFC), section numbers, the
# block glyph used by some publishers.
_HPREFIX = r"^[ \t#*>_\-■]*(?:<span[^>]*>\s*</span>\s*)?(?:\*\*)?\s*(?:[0-9IVXA-H]+\.?\s+)?"
_HNAMES = (
    r"supplementary references|references|bibliography|references and notes|references and links|reference|methods?|"
    r"materials and methods|experimental( section| methods| details)?|acknowledge?ments?|acknowledgments?|funding|"
    r"author contributions?|data availability( statement)?|code availability|competing interests?|"
    r"con(?:fl|\ufb02)icts? of interest|disclosures?|supplementary( information| materials?| note \d+)?|supporting information|"
    r"appendix( [a-z])?|conclusions?|discussion|results( and discussion)?|introduction|abstract"
)
HEADING_LINE = re.compile(_HPREFIX + r"(?P<h>" + _HNAMES + r")[ \t*:._]*$", re.I | re.M)
# Inline labels: a known ack / funding / disclosure heading followed by text on the same line.
INLINE_LABEL = re.compile(
    _HPREFIX
    + r"(?P<h>acknowledge?ments?|acknowledgments?|funding|disclosures?|competing interests?|con(?:fl|\ufb02)icts? of interest)"
    + r"(?:\*\*)?\s*[:.—-]\s*(?:\*\*)?\s*\S",
    re.I | re.M,
)
REF_HEADING = re.compile(
    r"^(references|bibliography|references and notes|references and links|reference|supplementary references)$", re.I
)
# D343 (R9): supplementary material appended after the reference list ("Supplementary Information for: <title>").
SUPP_LINE = re.compile(
    r"^[ \t#*>_-]*(?:\*\*)?(?:supplementary|supplemental|supporting)\s+(?:information|materials?|text)"
    r"(?:\s+for\b.*|\s*[:.]?\s*(?:\*\*)?\s*)$",
    re.I | re.M,
)
REF_ENTRY = re.compile(r"^\s*(?:[-*]\s*)?(?:\[1\]|1\.\s)", re.M)
REF_FIRST = re.compile(r"^\s*(?:[-*]\s*)?\[1\](?:\s+\S|\s*$)", re.M)
AFTER_REFS = re.compile(
    r"^(introduction|methods?|materials and methods|experimental|acknowledge?ments?|acknowledgments?|supplementary|"
    r"supporting information|appendix|data availability|code availability|author contributions?|funding|"
    r"competing interests?|con(?:fl|\ufb02)icts? of interest|disclosures?)",
    re.I,
)
ACK_HEADING = re.compile(r"^(acknowledge?ments?|acknowledgments?|funding|author contributions?)$", re.I)
COI_HEADING = re.compile(r"^(competing interests?|con(?:fl|\ufb02)icts? of interest|disclosures?)$", re.I)
FRONT_END = re.compile(r"^[ \t#*>_-]*(?:\*\*)?(abstract|introduction|[0-9I]+\.?\s+introduction)\b", re.I | re.M)
AFFIL = re.compile(
    r"\b(is|are|was|were) (now )?with\b|e-?mail|manuscript received|corresponding author|@|\bauthors? (is|are) with\b",
    re.I,
)
SENT_SPLIT = re.compile(r"(?<=[.;!?])\s+(?=[A-Z(\[])|\n\s*\n")
# Tokens before a full stop that do not end a sentence (company forms, references, Latin).
ABBREV = re.compile(
    r"(?:\b(?:Inc|Ltd|Co|Corp|Ltda|Bros|Fig|Figs|Eq|Eqs|Ref|Refs|No|Nos|Vol|Sec|Ch|vs|cf|e\.g|i\.e|et al|approx|ca|"
    r"Dr|Prof|Mr|Ms|St)|\b[A-Z])\.$"
)
WORD = r"(?<![A-Za-z0-9])(?:{})(?![A-Za-z0-9])"
# Page-1 sentences naming a postal address or country are author affiliations, not usage.
ADDRESS = re.compile(
    r"\b(Road|Street|Avenue|Blvd|Suite|USA|Canada|Japan|China|Singapore|Germany|Netherlands|Switzerland|France|Korea|"
    r"Taiwan|Italy|Spain|Belgium|Denmark|Sweden|Israel|Australia|United Kingdom|UK)\b"
)
SHORT_ACRONYM = re.compile(r"[A-Z0-9&-]{1,4}")
# Gazetteer-independent candidates (D294): a parenthetical "(Name Model)" / "(Model, Name ...)" or a company name
# with a legal suffix.
PAREN = re.compile(r"\(([^()\n]{3,120})\)")
MODEL_TOKEN = re.compile(
    r"^(?=[A-Za-z0-9.+/-]*\d)[A-Za-z0-9][A-Za-z0-9.+/-]*[A-Za-z0-9+]$|^[A-Z][A-Z0-9-]*\d[A-Z0-9-]*$"
)
UNIT_TOKEN = re.compile(
    r"^[~<>]?\d+(\.\d+)?(nm|um|µm|mm|cm|m|km|GHz|MHz|kHz|Hz|THz|dB|dBm|mW|W|kW|V|mV|kV|mA|A|s|ms|us|ns|ps|fs|K|C|"
    r"%|x|X|Gb|Gbps|Gbit|GBd|Gbaud|GS|GSa|pJ|nJ|mJ|J|deg|rpm|min|h|bit|bits)?$"
)
NAME = re.compile(r"[A-Z][A-Za-z&+]*(?:[ -][A-Z][A-Za-z&+]*){0,3}")
_SUFFIX = (
    r"(?:Inc|INC|Ltd|LTD|GmbH|GMBH|Corporation|CORPORATION|Corp|CORP|Co\.,?\s*Ltd|CO\.,?\s*LTD|AG|B\.V|BV|LLC|"
    r"S\.A|Pte\.?\s*Ltd|Oy|SAS|S\.r\.l|Srl|Limited|LIMITED|Incorporated|INCORPORATED)"
)
# Case-sensitive on purpose: "limited to" / "incorporated" are prose (D294).
COMPANY = re.compile(r"\b(?P<name>[A-Z][\w&+-]*(?:\s+[A-Z][\w&+-]*){0,3}),?\s+" + _SUFFIX + r"\b\.?")
LEGAL_TAIL = re.compile(r"\s+" + _SUFFIX + r"\.?$")
NAME_STOP = {
    "fig",
    "figs",
    "figure",
    "figures",
    "table",
    "tables",
    "eq",
    "eqs",
    "equation",
    "ref",
    "refs",
    "section",
    "sec",
    "supplementary",
    "supplemental",
    "note",
    "notes",
    "methods",
    "appendix",
    "inset",
    "see",
    "the",
    "a",
    "an",
    "in",
    "for",
    "with",
    "using",
    "and",
    "or",
    "of",
    "to",
    "via",
    "from",
    "by",
    "on",
    "at",
    "as",
    "university",
    "institute",
    "laboratory",
    "laboratories",
    "lab",
    "department",
    "center",
    "centre",
    "school",
    "college",
    "foundation",
    "council",
    "agency",
    "ministry",
    "national",
    "program",
    "programme",
    "grant",
    "fund",
    "project",
    "type",
    "model",
    "mode",
    "te",
    "tm",
    "rf",
    "dc",
    "ac",
    "nrz",
    "pam",
    "ook",
    "qam",
    "ber",
    "snr",
    "osnr",
    "ssmf",
    "smf",
    "mzm",
    "mrm",
    "pd",
    "vna",
    "osa",
    "awg",
    "edfa",
    "soa",
    "pic",
    "eo",
    "oe",
    "ic",
    "cmos",
    "soi",
    "sin",
    "ln",
    "tfln",
    "inp",
    "gaas",
    "si",
    "ge",
    "sio2",
    "al2o3",
    "hbn",
    "fdtd",
    "fem",
    "bpm",
    "eme",
    "fde",
    "ieee",
    "usa",
    "uk",
    "eu",
    "nsf",
    "darpa",
    "step",
    "steps",
    "phase",
    "case",
    "stage",
    "wiley",
    "wiley-vch",
    "macmillan",
    "springer",
    "elsevier",
    "optica",
}
# D321: footers, copyright lines and funding sentences never yield unlisted candidates.
FOOTER_LINE = re.compile(r"publisher|publishing|\u00a9|\(c\)\s*\d{4}|all rights reserved|copyright|wiley-vch", re.I)
FUNDING = re.compile(r"\b(supported|funded|sponsored|funding|grants?|programme|program)\b", re.I)
NUM_RANGE = re.compile(r"^\d+[-\u2013]\d+$")


def flex_spaces(rx: str) -> str:
    """Literal spaces outside character classes match any whitespace run (pymupdf text wraps lines mid-name); an
    optional space (" ?", " *") matches zero or more whitespace characters (D292, audit finding 1)."""
    out: list[str] = []
    depth, esc, i = 0, False, 0
    while i < len(rx):
        ch = rx[i]
        if esc:
            out.append(ch)
            esc = False
        elif ch == "\\":
            out.append(ch)
            esc = True
        elif ch == "[":
            depth += 1
            out.append(ch)
        elif ch == "]" and depth:
            depth -= 1
            out.append(ch)
        elif ch == " " and not depth:
            nxt = rx[i + 1] if i + 1 < len(rx) else ""
            if nxt in "?*":
                out.append(r"\s*")
                i += 1
            elif nxt == "+":
                out.append(r"\s+")
                i += 1
            else:
                out.append(r"\s+")
        else:
            out.append(ch)
        i += 1
    return "".join(out)


@dataclass
class Vendor:
    name: str
    org_id: str
    cat: str
    rx: re.Pattern[str]
    origin: str  # gazetteer | registry

    @property
    def key(self) -> str:
        """Grouping key: one candidate per sentence and vendor entity (registry twins of a gazetteer vendor share it)."""
        return self.org_id or self.name


@dataclass
class Model:
    rx: re.Pattern[str]
    vendor: str
    cat: str
    type: str
    infer: bool


@dataclass
class Dictionary:
    vendors: list[Vendor]
    models: list[Model]
    cues: re.Pattern[str]
    config_sha: str = ""
    lineage: dict[str, list[str]] = field(default_factory=dict)
    org_keys: set[str] = field(default_factory=set)
    warnings: list[str] = field(default_factory=list)
    by_name: dict[str, Vendor] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.by_name = {v.name: v for v in self.vendors if v.origin == "gazetteer"}


def _letters(s: str) -> int:
    return sum(c.isalpha() for c in s)


def load_dictionary(config: Path = CONFIG, registry: Path = REGISTRY) -> Dictionary:
    """Gazetteer org = explicit `org`, else the registry match of the vendor name (orgmatch, no ROR) unless
    `resolve: false` (ambiguous names); vendor names of >= 5 letters match case-insensitively unless `case: true`
    (D293). Registry orgs of vendor-like types are added by name and alias, except orgs the gazetteer covers, forms
    equal to a gazetteer name, stoplisted forms and all-capital forms of <= 4 characters (acronyms, D292)."""
    raw = config.read_bytes()
    cfg: dict[str, Any] = yaml.safe_load(raw)
    orgs = {o["org_id"]: o for o in read_csv(registry / "organizations.csv")}
    matcher = load_matcher(registry, with_ror=False)
    vendors: list[Vendor] = []
    seen_orgs: set[str] = set()
    for v in cfg["vendors"]:
        oid = str(v.get("org") or "")
        if oid and oid not in orgs:
            raise ValueError(f"supply_scanner.yaml vendor {v['name']}: org {oid} not in the registry")
        if not oid and v.get("resolve", True):
            ids, _ = matcher.match(str(v["name"]), "")
            oid = ids[0] if len(ids) == 1 else ""
        flags = 0 if v.get("case") or _letters(str(v["name"])) < 5 else re.I
        rx = re.compile(WORD.format(flex_spaces(v["re"])), flags)
        vendors.append(Vendor(str(v["name"]), oid, str(v["cat"]), rx, "gazetteer"))
        if oid:
            seen_orgs.add(oid)
    names = {v.name for v in vendors}
    if len(names) != len(vendors):
        raise ValueError("supply_scanner.yaml: duplicate vendor names")
    lineage = {str(k): [str(x) for x in vs] for k, vs in (cfg.get("lineage") or {}).items()}
    for k, vs in lineage.items():
        if bad := [x for x in [k, *vs] if x not in names]:
            raise ValueError(f"supply_scanner.yaml lineage {k}: unknown vendors {bad}")
    types = set(cfg.get("registry_org_types") or [])
    fac_types = set(cfg.get("registry_facility_types") or [])
    stop = set(cfg.get("stoplist") or [])
    keep_short = set(cfg.get("registry_short_forms_keep") or [])
    gz_names = {norm_ws(n).lower() for n in names}
    forms: dict[str, set[str]] = {}
    for o in orgs.values():
        if (o["org_type"] in types or o["org_type"] in fac_types) and o["org_id"] not in seen_orgs:
            forms.setdefault(o["org_id"], set()).add(o["name"])
    for a in read_csv(registry / "org_aliases.csv"):
        if a["org_id"] in forms:
            forms[a["org_id"]].add(a["alias"])
    for oid, fs in sorted(forms.items()):
        keep = sorted(
            {
                f.strip()
                for f in fs
                if len(f.strip()) >= 3
                and f.strip() not in stop
                and norm_ws(f).lower() not in gz_names
                and (not SHORT_ACRONYM.fullmatch(f.strip()) or f.strip() in keep_short)
            },
            key=len,
            reverse=True,
        )
        if not keep:
            continue
        rx = re.compile(WORD.format("|".join(r"\s+".join(map(re.escape, f.split())) for f in keep)))
        origin = "facility" if orgs[oid]["org_type"] in fac_types else "registry"
        vendors.append(Vendor(orgs[oid]["name"], oid, "B7" if origin == "facility" else "", rx, origin))
    models: list[Model] = []
    for m in cfg["models"]:
        if m["vendor"] not in names:
            raise ValueError(f"supply_scanner.yaml model {m['re']}: vendor {m['vendor']} not in vendors")
        rx = re.compile(WORD.format(flex_spaces(m["re"])))
        models.append(Model(rx, str(m["vendor"]), str(m["cat"]), str(m["type"]), bool(m.get("infer", True))))
    cues = re.compile(cfg["usage_cues"], re.I)
    # D318: a gazetteer vendor without org whose pattern matches a registry org name is a gap in the config (unless
    # `resolve: false` says the match is intentional or ambiguous).
    warnings = []
    for gv, v in zip(vendors, cfg["vendors"], strict=False):
        if gv.origin == "gazetteer" and not gv.org_id and v.get("resolve", True):
            hits = sorted(o["org_id"] for o in orgs.values() if gv.rx.fullmatch(o["name"]))
            if hits:
                warnings.append(f"gazetteer vendor {gv.name} has no org but matches registry {hits}")
    org_keys = {norm_key(o["name"]) for o in orgs.values()}
    org_keys |= {norm_key(a["alias"]) for a in read_csv(registry / "org_aliases.csv")}
    return Dictionary(vendors, models, cues, hashlib.sha1(raw).hexdigest()[:12], lineage, org_keys, warnings)


def page_marks(text: str, corpus: str) -> list[tuple[int, str]]:
    """(offset, locator) where each page starts; offset 0 = pNA unless a marker sits there (D4). OFC: figure markers
    `_page_k_` and span anchors `<span id="page-k-m">` both mean 0-based page k -> p.~(k+1) (D292)."""
    if corpus == "ofc2026":
        marks = [(m.end(), f"p.~{int(m.group(1) or m.group(2)) + 1}") for m in PAGE_OFC.finditer(text)]
        return [(0, "pNA"), *marks]
    return [(0, "pNA"), *[(m.end(), f"p.{m.group(1)}") for m in PAGE_MD.finditer(text)]]


def locator_at(marks: list[tuple[int, str]], pos: int) -> str:
    loc = "pNA"
    for off, lab in marks:
        if off <= pos:
            loc = lab
        else:
            break
    return loc


def _ref_heading(text: str, start: int, end: int, h: str) -> bool:
    """A singular "Reference" line is a reference-list heading only when a first entry ([1] / 1.) follows within
    400 characters (comparison tables use "Reference" as a column header, lit:mu2026)."""
    if not REF_HEADING.match(h):
        return False
    if h.lower() != "reference":
        return True
    return bool(REF_ENTRY.search(text[end : end + 400]))


def regions(text: str) -> list[tuple[int, int, str]]:
    """(start, end, kind) with kind in front / body / ack / coi / refs (refs are not scanned). Front = text before the
    first Abstract / Introduction line in the first 30 % of the text; a reference list runs from a References heading
    in the last 70 % (or, with no such heading, from a line starting with [1] followed by [2], bullets allowed) to the
    next Methods / Acknowledgements / Supplementary / ... heading; an acknowledgements or competing-interest block ends
    at the next known heading. Inline labels ("Acknowledgements: we thank ...") zone their paragraph (to a blank line,
    the next known heading, or 1500 characters)."""
    n = len(text)
    heads = [(m.start(), m.end(), m.group("h").strip()) for m in HEADING_LINE.finditer(text)]
    have = {st for st, _, _ in heads}
    heads += [(m.start(), m.end(), "supplementary") for m in SUPP_LINE.finditer(text) if m.start() not in have]
    heads.sort()
    # With no References heading before it, a [1] ... [2] run starts the reference list (a later "Supplementary
    # References" heading does not count, D343).
    refs_h = [(st, h) for st, en, h in heads if st > n * 0.3 and _ref_heading(text, st, en, h)]
    if not [st for st, h in refs_h if h.lower() != "supplementary references"]:
        upto = min((st for st, _ in refs_h), default=n)
        for m in REF_FIRST.finditer(text, int(n * 0.4), upto):
            if re.search(r"^\s*(?:[-*]\s*)?\[2\]", text[m.end() : m.end() + 3000], re.M):
                heads.append((m.start(), m.start(), "references"))
                heads.sort()
                break
    out: list[tuple[int, int, str]] = []
    fm = FRONT_END.search(text, 0, max(1, n * 3 // 10))
    pos, kind = 0, "body"
    if fm:
        out.append((0, fm.start(), "front"))
        pos = fm.start()
    for start, end, h in heads:
        if start < pos:
            continue
        early_oe = start <= n * 0.3 and any(st > start and hh.lower() == "introduction" for st, _, hh in heads)
        # D326a: OE-format reference lists precede the body
        if (start > n * 0.3 or early_oe) and _ref_heading(text, start, end, h):
            new = "refs"
        elif ACK_HEADING.match(h):
            new = "ack"
        elif COI_HEADING.match(h):
            new = "coi"
        elif kind == "refs" and not AFTER_REFS.match(h):
            new = "refs"
        elif REF_HEADING.match(h):
            new = kind
        else:
            new = "body"
        if new != kind:
            out.append((pos, start, kind))
            pos, kind = start, new
    out.append((pos, n, kind))
    base = [r for r in out if r[1] > r[0]]
    # Inline ack / coi labels overlay body text (never refs).
    head_starts = sorted(st for st, _, _ in heads)
    for m in INLINE_LABEL.finditer(text):
        st = m.start()
        lab = "coi" if COI_HEADING.match(m.group("h")) else "ack"
        blank = re.search(r"\n\s*\n", text[m.end() :])
        end = min(n, st + 1500, m.end() + blank.start() if blank else n)
        nxt = bisect.bisect_right(head_starts, st)
        if nxt < len(head_starts):
            end = min(end, head_starts[nxt])
        base = _overlay(base, st, end, lab)
    return base


def _overlay(rs: list[tuple[int, int, str]], s: int, e: int, kind: str) -> list[tuple[int, int, str]]:
    out: list[tuple[int, int, str]] = []
    for a, b, k in rs:
        if b <= s or a >= e or k in ("refs", "front"):
            out.append((a, b, k))
            continue
        if a < s:
            out.append((a, s, k))
        out.append((max(a, s), min(b, e), kind))
        if b > e:
            out.append((e, b, k))
    return [r for r in out if r[1] > r[0]]


def sentences(text: str, start: int, end: int) -> Iterator[tuple[int, int]]:
    """Sentence spans; no split inside parentheses or after an abbreviation (Inc., Co., Fig., e.g., initials; D292)."""
    pos = start
    for m in SENT_SPLIT.finditer(text, start, end):
        if m.group(0).count("\n") < 2:  # not a paragraph break
            seg = text[pos : m.start()]
            if len(seg) < 1500 and (seg.count("(") > seg.count(")") or ABBREV.search(seg[-12:])):
                continue
        if m.start() > pos:
            yield pos, m.start()
        pos = m.end()
    if end > pos:
        yield pos, end


def _context(text: str, s: int, e: int, at: int) -> str:
    if e - s > CONTEXT_MAX:
        s = max(s, at - CONTEXT_MAX // 2)
        e = min(e, s + CONTEXT_MAX)
    return re.sub(r"\s+", " ", text[s:e]).strip()


def clean_model(model: str) -> str:
    """Printed model as a candidate string: whitespace collapsed, line-break hyphens joined ("VCM- 330MS" ->
    "VCM-330MS"), trailing punctuation and trailing lowercase words dropped (D292, audit findings 2-3)."""
    m = norm_ws(model)
    m = re.sub(r"(\w)- (\w)", r"\1-\2", m)
    m = re.sub(r"[)\],.;:]+$", "", m)
    toks = m.split(" ")
    while len(toks) > 1 and re.fullmatch(r"[a-z]{2,}", toks[-1]):
        toks.pop()
    return " ".join(toks)


def scan_text(text: str, corpus: str, source_id: str, d: Dictionary) -> list[dict[str, Any]]:
    marks = page_marks(text, corpus)
    out: list[dict[str, Any]] = []
    for rs, rend, kind in regions(text):
        if kind == "refs":
            continue
        sents = list(sentences(text, rs, rend))
        starts = [a for a, _ in sents]
        vend: dict[int, dict[str, tuple[Vendor, re.Match[str]]]] = {}
        for v in d.vendors:
            for vm in v.rx.finditer(text, rs, rend):
                i = bisect.bisect_right(starts, vm.start()) - 1
                vend.setdefault(i, {}).setdefault(v.key, (v, vm))
        mods: dict[int, list[tuple[Model, re.Match[str]]]] = {}
        taken: list[tuple[int, int]] = []
        for mdl in d.models:
            for mm in mdl.rx.finditer(text, rs, rend):
                if any(mm.start() < b and a < mm.end() for a, b in taken):
                    continue
                taken.append((mm.start(), mm.end()))
                mods.setdefault(bisect.bisect_right(starts, mm.start()) - 1, []).append((mdl, mm))
        for i, (s, e) in enumerate(sents):
            sv = vend.get(i, {})
            sm = mods.get(i, [])
            sent = text[s:e]
            zone = kind
            if kind == "body" and (
                AFFIL.search(sent) or (locator_at(marks, s) in ("pNA", "p.1", "p.~1") and ADDRESS.search(sent))
            ):
                zone = "affil"
            cue = bool(d.cues.search(sent))
            if zone not in ("body", "ack"):  # D299a: facilities only in methods / acknowledgement text
                sv = {k: x for k, x in sv.items() if x[0].origin != "facility"}
            used: set[str] = set()
            for mdl, mm in sorted(sm, key=lambda x: x[1].start()):
                gv = d.by_name[mdl.vendor]
                hit = sv.get(gv.key)
                if hit is None:  # a lineage predecessor printed with the model (Agilent 8164B, Ando AQ6317B)
                    for alt in d.lineage.get(gv.name, []):
                        hit = sv.get(d.by_name[alt].key)
                        if hit:
                            break
                if hit:
                    used.add(hit[0].key)
                vv = hit[0] if hit and hit[0].origin == "gazetteer" else gv
                out.append(
                    _cand(text, corpus, source_id, marks, s, e, mm.start(), zone, cue, vv, hit, mdl, mm.group(0))
                )
            for key, (v, vm) in sv.items():
                if key not in used:
                    out.append(_cand(text, corpus, source_id, marks, s, e, vm.start(), zone, cue, v, (v, vm), None, ""))
            if zone == "body":  # D299c: never front matter, acknowledgements or funding text
                out.extend(_unlisted(text, corpus, source_id, marks, s, e, zone, cue, d, sv, sm))
    return out


def _model_token(tok: str) -> bool:
    """A printed model: letters and digits, no unit or measurement (1550nm, 8,000cm2/Vs), no numeric range."""
    if not MODEL_TOKEN.match(tok) or not tok.isascii() or NUM_RANGE.match(tok):
        return False
    return not any(UNIT_TOKEN.match(x) for x in tok.split("/")) and not re.search(r"\d(cm|nm|um|mm)\d?\b", tok)


def _vendor_name(name: str) -> bool:
    """Capitalized name of 1-4 words with at least 3 consecutive letters; not a stop word, initials or a person."""
    return bool(
        NAME.fullmatch(name)
        and name.split()[0].lower() not in NAME_STOP
        and re.search(r"[A-Za-z]{3}", name)
        and not re.fullmatch(r"([A-Z]\.\s?)+[A-Z][a-z]+", name)
    )


def _known(name: str, d: Dictionary) -> bool:
    return any(v.rx.search(name) for v in d.vendors)


def _unlisted(
    text: str,
    corpus: str,
    source_id: str,
    marks: list[tuple[int, str]],
    s: int,
    e: int,
    zone: str,
    cue: bool,
    d: Dictionary,
    sv: dict[str, tuple[Vendor, re.Match[str]]],
    sm: list[tuple[Model, re.Match[str]]],
) -> list[dict[str, Any]]:
    """Gazetteer-independent candidates (D294): "(Name Model)", "(Model, Name ...)" parentheticals and company names
    with a legal suffix, when no dictionary vendor or model already matches inside the span."""
    found: list[tuple[int, str, str]] = []
    if FUNDING.search(text[s:e]):
        return []
    covered = [vm.span() for _, vm in sv.values()] + [mm.span() for _, mm in sm]

    def free(a: int, b: int) -> bool:
        return not any(x < b and a < y for x, y in covered)

    for pm in PAREN.finditer(text, s, e):
        if not free(*pm.span()):
            continue
        parts = [LEGAL_TAIL.sub("", p.strip()) for p in re.split(r"[;,]", pm.group(1)) if p.strip()]
        name, model = "", ""
        for p in parts:
            toks = p.split()
            if len(toks) >= 2 and _vendor_name(" ".join(toks[:-1])):
                nm, tok = " ".join(toks[:-1]), toks[-1]
                # D321: an all-digit model only next to a registry org name ("(Metricon 2010)").
                digits = tok.isdigit() and len(tok) >= 3 and norm_key(nm) in d.org_keys
                if _model_token(tok) or digits:
                    name, model = nm, tok
                    break
        if not name:
            mod = next((p for p in parts if _model_token(p)), "")
            nam = next((p for p in parts if p != mod and _vendor_name(p)), "")
            if mod and nam:
                name, model = nam, mod
        if name and model and not _known(name, d):
            found.append((pm.start() + 1 + pm.group(1).find(name), name, model))
    for cm in COMPANY.finditer(text, s, e):
        nm = cm.group("name")
        ls = text.rfind("\n", 0, cm.start()) + 1
        le = text.find("\n", cm.end())
        if FOOTER_LINE.search(text[ls : le if le >= 0 else len(text)]):
            continue
        if free(*cm.span()) and _vendor_name(nm) and not _known(nm, d):
            if not any(norm_ws(nm) == f[1] or nm in f[1] for f in found):
                found.append((cm.start(), norm_ws(nm), ""))
    out = []
    for at, name, model in found:
        v = Vendor(norm_ws(name), "", "", re.compile(re.escape(name)), "unlisted")
        cand = _cand(text, corpus, source_id, marks, s, e, at, zone, cue, v, None, None, model)
        cand.update(kind="unlisted", vendor_printed=norm_ws(name), vendor_origin="unlisted")
        out.append(cand)
    return out


def _cand(
    text: str,
    corpus: str,
    source_id: str,
    marks: list[tuple[int, str]],
    s: int,
    e: int,
    at: int,
    zone: str,
    cue: bool,
    v: Vendor,
    hit: tuple[Vendor, re.Match[str]] | None,
    mdl: Model | None,
    model: str,
) -> dict[str, Any]:
    """Candidate record. The id hashes only what the paper prints (source, offset, printed vendor, printed model), so it
    is stable when the gazetteer or the registry changes (D293)."""
    kind = "vendor+model" if (mdl and hit) else ("model" if mdl else "vendor")
    model = clean_model(model)
    printed = norm_ws(hit[1].group(0)) if hit else ""
    cid = hashlib.sha1(f"{source_id}|{at}|{printed}|{model}".encode()).hexdigest()[:12]
    return {
        "cand_id": f"c{cid}",
        "source_id": source_id,
        "corpus": corpus,
        "locator": locator_at(marks, at),
        "zone": zone,
        "kind": kind,
        "cue": cue,
        "vendor": v.name,
        "vendor_printed": printed,
        "org_id": v.org_id,
        "vendor_origin": v.origin,
        "model": model,
        "model_type": mdl.type if mdl else "",
        "cat_hint": mdl.cat if mdl else v.cat,
        "infer_ok": bool(mdl.infer) if mdl else False,
        "offset": at,
        "context": _context(text, s, e, at),
    }


def page_text(text: str, corpus: str, locator: str) -> str:
    """Text of the page a locator names (first token p.N / p.~N / pNA); '' when the page is not found."""
    tok = locator.split()[0].rstrip(";,") if locator else ""
    marks = page_marks(text, corpus)
    parts = []
    for i, (off, lab) in enumerate(marks):
        if lab == tok:
            parts.append(text[off : marks[i + 1][0] if i + 1 < len(marks) else len(text)])
    return "".join(parts)


def norm_ws(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def text_path(source_id: str) -> Path | None:
    """Cached text of a source (eo / pk / lit text.md, OFC extracted .md); None when not cached."""
    corpus, _, native = source_id.partition(":")
    if corpus == "ofc2026":
        od = input_path("ofc_text_dir")
        hits = sorted(od.glob(f"{native}-*.md")) if od.is_dir() else []
        return hits[0] if hits else None
    base = {"eo": lambda: input_path("eo_atlas") / "references", "pk": lambda: input_path("pk_atlas") / "references"}
    root = base[corpus]() if corpus in base else (ROOT / "references" if corpus == "lit" else None)
    p = root / native / "text.md" if root else None
    return p if p and p.exists() else None


def text_variants(s: str) -> list[str]:
    """Normalized forms of a page for string checks: NFKC (ligatures), whitespace collapsed, and two de-hyphenations
    of line-break hyphens ("Amo- nics" -> "Amonics"; "VCM- 330MS" -> "VCM-330MS")."""
    t = norm_ws(unicodedata.normalize("NFKC", s))
    return [t, re.sub(r"(\w)- (\w)", r"\1\2", t), re.sub(r"(\w)- (\w)", r"\1-\2", t)]


def printed_on(needle: str, page: str) -> bool:
    n = norm_ws(unicodedata.normalize("NFKC", needle))
    return bool(n) and any(n in v for v in text_variants(page))
