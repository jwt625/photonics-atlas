"""Name normalization (D18), slugs (D14) and e-mail stripping (D24)."""

from __future__ import annotations

import re
import unicodedata

# Legal-form tokens dropped from the crosswalk key (D18). Whole tokens only, after punctuation removal.
LEGAL_SUFFIXES = {
    "inc",
    "incorporated",
    "corp",
    "corporation",
    "co",
    "company",
    "ltd",
    "limited",
    "llc",
    "lp",
    "gmbh",
    "mbh",
    "ag",
    "sa",
    "sas",
    "sarl",
    "se",
    "bv",
    "nv",
    "plc",
    "kk",
    "srl",
    "spa",
    "oy",
    "oyj",
    "ab",
    "as",
    "pte",
    "pty",
    "kg",
    "ug",
    "aps",
    "asa",
    "sl",
    "slu",
    "bhd",
    "sdn",
}
# Plain, grouped ({alice,bob}@mit.edu) and obfuscated (alice [at] mit [dot] edu, alice(at)mit.edu) addresses.
EMAIL_RE = re.compile(
    r"(?:\{[^{}]*\}|[\w.+-]+)\s*(?:@|\[at\]|\(at\))\s*[\w-]+(?:\s*(?:\.|\[dot\]|\(dot\))\s*[\w-]+)+",
    re.IGNORECASE,
)


def ascii_fold(s: str) -> str:
    s = s.replace("ß", "ss").replace("ø", "o").replace("Ø", "O").replace("æ", "ae").replace("Æ", "AE")
    s = s.replace("đ", "d").replace("Đ", "D").replace("ł", "l").replace("Ł", "L")
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()


def norm_key(name: str) -> str:
    """Crosswalk key: accents stripped, lowercase, & -> and, punctuation -> space, legal suffixes dropped."""
    s = ascii_fold(name).lower().replace("&", " and ").replace("'", "").replace("’", "")
    s = re.sub(r"[^a-z0-9]+", " ", s)
    toks = [t for t in s.split() if t not in LEGAL_SUFFIXES]
    return " ".join(toks)


def slug(name: str) -> str:
    s = ascii_fold(name).lower().replace("&", " and ").replace("'", "").replace("’", "")
    return "_".join(re.sub(r"[^a-z0-9]+", " ", s).split())


def strip_emails(s: str) -> str:
    return EMAIL_RE.sub("", s).strip()
