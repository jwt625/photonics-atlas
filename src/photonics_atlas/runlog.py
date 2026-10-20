"""Timestamped log file + JSONL progress for every script run (DevLog-001 script conventions)."""

from __future__ import annotations

import datetime as dt
import json
import sys
from pathlib import Path
from types import TracebackType
from typing import Any, TextIO

from .paths import LOGS


class RunLog:
    def __init__(self, script: str, dry_run: bool = False, log_dir: Path = LOGS) -> None:
        ts = dt.datetime.now().strftime("%Y%m%dT%H%M%S")
        log_dir.mkdir(parents=True, exist_ok=True)
        self.dry_run = dry_run
        self.log_path = log_dir / f"{script}_{ts}.log"
        self.jsonl_path = log_dir / f"{script}_{ts}.jsonl"
        self._log: TextIO = self.log_path.open("w", encoding="utf-8")
        self._jsonl: TextIO = self.jsonl_path.open("w", encoding="utf-8")
        self.info(f"start {script} dry_run={dry_run}")

    def info(self, msg: str) -> None:
        line = f"{dt.datetime.now().isoformat(timespec='seconds')} {msg}"
        print(line, file=sys.stderr)
        self._log.write(line + "\n")
        self._log.flush()

    def event(self, step: str, status: str = "ok", **data: Any) -> None:
        rec = {"ts": dt.datetime.now().isoformat(timespec="seconds"), "step": step, "status": status, **data}
        self._jsonl.write(json.dumps(rec, ensure_ascii=False, default=str) + "\n")
        self._jsonl.flush()

    def __enter__(self) -> RunLog:
        return self

    def __exit__(self, et: type[BaseException] | None, ev: BaseException | None, tb: TracebackType | None) -> None:
        if ev is not None:
            self.info(f"error {et.__name__ if et else ''}: {ev}")
            self.event("run", "failed", error=str(ev))
        else:
            self.info("done")
            self.event("run", "done")
        self._log.close()
        self._jsonl.close()
