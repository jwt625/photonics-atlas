from collections import Counter

from photonics_atlas.csvio import read_csv
from photonics_atlas.paths import REGISTRY


def test_sources_corpora_and_ofc_dedupe() -> None:
    src = read_csv(REGISTRY / "sources.csv")
    c = Counter(s["corpus"] for s in src)
    assert (c["eo"], c["pk"], c["ofc2026"], c["blog"], c["lin"]) == (233, 296, 830, 128, 282)
    dups = [s for s in src if s["same_as"]]
    assert len(dups) == 54
    assert all(s["corpus"] == "ofc2026" and s["same_as"].startswith("eo:") for s in dups)
    ids = {s["source_id"] for s in src}
    assert all(s["same_as"] in ids for s in dups)


def test_non_oa_corpora_are_restricted() -> None:
    for s in read_csv(REGISTRY / "sources.csv"):
        if s["corpus"] in ("ofc2026", "pk"):
            assert s["redistribution"] == "restricted_local_only", s["source_id"]
