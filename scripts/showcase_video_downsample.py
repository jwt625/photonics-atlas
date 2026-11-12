# /// script
# requires-python = ">=3.11"
# dependencies = ["pillow>=10"]
# ///
"""Supersampling helper for app/scripts/showcase-video.mjs (DevLog-018 D1132).

Reads tab-separated jobs from stdin, in order:
  <src>\t<dst>\t<factor>   box-filter <src> (a 2x device-pixel screenshot) down by the integer <factor>, write <dst>
                           as JPEG q92, delete <src>
  =\t<prev dst>\t<dst>     <dst> is a copy of an already written frame (held frames)
Prints "done <n>" on EOF. Keeps no large files on disk: the low disk on the capture machine is the reason it exists.
"""

import shutil
import sys
from pathlib import Path

from PIL import Image


def main() -> int:
    n = 0
    for line in sys.stdin:
        a, b, c = line.rstrip("\n").split("\t")
        if a == "=":
            shutil.copyfile(b, c)
        else:
            k = int(c)
            with Image.open(a) as im:
                im = im.convert("RGB")
                (im.reduce(k) if k > 1 else im).save(b, quality=92)
            Path(a).unlink()
        n += 1
    print(f"done {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
