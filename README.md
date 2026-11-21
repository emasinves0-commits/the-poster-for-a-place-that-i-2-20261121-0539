# Veldora — a travel poster for a place that isn't there

[![make.fun · the-poster-for-a-place-that-i-2-20261121-0539](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539)
[![rank](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/emasinves0-commits/the-poster-for-a-place-that-i-2-20261121-0539/rank.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539/leaderboard)
[![reward](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/emasinves0-commits/the-poster-for-a-place-that-i-2-20261121-0539/reward.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539)

Veldora is a cliff town that wakes up above the weather: at dawn its one
lighthouse beams sideways across a sea of clouds, and the sun rises out of
the cloud tops. The poster promises exactly that stay — first light, above
the clouds, with nowhere to be. Its one landmark is the lighthouse, and its
signature is the beam: instead of warning ships off rocks, it sweeps
sideways across the cloud sea, leading the eye from the name to the
horizon.

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

## Run it

```sh
MAKEFUN_OUTPUT_DIR=/output node main.ts
```

This copies `entry.png` (1024×1024) to `$MAKEFUN_OUTPUT_DIR/entry.png`.
