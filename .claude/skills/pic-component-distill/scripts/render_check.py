"""Headless render check of the built app (vite preview on the port). Usage: uv run python <skill>/scripts/render_check.py
<outdir> <n_components> <n_metrics> [port]. Prints console errors per page and the dashboard totals line; saves bench.png."""

import sys

from playwright.sync_api import sync_playwright

base = f"http://localhost:{sys.argv[4] if len(sys.argv) > 4 else 4791}"
out, NCOMP, NMET = sys.argv[1], sys.argv[2], sys.argv[3]
pages = ["", "components", "benchmark", "people", "orgs", "supply", "explore", "history"]
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    for name in pages:
        pg = b.new_page(viewport={"width": 1440, "height": 900})
        errs = []
        pg.on("console", lambda m, errs=errs: errs.append(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e, errs=errs: errs.append(str(e)))
        pg.goto(f"{base}/{name}", wait_until="networkidle")
        pg.wait_for_timeout(1500)
        txt = pg.inner_text("body")
        print(f"{name or 'dashboard':10s} errors={len(errs)} {errs[:2]}")
        if name == "":
            import re

            print(
                "   ",
                [
                    ln
                    for ln in txt.splitlines()
                    if re.search(rf"{NCOMP[:-3]}[,\s]?{NCOMP[-3:]}|{NMET[:-3]}[,\s]?{NMET[-3:]}", ln)
                ][:3],
            )
        if name == "benchmark":
            pg.screenshot(path=f"{out}/bench.png", full_page=False)
            print("   imec present:", "imec" in txt)
        pg.close()
    b.close()
