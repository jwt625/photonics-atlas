"""Page-1 title / correction check for one queue day. Run from repo root: uv run python <skill>/scripts/title_check.py <day>"""

import csv
import os
import re
import sys

day = sys.argv[1]
src = {r["native_id"] for r in csv.DictReader(open("data/registry/sources.csv")) if r["corpus"] == "lit"}
q = [r for r in csv.DictReader(open("data/_staging/literature/retrieval_queue.csv")) if r["day"] == day]
cl = {r["paper_id"]: r for r in csv.DictReader(open("data/_staging/literature/cache_list.csv"))}


def n(s):
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


res = []
for r in q:
    p = f"references/{r['paper_id']}/text.md"
    if not os.path.exists(p):
        continue
    t = open(p, errors="replace").read()
    body = t.split("<!-- page 2 -->")[0].split("<!-- page 1 -->")[-1]
    words = [w for w in n(cl[r["paper_id"]]["title"]).split() if len(w) > 2]
    nb = n(body)
    cov = sum(w in nb for w in words) / max(1, len(words))
    corr = bool(re.search(r"\b(erratum|corrigendum|correction to)\b", body[:3000], re.I))
    res.append(
        (
            round(cov, 2),
            r["paper_id"],
            r["route"],
            "REG" if r["paper_id"] in src else "new",
            "CORR?" if corr else "",
            cl[r["paper_id"]]["title"][:70],
        )
    )
res.sort()
print(len(res), "with text;", sum(x[3] == "new" for x in res), "unregistered; below 0.9 or correction:")
for x in res:
    if x[0] < 0.9 or x[4]:
        print(x)
