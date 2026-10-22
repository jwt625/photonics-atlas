"""Polite downloader for the open routes of the S7 retrieval queue (DevLog-006 S7): `arxiv` and `oa_publisher`.

Adapted from eo-modulator-atlas scripts/fetch_source.py, without any personal identifier in the request (generic
User-Agent, no mailto). Guarantees:
  - one fetcher at a time (non-blocking exclusive lock logs/.lit_fetch_oa.lock);
  - per-host serialization and spacing through logs/.lit_<host>.lock / .lit_<host>.last (the same files as
    photonics_atlas.litfetch): arxiv.org >= 5 s + 0-3 s jitter, doi.org >= 5 s + 0-3 s, every publisher or repository
    host >= 15 s + 0-5 s; redirects are followed hop by hop so each hop host gets its own spacing and breaker check;
  - per-host breaker logs/.lit_blocked_<host>.json (litfetch format, 30 min cooldown) on HTTP 403 / 429 / 503, a
    WAF challenge (HTTP 202, x-amzn-waf-action, cf-mitigated), a network error, a challenge / captcha page, or HTML where a PDF was expected; while active no request goes to that
    host. A breaker on arxiv.org stops the run;
  - landing pages (doi.org, publisher HTML): exactly one follow-up to the `citation_pdf_url` meta tag (else a
    `<meta http-equiv="refresh">` target), i.e. one HTML request + one PDF request, never a crawl. A URL that names a
    PDF (.pdf, /pdf/, /pdfdirect/, /article-pdf/) and answers HTML without such a tag arms the breaker. Non-PDF
    answers are saved for diagnosis in cache/literature/fetch_debug/ (first 200 kB). Optica (optica.org,
    osapublishing.org) and IEEE (ieee.org) hosts are never requested here (browser routes, lit_fetch_browser.py);
  - atomic cache: the body goes to cache/literature/fetch_part/<paper_id>.pdf.part and is moved to
    references/<paper_id>/source.pdf only after the %PDF magic, >= 20 kB and the full Content-Length are verified;
  - status per attempted paper appended to logs/lit_fetch_status.jsonl (ts, paper_id, route, status ok / blocked /
    not_pdf / error, bytes, sha256, url, reason); papers with a valid cached source.pdf are skipped;
  - arXiv copies: the license of the latest version from the arXiv OAI-PMH arXivRaw record (one request to
    oaipmh.arxiv.org through photonics_atlas.litfetch), stored in source.json; `--no-license` skips it.
Jobs come from data/_staging/literature/retrieval_queue.csv (stream R1); without the queue, `--paper-ids` falls back
to data/_staging/literature/cache_list.csv with a derived route. Next step: scripts/lit_extract.py --pending.

Usage: uv run python scripts/lit_fetch_oa.py (--day N | --paper-ids a,b) [--route arxiv|oa_publisher] [--max N]
         [--queue PATH] [--no-license] [--dry-run]
Exit codes: 0 all ok / skipped, 3 some paper failed, 4 stopped by a breaker (arxiv.org) or another fetcher running.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import fcntl
import hashlib
import http.client
import http.cookiejar
import json
import os
import random
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import defaultdict, deque
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

from photonics_atlas import litfetch
from photonics_atlas.paths import CACHE, LOGS, ROOT, STAGING
from photonics_atlas.runlog import RunLog

REFS = ROOT / "references"
LIT = STAGING / "literature"
QUEUE = LIT / "retrieval_queue.csv"
CACHE_LIST = LIT / "cache_list.csv"
STATUS_LOG = LOGS / "lit_fetch_status.jsonl"
PART_DIR = CACHE / "literature" / "fetch_part"
DEBUG_DIR = CACHE / "literature" / "fetch_debug"

UA = "photonics-atlas-literature-fetch/0.1 (open-access research corpus)"
ROUTES = ("arxiv", "oa_publisher")
MIN_PDF_BYTES = 20_000
TIMEOUT_S = 90
MAX_HOPS = 6
COOLDOWN_S = float(os.environ.get("LITFETCH_COOLDOWN_S", "1800"))
SPACING_S: dict[str, tuple[float, float]] = {"arxiv.org": (5.0, 3.0), "doi.org": (5.0, 3.0)}
PUBLISHER_SPACING_S = (15.0, 5.0)
EXCLUDED_HOST_SUFFIXES = ("optica.org", "osapublishing.org", "ieee.org")
BROWSER_DOI_PREFIXES = {"10.1364/": "optica_browser", "10.1109/": "ieee_browser", "10.23919/": "ieee_browser"}
BLOCK_CODES = (403, 429, 503)
CHALLENGE_MARKERS = (
    "captcha",
    "cf-chl",
    "challenge-platform",
    "just a moment",
    "are you a robot",
    "unusual traffic",
    "datadome",
    "access denied",
    "verify you are human",
    "client challenge",  # Fastly JS challenge on www.nature.com (pilot 2026-10-22)
    "/_fs-ch-",
)
OAI_URL = "https://oaipmh.arxiv.org/oai"
OAI_NS = {"o": "http://www.openarchives.org/OAI/2.0/", "r": "http://arxiv.org/OAI/arXivRaw/"}


class BlockedError(RuntimeError):
    """A host breaker is (now) active; no request was or will be sent to that host until the cooldown ends."""


class ExcludedHostError(RuntimeError):
    """The URL (or a redirect hop) points at a host reserved for the browser routes."""


# ---------------------------------------------------------------- pure helpers (tested)


def now_iso() -> str:
    return dt.datetime.now(dt.UTC).isoformat(timespec="seconds")


def host_of(url: str) -> str:
    return (urllib.parse.urlsplit(url).hostname or "").lower()


def excluded_host(host: str) -> bool:
    return any(host == s or host.endswith("." + s) for s in EXCLUDED_HOST_SUFFIXES)


def spacing_for(host: str) -> tuple[float, float]:
    """(minimum interval s, max jitter s) for a host; every host not listed counts as a publisher / repository."""
    return SPACING_S.get(host, PUBLISHER_SPACING_S)


def strip_arxiv_version(arxiv_id: str) -> str:
    return re.sub(r"v\d+$", "", arxiv_id.strip())


def arxiv_pdf_url(arxiv_id: str) -> str:
    """Latest-version PDF (no version suffix)."""
    return f"https://arxiv.org/pdf/{strip_arxiv_version(arxiv_id)}"


def derive_route(row: dict[str, str]) -> str:
    """Route for a cache_list row when the R1 queue is absent (the queue's own route always wins)."""
    if row.get("arxiv_id"):
        return "arxiv"
    url, doi = row.get("oa_url", ""), row.get("doi", "").lower()
    host = host_of(url)
    if row.get("access") != "oa" or not url:
        return "manual"
    if excluded_host(host) or host == "doi.org":
        for prefix, route in BROWSER_DOI_PREFIXES.items():
            if doi.startswith(prefix):
                return route
        if excluded_host(host):
            return "ieee_browser" if host.endswith("ieee.org") else "optica_browser"
    return "oa_publisher"


def browser_only(url: str, doi: str) -> bool:
    """True when fetching `url` would hit an Optica / IEEE host (directly or through the doi.org resolver)."""
    host = host_of(url)
    if excluded_host(host):
        return True
    return host == "doi.org" and any(doi.lower().startswith(p) for p in BROWSER_DOI_PREFIXES)


def looks_like_pdf(body: bytes) -> bool:
    return body[:5] == b"%PDF-"


def looks_like_html(body: bytes, content_type: str) -> bool:
    head = body[:1024].lstrip().lower()
    return "html" in content_type.lower() or head.startswith((b"<!doctype html", b"<html"))


def is_challenge(html: str) -> bool:
    low = html[:300_000].lower()
    return any(m in low for m in CHALLENGE_MARKERS)


def waf_challenge(status: int, headers: dict[str, str]) -> bool:
    """HTTP 202 to a document GET (AWS WAF answers its JS challenge this way; seen on degruyterbrill.com and Optica
    2026-10-22) or an explicit WAF / Cloudflare challenge header."""
    return (
        status == 202
        or bool(headers.get("x-amzn-waf-action"))
        or headers.get("cf-mitigated", "").lower() == "challenge"
    )


def complete_body(body: bytes, headers: dict[str, str]) -> bool:
    """Content-Length (when sent, and the body is not content-encoded) equals the received size."""
    declared = headers.get("content-length", "")
    if not declared.isdigit() or headers.get("content-encoding"):
        return True
    return int(declared) == len(body)


def pdf_problem(status: int, body: bytes, headers: dict[str, str]) -> str:
    """'' when the response is a complete PDF, else the reason."""
    if status != 200:
        return f"HTTP {status}"
    if not looks_like_pdf(body):
        return "not %PDF"
    if len(body) < MIN_PDF_BYTES:
        return f"too small ({len(body)} B)"
    if not complete_body(body, headers):
        return f"truncated ({len(body)} of {headers.get('content-length')} B)"
    return ""


class _MetaParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.found: list[str] = []
        self.refresh: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "meta":
            return
        a = {k.lower(): (v or "") for k, v in attrs}
        if a.get("name", "").lower() == "citation_pdf_url" and a.get("content"):
            self.found.append(a["content"].strip())
        if a.get("http-equiv", "").lower() == "refresh":
            m = re.search(r"url\s*=\s*['\"]?([^'\"\s>]+)", a.get("content", ""), re.I)
            if m:
                self.refresh.append(m.group(1))


def _parse_meta(html: str) -> _MetaParser:
    p = _MetaParser()
    try:
        p.feed(html)
    except Exception:  # noqa: BLE001  malformed HTML: whatever was parsed so far
        pass
    return p


def citation_pdf_url(html: str, base_url: str) -> str:
    """Absolute URL from the first <meta name="citation_pdf_url" content="..."> tag, '' if absent."""
    p = _parse_meta(html)
    return urllib.parse.urljoin(base_url, p.found[0]) if p.found else ""


def meta_refresh_url(html: str, base_url: str) -> str:
    """Absolute URL of a <meta http-equiv="refresh" content="0; url=..."> redirect, '' if absent."""
    p = _parse_meta(html)
    return urllib.parse.urljoin(base_url, p.refresh[0]) if p.refresh else ""


def pdf_like_url(url: str) -> bool:
    """The URL itself names a PDF (so an HTML answer is 'HTML instead of PDF', not a landing page)."""
    path = urllib.parse.urlsplit(url).path.lower()
    return path.endswith(".pdf") or bool(re.search(r"/(pdf|pdfdirect|pdfft|article-pdf)(/|$)", path))


def next_pdf_hop(html: str, base_url: str) -> str:
    """The one allowed follow-up from an HTML page: citation_pdf_url, else a meta refresh (never a crawl)."""
    return citation_pdf_url(html, base_url) or meta_refresh_url(html, base_url)


def round_robin(jobs: list[Job]) -> list[Job]:
    """Interleave jobs by host key so per-host spacing overlaps instead of adding up (order kept inside a host)."""
    by: dict[str, deque[Job]] = defaultdict(deque)
    for j in jobs:
        by[j.host_key()].append(j)
    out: list[Job] = []
    while by:
        for k in list(by):
            out.append(by[k].popleft())
            if not by[k]:
                del by[k]
    return out


def parse_arxiv_raw(xml: bytes) -> dict[str, str]:
    """license URL and latest version from an OAI-PMH GetRecord arXivRaw response ({} when absent)."""
    root = ET.fromstring(xml)
    rec = root.find(".//r:arXivRaw", OAI_NS)
    if rec is None:
        return {}
    lic = (rec.findtext("r:license", default="", namespaces=OAI_NS) or "").strip()
    versions = [v.get("version", "") for v in rec.findall("r:version", OAI_NS)]
    return {"arxiv_license": lic, "arxiv_version": versions[-1] if versions else ""}


# ---------------------------------------------------------------- jobs


@dataclass
class Job:
    paper_id: str
    uid: str
    doi: str
    arxiv_id: str
    route: str
    url: str
    access: str

    def host_key(self) -> str:
        host = host_of(self.url)
        if host == "doi.org" and "/" in self.doi:
            return "doi:" + self.doi.split("/", 1)[0]
        return host


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return [dict(r) for r in csv.DictReader(f)]


def cache_list_by_id() -> dict[str, dict[str, str]]:
    return {r["paper_id"]: r for r in read_rows(CACHE_LIST)}


def queue_by_id(path: Path = QUEUE) -> dict[str, dict[str, str]]:
    return {r["paper_id"]: r for r in read_rows(path)} if path.exists() else {}


def job_from(row: dict[str, str], cache_row: dict[str, str] | None) -> Job:
    c = cache_row or {}
    route = row.get("route") or derive_route(c or row)
    arxiv_id = row.get("arxiv_id") or c.get("arxiv_id", "")
    url = row.get("route_url", "")
    if not url:
        url = arxiv_pdf_url(arxiv_id) if route == "arxiv" and arxiv_id else c.get("oa_url", "")
    if route == "arxiv" and arxiv_id and host_of(url) != "arxiv.org":
        url = arxiv_pdf_url(arxiv_id)
    return Job(
        paper_id=row.get("paper_id") or c["paper_id"],
        uid=row.get("uid") or c.get("uid", ""),
        doi=row.get("doi") or c.get("doi", ""),
        arxiv_id=arxiv_id,
        route=route,
        url=url,
        access=row.get("access") or c.get("access", ""),
    )


def load_jobs(day: int | None, paper_ids: list[str], route: str | None, queue: Path) -> list[Job]:
    cl = cache_list_by_id()
    q = queue_by_id(queue)
    if day is not None:
        if not q:
            raise SystemExit(f"--day needs the retrieval queue {queue.relative_to(ROOT)} (not found)")
        rows = [r for r in q.values() if str(r.get("day", "")).strip() == str(day)]
    else:
        unknown = [p for p in paper_ids if p not in q and p not in cl]
        if unknown:
            raise SystemExit(f"unknown paper_id(s): {', '.join(unknown)}")
        rows = [q.get(p) or cl[p] for p in paper_ids]
    jobs = [job_from(r, cl.get(r["paper_id"])) for r in rows]
    return [j for j in jobs if j.route in ((route,) if route else ROUTES)]


# ---------------------------------------------------------------- breaker, spacing, HTTP


def _breaker(host: str) -> Path:
    return LOGS / f".lit_blocked_{host}.json"


def breaker_remaining(host: str) -> float:
    p = _breaker(host)
    if not p.exists():
        return 0.0
    try:
        until = float(json.loads(p.read_text())["until"])
    except (ValueError, KeyError, json.JSONDecodeError):
        return 0.0
    left = until - time.time()
    if left <= 0:
        p.unlink(missing_ok=True)
        return 0.0
    return left


def arm_breaker(host: str, reason: str, log: RunLog) -> None:
    until = time.time() + COOLDOWN_S
    until_iso = dt.datetime.fromtimestamp(until, dt.UTC).isoformat(timespec="seconds")
    _breaker(host).write_text(json.dumps({"until": until, "until_iso": until_iso, "reason": reason}))
    log.info(f"BREAKER armed for {host} until {until_iso}: {reason}")
    log.event("breaker", "armed", host=host, reason=reason, until=until_iso)


@contextmanager
def host_slot(host: str) -> Iterator[None]:
    """Exclusive per-host lock + breaker check + spacing; the stamp is written after the request."""
    LOGS.mkdir(exist_ok=True)
    with (LOGS / f".lit_{host}.lock").open("a+") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        left = breaker_remaining(host)
        if left > 0:
            raise BlockedError(f"{host} breaker active ({left:.0f} s left)")
        stamp = LOGS / f".lit_{host}.last"
        try:
            last = float(stamp.read_text() or 0) if stamp.exists() else 0.0
        except ValueError:
            last = 0.0
        interval, jitter = spacing_for(host)
        wait = last + interval + random.uniform(0, jitter) - time.time()
        if wait > 0:
            time.sleep(wait)
        try:
            yield
        finally:
            stamp.write_text(str(time.time()))


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args: Any, **kwargs: Any) -> None:
        return None


_OPENER = urllib.request.build_opener(_NoRedirect, urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))


@dataclass
class Resp:
    url: str
    status: int
    headers: dict[str, str]
    body: bytes
    hops: list[str]


def http_get(url: str, accept: str, log: RunLog) -> Resp:
    """GET with manual redirects; every hop goes through host_slot. Raises BlockedError / ExcludedHostError."""
    hops: list[str] = []
    for _ in range(MAX_HOPS):
        host = host_of(url)
        if excluded_host(host):
            raise ExcludedHostError(f"{host} is a browser-route host")
        hops.append(url)
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept})
        location = ""
        with host_slot(host):
            try:
                with _OPENER.open(req, timeout=TIMEOUT_S) as r:
                    resp = Resp(url, r.status, {k.lower(): v for k, v in r.headers.items()}, r.read(), hops)
            except urllib.error.HTTPError as e:
                headers = {k.lower(): v for k, v in (e.headers or {}).items()}
                if e.code in (301, 302, 303, 307, 308) and headers.get("location"):
                    location = urllib.parse.urljoin(url, headers["location"])
                    resp = Resp(url, e.code, headers, b"", hops)
                else:
                    try:
                        body = e.read()
                    except (OSError, http.client.HTTPException):
                        body = b""
                    resp = Resp(url, e.code, headers, body, hops)
                    if e.code in BLOCK_CODES:
                        arm_breaker(host, f"HTTP {e.code} on {url}", log)
                        log.event(
                            "http",
                            "blocked",
                            url=url,
                            http_status=e.code,
                            server=headers.get("server", ""),
                            cf_mitigated=headers.get("cf-mitigated", ""),
                            challenge=is_challenge(body.decode("utf-8", "replace")),
                            bytes=len(body),
                        )
                        raise BlockedError(f"{host}: HTTP {e.code}") from e
            except (urllib.error.URLError, TimeoutError, ConnectionError, http.client.HTTPException) as e:
                arm_breaker(host, f"network error on {url}: {e}", log)
                raise BlockedError(f"{host}: network error {e}") from e
        log.event(
            "http",
            "ok",
            url=url,
            http_status=resp.status,
            bytes=len(resp.body),
            content_type=resp.headers.get("content-type", ""),
        )
        if waf_challenge(resp.status, resp.headers):
            arm_breaker(host, f"WAF challenge (HTTP {resp.status}) on {url}", log)
            raise BlockedError(f"{host}: WAF challenge (HTTP {resp.status})")
        if not location:
            return resp
        url = location
    raise RuntimeError(f"more than {MAX_HOPS} redirects from {hops[0]}")


# ---------------------------------------------------------------- one paper


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def valid_cached(pdf: Path) -> bool:
    try:
        with pdf.open("rb") as f:
            head = f.read(5)
        return head == b"%PDF-" and pdf.stat().st_size >= MIN_PDF_BYTES
    except OSError:
        return False


def status_line(job: Job, status: str, **data: Any) -> None:
    LOGS.mkdir(exist_ok=True)
    rec = {
        "ts": now_iso(),
        "paper_id": job.paper_id,
        "route": job.route,
        "status": status,
        "bytes": 0,
        "sha256": "",
        **data,
    }
    with STATUS_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def merge_source_json(paper_id: str, fields: dict[str, Any]) -> None:
    path = REFS / paper_id / "source.json"
    meta: dict[str, Any] = json.loads(path.read_text()) if path.exists() else {}
    meta.update({k: v for k, v in fields.items() if v not in (None, "")})
    path.write_text(json.dumps(meta, indent=1, ensure_ascii=False) + "\n")


def arxiv_license(arxiv_id: str, log: RunLog) -> dict[str, str]:
    params = {
        "verb": "GetRecord",
        "identifier": f"oai:arXiv.org:{strip_arxiv_version(arxiv_id)}",
        "metadataPrefix": "arXivRaw",
    }
    try:
        info = parse_arxiv_raw(litfetch.get(OAI_URL, params))
    except (litfetch.BlockedError, urllib.error.URLError, TimeoutError, ET.ParseError, OSError) as e:
        log.event("arxiv_license", "error", arxiv_id=arxiv_id, error=str(e)[:200])
        return {}
    if info:
        info["license_source"] = "arXiv OAI-PMH arXivRaw <license> (latest version)"
    return info


def save_pdf(job: Job, resp: Resp, landing: str, license_info: dict[str, str]) -> tuple[int, str]:
    out = REFS / job.paper_id
    out.mkdir(parents=True, exist_ok=True)
    PART_DIR.mkdir(parents=True, exist_ok=True)
    part = PART_DIR / f"{job.paper_id}.pdf.part"
    part.write_bytes(resp.body)
    os.replace(part, out / "source.pdf")
    digest = sha256_bytes(resp.body)
    merge_source_json(
        job.paper_id,
        {
            "paper_id": job.paper_id,
            "uid": job.uid,
            "doi": job.doi,
            "arxiv_id": job.arxiv_id,
            "route": job.route,
            "url": resp.url,
            "landing_url": landing,
            "retrieved_on": now_iso(),
            "bytes": len(resp.body),
            "sha256": digest,
            "content_type": resp.headers.get("content-type", ""),
            **license_info,
        },
    )
    return len(resp.body), digest


def html_page(resp: Resp) -> bool:
    return (
        resp.status == 200
        and not looks_like_pdf(resp.body)
        and looks_like_html(resp.body, resp.headers.get("content-type", ""))
    )


def save_debug(paper_id: str, resp: Resp) -> None:
    """First 200 kB of a non-PDF answer, for diagnosis (git-ignored cache; never re-requested)."""
    DEBUG_DIR.mkdir(parents=True, exist_ok=True)
    n = len(list(DEBUG_DIR.glob(f"{paper_id}_*.html"))) + 1
    head = f"<!-- {resp.status} {resp.url} {json.dumps(resp.headers)} -->\n".encode()
    (DEBUG_DIR / f"{paper_id}_{n}.html").write_bytes(head + resp.body[:200_000])


def fetch_one(job: Job, log: RunLog, with_license: bool) -> str:
    """Returns the status written to the status log (ok / blocked / not_pdf / error)."""
    if not job.url:
        status_line(job, "error", reason="no url")
        return "error"
    if job.route == "oa_publisher" and browser_only(job.url, job.doi):
        status_line(job, "error", url=job.url, reason="browser-route host (Optica / IEEE); not fetched here")
        return "error"
    pdf_accept = "application/pdf,*/*;q=0.8"
    html_accept = "text/html,application/xhtml+xml,application/pdf;q=0.9,*/*;q=0.8"
    try:
        named_pdf = job.route == "arxiv" or pdf_like_url(job.url)
        resp = http_get(job.url, pdf_accept if named_pdf else html_accept, log)
        landing = ""
        if html_page(resp):
            html = resp.body.decode("utf-8", "replace")
            host = host_of(resp.url)
            save_debug(job.paper_id, resp)
            if is_challenge(html):
                arm_breaker(host, f"challenge page at {resp.url}", log)
                status_line(job, "blocked", url=resp.url, reason="challenge / captcha page")
                return "blocked"
            nxt = next_pdf_hop(html, resp.url) if job.route == "oa_publisher" else ""
            if not nxt or nxt == resp.url:
                if named_pdf:
                    arm_breaker(host, f"HTML ({len(resp.body)} B) instead of PDF at {resp.url}", log)
                    status_line(job, "not_pdf", url=resp.url, reason="HTML instead of PDF")
                else:
                    status_line(job, "not_pdf", url=resp.url, reason="landing page without citation_pdf_url")
                return "not_pdf"
            landing = resp.url
            resp = http_get(nxt, pdf_accept, log)
            if html_page(resp):
                html = resp.body.decode("utf-8", "replace")
                save_debug(job.paper_id, resp)
                arm_breaker(host_of(resp.url), f"HTML ({len(resp.body)} B) instead of PDF at {resp.url}", log)
                st = "blocked" if is_challenge(html) else "not_pdf"
                reason = "challenge / captcha page" if st == "blocked" else "HTML instead of PDF"
                status_line(job, st, url=resp.url, landing_url=landing, reason=reason)
                return st
        problem = pdf_problem(resp.status, resp.body, resp.headers)
        if problem:
            status_line(job, "not_pdf", url=resp.url, http_status=resp.status, bytes=len(resp.body), reason=problem)
            return "not_pdf"
        lic = arxiv_license(job.arxiv_id, log) if with_license and job.route == "arxiv" else {}
        size, digest = save_pdf(job, resp, landing, lic)
        status_line(
            job,
            "ok",
            url=resp.url,
            landing_url=landing,
            bytes=size,
            sha256=digest,
            arxiv_license=lic.get("arxiv_license", ""),
        )
        log.info(f"ok {job.paper_id} {size} B {resp.url}")
        return "ok"
    except BlockedError as e:
        status_line(job, "blocked", url=job.url, reason=str(e)[:300])
        log.info(f"blocked {job.paper_id}: {e}")
        return "blocked"
    except ExcludedHostError as e:
        status_line(job, "error", url=job.url, reason=str(e))
        return "error"
    except (RuntimeError, OSError) as e:
        status_line(job, "error", url=job.url, reason=str(e)[:300])
        log.info(f"error {job.paper_id}: {e}")
        return "error"


# ---------------------------------------------------------------- main


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--day", type=int)
    g.add_argument("--paper-ids", help="comma-separated paper_ids")
    ap.add_argument("--route", choices=ROUTES)
    ap.add_argument("--max", type=int, default=0, help="at most N network attempts (0 = no limit)")
    ap.add_argument("--queue", type=Path, default=QUEUE)
    ap.add_argument("--no-license", action="store_true", help="skip the arXiv OAI-PMH license lookup")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    ids = [p.strip() for p in (a.paper_ids or "").split(",") if p.strip()]
    jobs = round_robin(load_jobs(a.day, ids, a.route, a.queue))
    LOGS.mkdir(exist_ok=True)
    with (LOGS / ".lit_fetch_oa.lock").open("a+") as owner:
        try:
            fcntl.flock(owner, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print("another lit_fetch_oa.py run holds logs/.lit_fetch_oa.lock; not starting", file=sys.stderr)
            return 4
        with RunLog("lit_fetch_oa", a.dry_run) as log:
            counts: dict[str, int] = defaultdict(int)
            attempts = 0
            log.info(f"{len(jobs)} jobs ({', '.join(f'{r}={sum(j.route == r for j in jobs)}' for r in ROUTES)})")
            for job in jobs:
                if valid_cached(REFS / job.paper_id / "source.pdf"):
                    counts["cached"] += 1
                    log.event("fetch", "skip_cached", paper_id=job.paper_id)
                    continue
                if a.max and attempts >= a.max:
                    counts["deferred_max"] += 1
                    continue
                if a.dry_run:
                    hb = breaker_remaining(host_of(job.url)) if job.url else 0.0
                    log.info(
                        f"would fetch {job.paper_id} [{job.route}] {job.url}" + (f" (breaker {hb:.0f} s)" if hb else "")
                    )
                    counts["would_fetch"] += 1
                    attempts += 1
                    continue
                if job.route == "arxiv" and breaker_remaining("arxiv.org") > 0:
                    log.info("arxiv.org breaker active: stopping the run")
                    counts["stopped"] += 1
                    break
                attempts += 1
                st = fetch_one(job, log, not a.no_license)
                counts[st] += 1
                log.event("fetch", st, paper_id=job.paper_id, route=job.route, url=job.url)
            log.info(f"summary {dict(counts)}; status log {STATUS_LOG.relative_to(ROOT)}")
            log.event("summary", "ok", **counts)
    if counts.get("stopped"):
        return 4
    return 3 if any(counts.get(k) for k in ("blocked", "not_pdf", "error")) else 0


if __name__ == "__main__":
    sys.exit(main())
