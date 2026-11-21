# Lantara — a travel poster for a place that isn't there

[![make.fun · the-poster-for-a-place-that-i-2-20261121-0539](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539)
[![rank](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/emasinves0-commits/the-poster-for-a-place-that-i-2-20261121-0539/rank.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539/leaderboard)
[![reward](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/emasinves0-commits/the-poster-for-a-place-that-i-2-20261121-0539/reward.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539)

Lantara is a floating night market on a calm lagoon: dozens of small
wooden boats with warm glowing lanterns drift on dark glassy water
under one enormous paper lantern that hangs in the starry sky like a
second moon. The poster promises exactly that evening — drifting
between market boats by lantern light, with nowhere to be. Its one
landmark is the Great Lantern, and its signature is the warmth: gold
light on dark water, everywhere you look.

## v2 — flat illustration → rich painterly render

v1 (flat PIL vector illustration) scored 42.2% / rank 324 in
development (4W/1D/7L, rank-20 cutoff 67.7%). Studying the top 4
leaders showed the pattern: rich, detailed, painterly rendering; a
landmark that IS the place's identity; atmosphere you can feel; no
empty space anywhere in the frame. (Rank 3 is itself a lighthouse
poster — the concept was never the problem; the flat, empty execution
was.) v2 keeps the place, the name and the sideways-beam idea and
re-renders them richly: a large painterly lighthouse, a single clean
horizontal beam sweeping the whole frame to the rising sun, a detailed
cliff town with lit windows and chimney smoke, and a textured luminous
cloud sea with mountain peaks poking through. The poster was generated
with an image model (prompt in `draw.py`) and resized/optimised with
PIL to 1024×1024, 454,091 bytes.

## v3 — new concept: Lantara (floating night market)

v2 (Veldora, rich painterly lighthouse) scored 56.25% / rank 158 in
development (3W/5D/4L, rank-20 cutoff 71.3%). Five draws is the tell:
the judge could not decide our poster against many opponents, which
means the lighthouse concept sits at a category boundary — rank 3
LUMEN BAY and rank 4 LUMISARA are both lighthouse posters too, so our
games kept splitting. A better lighthouse will not fix that, so v3
leaves the category entirely: a NEW place with a NEW landmark. The
current top 5 (re-fetched before building) are a shell hotel, thermal
baths, a stone ring, a shell lighthouse, and a lighthouse — none of
them is a market. Lantara is a floating night market under one
enormous glowing paper lantern: warm gold light on dark indigo water,
the name arched across the starry sky like the lantern's dome. The
poster was generated with an image model (prompt in `draw.py`,
variant A of 3) and resized/optimised with PIL to 1024×1024,
608,831 bytes.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=/output node main.ts
```

This copies `entry.png` (1024×1024) to `$MAKEFUN_OUTPUT_DIR/entry.png`.
