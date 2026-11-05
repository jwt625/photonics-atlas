"""Geometry library for curated component layouts (DevLog-013 D505-D508).

A cell script draws one component in micrometres (x right, y up), after its source figures and text have been read.
Numbers come from the metric table through `Cell.um` / `Cell.num`, so a corrected row corrects the drawing. Every shape
states its source: `row("m18")`, `stated("p.3 Sec. II")`, `fig("Fig. 1(a)", "200 um scale bar", "10 %")` or
`assumed("why")`. Assumed shapes are drawn dashed. Figure readings never enter the metric table (D506).
"""

from __future__ import annotations

import json
import math
from collections.abc import Iterable, Sequence
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
COMPONENTS_JSON = ROOT / "app" / "static" / "data" / "components.json"

Pt = tuple[float, float]
TO_UM = {"nm": 1e-3, "um": 1.0, "mm": 1e3, "cm": 1e4}
# app/src/lib/layout/layout.css has a colour per material; keep in step
MATERIALS = {
    "si", "sin", "sion", "ln", "lt", "sio2", "glass", "inp", "active", "gaas", "ge", "metal", "polymer", "bto", "other",
    "unknown", "air", "doped_p", "doped_n", "contact",
}  # fmt: skip


def row(*ids: str) -> list[str]:
    """Dimension taken from metric rows of this component, by short id (m18)."""
    return [f"row:{i}" for i in ids]


def stated(at: str, what: str = "") -> list[str]:
    """Dimension or topology stated in the paper's text or a labelled figure, not in the metric table."""
    return [f"text:{at}" + (f": {what}" if what else "")]


def fig(at: str, how: str = "", unc: str = "") -> list[str]:
    """Topology or dimension read off a source figure (how: scale bar, ratio to a stated dimension; unc: uncertainty)."""
    return [f"fig:{at}" + (f": {how}" if how else "") + (f" (+-{unc})" if unc else "")]


def assumed(why: str) -> list[str]:
    """Not in the source: a drafting assumption. Drawn dashed."""
    return [f"assumed:{why}"]


def rot(p: Pt, deg: float, about: Pt = (0.0, 0.0)) -> Pt:
    a = math.radians(deg)
    x, y = p[0] - about[0], p[1] - about[1]
    return (about[0] + x * math.cos(a) - y * math.sin(a), about[1] + x * math.sin(a) + y * math.cos(a))


def move(pts: Iterable[Pt], dx: float = 0.0, dy: float = 0.0) -> list[Pt]:
    return [(x + dx, y + dy) for x, y in pts]


def turn(pts: Iterable[Pt], deg: float, about: Pt = (0.0, 0.0)) -> list[Pt]:
    return [rot(p, deg, about) for p in pts]


def mirror_y(pts: Iterable[Pt]) -> list[Pt]:
    return [(x, -y) for x, y in pts]


def rect(x0: float, y0: float, x1: float, y1: float) -> list[Pt]:
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def _arc_steps(radius: float, sweep_rad: float, tol: float) -> int:
    step = 2 * math.sqrt(2 * tol / max(radius, 1e-9)) if radius > tol else 1.0
    return max(2, math.ceil(abs(sweep_rad) / step))


def arc(c: Pt, radius: float, a0_deg: float, a1_deg: float, tol: float = 0.01) -> list[Pt]:
    """Points on a circular arc from angle a0 to a1 (degrees)."""
    a0, a1 = math.radians(a0_deg), math.radians(a1_deg)
    n = _arc_steps(radius, a1 - a0, tol)
    return [(c[0] + radius * math.cos(a0 + (a1 - a0) * i / n), c[1] + radius * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]


def circle(c: Pt, radius: float, tol: float = 0.01) -> list[Pt]:
    return arc(c, radius, 0.0, 360.0, tol)[:-1]


def annular_sector(c: Pt, r_in: float, r_out: float, a0_deg: float, a1_deg: float, tol: float = 0.01) -> list[Pt]:
    return arc(c, r_out, a0_deg, a1_deg, tol) + arc(c, r_in, a1_deg, a0_deg, tol)


class Route:
    """A waveguide centreline with a width along it: straights, circular arcs, tapers, S-bends. Headings in degrees."""

    def __init__(self, start: Pt, heading: float, width: float, tol: float = 0.01) -> None:
        self.tol = tol
        self.heading = heading
        self.width = width
        self.length = 0.0
        self.pts: list[Pt] = [start]
        self.ws: list[float] = [width]
        self.heads: list[float] = [heading]

    @property
    def pos(self) -> Pt:
        return self.pts[-1]

    def _add(self, p: Pt, w: float, h: float) -> None:
        self.pts.append(p)
        self.ws.append(w)
        self.heads.append(h)

    def straight(self, length: float, w_end: float | None = None) -> Route:
        """Straight run, optionally a linear taper to w_end."""
        h = math.radians(self.heading)
        x, y = self.pos
        w1 = self.width if w_end is None else w_end
        self._add((x + length * math.cos(h), y + length * math.sin(h)), w1, self.heading)
        self.width = w1
        self.length += length
        return self

    def taper(self, length: float, w_end: float, power: float = 1.0, n: int = 24) -> Route:
        """Straight taper, width(s) = w0 + (w1 - w0) * (s / L) ** power; power 2 is parabolic from the start."""
        h = math.radians(self.heading)
        x, y = self.pos
        w0 = self.width
        for i in range(1, n + 1):
            s = length * i / n
            self._add((x + s * math.cos(h), y + s * math.sin(h)), w0 + (w_end - w0) * (i / n) ** power, self.heading)
        self.width = w_end
        self.length += length
        return self

    def arc(self, radius: float, sweep_deg: float, w_end: float | None = None) -> Route:
        """Circular arc, sweep > 0 turns left (counter-clockwise)."""
        side = 1.0 if sweep_deg >= 0 else -1.0
        h0 = math.radians(self.heading)
        x, y = self.pos
        cx, cy = x - side * radius * math.sin(h0), y + side * radius * math.cos(h0)
        sweep = math.radians(sweep_deg)
        n = _arc_steps(radius, sweep, self.tol)
        w0 = self.width
        w1 = w0 if w_end is None else w_end
        for i in range(1, n + 1):
            h = h0 + sweep * i / n
            self._add((cx + side * radius * math.sin(h), cy - side * radius * math.cos(h)), w0 + (w1 - w0) * i / n, math.degrees(h))
        self.heading += sweep_deg
        self.width = w1
        self.length += radius * abs(sweep)
        return self

    def sbend(self, dx: float, dy: float, n: int = 48) -> Route:
        """Cosine S-bend advancing dx along and dy across the current heading; the heading is unchanged at its end."""
        h = math.radians(self.heading)
        x0, y0 = self.pos
        prev = (0.0, 0.0)
        for i in range(1, n + 1):
            u = dx * i / n
            v = dy * (1 - math.cos(math.pi * i / n)) / 2
            dv = dy * math.pi / (2 * dx) * math.sin(math.pi * i / n)
            p = (x0 + u * math.cos(h) - v * math.sin(h), y0 + u * math.sin(h) + v * math.cos(h))
            self.length += math.hypot(u - prev[0], v - prev[1])
            prev = (u, v)
            self._add(p, self.width, self.heading + math.degrees(math.atan(dv)))
        return self

    def to(self, target: Pt, w_end: float | None = None) -> Route:
        """Straight run to a point on the current heading (raises if the point is off the heading by more than 1 nm)."""
        x, y = self.pos
        h = math.radians(self.heading)
        along = (target[0] - x) * math.cos(h) + (target[1] - y) * math.sin(h)
        across = -(target[0] - x) * math.sin(h) + (target[1] - y) * math.cos(h)
        if abs(across) > 1e-3 or along < -1e-3:
            raise ValueError(f"target {target} is not ahead on heading {self.heading} from {self.pos}: along {along}, across {across}")
        return self.straight(max(along, 0.0), w_end)

    def polygon(self) -> list[Pt]:
        left: list[Pt] = []
        right: list[Pt] = []
        for p, w, hd in zip(self.pts, self.ws, self.heads, strict=True):
            h = math.radians(hd)
            nx, ny = -math.sin(h), math.cos(h)
            left.append((p[0] + nx * w / 2, p[1] + ny * w / 2))
            right.append((p[0] - nx * w / 2, p[1] - ny * w / 2))
        return left + right[::-1]


def _clean(x: float) -> float:
    return round(x, 4)


class View:
    def __init__(self, cell: Cell, vid: str, title: str, kind: str, like: str | None, window: Sequence[float] | None) -> None:
        self.cell, self.id, self.title, self.kind, self.like = cell, vid, title, kind, like
        self.window = list(window) if window else None
        self.shapes: list[dict[str, Any]] = []
        self.marks: list[dict[str, Any]] = []
        self.labels: list[dict[str, Any]] = []
        self.notes: list[str] = []

    def poly(self, pts: Iterable[Pt], mat: str, role: str, src: list[str], *, layer: str = "", alpha: float | None = None, lod: float | None = None) -> None:
        self.rings([list(pts)], mat, role, src, layer=layer, alpha=alpha, lod=lod)

    def rings(self, rings: list[list[Pt]], mat: str, role: str, src: list[str], *, layer: str = "", alpha: float | None = None, lod: float | None = None) -> None:
        """A shape of several rings, filled even-odd (an annulus is two rings). `lod`: feature size in um; the renderer
        hides the shape when that feature would be below about a pixel, so a dense grating does not alias."""
        if mat not in MATERIALS:
            raise ValueError(f"{self.cell.id}: unknown material {mat}")
        self.cell.check_src(src)
        s: dict[str, Any] = {"r": [[[_clean(x), _clean(y)] for x, y in r] for r in rings], "m": mat, "role": role, "src": src}
        if layer:
            s["layer"] = layer
        if alpha is not None:
            s["a"] = alpha
        if lod is not None:
            s["lod"] = lod
        self.shapes.append(s)

    def rect(self, x0: float, y0: float, x1: float, y1: float, mat: str, role: str, src: list[str], **kw: Any) -> None:
        self.poly(rect(x0, y0, x1, y1), mat, role, src, **kw)

    def route(self, r: Route, mat: str, role: str, src: list[str], **kw: Any) -> None:
        self.poly(r.polygon(), mat, role, src, **kw)

    def line(self, pts: Iterable[Pt], role: str, src: list[str], *, layer: str = "") -> None:
        """A thin reference line (facet, chip normal, fiber axis): not a physical layer."""
        self.cell.check_src(src)
        s: dict[str, Any] = {"r": [[[_clean(x), _clean(y)] for x, y in pts]], "m": "unknown", "role": role, "src": src, "line": True}
        if layer:
            s["layer"] = layer
        self.shapes.append(s)

    def dim(self, direction: str, a: float, b: float, pos: float, *, px: float = 12, ext: tuple[float, float] | None = None, row_id: str = "", text: str = "", src: list[str] | None = None, inset: bool = False) -> None:
        """A dimension line along x ('h') or y ('v') between a and b at perpendicular coordinate pos, offset px pixels.
        `row_id`: the label is that row's stored value (the app renders it, nothing is retyped). `text` + `src`: a figure
        reading or stated value outside the metric table, labelled as such."""
        if bool(row_id) == bool(text):
            raise ValueError(f"{self.cell.id}: a dim needs exactly one of row_id, text")
        if row_id:
            self.cell.metric(row_id)
        if text:
            if not src:
                raise ValueError(f"{self.cell.id}: dim '{text}' needs src")
            self.cell.check_src(src)
        self.marks.append({"dir": direction, "a": _clean(min(a, b)), "b": _clean(max(a, b)), "pos": _clean(pos), "px": px, "from": [_clean(ext[0]), _clean(ext[1])] if ext else [_clean(pos), _clean(pos)], "row": row_id, "text": text, "src": src or [], "inset": inset})

    def label(self, at: Pt, text: str, *, anchor: str = "middle", dx: float = 0, dy: float = 0, tip: str = "", row_id: str = "") -> None:
        """A text label. `row_id`: the row's stored value is appended by the app (a value with no axis-aligned extent)."""
        if row_id:
            self.cell.metric(row_id)
        self.labels.append({"at": [_clean(at[0]), _clean(at[1])], "text": text, "anchor": anchor, "dx": dx, "dy": dy, "tip": tip, "row": row_id})

    def note(self, text: str) -> None:
        self.notes.append(text)

    def out(self) -> dict[str, Any]:
        d: dict[str, Any] = {"id": self.id, "title": self.title, "kind": self.kind}
        if self.like:
            d["like"] = self.like
        if self.window:
            d["window"] = [_clean(x) for x in self.window]
        d.update({"shapes": self.shapes, "marks": self.marks, "labels": self.labels, "notes": self.notes})
        return d


_components: dict[str, dict[str, Any]] = {}


def _component(cid: str) -> dict[str, Any]:
    if not _components:
        _components.update({c["component_id"]: c for c in json.loads(COMPONENTS_JSON.read_text())["components"]})
    return _components[cid]


class Cell:
    """One curated component drawing. `sources`: figures and tables read. `summary`: what is drawn, one line."""

    def __init__(self, component_id: str, sources: list[str], summary: str) -> None:
        self.id = component_id
        self.sources = sources
        self.summary = summary
        self.comp = _component(component_id)
        self.rows: dict[str, dict[str, Any]] = {m["metric_id"].rsplit("-", 1)[-1]: m for m in self.comp["metrics"]}
        self.views: list[View] = []
        self.thumb: dict[str, Any] = {}
        self.checks: list[str] = []

    def metric(self, short: str) -> dict[str, Any]:
        if short not in self.rows:
            raise KeyError(f"{self.id}: no metric row {short}")
        return self.rows[short]

    def num(self, short: str) -> float:
        """Stored value of a row (a range: its midpoint)."""
        m = self.metric(short)
        v = float(m["value"])
        return (v + float(m["value_max"])) / 2 if m.get("value_max") else v

    def um(self, short: str) -> float:
        """A length row in micrometres."""
        m = self.metric(short)
        if m["unit"] not in TO_UM:
            raise ValueError(f"{self.id}: {short} has unit {m['unit']}, not a length")
        return self.num(short) * TO_UM[m["unit"]]

    def check_src(self, src: list[str]) -> None:
        if not src:
            raise ValueError(f"{self.id}: a shape without a source")
        for s in src:
            kind, _, val = s.partition(":")
            if kind not in ("row", "text", "fig", "assumed") or not val:
                raise ValueError(f"{self.id}: bad source {s!r}")
            if kind == "row":
                self.metric(val)

    def view(self, vid: str, title: str, kind: str = "top", *, like: str | None = None, window: Sequence[float] | None = None) -> View:
        v = View(self, vid, title, kind, like, window)
        self.views.append(v)
        return v

    def check(self, what: str, drawn: float, target: float, rel: float = 0.01) -> None:
        """Assert a drawn quantity against its source; the outcome is kept in the output as a verification record."""
        err = abs(drawn - target) / max(abs(target), 1e-12)
        if err > rel:
            raise AssertionError(f"{self.id}: {what}: drawn {drawn:.6g}, source {target:.6g}, {100 * err:.2f} % off (limit {100 * rel:.2f} %)")
        self.checks.append(f"{what}: drawn {drawn:.5g}, source {target:.5g}")

    def out(self) -> dict[str, Any]:
        return {"component_id": self.id, "sources": self.sources, "summary": self.summary, "thumb": self.thumb, "checks": self.checks, "views": [v.out() for v in self.views]}
