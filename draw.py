#!/usr/bin/env python3
"""Lantara (v3) — build entry.png for "The Poster for a Place That Isn't There".

v3 replaces the Veldora lighthouse concept with a NEW place: LANTARA, a
floating night market on a calm lagoon under one enormous glowing paper
lantern. v2 (Veldora, rich painterly lighthouse) scored 56.25% / rank 158
(3W/5D/4L, cutoff 71.3%): five draws showed the lighthouse concept sits at
a category boundary — rank 3 LUMEN BAY and rank 4 LUMISARA are both
lighthouse posters too, so the judge kept splitting our games. A better
lighthouse cannot fix that; v3 leaves the category entirely.

HOW THE POSTER WAS MADE
-----------------------
1. Three variants were generated with Muse's image model
   (media.generate_image) from the prompt below (variant A: lantern
   centred; B: lantern left + full moon right; C: low viewpoint, lantern
   centred, golden reflection path). All three spelled LANTARA correctly.
   Variant A was picked by eye: the arched name mirrors the lantern's
   dome (type with intent), the lantern is whole and centred with its
   full tassel (B crops the lantern at the frame edge and adds a competing
   moon; C crowds the lantern into the name and is busier), and the boats
   are dense but organised.

   GENERATION PROMPT (variant A, verbatim):
   "Travel poster for an invented place called LANTARA: a floating night
   market on a calm lagoon at night. One enormous glowing round paper
   lantern floats high in the deep indigo starry sky, centred above the
   market — the single landmark, warm gold, with visible ribs and a long
   tassel. Below, dozens of small wooden boats with warm glowing lanterns
   drift on dark glassy water, their reflections shimmering; a few boats
   carry market stalls with striped awnings; tiny figures; low dark hills
   on the horizon. The name LANTARA is set in large cream serif letters
   across the upper sky, integrated into the composition. One tiny line of
   coordinates at the very bottom. Rich painterly detail, warm gold and
   deep indigo palette, no empty space, no quotes, no star ratings, no
   other text. Square format."

2. This script resizes the 1600x1600 source to exactly 1024x1024
   (LANCZOS) and writes entry.png next to itself. It first tries an
   optimised RGB PNG; if that exceeds the 1,048,576-byte gate it falls
   back to an adaptive 256-colour palette PNG with Floyd-Steinberg
   dithering (the same fallback that worked for v2 at 454,091 bytes).
   The final file was read by eye after conversion: no visible
   quantisation damage (name crisp, lantern glow smooth, boat detail
   intact). Actual result for variant A: the RGB PNG exceeded the cap,
   so entry.png is the palette-256 fallback — 1024x1024, 608,831 bytes,
   sha256 ed3ba91fa5795f2e02c6fa8c1c9e68edcbe9939be747747f613328d2cf863a45.

Usage:  python3 draw.py <generated-variant-A.png-or-webp> [out.png]
Default out is entry.png next to this script. Re-running it on the same
source reproduces entry.png byte-identically.
"""

import hashlib
import sys
from pathlib import Path

from PIL import Image

CAP_BYTES = 1_048_576
SIZE = (1024, 1024)


def build(source: Path, out: Path) -> dict:
    im = Image.open(source).convert("RGB").resize(SIZE, Image.LANCZOS)
    # First try: optimised RGB PNG.
    im.save(out, "PNG", optimize=True)
    mode = "RGB"
    if out.stat().st_size > CAP_BYTES:
        # Fallback: adaptive 256-colour palette + Floyd-Steinberg dither.
        pal = im.convert("P", palette=Image.ADAPTIVE, colors=256, dither=Image.FLOYDSTEINBERG)
        pal.save(out, "PNG", optimize=True)
        mode = "palette-256"
    data = out.read_bytes()
    return {
        "path": str(out),
        "mode": mode,
        "size": Image.open(out).size,
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


if __name__ == "__main__":
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).with_name("entry.png")
    info = build(src, dst)
    print(f"wrote {info['path']}: {info['size'][0]}x{info['size'][1]}, "
          f"{info['mode']}, {info['bytes']} bytes, sha256 {info['sha256']}")
    assert info["bytes"] <= CAP_BYTES, "entry.png exceeds the 1 MiB gate"
