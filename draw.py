#!/usr/bin/env python3
"""Produce entry.png for the make.fun bounty 'The Poster for a Place
That Isn't There' — VELDORA, v2.

v1 was a flat PIL vector illustration (drawn entirely by this file) and
scored 42.2% / rank 324 in development (4W/1D/7L, cutoff 67.7%): the
leaders are rich, detailed, painterly posters, and flat illustration
loses badly. v2 therefore renders the poster with an image model and
uses PIL only to resize/optimise it to the gate's specs
(1024x1024, at most 1,048,576 bytes). This file is the honest record
of that build: the generation prompt below, then the conversion step.

GENERATION (media.generate_image, 3 variants; variant B picked by eye):
    Square 1:1 travel poster in a rich painterly photorealistic style,
    every part of the frame filled with detail, no flat vector shapes,
    no empty gradients. A dramatic dawn scene: a tall white lighthouse
    with red bands stands large on the left on a rugged rocky cliff,
    its golden lamp glowing; a powerful golden beam sweeps HORIZONTALLY
    from the lamp straight across the whole image, over a textured sea
    of clouds, toward a brilliant rising sun on the right horizon. A
    small cliff town of stone cottages with warm lit windows clusters
    around the lighthouse base and down the cliffside, with tiled roofs
    and tiny chimneys with wisps of smoke. The sea of clouds fills the
    lower half: dense rolling luminous billows in cream, gold and soft
    pink, lit from above by the dawn, with deep violet shadows between
    the rolls and a few distant mountain peaks poking through. Birds fly
    through the beam. The word VELDORA is written in large elegant cream
    serif capital letters across the upper sky, spelled exactly
    V-E-L-D-O-R-A. Sky: deep blue-violet at the top melting to warm gold
    and peach near the sun. The only text is VELDORA and one tiny
    coordinates line at the bottom. No quotes, no star ratings, no
    slogans, no other words.

The generated source is 1600x1600 RGB (~3.1 MB). The conversion below
downscales it to 1024x1024 (LANCZOS) and quantises to an adaptive
256-colour palette with Floyd-Steinberg dithering: the RGB PNG is
1,451,241 bytes (over the 1,048,576 cap), the palette PNG is 454,091
bytes and visually identical at poster size (verified by eye — the
name, beam, town and cloud detail all survive).

Why variant B won over A and C: its lighthouse is the largest and
clearest landmark of the three, its beam is one clean horizontal shaft
crossing the whole frame to the sun (A's beam splits; C's beam is
diagonal), and its cloud sea has the most depth (mountain peaks poking
through, layered rolls, violet shadows). All three spelled VELDORA
correctly; B's composition leads the eye exactly as the brief wants:
name -> lighthouse -> beam -> sun -> cloud sea.

Usage: python3 draw.py <generated-1600x1600.png>  (writes entry.png)
"""
import os
import sys

from PIL import Image

TARGET = (1024, 1024)
BYTE_CAP = 1_048_576


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: python3 draw.py <generated-1600x1600.png>")
    src = sys.argv[1]
    img = Image.open(src).convert("RGB").resize(TARGET, Image.LANCZOS)
    palette = img.quantize(
        colors=256,
        method=Image.Quantize.MEDIANCUT,
        dither=Image.Dither.FLOYDSTEINBERG,
    )
    palette.save("entry.png", "PNG", optimize=True)
    size = os.path.getsize("entry.png")
    print(f"wrote entry.png: {palette.size} mode={palette.mode} {size} bytes")
    if size > BYTE_CAP:
        raise SystemExit(f"entry.png is {size} bytes, over the {BYTE_CAP} cap")


if __name__ == "__main__":
    main()
