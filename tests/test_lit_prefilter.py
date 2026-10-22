"""Pure-function tests for the literature prefilter and batch writer (DevLog-006 S2). No network, no pool files."""

from __future__ import annotations

import collections
import sys
from pathlib import Path
from typing import Any

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import lit_make_score_batches as mb  # noqa: E402
import lit_prefilter as lp  # noqa: E402


@pytest.fixture(scope="module")
def b() -> lp.Buckets:
    return lp.load_buckets()


def rec(**kw: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "uid": "",
        "doi": "",
        "arxiv_id": "",
        "openalex_id": "",
        "title": "",
        "year": 2024,
        "type": "article",
        "venue": "",
        "venue_type": "journal",
        "authors": ["Ada Lovelace"],
        "abstract": "",
        "is_oa": False,
        "oa_url": "",
        "lane": "journals",
        "discovered_via": "x",
    }
    base.update(kw)
    return base


def test_normalizers() -> None:
    assert lp.norm_arxiv("arXiv:2401.01234v3") == "2401.01234"
    assert lp.split_doi("https://doi.org/10.48550/arXiv.2401.01234") == ("", "2401.01234")
    assert lp.split_doi("10.1364/OE.1.2") == ("10.1364/oe.1.2", "")
    assert lp.name_tokens("Wei Wang") == lp.name_tokens("Wang Wei") == {"wang", "wei"}
    assert lp.title_key("Short title") == ""
    assert lp.clean_text("Low-loss <i>SiN</i> &amp; Si") == "Low-loss SiN & Si"


def test_merge_preprint_and_published() -> None:
    t = "Ultra-low-loss silicon nitride waveguides at visible wavelengths"
    pre = rec(
        uid="arxiv:2401.00001",
        arxiv_id="2401.00001",
        title=t,
        type="preprint",
        venue="arXiv",
        venue_type="repository",
        oa_url="https://arxiv.org/pdf/2401.00001",
        is_oa=True,
        lane="arxiv",
        abstract="A much longer preprint abstract " * 10,
        authors=["Wei Wang", "B C"],
    )
    pub = rec(uid="10.1364/optica.1", doi="10.1364/optica.1", title=t + ".", abstract="short", authors=["Wang Wei"])
    other = rec(uid="10.1/other", doi="10.1/other", title="A completely different paper on grating couplers")
    groups = lp.group_records([pre, pub, other])
    assert sorted(len(g) for g in groups) == [1, 2]
    m = lp.merge_group(next(g for g in groups if len(g) == 2))
    assert m["uid"] == "10.1364/optica.1" and m["doi"] == "10.1364/optica.1"
    assert m["arxiv_id"] == "2401.00001"
    assert m["preprint_oa_url"] == "https://arxiv.org/pdf/2401.00001" and m["is_oa"]
    assert m["abstract"].startswith("A much longer")
    assert m["lane"] == ["arxiv", "journals"]
    assert m["alt_uids"] == ["arxiv:2401.00001"]


def test_merge_by_arxiv_journal_doi_and_drop_types() -> None:
    pre = rec(
        uid="arxiv:2402.1",
        arxiv_id="2402.1",
        arxiv_dois=["10.1038/X"],
        type="preprint",
        venue_type="repository",
        title="Title A about microring resonators here",
    )
    pub = rec(uid="10.1038/x", doi="10.1038/x", title="Different published title of microring work")
    err = rec(uid="10.1/err", doi="10.1/err", type="erratum", title="Erratum: something about rings and things")
    merged, st = lp.merge_pool([pre, pub, err], {"erratum"}, None)
    assert st["dropped_type:erratum"] == 1 and st["duplicates_merged"] == 1 and len(merged) == 1


def test_known_index() -> None:
    k = lp.KnownIndex()
    k.add("eo_papers", doi="10.1364/OE.9", title="")
    k.add("ofc2026", title="A long enough OFC title about co-packaged lasers")
    assert k.match(rec(doi="10.1364/oe.9")) == ["eo_papers"]
    assert k.match(rec(title="A long enough OFC title about co-packaged lasers.")) == ["ofc2026"]
    assert k.match(rec(title="Unrelated long title about something else")) == []


def test_class_hits_and_best(b: lp.Buckets) -> None:
    hits = lp.class_hits("Low-loss grating coupler with integrated germanium photodetector", "", b)
    assert hits[0].cls == "fiber_chip_coupler" and hits[0].where == "title"
    assert "photodetector" in {h.cls for h in hits}
    assert "fiber_chip_coupler.grating" in lp.hit_labels(hits)
    hits = lp.class_hits("Silicon nitride arrayed waveguide grating for CWDM", "", b)
    assert hits[0].cls == "wdm" and "awg" in hits[0].subtypes
    assert not lp.class_hits("Polarization beam splitter on SOI", "", b)[0].cls == "splitter"
    seeded = lp.class_hits("A paper with no component words at all", "", b, ["nonreciprocal.isolator"])
    assert [(h.cls, h.where, h.subtypes) for h in seeded] == [("nonreciprocal", "seed", ["isolator"])]


def test_exclusions(b: lp.Buckets) -> None:
    def ex(title: str, abstract: str = "") -> str:
        return lp.exclusion(title, abstract, lp.class_hits(title, abstract, b), b)

    assert ex("100 GHz thin-film lithium niobate Mach-Zehnder modulator") == "eo_modulator_only"
    assert ex("Silicon microring modulator") == "eo_modulator_only"
    assert ex("Lithium niobate modulator with integrated photodetector") == ""
    assert ex("Mode-locked fiber laser with 10 fs pulses") == "fiber_laser_amplifier"
    assert ex("Erbium-doped waveguide amplifier on silicon nitride") == ""
    assert ex("Perovskite solar cells with 25% efficiency") == "solar_cells"
    assert ex("Topological photonic crystal theory", "We theoretically show edge states. " * 5) == "metamaterial_theory"
    assert ex("Topological photonic crystal ring laser", "We fabricate and measure the device. " * 5) == ""


def test_rule_score(b: lp.Buckets) -> None:
    title = "Low-loss silicon nitride microring resonator"
    abstract = "We fabricate and measure a ring with intrinsic Q of 10 million and 0.5 dB/m loss at 1550 nm. " * 2
    hits = lp.class_hits(title, abstract, b)
    s, c, flags, nq = lp.rule_score(title, abstract, hits[0], ["sin"], False, False, {}, b)
    assert c["title_class"] == 4 and c["experimental"] == 2 and c["quantitative"] == 2 and c["integrated"] == 1
    assert s == 10 and not flags and nq >= 2
    s2, c2, f2, _ = lp.rule_score("A review of microring resonators", "", hits[0], [], True, True, {}, b)
    assert c2["review"] == -4 and "abstract_missing" in f2 and "abstract_missing" not in c2
    sim = "We propose and numerically simulate a ring design with FDTD. " * 3
    _, c3, _, _ = lp.rule_score(title, sim, hits[0], [], False, False, {}, b)
    assert c3["sim_only"] == -3


def test_apply_caps_seeds_kept(b: lp.Buckets) -> None:
    def cand(i: int, score: int, seed: bool = False) -> dict[str, Any]:
        return {
            "uid": f"u{i}",
            "best_class": "crossing",
            "seed": seed,
            "rule_score": score,
            "hit_where": "title",
            "flags": [],
            "year": 2024,
            "n_quant": 0,
        }

    cands = [cand(i, 9) for i in range(300)] + [cand(999, 0, seed=True)]
    eff = lp.apply_caps(cands, {"crossing": 30}, b)
    cap = max(int(b.caps["cap_min"]), int(b.caps["cap_mult"] * 30))
    # seeds rank first and count toward the cap, but are kept even when the cap is full
    assert eff["crossing"]["cap"] == cap and eff["crossing"]["kept"] == cap and eff["crossing"]["seeds"] == 1
    assert next(c for c in cands if c["uid"] == "u999")["score_keep"]


def test_batches_helpers() -> None:
    assert mb.short_authors(["a", "b", "c", "d", "e"], "e") == ["a", "b", "c", "e"]
    assert mb.short_authors(["a", "b"], "b") == ["a", "b"]
    assert mb.short_authors(["a"] * 30 + ["z"], "real last") == ["a", "a", "a", "real last"]
    long = "word " * 1000
    t = mb.truncate(long, 2500)
    assert len(t) <= 2504 and t.endswith(" ...")
    keep = [{"uid": f"u{i}", "group": "G2", "best_class": "splitter", "cap_rank": i, "alt_uids": []} for i in range(5)]
    keep[0]["alt_uids"] = ["arxiv:old"]
    man: dict[str, Any] = {"batches": [{"file": "G2_b001.jsonl", "uids": ["u1"], "aliases": ["arxiv:old"]}]}
    plans, held, done = mb.plan_batches(keep, man, 2, flush=False)
    assert done == 2 and [p[0] for p in plans] == ["G2_b002.jsonl"] and held == {"G2": 1}
    plans, held, _ = mb.plan_batches(keep, man, 2, flush=True)
    assert [p[0] for p in plans] == ["G2_b002.jsonl", "G2_b003.jsonl"] and not held
    rec_out = mb.batch_record({"uid": "u", "title": "t", "authors": ["a"], "abstract": "x", "extra": 1})
    assert list(rec_out) == mb.FIELDS


def test_read_pool_skips_torn_lines(tmp_path: Path) -> None:
    (tmp_path / "journals_x.jsonl").write_text('{"uid": "a", "title": "T"}\n{"uid": "b", "ti', encoding="utf-8")
    (tmp_path / "arxiv_y.jsonl.part").write_text('{"uid": "c", "title": "T"}\n', encoding="utf-8")
    st: collections.Counter[str] = collections.Counter()
    recs = list(lp.read_pool(tmp_path, st))
    assert [r["uid"] for r in recs] == ["a"] and st["bad_lines"] == 1 and recs[0]["lane"] == "journals"


def test_strict_files(b: lp.Buckets) -> None:
    abstract = "We fabricate a microring resonator on chip and measure Q of 1 million at 1550 nm. " * 2
    title = "Quantum dynamics of a driven two-level system"
    assert lp.class_hits(title, abstract, b)  # abstract-only (weak) hit when not strict
    assert not lp.class_hits(title, abstract, b, strict=True)
    assert lp.is_strict({"pool_file": ["arxiv_appq_2026-01.jsonl"]}, b)
    assert not lp.is_strict({"pool_file": ["arxiv_appq_2026-01.jsonl", "journals_optica_2025.jsonl"]}, b)


def test_seed_tiers(b: lp.Buckets) -> None:
    abstract = "We fabricate and measure the device with 0.5 dB loss at 1550 nm. " * 3

    def merged(files: list[str], title: str, year: int = 2020, **kw: Any) -> dict[str, Any]:
        members = [
            rec(
                uid="10.1/x",
                doi="10.1/x",
                title=title,
                abstract=abstract,
                year=year,
                pool_file=f,
                lane=f.split("_")[0],
                **kw,
            )
            for f in files
        ]
        return lp.merge_group(members)

    a = lp.analyse(
        merged(["seeds_local.jsonl"], "A paper with no component words at all", seed_class="nonreciprocal"), b
    )
    assert a["status"] == "candidate" and a["seed_tier"] == "A" and a["components"]["seed_a"] == 2 and a["seed"]
    bt = lp.analyse(merged(["seeds_refs_laser.jsonl"], "A paper with no component words at all", seed_class="laser"), b)
    assert bt["status"] == "no_class_hit"
    title = "Low-loss silicon nitride microring resonator"
    b1 = lp.analyse(merged(["seeds_refs_resonator.jsonl"], title, seed_class="resonator", refs_of_all=["r1"]), b)
    assert b1["status"] == "candidate" and b1["components"]["seed_b"] == 1 and "seed_b_multi" not in b1["components"]
    assert not b1["seed"]
    b2m = merged(["seeds_refs_resonator.jsonl", "seeds_refs_laser.jsonl"], title)
    b2m["seed_members"] = [
        {"pool_file": "seeds_refs_laser.jsonl", "seed_class": "laser"},
        {"pool_file": "seeds_refs_resonator.jsonl", "seed_class": "resonator"},
    ]
    assert lp.analyse(b2m, b)["components"]["seed_b_multi"] == 1  # reviews of two classes
    b3 = lp.analyse(merged(["seeds_refs_resonator.jsonl"], title, seed_class="resonator", refs_of_all=["r1", "r2"]), b)
    assert b3["components"]["seed_b_multi"] == 1  # two reviews
    old = merged(["seeds_refs_resonator.jsonl"], title, year=1990, seed_class="resonator")
    old["abstract"] = ""
    assert lp.analyse(old, b)["status"] == "seed_b_pre2005_no_cue"
    weak = merged(["seeds_refs_resonator.jsonl"], "A study of things on a chip", seed_class="resonator")
    weak["abstract"] = "We fabricate a microring resonator and measure Q of 1 million at 1550 nm. " * 2
    assert lp.analyse(weak, b)["status"] == "seed_b_no_title_hit"
    weak["pool_file"] = ["journals_x.jsonl", "seeds_refs_resonator.jsonl"]
    assert lp.analyse(weak, b)["status"] == "candidate"  # a lane also found it: normal rules + tier-B bonus
    rv = merged(["seeds_reviews.jsonl"], title, is_review_seed=True)
    assert lp.analyse(rv, b)["status"] == "review_seed"
