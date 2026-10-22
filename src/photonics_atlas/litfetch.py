"""Shared polite HTTP client for literature scouting (DevLog-006): OpenAlex, Crossref, arXiv, Semantic Scholar.

Every caller (any number of scripts / subagents at once) goes through `get`, which:
  - serializes requests per host with an exclusive file lock (logs/.lit_<host>.lock) and enforces the host's minimum
    interval plus jitter, so parallel callers never exceed the host's rate;
  - arms a per-host breaker (logs/.lit_blocked_<host>.json, cooldown) on HTTP 403/429/503 or a network error; while it
    is active every caller gets BlockedError without sending a request;
  - tracks the OpenAlex cost reported in X-RateLimit-Cost-USD per UTC day (logs/.lit_openalex_cost_<date>.json) and
    refuses requests once the cap (env OPENALEX_DAILY_CAP_USD, default 0.08) is reached;
  - sends a generic User-Agent and never any personal identifier (no mailto, no email). OPENALEX_API_KEY is used when
    the environment provides it and is never logged.
  - logs every request to logs/litfetch_<date>.jsonl (url without api_key, status, cost, bytes).
"""

from __future__ import annotations

import datetime as dt
import fcntl
import http.client
import json
import os
import random
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from .paths import LOGS

UA = "photonics-atlas-literature-scout/0.1"
MIN_INTERVAL_S = {
    "api.openalex.org": 1.0,
    "api.crossref.org": 1.0,
    "export.arxiv.org": 3.5,
    "api.semanticscholar.org": 3.0,
}
DEFAULT_INTERVAL_S = 5.0
JITTER_S = 0.5
COOLDOWN_S = float(os.environ.get("LITFETCH_COOLDOWN_S", "1800"))
OPENALEX_CAP_USD = float(os.environ.get("OPENALEX_DAILY_CAP_USD", "0.08"))
TIMEOUT_S = 60


class BlockedError(RuntimeError):
    """Host breaker active or OpenAlex daily cap reached; do not retry until the cooldown / next UTC day."""


def _today() -> str:
    return dt.datetime.now(dt.UTC).date().isoformat()


def _now() -> str:
    return dt.datetime.now(dt.UTC).isoformat(timespec="seconds")


def _log(entry: dict[str, Any]) -> None:
    LOGS.mkdir(exist_ok=True)
    with (LOGS / f"litfetch_{_today()}.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps({"ts": _now(), **entry}) + "\n")


def _breaker(host: str) -> Path:
    return LOGS / f".lit_blocked_{host}.json"


def _cost_file() -> Path:
    return LOGS / f".lit_openalex_cost_{_today()}.json"


def openalex_cost_today() -> float:
    p = _cost_file()
    return float(json.loads(p.read_text())["usd"]) if p.exists() else 0.0


def _check_breaker(host: str) -> None:
    p = _breaker(host)
    if p.exists():
        info = json.loads(p.read_text())
        if time.time() < float(info["until"]):
            raise BlockedError(f"{host} blocked until {info['until_iso']} ({info['reason']})")
        p.unlink()


def _arm_breaker(host: str, reason: str) -> None:
    until = time.time() + COOLDOWN_S
    until_iso = dt.datetime.fromtimestamp(until, dt.UTC).isoformat(timespec="seconds")
    _breaker(host).write_text(json.dumps({"until": until, "until_iso": until_iso, "reason": reason}))
    _log({"host": host, "event": "breaker_armed", "reason": reason, "until": until_iso})


def _public_url(url: str) -> str:
    parts = urllib.parse.urlsplit(url)
    q = [(k, v) for k, v in urllib.parse.parse_qsl(parts.query) if k != "api_key"]
    return urllib.parse.urlunsplit(parts._replace(query=urllib.parse.urlencode(q)))


def get(url: str, params: dict[str, Any] | None = None) -> bytes:
    """GET with per-host serialization, breaker and OpenAlex cost cap. Raises BlockedError or urllib errors."""
    params = dict(params or {})
    host = urllib.parse.urlsplit(url).netloc
    if host == "api.openalex.org" and os.environ.get("OPENALEX_API_KEY"):
        params["api_key"] = os.environ["OPENALEX_API_KEY"]
    full = url + ("?" + urllib.parse.urlencode(params) if params else "")
    LOGS.mkdir(exist_ok=True)
    interval = MIN_INTERVAL_S.get(host, DEFAULT_INTERVAL_S)
    with (LOGS / f".lit_{host}.lock").open("a+") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        _check_breaker(host)
        if host == "api.openalex.org" and openalex_cost_today() >= OPENALEX_CAP_USD:
            raise BlockedError(f"OpenAlex daily cap {OPENALEX_CAP_USD} USD reached for {_today()} (UTC)")
        stamp = LOGS / f".lit_{host}.last"
        last = float(stamp.read_text()) if stamp.exists() else 0.0
        wait = last + interval + random.uniform(0, JITTER_S) - time.time()
        if wait > 0:
            time.sleep(wait)
        req = urllib.request.Request(full, headers={"User-Agent": UA, "Accept": "application/json"})
        status, body, cost = 0, b"", 0.0
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
                status = resp.status
                body = bytes(resp.read())
                cost = float(resp.headers.get("X-RateLimit-Cost-USD") or 0.0)
        except urllib.error.HTTPError as e:
            status = e.code
            if e.code in (403, 429, 503):
                _arm_breaker(host, f"HTTP {e.code}")
            raise
        except (urllib.error.URLError, TimeoutError) as e:
            _arm_breaker(host, f"network error: {e}")
            raise
        finally:
            stamp.write_text(str(time.time()))
            if cost:
                _cost_file().write_text(json.dumps({"usd": round(openalex_cost_today() + cost, 6)}))
            _log({"host": host, "url": _public_url(full), "status": status, "cost_usd": cost, "bytes": len(body)})
    return body


def get_json(url: str, params: dict[str, Any] | None = None, attempts: int = 4) -> Any:
    """`get` + JSON parse; a truncated body (incomplete read or invalid JSON, seen on OpenAlex 2026-10-22 00:01Z) is
    retried with a growing pause (each retry is a normal rate-limited request), then re-raised."""
    for i in range(1, attempts + 1):
        try:
            return json.loads(get(url, params))
        except (json.JSONDecodeError, http.client.IncompleteRead) as e:
            _log(
                {
                    "host": urllib.parse.urlsplit(url).netloc,
                    "event": "truncated_body",
                    "attempt": i,
                    "error": str(e)[:200],
                }
            )
            if i == attempts:
                raise
            time.sleep(15 * i)
    raise AssertionError("unreachable")
