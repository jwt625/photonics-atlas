"""Printed org string -> registry org_ids (D18, D19, D25): registry name key, then alias key (corpus-scoped aliases
first), then ROR display name/label whose ror_id is on a registry org. No fuzzy matching."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from .adapters import ror
from .csvio import read_csv, split_list
from .paths import REGISTRY
from .textnorm import norm_key


@dataclass
class Matcher:
    by_name: dict[str, str] = field(default_factory=dict)
    by_alias: dict[str, set[str]] = field(default_factory=lambda: defaultdict(set))
    by_scoped_alias: dict[tuple[str, str], set[str]] = field(default_factory=lambda: defaultdict(set))
    by_ror: dict[str, str] = field(default_factory=dict)
    ridx: ror.RorIndex | None = None

    def match(self, printed: str, corpus: str) -> tuple[list[str], str]:
        """Return (org_ids, basis) with basis in name | alias | ror | unmapped."""
        k = norm_key(printed)
        if not k:
            return [], "unmapped"
        scoped = self.by_scoped_alias.get((k, corpus))
        if scoped:
            return sorted(scoped), "alias"
        if k in self.by_name:
            return [self.by_name[k]], "name"
        if k in self.by_alias:
            return sorted(self.by_alias[k]), "alias"
        if self.ridx is not None:
            ids = {self.by_ror[r.ror_id] for r in self.ridx.lookup(printed) if r.ror_id in self.by_ror}
            if len(ids) == 1:
                return sorted(ids), "ror"
        return [], "unmapped"


def load_matcher(registry: Path = REGISTRY, with_ror: bool = True) -> Matcher:
    m = Matcher()
    for o in read_csv(registry / "organizations.csv"):
        if o.get("no_name_match") != "true":
            m.by_name[norm_key(o["name"])] = o["org_id"]
        # no_name_match orgs are kept out of the ROR display / label route too: their ROR display name is their
        # name (D310; e.g. Italy's CNR, ROR display "National Research Council").
        if o["ror_id"] and o.get("no_name_match") != "true":
            m.by_ror.setdefault(o["ror_id"], o["org_id"])
    for a in read_csv(registry / "org_aliases.csv"):
        k = norm_key(a["alias"])
        if a["scope"]:
            for c in split_list(a["scope"]):
                m.by_scoped_alias[(k, c)].add(a["org_id"])
        else:
            m.by_alias[k].add(a["org_id"])
    if with_ror:
        m.ridx = ror.load()
    return m
