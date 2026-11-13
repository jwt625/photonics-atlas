# /// script
# requires-python = ">=3.11"
# dependencies = ["pillow>=10", "numpy>=1.26"]
# ///
"""History stories video compositor (DevLog-018).

Reads the per-story frame sequences written by app/scripts/showcase-video.mjs (one loop of N frames each, all in phase),
plays the hero story full frame for two loops, and zooms out from the hero tile to the 4x4 chronological grid between
--zoom-start (default 1/2 of the duration, D1130) and the last frame. The zoom is one scale about the fixed point of the
hero-tile-to-frame map, interpolated in log scale with a sine ease-in-out, so it ends exactly on the grid; the grid then
holds for --hold s with every tile still looping (default 8 s, D1134; tiles restart at 30 s and stop part way).

Usage (repo root):
  uv run scripts/showcase_video_grid.py [--src cache/showcase_video] [--hero macchesney1974] [--loops 2]
      [--zoom-start 0.5] [--gap 4] [--hold 8] [--out cache/showcase_video/history_stories_grid.mp4] [--frames a:b --png DIR]
"""

from __future__ import annotations

import argparse
import json
import math
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

W, H = 1920, 1080
BG = (0x38, 0x38, 0x35)  # gap colour = history tab rule colour #383835 (D997); tiles carry their own #0d0d0d


def ease(t: float) -> float:
    t = min(1.0, max(0.0, t))
    return 0.5 - 0.5 * math.cos(math.pi * t)  # sine ease-in-out: visible motion from the zoom start


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="cache/showcase_video")
    ap.add_argument("--hero", default="macchesney1974")
    ap.add_argument("--loops", type=int, default=2)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--zoom-start", type=float, default=0.5)
    ap.add_argument("--gap", type=float, default=4)
    ap.add_argument("--hold", type=float, default=8, help="s of the full grid after the zoom, all tiles playing (D1131, D1134)")
    ap.add_argument("--out", default=None)
    ap.add_argument("--frames", default=None, help="a:b subset (test); writes PNGs to --png instead of a video")
    ap.add_argument("--png", default=None)
    a = ap.parse_args()

    src = Path(a.src)
    ids = sorted(
        (p.name for p in (src / "frames").iterdir() if (p / "done.json").exists()),
        key=lambda i: (int(re.search(r"\d{4}", i).group()), i),
    )
    if len(ids) != 16 or a.hero not in ids:
        print(f"need 16 finished stories incl. {a.hero}, have {len(ids)}: {ids}", file=sys.stderr)
        return 2
    n_loop = {i: json.loads((src / "frames" / i / "done.json").read_text())["frames"] for i in ids}
    N = n_loop[a.hero]
    total = N * a.loops
    z0 = round(a.zoom_start * total)
    out_n = total + round(a.hold * a.fps)  # zoom ends at total - 1, then the grid holds

    # final grid: 16:9 tiles, gap between and around (vertical), centred horizontally
    g = a.gap
    th = (H - 5 * g) / 4
    tw = th * 16 / 9
    mx = (W - 4 * tw - 3 * g) / 2
    rects = {}
    for k, i in enumerate(ids):
        r, c = divmod(k, 4)
        rects[i] = (mx + c * (tw + g), g + r * (th + g), tw, th)
    hx, hy, _, _ = rects[a.hero]
    s0 = W / tw  # hero tile fills the frame
    fx, fy = s0 * hx / (s0 - 1), s0 * hy / (s0 - 1)  # fixed point of the zoom
    print(f"order {ids}\nhero at {ids.index(a.hero)} tile {tw:.1f}x{th:.1f} s0 {s0:.3f} frames {out_n} zoom {z0}-{total - 1} hold {total}-{out_n - 1}")

    cache: dict[tuple[str, int], Image.Image] = {}

    def frame_img(i: str, idx: int) -> Image.Image:
        key = (i, idx)
        if key not in cache:
            if len(cache) > 64:
                cache.clear()
            cache[key] = Image.open(src / "frames" / i / f"{idx:04d}.jpg").convert("RGB")
        return cache[key]

    def compose(f: int) -> Image.Image:
        idx = f % N
        if f < z0:
            return frame_img(a.hero, idx)
        t = min(1.0, (f - z0) / max(1, total - 1 - z0))
        s = math.exp(math.log(s0) * (1 - ease(t)))
        canvas = Image.new("RGB", (W, H), BG)
        for i in ids:
            x, y, w, h = rects[i]
            X0, Y0 = fx + s * (x - fx), fy + s * (y - fy)
            X1, Y1 = X0 + s * w, Y0 + s * h
            ix0, iy0 = max(0, math.floor(X0)), max(0, math.floor(Y0))
            ix1, iy1 = min(W, math.ceil(X1)), min(H, math.ceil(Y1))
            if ix1 <= ix0 or iy1 <= iy0:
                continue
            im = frame_img(i, (f % n_loop[i]))
            sw, sh = im.size
            box = (
                max(0.0, (ix0 - X0) / (X1 - X0) * sw),
                max(0.0, (iy0 - Y0) / (Y1 - Y0) * sh),
                min(float(sw), (ix1 - X0) / (X1 - X0) * sw),
                min(float(sh), (iy1 - Y0) / (Y1 - Y0) * sh),
            )
            canvas.paste(im.resize((ix1 - ix0, iy1 - iy0), Image.Resampling.LANCZOS, box=box, reducing_gap=2.0), (ix0, iy0))
        return canvas

    if a.frames:
        f0, f1 = (int(v) for v in a.frames.split(":"))
        out = Path(a.png or src / "check")
        out.mkdir(parents=True, exist_ok=True)
        for f in range(f0, min(f1, out_n)):
            compose(f).save(out / f"comp_{f:04d}.png")
        return 0

    out = Path(a.out or src / "history_stories_grid.mp4")
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(a.fps),
        "-i", "-", "-an", "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-r", str(a.fps),
        "-movflags", "+faststart", str(out),
    ]  # fmt: skip
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    assert p.stdin
    for f in range(out_n):
        p.stdin.write(np.asarray(compose(f), dtype=np.uint8).tobytes())
        if f % 100 == 0:
            print(f"frame {f}/{out_n}", flush=True)
    p.stdin.close()
    return p.wait()


if __name__ == "__main__":
    raise SystemExit(main())
