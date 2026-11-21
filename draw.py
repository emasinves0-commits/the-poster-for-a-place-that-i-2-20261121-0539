#!/usr/bin/env python3
"""Draw the Veldora travel poster (1024x1024) for the make.fun bounty
'The Poster for a Place That Isn't There'.

Veldora: a cliff town above a sea of clouds at dawn. One landmark — a
lighthouse that beams sideways across the cloud sea. The promise of the
stay: wake up above the weather, in the first light.

Pure PIL (no numpy): gradients are drawn row by row, glow is layered
blur. Deterministic (seeded random) so re-runs are byte-identical.
"""
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W = H = 1024
random.seed(11)

SERIF_BLACK = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Black.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

# Palette: indigo dawn sky, violet, peach-gold light, cream, coral accent.
SKY_STOPS = [
    (0, (18, 26, 48)),
    (200, (38, 53, 92)),
    (380, (84, 70, 127)),
    (520, (143, 95, 126)),
    (620, (217, 138, 107)),
    (700, (247, 178, 103)),
    (1024, (242, 166, 90)),
]
CREAM = (255, 243, 220)
GOLD = (247, 200, 115)
CORAL = (192, 57, 43)
CLIFF = (35, 42, 66)
CLIFF_DARK = (27, 33, 54)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def sky_color(y):
    for (y0, c0), (y1, c1) in zip(SKY_STOPS, SKY_STOPS[1:]):
        if y0 <= y <= y1:
            return lerp(c0, c1, (y - y0) / max(1, y1 - y0))
    return SKY_STOPS[-1][1]


def letterspaced_size(draw, text, font, spacing):
    w = sum(draw.textlength(ch, font=font) for ch in text) + spacing * (len(text) - 1)
    bbox = draw.textbbox((0, 0), text, font=font)
    return w, bbox[3] - bbox[1]


def draw_letterspaced(draw, cx, y, text, font, fill, spacing):
    w, _ = letterspaced_size(draw, text, font, spacing)
    x = cx - w / 2
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + spacing


def main():
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)

    # --- Sky gradient (row by row) ---
    for y in range(H):
        d.line([(0, y), (W, y)], fill=sky_color(y))

    # --- Faint dawn stars in the upper sky ---
    stars = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ds = ImageDraw.Draw(stars)
    for _ in range(70):
        x = random.uniform(0, W)
        y = random.uniform(0, 330)
        r = random.uniform(0.6, 1.8)
        a = int(random.uniform(40, 130) * (1 - y / 420))
        if a > 0:
            ds.ellipse([x - r, y - r, x + r, y + r], fill=(255, 244, 220, a))
    img = Image.alpha_composite(img.convert("RGBA"), stars)
    d = ImageDraw.Draw(img)

    # --- Sun: halo then disc, low over the cloud sea ---
    halo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dh = ImageDraw.Draw(halo)
    dh.ellipse([660 - 300, 600 - 300, 660 + 300, 600 + 300], fill=(255, 205, 120, 130))
    halo = halo.filter(ImageFilter.GaussianBlur(70))
    img = Image.alpha_composite(img, halo)
    d = ImageDraw.Draw(img)
    d.ellipse([660 - 105, 600 - 105, 660 + 105, 600 + 105], fill=(255, 233, 184, 255))

    # --- Lighthouse beam (drawn before the cliff so the tower overlaps its root) ---
    beam = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    db = ImageDraw.Draw(beam)
    db.polygon([(270, 326), (1024, 270), (1024, 410), (270, 350)], fill=(255, 198, 96, 70))
    db.polygon([(270, 333), (1024, 312), (1024, 366), (270, 343)], fill=(255, 222, 140, 150))
    beam = beam.filter(ImageFilter.GaussianBlur(9))
    img = Image.alpha_composite(img, beam)
    d = ImageDraw.Draw(img)

    # --- Cliff silhouette, left side, rising out of the cloud sea ---
    d.polygon(
        [(0, 1024), (0, 580), (60, 555), (110, 515), (150, 530), (210, 478),
         (260, 482), (300, 520), (330, 600), (350, 690), (340, 1024)],
        fill=CLIFF + (255,),
    )
    # A lighter facet along the cliff's sun-facing edge.
    d.polygon(
        [(300, 520), (330, 600), (350, 690), (340, 1024), (300, 1024), (310, 690)],
        fill=(46, 56, 82, 255),
    )

    # --- The town: tiny houses along the cliff top, a few windows lit ---
    houses = [(28, 505, 34, 26), (70, 493, 30, 24), (106, 499, 36, 28),
              (150, 478, 32, 26), (188, 486, 30, 24), (222, 474, 26, 22)]
    for x, y, w, h in houses:
        d.rectangle([x, y, x + w, y + h], fill=CLIFF_DARK + (255,))
        d.polygon([(x - 3, y), (x + w + 3, y), (x + w / 2, y - 12)],
                  fill=(20, 26, 44, 255))
        for wx in (x + 6, x + w - 12):
            if random.random() < 0.7:
                d.rectangle([wx, y + 8, wx + 6, y + 15], fill=(255, 217, 138, 255))

    # --- The lighthouse: ONE landmark, white with coral bands ---
    d.polygon([(245, 520), (285, 520), (275, 360), (255, 360)], fill=CREAM + (255,))
    d.polygon([(250, 445), (280, 445), (278, 410), (252, 410)], fill=CORAL + (255,))
    d.polygon([(247, 502), (283, 502), (281, 472), (249, 472)], fill=CORAL + (255,))
    d.rectangle([248, 348, 282, 360], fill=CLIFF_DARK + (255,))  # gallery
    d.rectangle([256, 324, 274, 348], fill=(60, 48, 40, 255))    # lamp room
    d.pieslice([250, 306, 280, 330], start=180, end=360, fill=CLIFF_DARK + (255,))
    d.line([(265, 306), (265, 298)], fill=CLIFF_DARK + (255,), width=3)
    d.ellipse([263, 294, 267, 298], fill=GOLD + (255,))           # finial
    # Lamp glow.
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dg = ImageDraw.Draw(glow)
    dg.ellipse([265 - 42, 336 - 42, 265 + 42, 336 + 42], fill=(255, 230, 170, 150))
    glow = glow.filter(ImageFilter.GaussianBlur(18))
    img = Image.alpha_composite(img, glow)
    d = ImageDraw.Draw(img)
    d.ellipse([265 - 7, 336 - 7, 265 + 7, 336 + 7], fill=(255, 244, 210, 255))

    # --- Birds: a few dark chevrons for scale, clear of the title rule ---
    for bx, by, s in [(700, 320, 16), (780, 290, 12), (860, 350, 14),
                      (920, 300, 10), (640, 390, 11)]:
        d.line([(bx - s, by + s // 3), (bx, by), (bx + s, by + s // 3)],
               fill=(30, 36, 56, 255), width=3)

    # --- Cloud sea: one soft mass, not stacked stripes. ---
    # v2's four scalloped bands read as a stack of pink dumplings (dark
    # seams where each blurred band edge met the next). Instead: fill the
    # lower third with lit cream, roll its top edge with large soft
    # puffs, then suggest depth with a few very soft shadow masses.
    sea = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dsea = ImageDraw.Draw(sea)
    dsea.rectangle([0, 680, W, H], fill=(251, 231, 198, 255))
    x = -60
    while x < W + 60:
        r = random.uniform(80, 130)
        cy = 660 + random.uniform(-18, 18)
        dsea.ellipse([x - r, cy - r * 0.55, x + r, cy + r * 0.55],
                     fill=(251, 231, 198, 255))
        x += r * random.uniform(1.2, 1.6)
    sea = sea.filter(ImageFilter.GaussianBlur(5))
    img = Image.alpha_composite(img, sea)
    # Soft shadow masses for depth (heavily blurred, low contrast).
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dsh2 = ImageDraw.Draw(shade)
    for (sx, sy, sr, col, a) in [
        (180, 800, 260, (239, 201, 160), 110),
        (620, 760, 300, (244, 208, 170), 100),
        (900, 830, 260, (238, 196, 158), 110),
        (300, 950, 320, (216, 160, 160), 110),
        (800, 970, 340, (210, 154, 156), 120),
        (520, 880, 260, (228, 178, 152), 90),
    ]:
        dsh2.ellipse([sx - sr, sy - sr * 0.45, sx + sr, sy + sr * 0.45],
                     fill=col + (a,))
    shade = shade.filter(ImageFilter.GaussianBlur(45))
    img = Image.alpha_composite(img, shade)
    # Bright highlights catching the dawn on the nearest puffs.
    hi = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dhi = ImageDraw.Draw(hi)
    for (hx, hy, hr) in [(240, 700, 150), (700, 690, 170), (950, 720, 130)]:
        dhi.ellipse([hx - hr, hy - hr * 0.4, hx + hr, hy + hr * 0.4],
                    fill=(255, 246, 226, 90))
    hi = hi.filter(ImageFilter.GaussianBlur(25))
    img = Image.alpha_composite(img, hi)
    d = ImageDraw.Draw(img)

    # --- Title: VELDORA, large, cream, set into the dawn sky ---
    title_font = ImageFont.truetype(SERIF_BLACK, 118)
    tw, th = letterspaced_size(d, "VELDORA", title_font, 14)
    # Soft dark shadow so the letters hold against the sky.
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dsh = ImageDraw.Draw(shadow)
    draw_letterspaced(dsh, W / 2, 108, "VELDORA", title_font, (18, 26, 48, 160), 14)
    shadow = shadow.filter(ImageFilter.GaussianBlur(4))
    img = Image.alpha_composite(img, shadow)
    d = ImageDraw.Draw(img)
    draw_letterspaced(d, W / 2, 104, "VELDORA", title_font, CREAM + (255,), 14)
    # Thin gold rule under the title with a small diamond at its centre.
    d.line([(W / 2 - 220, 262), (W / 2 + 220, 262)], fill=GOLD + (220,), width=2)
    d.polygon([(W / 2, 254), (W / 2 + 8, 262), (W / 2, 270), (W / 2 - 8, 262)],
              fill=GOLD + (255,))

    # --- One tiny atmospheric line: coordinates, bottom centre ---
    small_font = ImageFont.truetype(SANS, 24)
    draw_letterspaced(d, W / 2, 978, "47°12' N  —  09°44' W", small_font,
                      (255, 243, 220, 210), 6)

    # --- Thin inner frame, quiet poster craft ---
    d.rectangle([18, 18, W - 18, H - 18], outline=(255, 243, 220, 110), width=3)

    img.convert("RGB").save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
