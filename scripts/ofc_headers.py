"""OFC 2026 paper-header extraction: queue, extraction aid and checker (DevLog-008, D170-D179).

Batches live in data/_staging/people/ofc_headers/<batch>/: papers.csv (queue), headers.yaml (written by the extractor,
see CONTRACT.md), and the derived header_rows.csv, compare.csv, unmapped_orgs.csv (written by `check`).

Usage:
  uv run python scripts/ofc_headers.py pilot CODE [CODE ...]      # write pilot/papers.csv (refuses to overwrite)
  uv run python scripts/ofc_headers.py queue [--size 40] [--dry-run]  # batches ofc_hNN of the remaining papers
  uv run python scripts/ofc_headers.py show <batch> [--codes C ...] [--pdf]  # header text (contacts masked) + metadata
  uv run python scripts/ofc_headers.py check <batch> [<batch> ...] [--dry-run]  # validate; derived files at 0 errors
  uv run python scripts/ofc_headers.py aggregate   # coordinator: org_requests.csv + local lists from all batches

`show` prints to the terminal only (restricted corpus, D172); nothing it prints is stored. The merge into the people
build is designed in DevLog-008 and not implemented here.
"""

from __future__ import annotations

import argparse
import bisect
import csv
import hashlib
import io
import os
import re
import sys
from collections import Counter, defaultdict
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, ValidationError

from photonics_atlas.adapters import ofc
from photonics_atlas.csvio import _cell, read_csv, split_list, write_csv
from photonics_atlas.orgmatch import Matcher, load_matcher
from photonics_atlas.paths import CROSSWALK, REGISTRY, ROOT, STAGING, input_path
from photonics_atlas.people import SPELLED_EMAIL_RE, fold, org_root
from photonics_atlas.rules_people import PHONE_RE
from photonics_atlas.runlog import RunLog
from photonics_atlas.textnorm import EMAIL_RE, ascii_fold, norm_key

BASE = STAGING / "people" / "ofc_headers"
PILOT = "pilot"
ABSTRACT_RE = re.compile(r"(\*\*\s*Abstract|^\s*Abstract|Abstract\s*:)", re.M | re.I)
CODE_RE = re.compile(r"^(M|Tu|W|Th)(\d+)([A-Z]+)\.(\d+)$")
DAY = {"M": 0, "Tu": 1, "W": 2, "Th": 3}
LOCATOR_RE = re.compile(r"^p\.~[0-9]+( [a-z]+)?$")
COUNTRY_RE = re.compile(r"^[A-Z]{2}$")
# D176 (a): contact data in any file of a batch directory.
CONTACT_RES = [
    ("at sign", re.compile(r"[@＠]")),
    ("e-mail", EMAIL_RE),
    ("spelled e-mail", SPELLED_EMAIL_RE),
    ("phone", PHONE_RE),
    ("url", re.compile(r"https?:|www\.", re.I)),
    ("e-mail word", re.compile(r"\be-?mail\b", re.I)),
]
# D244: no street addresses or postal codes in committed files (restricted corpus).
ADDRESS_RES = [
    ("postal code", re.compile(r"\b\d{3}-\d{4}\b|\b\d{5}(?:-\d{4})?\b|\b\d{6}\b|\b\d{3} \d{2}\b")),
    ("postal code", re.compile(r"\b[A-Z]{1,2}\d[A-Z\d]? \d[A-Z]{2}\b")),  # UK
    ("postal code", re.compile(r"\b\d{4} ?[A-Z]{2}\b")),  # NL
    ("postal code", re.compile(r"\b[A-Z]\d[A-Z] ?\d[A-Z]\d\b")),  # CA
    ("postal code", re.compile(r"\b[A-Z]{1,2}-\d{4,5}\b")),  # DK-2800, CH-8092, D-70569
    ("street number", re.compile(r"\b\d{1,4}-\d{1,4}-\d{1,4}\b|#\d+-\d+|\b\d{4}-\d{3}\b|\b\d{1,4}-\d{1,4},\s+[A-Z]")),
    (
        "street",
        re.compile(
            r"\b\d+[A-Za-z]?,?\s+(?:[A-Z][\w.'-]*\s+){0,3}(?:Street|St|Road|Rd|Avenue|Ave|Boulevard|Blvd|Drive|Dr|Way|"
            r"Lane|Ln|Plaza|Strasse|Straße|Weg|Ring|Science Park)\b|\b(?:Via|Rue|Calle|Avenida|Carrer)\s+[A-Z]"
        ),
    ),
    (  # house number after the street name (NL / DE / BE / DK / SE form)
        "street",
        re.compile(
            r"\b[A-Z][a-zäöüåæø]+(?:straat|strasse|straße|weg|laan|gasse|plein|dreef|vej|gade|allee|platz|ring|"
            r"gatan|vägen|kade|singel|park)\s+\d+|\b(?:Street|St|Road|Rd|Avenue|Ave)\.?\s+\d+"
        ),
    ),
    ("room / building", re.compile(r"\b(?:Room|Rm|Building|Bldg|Floor|Fl|Suite|Level)\.?\s*[A-Z]?\d+", re.I)),
    ("postal code + city", re.compile(r"\b\d{4}\s+[A-Z][a-z]+")),
]
ISO_DATE_RE = re.compile(r"\b\d{4}-\d{2}-\d{2}(?:[T ]\d{2}:\d{2}(?::\d{2})?)?\b")
LISTING_NOTE = "affiliation marker inferred from block order"
GRADE_OF_BASIS = {  # D240, D246
    "listing_order": ("B", LISTING_NOTE),
    "layout": ("B", "affiliation grouping read from the printed layout"),
}
STAMP = "check_stamp.txt"
DERIVED = {"header_rows.csv", "compare.csv", "unmapped_orgs.csv", STAMP}
# D246: printed country names / forms per ISO 3166-1 alpha-2 code (word match inside the block window). HK, MO, TW
# carry their own codes when the block prints them (registry convention).
COUNTRIES: dict[str, tuple[str, ...]] = {  # all 249 ISO 3166-1 alpha-2 codes (D286a): printed names / forms
    "AD": ("andorra",),
    "AE": ("united arab emirates", "uae"),
    "AF": ("afghanistan",),
    "AG": ("antigua and barbuda",),
    "AI": ("anguilla",),
    "AL": ("albania",),
    "AM": ("armenia",),
    "AO": ("angola",),
    "AQ": ("antarctica",),
    "AR": ("argentina",),
    "AS": ("american samoa",),
    "AT": ("austria",),
    "AU": ("australia",),
    "AW": ("aruba",),
    "AX": ("aland islands",),
    "AZ": ("azerbaijan",),
    "BA": ("bosnia and herzegovina", "bosnia"),
    "BB": ("barbados",),
    "BD": ("bangladesh",),
    "BE": ("belgium",),
    "BF": ("burkina faso",),
    "BG": ("bulgaria",),
    "BH": ("bahrain",),
    "BI": ("burundi",),
    "BJ": ("benin",),
    "BL": ("saint barthelemy",),
    "BM": ("bermuda",),
    "BN": ("brunei", "brunei darussalam"),
    "BO": ("bolivia",),
    "BQ": ("bonaire",),
    "BR": ("brazil", "brasil"),
    "BS": ("bahamas",),
    "BT": ("bhutan",),
    "BV": ("bouvet island",),
    "BW": ("botswana",),
    "BY": ("belarus",),
    "BZ": ("belize",),
    "CA": ("canada",),
    "CC": ("cocos islands",),
    "CD": ("democratic republic of the congo", "dr congo"),
    "CF": ("central african republic",),
    "CG": ("republic of the congo", "congo"),
    "CH": ("switzerland",),
    "CI": ("cote d ivoire", "ivory coast"),
    "CK": ("cook islands",),
    "CL": ("chile",),
    "CM": ("cameroon",),
    "CN": ("china", "p r china", "pr china", "prc", "p r c", "people s republic of china", "peoples republic of china"),
    "CO": ("colombia",),
    "CR": ("costa rica",),
    "CU": ("cuba",),
    "CV": ("cabo verde", "cape verde"),
    "CW": ("curacao",),
    "CX": ("christmas island",),
    "CY": ("cyprus",),
    "CZ": ("czech republic", "czechia"),
    "DE": ("germany", "deutschland"),
    "DJ": ("djibouti",),
    "DK": ("denmark",),
    "DM": ("dominica",),
    "DO": ("dominican republic",),
    "DZ": ("algeria",),
    "EC": ("ecuador",),
    "EE": ("estonia",),
    "EG": ("egypt",),
    "EH": ("western sahara",),
    "ER": ("eritrea",),
    "ES": ("spain", "espana"),
    "ET": ("ethiopia",),
    "FI": ("finland",),
    "FJ": ("fiji",),
    "FK": ("falkland islands",),
    "FM": ("micronesia",),
    "FO": ("faroe islands",),
    "FR": ("france",),
    "GA": ("gabon",),
    "GB": ("uk", "u k", "united kingdom", "england", "scotland", "wales", "northern ireland", "great britain"),
    "GD": ("grenada",),
    "GE": ("georgia",),
    "GF": ("french guiana",),
    "GG": ("guernsey",),
    "GH": ("ghana",),
    "GI": ("gibraltar",),
    "GL": ("greenland",),
    "GM": ("gambia",),
    "GN": ("guinea",),
    "GP": ("guadeloupe",),
    "GQ": ("equatorial guinea",),
    "GR": ("greece",),
    "GS": ("south georgia",),
    "GT": ("guatemala",),
    "GU": ("guam",),
    "GW": ("guinea bissau",),
    "GY": ("guyana",),
    "HK": ("hong kong", "hong kong sar"),
    "HM": ("heard island",),
    "HN": ("honduras",),
    "HR": ("croatia",),
    "HT": ("haiti",),
    "HU": ("hungary",),
    "ID": ("indonesia",),
    "IE": ("ireland",),
    "IL": ("israel",),
    "IM": ("isle of man",),
    "IN": ("india",),
    "IO": ("british indian ocean territory",),
    "IQ": ("iraq",),
    "IR": ("iran",),
    "IS": ("iceland",),
    "IT": ("italy", "italia"),
    "JE": ("jersey",),
    "JM": ("jamaica",),
    "JO": ("jordan",),
    "JP": ("japan",),
    "KE": ("kenya",),
    "KG": ("kyrgyzstan",),
    "KH": ("cambodia",),
    "KI": ("kiribati",),
    "KM": ("comoros",),
    "KN": ("saint kitts and nevis",),
    "KP": ("north korea", "dprk"),
    "KR": ("korea", "south korea", "republic of korea", "r o korea", "rep of korea"),
    "KW": ("kuwait",),
    "KY": ("cayman islands",),
    "KZ": ("kazakhstan",),
    "LA": ("laos", "lao pdr"),
    "LB": ("lebanon",),
    "LC": ("saint lucia",),
    "LI": ("liechtenstein",),
    "LK": ("sri lanka",),
    "LR": ("liberia",),
    "LS": ("lesotho",),
    "LT": ("lithuania",),
    "LU": ("luxembourg",),
    "LV": ("latvia",),
    "LY": ("libya",),
    "MA": ("morocco",),
    "MC": ("monaco",),
    "MD": ("moldova",),
    "ME": ("montenegro",),
    "MF": ("saint martin",),
    "MG": ("madagascar",),
    "MH": ("marshall islands",),
    "MK": ("north macedonia", "macedonia"),
    "ML": ("mali",),
    "MM": ("myanmar",),
    "MN": ("mongolia",),
    "MO": ("macau", "macao"),
    "MP": ("northern mariana islands",),
    "MQ": ("martinique",),
    "MR": ("mauritania",),
    "MS": ("montserrat",),
    "MT": ("malta",),
    "MU": ("mauritius",),
    "MV": ("maldives",),
    "MW": ("malawi",),
    "MX": ("mexico",),
    "MY": ("malaysia",),
    "MZ": ("mozambique",),
    "NA": ("namibia",),
    "NC": ("new caledonia",),
    "NE": ("niger",),
    "NF": ("norfolk island",),
    "NG": ("nigeria",),
    "NI": ("nicaragua",),
    "NL": ("netherlands", "the netherlands", "holland"),
    "NO": ("norway",),
    "NP": ("nepal",),
    "NR": ("nauru",),
    "NU": ("niue",),
    "NZ": ("new zealand",),
    "OM": ("oman",),
    "PA": ("panama",),
    "PE": ("peru",),
    "PF": ("french polynesia",),
    "PG": ("papua new guinea",),
    "PH": ("philippines",),
    "PK": ("pakistan",),
    "PL": ("poland",),
    "PM": ("saint pierre and miquelon",),
    "PN": ("pitcairn",),
    "PR": ("puerto rico",),
    "PS": ("palestine",),
    "PT": ("portugal",),
    "PW": ("palau",),
    "PY": ("paraguay",),
    "QA": ("qatar",),
    "RE": ("reunion",),
    "RO": ("romania",),
    "RS": ("serbia",),
    "RU": ("russia", "russian federation"),
    "RW": ("rwanda",),
    "SA": ("saudi arabia",),
    "SB": ("solomon islands",),
    "SC": ("seychelles",),
    "SD": ("sudan",),
    "SE": ("sweden",),
    "SG": ("singapore", "republic of singapore"),
    "SH": ("saint helena",),
    "SI": ("slovenia",),
    "SJ": ("svalbard",),
    "SK": ("slovakia",),
    "SL": ("sierra leone",),
    "SM": ("san marino",),
    "SN": ("senegal",),
    "SO": ("somalia",),
    "SR": ("suriname",),
    "SS": ("south sudan",),
    "ST": ("sao tome and principe",),
    "SV": ("el salvador",),
    "SX": ("sint maarten",),
    "SY": ("syria",),
    "SZ": ("eswatini", "swaziland"),
    "TC": ("turks and caicos islands",),
    "TD": ("chad",),
    "TF": ("french southern territories",),
    "TG": ("togo",),
    "TH": ("thailand",),
    "TJ": ("tajikistan",),
    "TK": ("tokelau",),
    "TL": ("timor leste", "east timor"),
    "TM": ("turkmenistan",),
    "TN": ("tunisia",),
    "TO": ("tonga",),
    "TR": ("turkey", "turkiye"),
    "TT": ("trinidad and tobago",),
    "TV": ("tuvalu",),
    "TW": ("taiwan", "taiwan r o c", "r o c"),
    "TZ": ("tanzania",),
    "UA": ("ukraine",),
    "UG": ("uganda",),
    "UM": ("united states minor outlying islands",),
    "US": ("usa", "u s a", "us", "u s", "united states", "united states of america"),
    "UY": ("uruguay",),
    "UZ": ("uzbekistan",),
    "VA": ("vatican", "holy see"),
    "VC": ("saint vincent and the grenadines",),
    "VE": ("venezuela",),
    "VG": ("british virgin islands",),
    "VI": ("us virgin islands",),
    "VN": ("vietnam", "viet nam"),
    "VU": ("vanuatu",),
    "WF": ("wallis and futuna",),
    "WS": ("samoa",),
    "YE": ("yemen",),
    "YT": ("mayotte",),
    "ZA": ("south africa",),
    "ZM": ("zambia",),
    "ZW": ("zimbabwe",),
}
PAPER_COLS = ["source_id", "code", "n_authors_meta", "local_pdf"]
ROW_COLS = [
    "source_id",
    "author_index",
    "header_pos",
    "printed_name",
    "aff_order",
    "aff_marker",
    "aff_role",
    "org_k",
    "org_name",
    "unit",
    "locality",
    "country",
    "marker_basis",
    "evidence_grade",
    "grade_note",
    "locator",
    "org_ids",
    "match_basis",
]
CMP_COLS_LIT_EXTRA = ["order_differs"]  # D363: lit only (OFC compare.csv unchanged)
CMP_COLS = [
    "source_id",
    "author_index",
    "meta_name",
    "header_name",
    "meta_org_ids",
    "header_org_ids",
    "n_aff_rows",
    "present_address",
    "outcome",
]
UNMAPPED_COLS = ["org_name", "unit", "country", "n_rows", "examples"]
LOCAL = ROOT / "data" / "_local"
REQUEST_COLS = ["printed_org", "unit", "locality", "country", "count", "locators", "proposed_org_id", "curation_note"]
# D305: requests that need more than an alias (no registry edit here; the org-curation stream decides)
CURATION_NOTES = {
    "State Key Laboratory of Optical Fiber and Cable Manufacture Technology": (
        "request: child org of org_yofc (printed as a YOFC unit in YOFC blocks and as a separate org beside China "
        "Telecom Research Institute; DevLog-008 D305)"
    ),
}
CONFLICT_COLS = [
    "source_id",
    "author_index",
    "meta_name",
    "header_name",
    "meta_affiliation",
    "meta_org_ids",
    "header_org_ids",
]
EXTRA_AUTHOR_COLS = ["source_id", "header_pos", "printed_name", "markers", "note"]


# ---------------------------------------------------------------- YAML model (CONTRACT.md)


class _Loader(yaml.SafeLoader):
    """SafeLoader whose booleans are only true / false: YAML 1.1 reads NO (Norway), YES, ON, OFF as booleans."""


_Loader.yaml_implicit_resolvers = {
    k: [(tag, rx) for tag, rx in v if tag != "tag:yaml.org,2002:bool"]
    for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()
}
_Loader.add_implicit_resolver(
    "tag:yaml.org,2002:bool", re.compile(r"^(?:true|True|TRUE|false|False|FALSE)$"), list("tTfF")
)


def load_yaml(text: str) -> object:
    return yaml.load(text, Loader=_Loader)  # noqa: S506 - SafeLoader subclass


class _M(BaseModel):
    model_config = ConfigDict(extra="forbid", coerce_numbers_to_str=True)


class MoreOrg(_M):
    """D367: a further organization of a joint-printed block with its own printed unit / city / country (None =
    the block's)."""

    org: str
    unit: str = ""
    locality: str | None = None
    country: str | None = None


class AffIn(_M):
    marker: str = ""
    org: str
    org_from_prefix: bool = False  # D283: org printed once before several marked blocks ("Org: 1 City, 2 City")
    more_orgs: list[str | MoreOrg] = []  # joint-printed block: further orgs, one row each (structured: D367)
    unit: str = ""
    locality: str = ""  # city only (D244)
    country: str = ""
    basis: Literal["printed", "single", "listing_order", "pdf", "layout", "prose", "grouped", "per_author"]
    role: Literal["affiliation", "present_address"] = "affiliation"
    locator: str = "p.~1 header"
    campus: str = ""  # D301: printed place that with the org names a distinct campus / institution ("..., Shenzhen")
    continued: str = ""  # D360 (prose): first printed word(s) of the statement's continuation in another column
    marker_trailing: bool = False  # D286e: block printed as "Org, City, Country (1)", marker after the block
    clause: bool = False  # D366 (prose): an "and (also) with" clause of the previous block's statement
    skip_prefix: str = ""  # D366 (prose): printed address-like span between the verb and the first field; not stored
    skip_between: str = ""  # D380 building / site name between unit and org (D410 "<postal box>"); never stored

    @property
    def mo(self) -> list[MoreOrg]:
        return [MoreOrg(org=x) if isinstance(x, str) else x for x in self.more_orgs]


class DroppedIn(_M):
    """D286d: a printed marker after the author's name that is not an affiliation (with the reason)."""

    marker: str
    reason: str


class AuthorIn(_M):
    name: str
    markers: list[str] = []
    dropped_markers: list[DroppedIn] = []
    slot: int | None = None
    unreadable: bool = False
    note: str = ""


class PaperIn(_M):
    source_id: str
    status: Literal["ok", "partial", "unreadable"]
    affiliations: list[AffIn] = []
    authors: list[AuthorIn] = []
    author_list_differs: bool = False
    slots_from_header: bool = False  # D352 (lit): no ordered author list; slots = header order (flagged)
    note: str = ""


# ---------------------------------------------------------------- inputs


def code_key(code: str) -> tuple[int, int, str, int]:
    m = CODE_RE.match(code)
    if not m:
        return (9, 0, code, 0)
    return (DAY[m.group(1)], int(m.group(2)), m.group(3), int(m.group(4)))


def text_files() -> dict[str, Path]:
    tdir = input_path("ofc_text_dir")
    return {p.name.split("-", 1)[0]: p for p in sorted(tdir.glob("*.md"))}


def pdf_files() -> dict[str, Path]:
    pdir = input_path("ofc_metadata").parent / "ofc_browser" / "pdfs"
    return {p.name.split("-", 1)[0]: p for p in sorted(pdir.glob("*.pdf"))} if pdir.is_dir() else {}


def header_text(path: Path) -> str | None:
    """Text before the abstract (title, author line, affiliation blocks, contact line); None when absent."""
    t = path.read_text(encoding="utf-8", errors="replace")
    m = ABSTRACT_RE.search(t)
    return t[: m.start()] if m else None


# D282: extraction artefacts that ascii_fold drops or splits: dotless / dotted i, spacing accents printed before or
# after the letter ("Lu\u00b4\u0131s" for "Lu\u00eds").
FOLD_FIX = str.maketrans(
    {
        "\u0131": "i",
        "\u0153": "oe",
        "\u0152": "OE",
        "\u0130": "I",
        "\u0237": "j",
        **{c: "" for c in "\u00b4\u02dc\u02c6\u00a8\u00b8\u02d8\u02c7\u02d9\u02da\u02dd\u02db`"},
    }
)


def fold_text(s: str) -> str:
    return ascii_fold(s.translate(FOLD_FIX))


def alnum(s: str) -> str:
    """D176 (b) comparison form: markup-free, accents folded, lower case, letters and digits only."""
    s = re.sub(r"</?(sup|sub|a|span|b|i|em|strong)[^>]*>", " ", s, flags=re.I)
    return re.sub(r"[^a-z0-9]", "", fold_text(s).lower())


def mask(s: str) -> str:
    s = re.sub(r"\S*[@＠]\S*", "[contact removed]", s)
    return EMAIL_RE.sub("[contact removed]", s)


def render_csv(columns: list[str], rows: list[dict[str, object]]) -> str:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=columns, lineterminator="\n")
    w.writeheader()
    for r in rows:
        w.writerow({c: _cell(r.get(c)) for c in columns})
    return buf.getvalue()


def write_atomic(path: Path, text: str) -> None:
    """Write through a temporary file in the same directory and rename (D248: parallel batch checks)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def eo_duplicates() -> set[str]:
    return {
        r["native_id"]
        for r in read_csv(REGISTRY / "sources.csv")
        if r["corpus"] == "ofc2026" and r["same_as"].startswith("eo:")
    }


def batch_dirs(spec: Spec | None = None) -> list[Path]:
    base = (spec or OFC).base()
    return sorted(p for p in base.iterdir() if p.is_dir() and (p / "papers.csv").exists()) if base.is_dir() else []


# ---------------------------------------------------------------- corpora (D350: one tool, OFC default)


@dataclass(frozen=True)
class Spec:
    corpus: str  # source corpus and org-alias scope
    staging: str  # directory under data/_staging/people/ and prefix of the local lists
    locator_re: re.Pattern[str]

    def base(self) -> Path:
        return BASE if self.corpus == "ofc2026" else LIT_BASE  # module globals (tests monkeypatch them)


OFC = Spec("ofc2026", "ofc_headers", LOCATOR_RE)
LIT = Spec("lit", "lit_headers", re.compile(r"^p\.[0-9]+( [a-z]+)?$"))  # D353: exact page of text.md
LIT_BASE = STAGING / "people" / "lit_headers"
REFS = ROOT / "references"
PAGE_RE = re.compile(r"<!-- page (\d+) -->")


@dataclass
class LitPaper:
    code: str
    authors: list[ofc.OfcAuthor]  # ordered author list (merged.jsonl); empty when the paper has none (D352)


def lit_papers() -> dict[str, LitPaper]:
    """`lit` sources with their ordered author lists (cache_list uid -> merged.jsonl `authors`)."""
    import json

    codes = [r["native_id"] for r in read_csv(REGISTRY / "sources.csv") if r["corpus"] == "lit"]
    uid = {r["paper_id"]: r["uid"] for r in read_csv(STAGING / "literature" / "cache_list.csv")}
    want = {uid[c]: c for c in codes if c in uid}
    names: dict[str, list[str]] = {}
    # merged.jsonl first; cache/literature/curator_adds.jsonl (same `authors` field) for curator-added papers that
    # are not in it (D362)
    for src in ("merged.jsonl", "curator_adds.jsonl"):
        path = ROOT / "cache" / "literature" / src
        if not path.exists():
            continue
        with path.open(encoding="utf-8") as f:
            for line in f:
                if '"uid"' not in line:
                    continue
                r = json.loads(line)
                c = want.get(r.get("uid", ""))
                if c and c not in names and r.get("authors"):
                    names[c] = [str(x) for x in r["authors"]]
    return {
        c: LitPaper(c, [ofc.OfcAuthor(index=i, name=n, affiliation="") for i, n in enumerate(names.get(c, []), 1)])
        for c in codes
    }


def lit_pages(code: str) -> dict[int, str]:
    path = REFS / code / "text.md"
    if not path.exists():
        return {}
    parts = PAGE_RE.split(path.read_text(encoding="utf-8", errors="replace"))
    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts) - 1, 2)}


def lit_text(code: str, pages: set[int], sep: bool = False) -> str | None:
    """D353: the header page plus the pages named in block locators, in page order (`sep`: page separators for
    `show`, D366)."""
    pg = lit_pages(code)
    if not pg:
        return None
    if sep:
        return "\n".join(f"----- text.md page {k} -----\n{pg[k]}" for k in sorted(pages) if k in pg)
    return "\n".join(pg[k] for k in sorted(pages) if k in pg)


def lit_search_pages(locators: list[str]) -> set[int]:
    """D366: the author line is searched from the first page a locator names as `header` (cover pages are skipped),
    else page 1; plus every page named in a locator."""
    named = {int(m.group(1)) for x in locators if (m := re.match(r"p\.([0-9]+)", x))}
    header = {int(m.group(1)) for x in locators if (m := re.match(r"p\.([0-9]+) header$", x))}
    base = min(header) if header else 1
    return {base} | {k for k in named if k >= base}


def lit_pdf_text(code: str, pages: set[int]) -> str | None:
    path = REFS / code / "source.pdf"
    if not path.exists():
        return None
    return pdf_pages(path, sorted(pages))


def pdf_pages(path: Path, pages: list[int]) -> str:
    """Text of the given 1-based pages, superscript spans marked ^{...}; no cut at the abstract (D353)."""
    import pymupdf  # optional dependency (extra 'fetch')

    parts: list[str] = []
    with pymupdf.open(path) as doc:  # type: ignore[no-untyped-call]
        for k in pages:
            if not 1 <= k <= len(doc):
                continue
            for block in doc[k - 1].get_text("dict")["blocks"]:
                for line in block.get("lines", []):
                    s = ""
                    for span in line["spans"]:
                        t = span["text"]
                        s += f"^{{{t.strip()}}}" if span["flags"] & 1 and t.strip() else t
                    parts.append(s)
                parts.append("")
    return "\n".join(parts)


def lit_duplicates() -> set[str]:
    return {r["native_id"] for r in read_csv(REGISTRY / "sources.csv") if r["corpus"] == "lit" and r["same_as"]}


def cmd_lit_pilot(codes: list[str]) -> int:
    out = LIT_BASE / PILOT / "papers.csv"
    if out.exists():
        print(f"{out} exists; not overwritten", file=sys.stderr)
        return 1
    meta = lit_papers()
    rows = [
        {
            "source_id": f"lit:{c}",
            "code": c,
            "n_authors_meta": len(meta[c].authors),
            "local_pdf": (REFS / c / "source.pdf").exists(),
        }
        for c in codes
    ]
    write_csv(out, PAPER_COLS, rows)
    print(f"wrote {out} ({len(rows)} papers)")
    return 0


def cmd_lit_queue(size: int, dry_run: bool) -> int:
    """Incremental (D351): papers already in a batch stay there; new `lit` sources go to new batches."""
    with RunLog(f"lit_headers_queue_{os.getpid()}", dry_run) as log:
        meta = lit_papers()
        dup = lit_duplicates()
        existing = batch_dirs(LIT)
        taken = {r["code"] for b in existing for r in read_csv(b / "papers.csv")}
        skipped: list[dict[str, str]] = []
        todo: list[str] = []
        for code in sorted(meta):
            if code in taken:
                continue
            reason = "no_text" if not lit_pages(code) else ("duplicate_source" if code in dup else "")
            if reason:
                skipped.append({"source_id": f"lit:{code}", "code": code, "reason": reason})
            else:
                todo.append(code)
        n0 = sum(1 for b in existing if b.name.startswith("lit_h"))
        batches = [todo[i : i + size] for i in range(0, len(todo), size)]
        log.info(f"existing batches {len(existing)} ({len(taken)} papers); to queue {len(todo)} in {len(batches)}")
        log.info(f"skipped {dict(Counter(x['reason'] for x in skipped))}")
        if dry_run:
            return 0
        for i, codes in enumerate(batches, start=n0 + 1):
            d = LIT_BASE / f"lit_h{i:02d}"
            if d.exists():
                raise SystemExit(f"{d} exists; refusing to overwrite")
            rows = [
                {
                    "source_id": f"lit:{c}",
                    "code": c,
                    "n_authors_meta": len(meta[c].authors),
                    "local_pdf": (REFS / c / "source.pdf").exists(),
                }
                for c in codes
            ]
            write_csv(d / "papers.csv", PAPER_COLS, rows)
            log.event("batch", batch=d.name, papers=len(rows), authors=sum(len(meta[c].authors) for c in codes))
        if skipped or not (LIT_BASE / "skipped.csv").exists():
            write_csv(LIT_BASE / "skipped.csv", ["source_id", "code", "reason"], skipped)
        log.info(f"wrote {len(batches)} batches")
    return 0


def cmd_lit_show(batch: str, codes: list[str], pdf: bool, pages: list[int]) -> int:
    papers = read_csv(LIT_BASE / batch / "papers.csv")
    meta = lit_papers()
    for r in papers:
        c = r["code"]
        if codes and c not in codes:
            continue
        want = set(pages) | {1}
        print(f"===== {r['source_id']}  author list {len(meta[c].authors)}  pages {sorted(want)}")
        print(mask(lit_text(c, want, sep=True) or "[no text]").strip())
        if pdf:
            print(f"----- local PDF, pages {sorted(want)} (superscripts as ^{{...}})")
            print(mask(lit_pdf_text(c, want) or "[no pdf]").strip())
        print("----- author list slots (index | name)")
        for a in meta[c].authors:
            print(f"  {a.index} | {a.name}")
        if not meta[c].authors:
            print("  [no author list: slots_from_header (D352)]")
        print()
    return 0


# ---------------------------------------------------------------- pilot / queue


def cmd_pilot(codes: list[str]) -> int:
    out = BASE / PILOT / "papers.csv"
    if out.exists():
        print(f"{out} exists; not overwritten", file=sys.stderr)
        return 1
    meta = {p.code: p for p in ofc.presentations()}
    pdfs = pdf_files()
    rows = [
        {"source_id": f"ofc2026:{c}", "code": c, "n_authors_meta": len(meta[c].authors), "local_pdf": c in pdfs}
        for c in codes
    ]
    write_csv(out, PAPER_COLS, rows)
    print(f"wrote {out} ({len(rows)} papers)")
    return 0


def cmd_queue(size: int, dry_run: bool) -> int:
    with RunLog("ofc_headers_queue", dry_run) as log:
        meta = {p.code: p for p in ofc.presentations()}
        texts = text_files()
        pdfs = pdf_files()
        eo = eo_duplicates()
        taken: set[str] = set()
        existing = batch_dirs()
        for b in existing:
            taken |= {r["code"] for r in read_csv(b / "papers.csv")}
        skipped: list[dict[str, str]] = []
        todo: list[str] = []
        for code in sorted(meta, key=code_key):
            p = meta[code]
            if code in taken:
                continue
            reason = ""
            if code not in texts:
                reason = "no_text"
            elif code in eo:
                reason = "eo_duplicate"
            elif not p.authors:
                reason = "no_metadata_authors"
            elif header_text(texts[code]) is None:
                reason = "no_header"
            if reason:
                skipped.append({"source_id": f"ofc2026:{code}", "code": code, "reason": reason})
            else:
                todo.append(code)
        n0 = sum(1 for b in existing if b.name.startswith("ofc_h"))
        batches = [todo[i : i + size] for i in range(0, len(todo), size)]
        log.info(f"existing batches {len(existing)} ({len(taken)} papers); to queue {len(todo)} in {len(batches)}")
        log.info(f"skipped {dict(Counter(s['reason'] for s in skipped))}")
        if dry_run:
            return 0
        for i, codes in enumerate(batches, start=n0 + 1):
            d = BASE / f"ofc_h{i:02d}"
            if d.exists():
                raise SystemExit(f"{d} exists; refusing to overwrite")
            rows = [
                {
                    "source_id": f"ofc2026:{c}",
                    "code": c,
                    "n_authors_meta": len(meta[c].authors),
                    "local_pdf": c in pdfs,
                }
                for c in codes
            ]
            write_csv(d / "papers.csv", PAPER_COLS, rows)
            log.event("batch", batch=d.name, papers=len(rows), authors=sum(len(meta[c].authors) for c in codes))
        write_csv(BASE / "skipped.csv", ["source_id", "code", "reason"], skipped)
        log.info(f"wrote {len(batches)} batches and skipped.csv")
    return 0


# ---------------------------------------------------------------- show


def pdf_header(path: Path) -> str:
    """First-page text before the abstract, superscript spans marked ^{...} (marker recovery, D173 basis pdf)."""
    import pymupdf  # optional dependency (extra 'fetch')

    with pymupdf.open(path) as doc:  # type: ignore[no-untyped-call]
        page = doc[0]
        parts: list[str] = []
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                s = ""
                for span in line["spans"]:
                    t = span["text"]
                    s += f"^{{{t.strip()}}}" if span["flags"] & 1 and t.strip() else t
                parts.append(s)
            parts.append("")
    text = "\n".join(parts)
    m = ABSTRACT_RE.search(text)
    return text[: m.start()] if m else text[:3000]


def cmd_show(batch: str, codes: list[str], pdf: bool) -> int:
    papers = read_csv(BASE / batch / "papers.csv")
    meta = {p.code: p for p in ofc.presentations()}
    texts = text_files()
    pdfs = pdf_files()
    for r in papers:
        c = r["code"]
        if codes and c not in codes:
            continue
        h = header_text(texts[c])
        print(f"===== {r['source_id']}  metadata authors {len(meta[c].authors)}  local pdf {c in pdfs}")
        print(mask(h if h is not None else "[no header before an abstract]").strip())
        if pdf and c in pdfs:
            print("----- local PDF, page 1 (superscripts as ^{...})")
            print(mask(pdf_header(pdfs[c])).strip())
        print("----- metadata slots (index | name | affiliation)")
        for a in meta[c].authors:
            print(f"  {a.index} | {a.name} | {a.affiliation}")
        print()
    return 0


# ---------------------------------------------------------------- check


def _toks(name: str) -> list[str]:
    return fold(name.translate(FOLD_FIX)).split()  # D362: also oe ligature, dotless i


def _exact(h: str, m: str) -> bool:
    a, b = _toks(h), _toks(m)
    return len(a) >= 2 and (a == b or sorted(a) == sorted(b) or "".join(a) == "".join(b))


def compatible(h: str, m: str) -> bool:
    """Within one paper: header name vs metadata name (D174 as tightened by D247). Both sides need >= 2 tokens. Two
    full given names must be equal (joined, or the first one with a shared family token: dropped middle / second
    family names); an initial must agree with the other side's first given name; family name printed first only
    with an initial ("F. Masahisa" ~ "Masahisa Fujino", fictitious-style)."""
    a, b = _toks(h), _toks(m)
    if len(a) < 2 or len(b) < 2:
        return False
    if _exact(h, m):
        return True
    fam_ok = a[-1] == b[-1] or bool({t for t in a[1:] if len(t) > 1} & {t for t in b[1:] if len(t) > 1})
    full_a, full_b = len(a[0]) > 1, len(b[0]) > 1
    if full_a and full_b:
        return ("".join(a[:-1]) == "".join(b[:-1]) and a[-1] == b[-1]) or (a[0] == b[0] and fam_ok)
    if a[0][0] == b[0][0] and fam_ok:
        return True
    if not full_a and a[-1] == b[0] and a[0] == b[-1][0]:
        return True
    return not full_b and b[-1] == a[0] and b[0] == a[-1][0]


class Check:
    def __init__(self, log: RunLog) -> None:
        self.log = log
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def err(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)


def scan_text(name: str, text: str, address: bool, ck: Check) -> None:
    for i, line in enumerate(text.splitlines(), 1):
        for label, rx in CONTACT_RES:
            if rx.search(line):
                ck.err(f"{name}:{i}: {label} (D176 a)")
        if address:
            bare = ISO_DATE_RE.sub(" ", line)
            for label, rx in ADDRESS_RES:
                if rx.search(bare):
                    ck.err(f"{name}:{i}: {label} (D244: no street address or postal code)")


def scan_contacts(d: Path, ck: Check) -> None:
    """Every non-derived file of the batch directory (derived files are scanned in memory before they are written)."""
    for f in sorted(d.iterdir()):
        if f.is_file() and f.name not in DERIVED:
            scan_text(f.name, f.read_text(encoding="utf-8", errors="replace"), f.suffix in (".yaml", ".csv"), ck)


def map_org(m: Matcher, a: AffIn, corpus: str = "ofc2026") -> tuple[list[str], str]:
    """D177 (order amended by D249): exact matcher rules on deterministic variants of the printed org: as printed,
    parenthesized part removed, unit + org; last, a parenthesized acronym alone, through ofc2026-scoped aliases only.
    No fuzzy matching."""
    places = set(_words(f"{a.locality} {a.campus}").split())
    parens = re.findall(r"\(([^)]*)\)", a.org)
    # D301: a parenthesized place ("(Guangzhou)", "(Shenzhen)") names a campus; it is never dropped
    keep = any(set(_words(x).split()) & places for x in parens)
    bare = "" if keep else re.sub(r"\s*\([^)]*\)", "", a.org).strip()
    variants = [(a.org, ""), (bare, "no_parenthetical")]
    if re.match(r"(?i)the\s+", a.org):
        variants.append((re.sub(r"(?i)^the\s+", "", a.org), "no_article"))  # D288
    if a.unit:
        variants.append((f"{a.unit}, {a.org}", "unit_org"))
    for v, tag in variants:
        if not v:
            continue
        ids, basis = m.match(v, corpus)
        if ids:
            return ids, f"{basis}:{tag}" if tag else basis
    for acro in re.findall(r"\(([A-Z][A-Za-z*&+-]{1,11})\)", a.org):
        scoped = m.by_scoped_alias.get((norm_key(acro), corpus))
        if scoped:
            return sorted(scoped), "alias:acronym_scoped"
    return [], "unmapped"


# ---------------------------------------------------------------- provenance (D246)

SYMBOLS = [
    (re.compile(r"\\ddagger|\u2021"), " ddagger "),
    (re.compile(r"\\dagger|\u2020"), " dagger "),
    (re.compile("\u00a7"), " section "),
    (re.compile("\u00b6"), " pilcrow "),
]
SYM_OPT = "(?:star|dagger|ddagger|section|pilcrow)*"
CUES = ("nowwith", "nowat", "nowin", "presentaddress", "currentlywith", "currentlyat", "presentlywith", "presentlyat")
CUE_OPT = "(?:" + "|".join(CUES) + ")?"
CUE_WORDS = re.compile(
    r" (?:now with|now at|now in|present address|currently with|currently at|presently with|presently at) "
)
NON_AFF_RE = re.compile(r"\b(?:no longer|deceased|passed away|visiting|on leave|retired)\b", re.I)
TAG_RE = re.compile(r"</?(?:sup|sub|a|span|b|i|em|strong|br|u)\b[^>]*>", re.I)
WINDOW_TAIL = 600  # normalized characters after the last block start


MEMBERSHIP_RE = re.compile(  # D355: "Member, IEEE", "Senior Member, IEEE, Fellow, OSA" in author lines
    r",?\s*(?:(?:Graduate\s+)?Student\s+|Senior\s+|Life\s+|Associate\s+)?(?:Member|Fellow)\s*,?\s*"
    r"(?:IEEE|OSA|Optica|SPIE|IET|IEICE|JSAP|APS)"
    r"(?:\s*,\s*(?:(?:Graduate\s+)?(?:Student\s+|Senior\s+|Life\s+)?(?:Member|Fellow)\s*,?\s*)?"
    r"(?:IEEE|OSA|Optica|SPIE|IET|IEICE|JSAP|APS))*"
)


def _prep(t: str, pdf: bool) -> str:
    t = MEMBERSHIP_RE.sub(" ", t)
    t = re.sub(r"\[([^\]]*)\]\(mailto:[^)]*\)", " ", t)
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", t)  # images
    t = re.sub(r"\[([^\]]*)\]\((?:https?:|www\.)[^)]*\)", r" \1 ", t)  # D286b: link text kept, target dropped
    t = re.sub(r"(?:https?://|www\.)\S+", " ", t)
    # first: an address ends at whitespace or a bracket / separator (EMAIL_RE runs over ". \nName"); the closing
    # ")" of "(email: ...)" stays, it is a statement boundary (D366)
    t = re.sub(r"[\w.+-]*[@\uff20][\w.-]*", " ", t)
    t = EMAIL_RE.sub(" ", t)
    t = TAG_RE.sub(" ", t)
    t = t.replace("*", " star ") if pdf else t.replace("\\*", " star ").replace("*", " ")
    for rx, w in SYMBOLS:
        t = rx.sub(w, t)
    return t


def _norm_map(t: str) -> tuple[str, list[int]]:
    out: list[str] = []
    idx: list[int] = []
    for i, ch in enumerate(t):
        for c in fold_text(ch).lower():
            if c.isascii() and c.isalnum():
                out.append(c)
                idx.append(i)
    return "".join(out), idx


def mnorm(marker: str) -> str:
    return _norm_map(_prep(marker, True))[0]


def _words(s: str) -> str:
    s = re.sub(r"(?<=\d)(?=[A-Za-z])|(?<=[A-Za-z])(?=\d)", " ", fold_text(s))  # "3Now with" -> "3 Now with"
    s = re.sub(r"\b([a-z])(?=[A-Z][a-z])", r"\1 ", s)  # D366: letter marker glued to a cue, "aPresent address"
    return " " + " ".join(re.sub(r"[^a-z0-9]+", " ", s.lower()).split()) + " "


def _country_hit(code: str, words: str) -> bool:
    return any(f" {a} " in words for a in COUNTRIES.get(code, ()))


TOK_RE = re.compile(r"ddagger|dagger|section|pilcrow|star|\d|[a-z]")
SYM_TOKENS = {"ddagger", "dagger", "section", "pilcrow", "star"}


def _starts_word(t: str, idx: list[int], i: int) -> bool:
    j = idx[i] - 1
    return j < 0 or not t[j].isalpha()


def _ends_word(t: str, idx: list[int], i_end: int) -> bool:
    j = idx[i_end - 1] + 1
    return j >= len(t) or not t[j].isalpha()


def _find_word(n: str, t: str, idx: list[int], needle: str, pos: int) -> list[int]:
    """Start positions (normalized) of `needle` at or after pos that start and end on word boundaries (D286c)."""
    out: list[int] = []
    if not needle:
        return out
    i = n.find(needle, max(pos, 0))
    while i >= 0:
        if _starts_word(t, idx, i) and _ends_word(t, idx, i + len(needle)):
            out.append(i)
        i = n.find(needle, i + 1)
    return out


def _locate_block(b: AffIn, n: str, t: str, idx: list[int], pos: int, need: bool) -> tuple[int | None, int]:
    """Start of block b at or after pos (D246 / D286c): unit first (the org may be printed directly before it), else
    the org (or the city for prefix blocks); `need` = the marker (and an optional cue) must precede the start.
    Returns (start, end of the last located field)."""
    first = b.unit or (b.locality if b.org_from_prefix else b.org)
    fn = alnum(first)
    for fs in _find_word(n, t, idx, fn, pos):
        cs = fs
        if b.unit and b.org and not b.org_from_prefix:
            hit = re.search(re.escape(alnum(b.org)) + "[a-z]{0,10}$", n[max(0, fs - len(alnum(b.org)) - 10) : fs])
            if hit:
                cs = max(0, fs - len(alnum(b.org)) - 10) + hit.start()
                if cs < pos:
                    cs = fs
        if need:
            pre = re.search(re.escape(mnorm(b.marker)) + CUE_OPT + "$", n[max(0, cs - 40) : cs])
            if not pre:
                continue
            cs = max(0, cs - 40) + pre.start()
        else:
            cue = next((c for c in CUES if n.startswith(c, max(0, cs - len(c))) and cs - len(c) >= pos), "")
            cs -= len(cue)
        last = fs + len(fn)
        for v in [b.org if not b.org_from_prefix else "", b.unit, b.locality] + [
            y for x in b.mo for y in (x.org, x.unit, x.locality or "")
        ]:
            hits = _find_word(n, t, idx, alnum(v), cs) if v else []
            if hits:
                last = max(last, hits[0] + len(alnum(v)))
        return cs, last
    return None, pos


def _author_marks(
    au: AuthorIn, seg: str, block_syms: set[str], exact: bool, optional: frozenset[str] = frozenset()
) -> bool:
    """D286d: the printed marker run after the name equals the recorded markers plus `dropped_markers`; symbols
    that no block uses (corresponding author, equal contribution) are ignored. `exact=False` (last author, or the
    next name not located): the recorded markers must start the run."""

    def toks(x: str) -> list[str]:
        return [k for k in TOK_RE.findall(x) if not (k in SYM_TOKENS and k not in block_syms)]

    rec = [k for mk in au.markers for k in toks(mnorm(mk))]
    if not exact:
        return toks(seg)[: len(rec)] == rec
    seg = re.sub(r"and$", "", seg)
    printed = toks(seg)
    drop = [k for d in au.dropped_markers for k in toks(mnorm(d.marker))]
    for k in optional:  # a "1" printed on the authors of a single unmarked block (contract, D285)
        for _ in range(printed.count(k) - (rec + drop).count(k)):
            printed.remove(k)
    if Counter(printed) != Counter(rec + drop):
        return False
    it = iter(printed)
    return all(k in it for k in rec)  # recorded markers in printed order


def analyse(p: PaperIn, text: str, src: str, coverage: bool = False) -> list[str]:
    """One source text (md extraction or local PDF page 1), D246 as amended by D286: authors located in order, each
    followed by exactly its printed markers; blocks located after the author line in printed order (unit first,
    whole words, each after the previous block's last field; marker + cue before the first field for printed
    blocks, after the block for trailing markers); fields inside the block window; unit and org one printed
    segment; present-address cue iff role present_address; country printed in the window. Returns errors."""
    errs: list[str] = []
    t = _prep(text, src == "pdf")
    n, idx = _norm_map(t)
    block_syms = {k for b in p.affiliations for k in TOK_RE.findall(mnorm(b.marker)) if k in SYM_TOKENS}
    regular = [b for b in p.affiliations if b.role == "affiliation"]
    single_one = frozenset({"1"}) if len(regular) == 1 and regular[0].basis == "single" else frozenset()
    prose_marks = {b.marker for b in p.affiliations if b.basis in ("prose", "grouped", "per_author")}  # not printed
    located: list[tuple[AuthorIn, int, int]] = []
    cur = 0
    for au in p.authors:
        hits = _find_word(n, t, idx, alnum(au.name), cur)
        if not hits:
            only_prose = bool(au.markers) and set(au.markers) <= prose_marks  # D354: checked in the statement
            if not au.unreadable and not only_prose:  # D284: an unreadable author's name is not checked
                errs.append(f"{src}: author {au.name!r} not printed after the previous author (D246)")
            continue
        located.append((au, hits[0], hits[0] + len(alnum(au.name))))
        cur = hits[0] + len(alnum(au.name))
    end = located[-1][2] if located else 0
    for k, (au0, _s, e) in enumerate(located):
        if au0.unreadable:
            continue
        if au0.markers and set(au0.markers) <= prose_marks:
            continue  # D354: prose markers are not printed after the name
        au = au0.model_copy(update={"markers": [mk for mk in au0.markers if mk not in prose_marks]})
        nxt = located[k + 1][1] if k + 1 < len(located) else None
        seg = n[e:nxt] if nxt is not None else n[e : e + 12]
        if not _author_marks(au, seg, block_syms, nxt is not None, single_one):
            errs.append(f"{src}: author {au.name!r}: printed markers differ from {au.markers} (+ dropped) (D286d)")
        if nxt is None:  # the last author's markers extend the author line
            rec = "".join(mnorm(mk) for mk in au.markers)
            hit = re.match(SYM_OPT + "".join(re.escape(mnorm(mk)) + SYM_OPT for mk in au.markers), n[e:])
            end = max(end, e + (hit.end() if hit else len(rec)))
    pos = end
    starts: list[tuple[int, int, AffIn]] = []
    for b in p.affiliations:
        if b.basis in ("prose", "grouped", "per_author"):
            continue  # D354 / D368: located by their statement or author position, below
        need = (
            bool(b.marker) and not b.marker_trailing and (b.basis == "printed" or (b.basis == "pdf" and src == "pdf"))
        )
        best, last = _locate_block(b, n, t, idx, pos, need)
        if best is None:
            first = "unit or city" if b.org_from_prefix else "unit or org"
            what = f"marker + first field ({first})" if need else f"first field ({first})"
            errs.append(f"{src}: block {b.marker!r}: {what} not printed after the author line / previous block (D246)")
            continue
        starts.append((best, last, b))
        pos = max(last, best + 1)
    for i, (s, last, b) in enumerate(starts):
        e = starts[i + 1][0] if i + 1 < len(starts) else min(len(n), s + WINDOW_TAIL)
        w = n[s:e]
        ws = _words(t[idx[s] : idx[e - 1] + 1]) if e > s else " "
        tag = f"{src}: block {b.marker!r}"
        if b.org_from_prefix:
            # D283: the org is printed once, directly before the first block of a run of prefixed blocks
            j = i
            while j > 0 and starts[j - 1][2].org_from_prefix and starts[j - 1][2].org == b.org:
                j -= 1
            if not n[: starts[j][0]].endswith(alnum(b.org)):
                errs.append(
                    f"{tag}: org {b.org!r} is not printed as a prefix directly before this run of blocks (D283)"
                )
        if b.marker_trailing:
            tail = n[last:e]
            if b.basis not in ("printed", "pdf") or not re.match(
                "[a-z]{0,40}" + re.escape(mnorm(b.marker)) + "(?![0-9])", tail
            ):
                errs.append(f"{tag}: trailing marker not printed after the block's last field (D286e)")
        _window_checks(b, w, ws, tag, errs)
    _prose_checks(p, n, t, idx, src, errs, coverage)
    _grouped_checks(p, n, t, idx, src, errs, located)
    return errs


def _window_checks(b: AffIn, w: str, ws: str, tag: str, errs: list[str]) -> None:
    """Fields inside the block window (normalized `w`, word view `ws`); unit + org one segment; cue; country."""
    for fld, v in [
        ("org", "" if b.org_from_prefix else b.org),
        ("unit", b.unit),
        ("locality", b.locality),
        ("campus", b.campus),
    ] + [
        (f, v)
        for x in b.mo
        for f, v in (("more_orgs", x.org), ("more_orgs unit", x.unit), ("more_orgs locality", x.locality or ""))
    ]:
        if v and alnum(v) not in w:
            errs.append(f"{tag}: {fld} {v!r} not inside this printed block (D246)")
    for x in b.mo:
        if x.unit:
            u, o = re.escape(alnum(x.unit)), re.escape(alnum(x.org))
            if not (re.search(u + "[a-z]{0,10}" + o, w) or re.search(o + "[a-z]{0,10}" + u, w)):
                errs.append(f"{tag}: more_orgs unit and org are not one contiguous printed segment (D367)")
        if x.country and not _country_hit(x.country, ws):
            errs.append(f"{tag}: more_orgs country {x.country!r} is not printed in this block (D367)")
    postal = b.skip_between == POSTAL_BOX
    if b.skip_between and not postal and alnum(b.skip_between) not in w:
        errs.append(f"{tag}: skip_between {b.skip_between!r} not inside this printed block (D380)")
    if b.unit and b.org and not b.org_from_prefix:
        u, o = re.escape(alnum(b.unit)), re.escape(alnum(b.org))
        k = POSTAL_BOX_RE if postal else re.escape(alnum(b.skip_between)) if b.skip_between else ""
        gap = "[a-z]{0,10}" + (k + "[a-z]{0,10}" if k else "")
        if not (re.search(u + gap + o, w) or re.search(o + gap + u, w)):
            errs.append(f"{tag}: unit and org are not one contiguous printed segment (D246)")
    if bool(CUE_WORDS.search(ws)) != (b.role == "present_address"):
        errs.append(
            f"{tag}: role {b.role} but the block "
            f"{'has' if b.role != 'present_address' else 'lacks'} a present-address cue (D246)"
        )
    if b.country and not _country_hit(b.country, ws):
        errs.append(f"{tag}: country {b.country!r} is not printed in this block (D246)")


# D410: a postal-box code printed between unit and org (e.g. "CP 123/4") is verified by pattern and never stored
POSTAL_BOX = "<postal box>"
POSTAL_BOX_RE = "(?:cp|bp|pobox|postbus|postfach|box)[0-9]+"
VERB_RE = "(?:is|are|was|were)(?:also|now|currently|presently)?with(?:the)?"
CLAUSE_RE = "(?:and(?:is|are|was|were)?(?:also)?|also)with(?:the)?"  # D366: "<names> is with A, and (also) with B" clause of one statement
# D366: a statement subject starts after a real sentence boundary: ")" (contact parentheses), ";", a blank line, a
# number or an upper-case / lower-case word or a country name followed by ". ", or the previous statement's verb.
# A period after a capitalized name ("F. Ferraro. Y. Ban") is not a boundary.
_NOT_BOUNDARY = {"jordan", "chad", "georgia", "guinea", "niger", "mali", "peru", "cuba", "togo", "oman", "wales"}
_COUNTRY_WORDS = sorted(
    {a for v in COUNTRIES.values() for a in v if len(a) > 3 and a not in _NOT_BOUNDARY}, key=len, reverse=True
)
PROSE_CUT_RE = re.compile(
    r"\)|;\s|\n\s*\n|\d\.\s|\b[A-Z]{2,}\.\s|\b[a-z]{2,}\.\s|[\u201d\u2019\"]\.\s|\.[\u201d\u2019\"]\s|"
    r"(?i:\b(?:" + "|".join(re.escape(c).replace(r"\ ", r"\s+") for c in _COUNTRY_WORDS) + r"))\.\s|"
    r"\b(?:is|are|was|were)(?:\s+(?:also|now|currently|presently))?\s+with\b"
)


def _subject(t: str, idx: list[int], start: int) -> tuple[str, list[str]]:
    """Subject of the statement whose verb phrase starts at normalized position `start` and its name candidates
    (split at commas, "and", "&", and a period after a full word: "F. Ferraro. Y. Ban" -> two names)."""
    before = t[max(0, idx[start] - 600) : idx[start]]
    cut = max((m.end() for m in PROSE_CUT_RE.finditer(before)), default=0)
    subject = before[cut:].strip(" .\n")
    parts = re.split(r",|\band\b|&|(?<=[A-Za-z]{2})\.\s", subject)
    names = [c.strip(" .\n").translate(FOLD_FIX) for c in parts if c.strip(" .\n")]
    return subject, names


def _at_line_start(t: str, i: int) -> bool:
    j = i - 1
    while j >= 0 and t[j] in " \t":
        j -= 1
    return j < 0 or t[j] == "\n"


def _first_field_hits(
    b: AffIn, n: str, t: str, idx: list[int], pos: int, bounded: bool = True
) -> list[tuple[int, int]]:
    """(block start candidate, end of the first field): unit first, an org printed directly before the unit starts
    the block (D246 / D286c)."""
    out = []
    fo = alnum(b.org)
    first = alnum(b.unit or b.org)
    occ = _find_word(n, t, idx, first, pos) if bounded else [m.start() for m in re.finditer(re.escape(first), n[pos:])]
    for fs in occ if bounded else [pos + x for x in occ]:
        cs = fs
        if b.unit and b.org:
            lo = max(0, fs - len(fo) - 10)
            hit = re.search(re.escape(fo) + "[a-z]{0,10}$", n[lo:fs])
            if hit:
                cs = lo + hit.start()
        out.append((cs, fs + len(first)))
    return out


def _prose_checks(p: PaperIn, n: str, t: str, idx: list[int], src: str, errs: list[str], coverage: bool) -> None:
    """D354: each prose block is a statement "<names> is / are (also / now) with <block>": located by the verb
    phrase directly before its first field (unit first; an org printed directly before the unit starts the block;
    a verified `skip_prefix` may sit between, D366), in printed order; a `clause` block is an "and (also) with"
    clause of the previous block's statement (same subject, own fields, D366); window up to the next statement or
    clause (<= 300 normalized characters), plus the continuation window when the statement goes on in another
    column (`continued`, D360); the subject must name every author carrying the block's marker and no other author;
    "The authors" = every author; "He / She / They" = the previous statement's subject. With `coverage` (lit, D361,
    D366) every statement or clause of the searched text whose subject names an author must be a recorded block."""
    pos = 0
    prev: list[str] = []
    recorded: list[int] = []
    stmt_names: list[str] = []
    stmt_subject = ""
    stop = re.compile(f"{VERB_RE}|{CLAUSE_RE}")
    for b in [x for x in p.affiliations if x.basis == "prose"]:
        tag = f"{src}: block {b.marker!r}"
        anchor = (CLAUSE_RE if b.clause else VERB_RE) + re.escape(alnum(b.skip_prefix))
        start = None
        first_end = pos
        field_start = pos
        for cs, fe in _first_field_hits(b, n, t, idx, pos, bounded=False):  # the verb / clause anchor bounds it
            v = re.search(anchor + "$", n[max(0, cs - 40 - len(alnum(b.skip_prefix))) : cs])
            if v:
                start = max(0, cs - 40 - len(alnum(b.skip_prefix))) + v.start()
                first_end, field_start = fe, cs
                break
        if start is None and b.continued:  # the first field itself may continue in the other part ("Intel | Corp.")
            for v2 in re.finditer(anchor, n[pos:]):
                vs = pos + v2.start()
                if n.startswith(alnum(b.org)[: max(1, len(alnum(b.org)) - len(alnum(b.continued)))], pos + v2.end()):
                    start, first_end = vs, pos + v2.end()
                    break
        if start is None:
            what = "'and (also) with'" if b.clause else "'<names> is / are with'"
            errs.append(f"{tag}: {what} + first field (unit or org) not printed (D354)")
            continue
        recorded.append(start)
        nxt = stop.search(n, max(field_start, start + 6))  # after this block's own anchor
        e = min(nxt.start() if nxt else len(n), start + 300, len(n))
        if b.continued:  # the printed first part ends with the verb's line
            line_end = t.find("\n", idx[start])
            if line_end >= 0:
                e = min(e, bisect.bisect_left(idx, line_end))
        w, ws = n[start:e], _words(t[idx[start] : idx[e - 1] + 1])
        if b.continued:  # D360: the rest of the statement is printed elsewhere on the page, at a line start
            ca = alnum(b.continued)
            hits = [h for h in _find_word(n, t, idx, ca, e) if _at_line_start(t, idx[h])]
            if not hits:
                errs.append(
                    f"{tag}: continuation {b.continued!r} not printed at a line start after the statement (D360)"
                )
            else:
                cs2 = hits[0]
                n2 = stop.search(n, cs2 + len(ca))
                ce = min(n2.start() if n2 else len(n), cs2 + 300, len(n))
                w += n[cs2:ce]
                ws += _words(t[idx[cs2] : idx[ce - 1] + 1])
        _window_checks(b, w, ws, tag, errs)
        if b.clause:
            if not stmt_subject and not stmt_names:
                errs.append(f"{tag}: clause without a preceding statement block (D366)")
            subject, names = stmt_subject, stmt_names
        else:
            subject, names = _subject(t, idx, start)
            if re.fullmatch(r"(?i)(he|she|they)", subject):
                names = prev
            else:
                prev = names
            stmt_subject, stmt_names = subject, names
        carriers = [au for au in p.authors if b.marker in au.markers and not au.unreadable]
        if re.search(r"(?i)\bauthors\b", subject):
            missing = [au.name for au in p.authors if b.marker not in au.markers and not au.unreadable]
            if missing:
                errs.append(f"{tag}: statement names all authors; {missing} do not carry {b.marker!r} (D354)")
        else:
            for au in carriers:
                if not any(compatible(au.name, c) for c in names):
                    errs.append(f"{tag}: author {au.name!r} is not named in the statement subject (D354)")
            for c in names:
                hits2 = [au for au in p.authors if compatible(au.name, c)]
                if hits2 and not any(b.marker in au.markers for au in hits2):
                    errs.append(f"{tag}: {c!r} is named in the statement but carries no {b.marker!r} (D354)")
        pos = first_end  # the next statement starts after this block's first field
    if not coverage:
        return
    names_prev = False
    last_verb = None
    for v in re.finditer(f"{VERB_RE}|{CLAUSE_RE}", n):
        vs = v.start()
        if not _starts_word(t, idx, vs):
            continue
        if v.group(0).startswith("and"):  # a clause belongs to the statement it follows, in the same sentence
            if last_verb is None or not last_verb[1] or vs - last_verb[0] > 300:
                continue
            if PROSE_CUT_RE.search(t[idx[last_verb[2] - 1] + 1 : idx[vs]]):
                continue  # body text after the statement ended ("... high-volume and with a high yield")
            names_author = True
        else:
            subject, names = _subject(t, idx, vs)
            if re.fullmatch(r"(?i)(he|she|they)", subject):
                names_author = names_prev
            else:
                names_author = bool(re.search(r"(?i)\bauthors\b", subject)) or any(
                    compatible(au.name, c) for au in p.authors for c in names
                )
                names_prev = names_author
            last_verb = (vs, names_author, v.end())
        if names_author and not any(abs(vs - r) <= 3 for r in recorded):
            snippet = " ".join(t[max(0, idx[vs] - 60) : idx[vs]].split()[-6:])
            errs.append(f"{src}: statement '... {snippet} {v.group(0)} ...' names an author but is not recorded (D361)")


def _grouped_checks(
    p: PaperIn, n: str, t: str, idx: list[int], src: str, errs: list[str], located: list[tuple[AuthorIn, int, int]]
) -> None:
    """D368: `grouped` blocks follow their author group (the group's names printed consecutively, then its
    block(s)); `per_author` blocks follow their single author. Verified by position, independent of the author line:
    the block's first field is found after the previous grouped block; every carrier's name is printed between the
    previous grouped block and this one, and no other author's name after the group's first name (a group's further
    block may follow its previous block directly); fields inside the window up to the next author name or block
    (<= 400 normalized characters)."""
    gb = [b for b in p.affiliations if b.basis in ("grouped", "per_author")]
    names = {id(au): alnum(au.name) for au in p.authors if alnum(au.name)}
    pos = 0
    prev_carriers: set[int] = set()
    prev_start = 0
    for b in gb:
        tag = f"{src}: block {b.marker!r}"
        carriers = [au for au in p.authors if b.marker in au.markers and not au.unreadable]
        if not carriers:
            continue
        cid = {id(au) for au in carriers}
        if b.basis == "per_author" and len(carriers) != 1:
            errs.append(f"{tag}: per_author block carried by {len(carriers)} authors (D368)")
        hits = _first_field_hits(b, n, t, idx, pos)
        if not hits:
            errs.append(f"{tag}: first field (unit or org) not printed after the previous block (D368)")
            continue
        start, fe = hits[0]
        if cid == prev_carriers and not any(
            _find_word(n, t, idx, nm, prev_start) and _find_word(n, t, idx, nm, prev_start)[0] < start
            for k, nm in names.items()
        ):
            pass  # a further block of the same group, printed right after the previous one
        else:
            last_hit: dict[int, int] = {}
            for au in carriers:
                occ = [h for h in _find_word(n, t, idx, names.get(id(au), ""), pos) if h < start]
                if not occ:
                    errs.append(f"{tag}: author {au.name!r} is not printed before this block (D368)")
                else:
                    last_hit[id(au)] = occ[-1]
            if last_hit:
                first = min(last_hit.values())
                others = [
                    au.name
                    for au in p.authors
                    if id(au) not in cid
                    and any(first <= h < start for h in _find_word(n, t, idx, names.get(id(au), ""), first))
                ]
                if others:
                    errs.append(f"{tag}: authors {others} are printed between the group and its block (D368)")
        nxt = [h[0] for k, nm in names.items() if (h := _find_word(n, t, idx, nm, fe))]
        e = min(min(nxt) if nxt else len(n), start + 400, len(n))
        _window_checks(b, n[start:e], _words(t[idx[start] : idx[e - 1] + 1]), tag, errs)
        pos, prev_carriers, prev_start = fe, cid, start


def check_provenance(p: PaperIn, tag: str, md: str | None, pdf: str | None, ck: Check, coverage: bool = False) -> None:
    """Pass when the PDF analysis is clean, or the md analysis is clean and no block claims basis pdf."""
    has_pdf_block = any(b.basis == "pdf" for b in p.affiliations)
    md_errs = analyse(p, md, "md", coverage) if md is not None else ["md: no header text"]
    pdf_errs = analyse(p, pdf, "pdf", coverage) if pdf is not None else None
    if pdf_errs == [] or (not md_errs and not has_pdf_block):
        return
    for e in md_errs:
        ck.err(f"{tag}: {e}")
    for e in pdf_errs or (["pdf: blocks with basis pdf need a local PDF"] if has_pdf_block else []):
        ck.err(f"{tag}: {e}")


def strict_compatible(h: str, m: str) -> bool:
    """D369 (lit slot matching): `compatible`, and when one form is abbreviated every initial must be explained by
    the other form: by its given-name syllables, or, for a joined given name, by its letters in order ("S. H. Tao" ~
    "Shaohua Tao", "D. L. Kwong" ~ "DimLee Kwong"; "S. F. Yu" !~ "Siyuan Yu", "M. B. Yu" !~ "Ming Yu")."""
    if not compatible(h, m):
        return False
    from photonics_atlas.people import parse

    a, b = parse(h.translate(FOLD_FIX)), parse(m.translate(FOLD_FIX))
    if a.abbreviated == b.abbreviated:
        return True
    ab, full = (a, b) if a.abbreviated else (b, a)
    if len(ab.inits) <= len(full.inits):
        return True
    # extra initials must be provable inside the joined full given name, in order ("S. H." ~ "Shaohua")
    g = "".join(full.given)
    pos = 0
    for k, ch in enumerate(ab.inits):
        hit = g.find(ch, pos) if k else (0 if g.startswith(ch) else -1)
        if hit < 0:
            return False
        pos = hit + 2
    return True


def match_slots(
    p: PaperIn, pres: ofc.OfcPresentation | LitPaper, tag: str, ck: Check, strict: bool = False
) -> dict[int, int]:
    """D174 / D247: header position -> metadata slot. Exact name first, then compatible; no positional fallback; an
    ambiguous name needs an explicit `slot:`."""
    comp = strict_compatible if strict else compatible
    n_meta = len(pres.authors)
    slot_of: dict[int, int] = {}
    for k, au in enumerate(p.authors, 1):
        if au.slot is not None:
            if au.slot and not 1 <= au.slot <= n_meta:
                ck.err(f"{tag}: author {au.name!r} slot {au.slot} outside 1..{n_meta}")
            elif au.slot:
                if not comp(au.name, pres.authors[au.slot - 1].name):
                    ck.warn(f"{tag}: author {au.name!r} set to slot {au.slot} ({pres.authors[au.slot - 1].name!r})")
                slot_of[k] = au.slot
            continue
        exact = [a.index for a in pres.authors if _exact(au.name, a.name)]
        cands = exact or [a.index for a in pres.authors if comp(au.name, a.name)]
        if len(cands) == 1:
            slot_of[k] = cands[0]
        else:
            ck.err(f"{tag}: author {au.name!r} (pos {k}) matches {len(cands)} metadata slots {cands}; set slot (D247)")
    dup = [s for s, c in Counter(slot_of.values()).items() if c > 1]
    if dup:
        ck.err(f"{tag}: slots {dup} matched twice")
    unmatched = [a for a in pres.authors if a.index not in set(slot_of.values())]
    for au in p.authors:
        if au.slot == 0:
            hits = [a.index for a in unmatched if comp(au.name, a.name)]
            if hits:
                ck.err(f"{tag}: author {au.name!r} has slot 0 but matches unmatched metadata slot(s) {hits} (D302)")
    return slot_of


def check_batch(
    d: Path,
    ck: Check,
    meta: Mapping[str, ofc.OfcPresentation | LitPaper],
    texts: dict[str, Path],
    pdfs: dict[str, Path],
    eo: set[str],
    m: Matcher,
    orgs: dict[str, dict[str, str]],
    xw: dict[tuple[str, str], list[str]],
    write: bool,
    spec: Spec | None = None,
) -> Counter[str]:
    """Validate one batch; derived files are written (atomically, with a stamp of the YAML) only when the batch has
    0 errors (D248)."""
    spec = spec or OFC
    lit = spec.corpus == "lit"
    stats: Counter[str] = Counter()
    n_err0 = len(ck.errors)
    queue = {r["source_id"]: r for r in read_csv(d / "papers.csv")}
    yp = d / "headers.yaml"
    scan_contacts(d, ck)
    if not yp.exists():
        ck.warn(f"{d.name}: no headers.yaml yet")
        return stats
    yaml_bytes = yp.read_bytes()
    raw = load_yaml(yaml_bytes.decode("utf-8")) or []
    if not isinstance(raw, list):
        ck.err(f"{d.name}: headers.yaml must be a list of papers")
        return stats
    papers: list[PaperIn] = []
    for i, r in enumerate(raw):
        if lit and isinstance(r, dict):  # D353: lit locators are exact pages; the OFC default does not apply
            for a in r.get("affiliations") or []:
                if isinstance(a, dict):
                    a.setdefault("locator", "p.1 header")
        try:
            papers.append(PaperIn.model_validate(r))
        except ValidationError as e:
            ck.err(f"{d.name} paper #{i + 1} ({(r or {}).get('source_id', '?')}): {e}")
    seen = Counter(p.source_id for p in papers)
    for sid, c in seen.items():
        if c > 1:
            ck.err(f"{d.name} {sid}: {c} entries")
    for sid in sorted(set(queue) - set(seen)):
        ck.warn(f"{d.name} {sid}: queued, not extracted yet")
    rows: list[dict[str, object]] = []
    cmp_rows: list[dict[str, object]] = []
    unmapped: dict[tuple[str, str, str], list[str]] = defaultdict(list)
    for p in papers:
        sid = p.source_id
        tag = f"{d.name} {sid}"
        code = sid.split(":", 1)[1] if sid.startswith(f"{spec.corpus}:") else sid
        if sid not in queue:
            ck.err(f"{tag}: not in this batch's papers.csv (D176 f)")
            continue
        if code in eo and d.name != PILOT:
            ck.err(f"{tag}: EO duplicate, not queued (D175)")
        stats[f"papers_{p.status}"] += 1
        pres: ofc.OfcPresentation | LitPaper = meta[code]
        if lit and not pres.authors:  # D352: no ordered author list
            if not p.slots_from_header:
                ck.err(f"{tag}: no author list for this paper; set slots_from_header: true (D352)")
            pres = LitPaper(
                code,
                [ofc.OfcAuthor(index=k, name=au.name, affiliation="") for k, au in enumerate(p.authors, 1)],
            )
            stats["papers_slots_from_header"] += 1
        elif p.slots_from_header:
            ck.err(f"{tag}: slots_from_header but the paper has an author list (D352)")
        if p.status == "unreadable":
            if p.affiliations or p.authors:
                ck.err(f"{tag}: unreadable paper must carry no affiliations or authors (D175)")
            if not p.note:
                ck.err(f"{tag}: unreadable needs a note saying what is unreadable")
            for a in pres.authors:
                cmp_rows.append(_cmp(sid, a, "", [], 0, False, "no_header"))
            stats["outcome_no_header"] += len(pres.authors)
            stats["slots"] += len(pres.authors)
            continue
        n_unreadable = sum(au.unreadable for au in p.authors)
        if p.status == "partial" and not n_unreadable:
            ck.err(f"{tag}: status partial needs >= 1 author with unreadable: true (D249)")
        if p.status == "ok" and n_unreadable:
            ck.err(f"{tag}: status ok with unreadable authors; use partial (D249)")
        # field rules, markers
        by_marker: dict[str, AffIn] = {}
        for b in p.affiliations:
            if b.marker in by_marker:
                ck.err(f"{tag}: block marker {b.marker!r} defined twice")
            by_marker[b.marker] = b
            for fld, v in [("org", b.org), ("unit", b.unit), ("locality", b.locality)] + [
                (f, v)
                for x in b.mo
                for f, v in (("more_orgs", x.org), ("more_orgs unit", x.unit), ("more_orgs locality", x.locality or ""))
            ]:
                for label, rx in ADDRESS_RES:
                    if v and rx.search(v):
                        ck.err(f"{tag}: block {b.marker!r} {fld} {v!r}: {label} (D244)")
                if v and NON_AFF_RE.search(v):
                    ck.err(f"{tag}: block {b.marker!r} {fld} {v!r} is a status footnote, not an affiliation (D249)")
            if re.search(r"\d", b.campus) or "," in b.campus:
                ck.err(f"{tag}: block {b.marker!r} campus {b.campus!r} must be the printed place only (D301)")
            if re.search(r"\d", b.locality) or "," in b.locality:
                ck.err(f"{tag}: block {b.marker!r} locality {b.locality!r} must be the city only (D244)")
            if b.basis == "pdf" and code not in pdfs:
                ck.err(f"{tag}: block {b.marker!r} basis pdf without a local PDF")
            if b.basis == "listing_order" and code in pdfs:
                ck.warn(f"{tag}: block {b.marker!r} listing_order although a local PDF exists; prefer pdf")
            if b.basis == "layout" and not p.note:
                ck.err(f"{tag}: basis layout needs a paper note describing the layout (D246)")
            if not b.org.strip():
                ck.err(f"{tag}: block {b.marker!r} has no org")
            if b.country and (not COUNTRY_RE.match(b.country) or b.country not in COUNTRIES):
                ck.err(f"{tag}: block {b.marker!r} country {b.country!r} is not a known ISO alpha-2 code")
            if b.basis == "prose" and not re.fullmatch(r"P[0-9]+", b.marker):
                ck.err(f"{tag}: prose block marker {b.marker!r} must be a synthetic P<n> (never printed, D354)")
            if b.basis in ("grouped", "per_author") and not re.fullmatch(r"G[0-9]+", b.marker):
                ck.err(f"{tag}: {b.basis} block marker {b.marker!r} must be a synthetic G<n> (never printed, D368)")
            if (b.clause or b.skip_prefix) and b.basis != "prose":
                ck.err(f"{tag}: clause / skip_prefix only for prose blocks (D366)")
            for mx in b.mo:
                if mx.country and (not COUNTRY_RE.match(mx.country) or mx.country not in COUNTRIES):
                    ck.err(f"{tag}: more_orgs country {mx.country!r} is not a known ISO alpha-2 code (D367)")
            if not spec.locator_re.match(b.locator):
                ck.err(f"{tag}: block {b.marker!r} locator {b.locator!r} (D176 e)")
        regular = [a for a in p.affiliations if a.role == "affiliation"]
        if any(a.basis == "single" for a in p.affiliations) and (len(regular) != 1 or regular[0].marker):
            ck.err(f"{tag}: basis single needs exactly one regular block without a marker (D173)")
        unmarked = [a for a in regular if not a.marker]
        default = unmarked[0] if len(unmarked) == 1 else None  # D286f: the block of authors without a marker
        if len(unmarked) > 1:
            ck.err(f"{tag}: {len(unmarked)} unmarked regular blocks; at most one (D286f)")
        if default is not None and len(regular) > 1 and default.basis != "layout":
            ck.err(f"{tag}: an unmarked block next to marked blocks needs basis layout and a note (D286f)")
        for b in p.affiliations:
            if b.marker_trailing and (not b.marker or b.basis not in ("printed", "pdf")):
                ck.err(f"{tag}: block {b.marker!r} marker_trailing needs a printed marker (D286e)")
        if any(a.basis == "listing_order" for a in p.affiliations):
            nums = [a.marker for a in regular]
            author_max = max((int(x) for au in p.authors for x in au.markers if x.isdigit()), default=0)
            if nums != [str(i) for i in range(1, len(nums) + 1)] or author_max != len(nums):
                ck.err(f"{tag}: listing_order needs blocks 1..N in order with N = largest author marker (D173)")
        used: set[str] = set()
        for au in p.authors:
            if re.search(r"[\d*†‡§¶#,]", au.name):
                ck.err(f"{tag}: author {au.name!r} carries a marker or punctuation; markers go to 'markers'")
            for mk in au.markers:
                if mk not in by_marker:
                    ck.err(f"{tag}: author {au.name!r} marker {mk!r} has no block (D176 c)")
                used.add(mk)
            if au.unreadable and p.status != "partial":
                ck.err(f"{tag}: author {au.name!r} unreadable needs paper status partial (D175)")
            for dm in au.dropped_markers:
                if dm.marker in by_marker:
                    ck.err(f"{tag}: author {au.name!r} drops marker {dm.marker!r} that is a recorded block (D286d)")
                if not dm.reason.strip():
                    ck.err(f"{tag}: author {au.name!r} dropped marker {dm.marker!r} needs a reason (D286d)")
            regular_marked = [mk for mk in au.markers if mk in by_marker and by_marker[mk].role == "affiliation"]
            if not regular_marked and not au.unreadable and default is None:
                ck.err(f"{tag}: author {au.name!r} has no markers and the paper has no unmarked block")
        if default is not None:
            used.add("")
        for mk in set(by_marker) - used:
            ck.err(f"{tag}: block {mk!r} is used by no author (D176 c)")
        # (b) provenance against the printed text (D246)
        if lit:
            pages = lit_search_pages([b.locator for b in p.affiliations])
            md = lit_text(code, pages)
            pdf = lit_pdf_text(code, pages)
        else:
            md = header_text(texts[code]) if code in texts else None
            pdf = pdf_header(pdfs[code]) if code in pdfs else None
        check_provenance(p, tag, md, pdf, ck, coverage=lit)
        # (d) slot matching (D174 / D247)
        slot_of = match_slots(p, pres, tag, ck, strict=lit)
        seq = [slot_of[k] for k in sorted(slot_of)]
        order_differs = lit and seq != sorted(seq)
        if order_differs:  # D363: slot = author-list position (D62 / D359); header_pos keeps the printed order
            ck.warn(f"{tag}: printed author order differs from the author list (slots by name; header_pos kept)")
            stats["papers_order_differs"] += 1
        n_meta = len(pres.authors)
        missing = sorted(set(range(1, n_meta + 1)) - set(slot_of.values()))
        extra_header = [au.name for au in p.authors if au.slot == 0]
        if (missing or extra_header) and not p.author_list_differs:
            ck.err(
                f"{tag}: metadata slots {missing} unmatched / header-only {extra_header}; author_list_differs (D174)"
            )
        if p.author_list_differs and not p.note:
            ck.err(f"{tag}: author_list_differs needs a note")
        # rows + comparison
        regular_only = default
        by_slot: dict[int, tuple[AuthorIn, int]] = {s: (p.authors[k - 1], k) for k, s in slot_of.items()}
        for a in pres.authors:
            got = by_slot.get(a.index)
            if got is None or got[0].unreadable:
                cmp_rows.append(_cmp(sid, a, got[0].name if got else "", [], 0, False, "no_header"))
                stats["outcome_no_header"] += 1
                continue
            au, k = got
            affs = [by_marker[mk] for mk in au.markers if mk in by_marker]
            if regular_only is not None and not any(
                by_marker[mk].role == "affiliation" for mk in au.markers if mk in by_marker
            ):
                affs = [regular_only, *affs]  # single unmarked block (+ a present-address marker, if any)
            # aff_order: regular blocks first in printed marker order, present-address blocks after them
            ordered = [x for x in affs if x.role == "affiliation"] + [x for x in affs if x.role == "present_address"]
            hdr_ids: set[str] = set()
            pa_ids: set[str] = set()
            n_aff = 0
            pa = False
            unmapped_here = False
            for j, x in enumerate(ordered, 1):
                role = "present_address" if x.role == "present_address" else ("primary" if j == 1 else "additional")
                pa = pa or x.role == "present_address"
                n_aff += x.role == "affiliation"
                grade, note = GRADE_OF_BASIS.get(x.basis, ("A", ""))
                for kk, mo in enumerate([MoreOrg(org=x.org, unit=x.unit), *x.mo], 1):
                    org = mo.org
                    if kk == 1 and x.campus:  # D301: org + campus is the institution; never the parent / homonym
                        org = f"{org}, {x.campus}"
                    loc = x.locality if mo.locality is None or kk == 1 else mo.locality
                    ctry = x.country if mo.country is None or kk == 1 else mo.country
                    xo = x.model_copy(update={"org": org, "unit": mo.unit, "locality": loc, "country": ctry})
                    ids, basis = map_org(m, xo, spec.corpus)
                    rows.append(
                        {
                            "source_id": sid,
                            "author_index": a.index,
                            "header_pos": k,
                            "printed_name": au.name,
                            "aff_order": j,
                            "aff_marker": x.marker,
                            "aff_role": role,
                            "org_k": kk,
                            "org_name": org,
                            "unit": xo.unit,
                            "locality": xo.locality,
                            "country": xo.country,
                            "marker_basis": x.basis,
                            "evidence_grade": grade,  # D240 / D246
                            "grade_note": note,
                            "locator": x.locator,
                            "org_ids": ids,
                            "match_basis": basis,
                        }
                    )
                    stats[f"rows_{role}"] += 1
                    stats[f"rows_basis_{x.basis}"] += 1
                    stats[f"rows_grade_{grade}"] += 1
                    if x.role == "present_address":
                        pa_ids |= set(ids)
                    elif ids:
                        hdr_ids |= set(ids)
                    else:
                        unmapped_here = True
                    if not ids:
                        unmapped[(org, xo.unit, x.country)].append(sid)
            if ordered and ordered[0].role == "present_address":
                ck.warn(f"{tag}: author {au.name!r} has only a present-address block")
            # D356: lit has no per-author metadata org to compare with
            outcome = "recorded" if lit else _outcome(a, hdr_ids, pa_ids, unmapped_here, orgs, xw)
            meta_ids = [] if lit else xw.get(("ofc2026", a.affiliation), [])
            cmp_rows.append(_cmp(sid, a, au.name, sorted(hdr_ids), n_aff, pa, outcome, meta_ids))
            stats[f"outcome_{outcome}"] += 1
            stats["slots_multi_aff"] += n_aff >= 2
            stats["slots_present_address"] += pa
        if lit:
            for r in cmp_rows:
                if r["source_id"] == sid:
                    r["order_differs"] = order_differs
        stats["slots"] += n_meta
    derived = {
        "header_rows.csv": render_csv(ROW_COLS, rows),
        "compare.csv": render_csv(CMP_COLS + (CMP_COLS_LIT_EXTRA if lit else []), cmp_rows),
        "unmapped_orgs.csv": render_csv(
            UNMAPPED_COLS,
            [
                {"org_name": k[0], "unit": k[1], "country": k[2], "n_rows": len(v), "examples": sorted(set(v))[:5]}
                for k, v in sorted(unmapped.items())
            ],
        ),
    }
    for name, text in derived.items():
        scan_text(name, text, True, ck)
    stats["rows"] = len(rows)
    stats["unmapped_org_strings"] = len(unmapped)
    if len(ck.errors) > n_err0:
        if write:
            ck.warn(f"{d.name}: errors, derived files not written (D248)")
        return stats
    if write:
        for name, text in derived.items():
            write_atomic(d / name, text)
        write_atomic(d / STAMP, f"headers.yaml sha256 {hashlib.sha256(yaml_bytes).hexdigest()}\n")
    return stats


def _roots(ids: list[str] | set[str], orgs: dict[str, dict[str, str]]) -> set[str]:
    return {org_root(orgs, o) for o in ids}


def _outcome(
    a: ofc.OfcAuthor,
    hdr_ids: set[str],
    pa_ids: set[str],
    unmapped_here: bool,
    orgs: dict[str, dict[str, str]],
    xw: dict[tuple[str, str], list[str]],
) -> str:
    """D178 classes on registry roots."""
    meta_ids = xw.get(("ofc2026", a.affiliation), [])
    if not meta_ids or not hdr_ids:
        return "unmapped"
    mr, hr = _roots(meta_ids, orgs), _roots(hdr_ids, orgs)
    if mr <= hr:
        return "agree" if mr == hr and not unmapped_here else "extra"
    if pa_ids and mr <= hr | _roots(pa_ids, orgs):
        return "present_address"  # the metadata holds the printed present address
    return "unmapped" if unmapped_here else "conflict"


def _cmp(
    sid: str,
    a: ofc.OfcAuthor,
    header_name: str,
    hdr_ids: list[str],
    n_aff: int,
    pa: bool,
    outcome: str,
    meta_ids: list[str] | None = None,
) -> dict[str, object]:
    return {
        "source_id": sid,
        "author_index": a.index,
        "meta_name": a.name,
        "header_name": header_name,
        "meta_org_ids": meta_ids or [],
        "header_org_ids": hdr_ids,
        "n_aff_rows": n_aff,
        "present_address": pa,
        "outcome": outcome,
    }


def stamp_ok(d: Path) -> bool:
    """D248: derived files belong to the current headers.yaml."""
    st, yp = d / STAMP, d / "headers.yaml"
    if not (st.exists() and yp.exists()):
        return False
    return st.read_text(encoding="utf-8").split()[-1] == hashlib.sha256(yp.read_bytes()).hexdigest()


def write_aggregates(
    log: RunLog,
    meta: Mapping[str, ofc.OfcPresentation | LitPaper],
    orgs: dict[str, dict[str, str]],
    spec: Spec | None = None,
) -> int:
    """Across all batches with current derived files (stamp matches the YAML): org alias requests (D242, committed
    staging), conflict review list (D241) and header-only authors (D243), both local only (data/_local/, git-ignored).
    Returns the number of extracted batches skipped as stale."""
    by_name: dict[str, str] = {}
    for o in orgs.values():
        by_name.setdefault(ascii_fold(o["name"]).casefold().strip(), o["org_id"])
    req: dict[tuple[str, str, str], list[tuple[str, str]]] = defaultdict(list)
    conflicts: list[dict[str, object]] = []
    extra: list[dict[str, object]] = []
    stale = 0
    spec = spec or OFC
    for d in batch_dirs(spec):
        if not (d / "headers.yaml").exists():
            continue
        if not stamp_ok(d):
            log.info(f"ERROR {d.name}: derived files missing or older than headers.yaml; run check {d.name}")
            stale += 1
            continue
        for r in read_csv(d / "header_rows.csv"):
            if not r["org_ids"]:
                req[(r["org_name"], r["locality"], r["country"])].append(
                    (f"{r['source_id']} {r['locator']}", r["unit"])
                )
        for r in read_csv(d / "compare.csv"):
            if r["outcome"] != "conflict":
                continue
            code = r["source_id"].split(":", 1)[1]
            aff = next(a.affiliation for a in meta[code].authors if a.index == int(r["author_index"]))
            conflicts.append({**{k: r[k] for k in CONFLICT_COLS if k in r}, "meta_affiliation": aff})
        for raw in load_yaml((d / "headers.yaml").read_text(encoding="utf-8")) or []:  # type: ignore[attr-defined]
            for k, au in enumerate(raw.get("authors") or [], 1):
                if au.get("slot") == 0:
                    extra.append(
                        {
                            "source_id": raw["source_id"],
                            "header_pos": k,
                            "printed_name": au["name"],
                            "markers": [str(x) for x in au.get("markers") or []],
                            "note": au.get("note", ""),
                        }
                    )
    rows: list[dict[str, object]] = []
    for (name, locality, country), hits in sorted(req.items()):
        key = ascii_fold(name).casefold().strip()
        bare = ascii_fold(re.sub(r"\s*\([^)]*\)", "", name)).casefold().strip()
        rows.append(
            {  # D303: unit / locality / country from the printed blocks resolve generic names
                "printed_org": name,
                "unit": sorted({u for _, u in hits if u})[:5],
                "locality": locality,
                "country": country,
                "count": len(hits),
                "locators": sorted({loc for loc, _ in hits})[:5],
                "proposed_org_id": by_name.get(key) or by_name.get(bare, ""),
                "curation_note": CURATION_NOTES.get(name, ""),
            }
        )
    write_atomic(spec.base() / "org_requests.csv", render_csv(REQUEST_COLS, rows))
    write_atomic(LOCAL / f"{spec.staging}_conflicts.csv", render_csv(CONFLICT_COLS, conflicts))
    write_atomic(LOCAL / f"{spec.staging}_extra_authors.csv", render_csv(EXTRA_AUTHOR_COLS, extra))
    log.info(f"org_requests {len(rows)} strings; local conflicts {len(conflicts)}, extra authors {len(extra)}")
    return stale


def _inputs() -> tuple[dict[str, ofc.OfcPresentation], dict[str, dict[str, str]], dict[tuple[str, str], list[str]]]:
    meta = {p.code: p for p in ofc.presentations()}
    orgs = {r["org_id"]: r for r in read_csv(REGISTRY / "organizations.csv")}
    xw = {(r["corpus"], r["printed"]): split_list(r["org_ids"]) for r in read_csv(CROSSWALK / "org_crosswalk.csv")}
    return meta, orgs, xw


def cmd_check(batches: list[str], dry_run: bool, corpus: str = "ofc2026") -> int:
    """Per-batch outputs only (safe to run in parallel, D248); `aggregate` writes the cross-batch files."""
    spec = LIT if corpus == "lit" else OFC
    label = "all" if batches == ["all"] else "_".join(batches)[:40]
    with RunLog(f"{spec.staging}_check_{label}_{os.getpid()}", dry_run) as log:
        meta: Mapping[str, ofc.OfcPresentation | LitPaper]
        if spec is LIT:
            _, orgs, xw = _inputs()
            meta, texts, pdfs, eo = lit_papers(), {}, {}, lit_duplicates()
        else:
            meta, orgs, xw = _inputs()
            texts, pdfs, eo = text_files(), pdf_files(), eo_duplicates()
        m = load_matcher()
        ck = Check(log)
        # (f) no paper in two batches
        where: dict[str, list[str]] = defaultdict(list)
        for b in batch_dirs(spec):
            for r in read_csv(b / "papers.csv"):
                where[r["source_id"]].append(b.name)
        for sid, bs in where.items():
            if len(bs) > 1:
                ck.err(f"{sid} queued in {bs} (D176 f)")
        total: Counter[str] = Counter()
        names = [b.name for b in batch_dirs(spec)] if batches == ["all"] else batches
        for name in names:
            d = spec.base() / name
            st = check_batch(d, ck, meta, texts, pdfs, eo, m, orgs, xw, write=not dry_run, spec=spec)
            log.info(f"{name}: {dict(sorted(st.items()))}")
            log.event("batch", batch=name, stats=dict(st))
            total.update(st)
        for w in ck.warnings:
            log.info(f"WARN {w}")
        for e in ck.errors:
            log.info(f"ERROR {e}")
        log.info(f"total: {dict(sorted(total.items()))}")
        log.info(f"errors {len(ck.errors)}, warnings {len(ck.warnings)}")
        log.event("summary", "ok" if not ck.errors else "errors", errors=len(ck.errors), stats=dict(total))
    return 1 if ck.errors else 0


def cmd_aggregate(corpus: str = "ofc2026") -> int:
    """Coordinator step after the batch checks (D248)."""
    spec = LIT if corpus == "lit" else OFC
    with RunLog(f"{spec.staging}_aggregate_{os.getpid()}", False) as log:
        meta: Mapping[str, ofc.OfcPresentation | LitPaper]
        if spec is LIT:
            _, orgs, _ = _inputs()
            meta = lit_papers()
        else:
            meta, orgs, _ = _inputs()
        stale = write_aggregates(log, meta, orgs, spec)
    return 1 if stale else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sp = sub.add_parser("pilot")
    sp.add_argument("codes", nargs="+")
    sq = sub.add_parser("queue")
    sq.add_argument("--size", type=int, default=40)
    sq.add_argument("--dry-run", action="store_true")
    ss = sub.add_parser("show")
    ss.add_argument("batch")
    ss.add_argument("--codes", nargs="*", default=[])
    ss.add_argument("--pdf", action="store_true")
    sc = sub.add_parser("check")
    sc.add_argument("batches", nargs="+", help="batch names, or 'all'")
    sc.add_argument("--dry-run", action="store_true")
    ss.add_argument("--pages", nargs="*", type=int, default=[], help="lit: further pages to print (page 1 always)")
    sg = sub.add_parser(
        "aggregate", help="cross-batch org_requests.csv and local review lists (coordinator, after checks)"
    )
    for x in (sp, sq, ss, sc, sg):
        x.add_argument("--corpus", choices=["ofc2026", "lit"], default="ofc2026", help="D350 (default ofc2026)")
    a = ap.parse_args()
    lit = a.corpus == "lit"
    if a.cmd == "pilot":
        return cmd_lit_pilot(a.codes) if lit else cmd_pilot(a.codes)
    if a.cmd == "queue":
        return cmd_lit_queue(a.size, a.dry_run) if lit else cmd_queue(a.size, a.dry_run)
    if a.cmd == "show":
        return cmd_lit_show(a.batch, a.codes, a.pdf, a.pages) if lit else cmd_show(a.batch, a.codes, a.pdf)
    if a.cmd == "aggregate":
        return cmd_aggregate(a.corpus)
    return cmd_check(a.batches, a.dry_run, a.corpus)


if __name__ == "__main__":
    sys.exit(main())
