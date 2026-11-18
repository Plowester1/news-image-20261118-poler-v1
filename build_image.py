#!/usr/bin/env python3
"""Build entry.png: a 1024x1024 infographic summing up Wednesday 18 November
2026's world news. Programmatic PIL composition so every headline is crisp
and legible (the vision judge reads the text).

Design: dark neon cyber — near-black page, cyan/magenta neon accents,
glowing hero card, grid of neon-bordered cards with drawn icon motifs.
All 8 headlines verified against the 18 Nov 2026 story pool."""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (5, 8, 16)            # near-black page
HEADER_BG = (8, 13, 28)
CARD = (10, 18, 34)        # card fill
CYAN = (0, 229, 255)
MAGENTA = (255, 0, 153)
GREEN = (0, 255, 170)
GOLD = (255, 200, 40)
ORANGE = (255, 110, 40)
VIOLET = (168, 96, 255)
BLUE = (64, 156, 255)
RED = (255, 70, 70)
HEAD = (245, 248, 255)     # headline white
SUB = (178, 196, 220)      # subhead light blue-grey
FOOT = (120, 140, 170)
GRID = (0, 229, 255)       # faint grid lines

SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"

# (tag, neon_color, headline, subhead, icon) — all verified 18 Nov 2026 stories.
STORIES = [
    ("TECH / NVIDIA", MAGENTA,
     "Nvidia board rejects Huang's return, record $115.8B quarter",
     "Board turns down Jensen Huang's return as CEO; record $115.8B quarter.",
     "chip"),
    ("TECH / OPENAI", CYAN,
     "OpenAI launches GPT-6.2 Astra and Sol, cuts prices",
     "New models Astra and Sol, lower API prices.",
     "spark"),
    ("CYBER", RED,
     "Cyberattack hits Zoom, CNN, HSBC, IKEA and more",
     "Major incident hits Zoom, CNN, HSBC, IKEA.",
     "lock"),
    ("DIPLOMACY", GOLD,
     "Xi greets Trump in Shenzhen as APEC opens",
     "Xi meets Trump at Air Force One in Shenzhen.",
     "circles"),
    ("MIDDLE EAST", ORANGE,
     "US strikes Iran's Qeshm Island as Iran hits back",
     "US jets hit a Guard site; Iran hits back.",
     "flame"),
    ("EUROPE", BLUE,
     "Ukraine hits Crimean Bridge for a second day",
     "Road span collapses into the strait.",
     "bridge"),
    ("US POLITICS", GREEN,
     "Peltola wins Alaska, Democrats take Senate 56-44",
     "Peltola beats Sullivan; Senate goes 56-44.",
     "ballot"),
    ("RUSSIA", VIOLET,
     "Russia plans 20 million drones for Ukraine next year",
     "Moscow plans to launch 20 million drones at Ukraine in 2027.",
     "drone"),
]


def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ---- drawn icon motifs (all pure PIL shapes, deterministic) ----
def draw_chip(d, cx, cy, s, color):
    """Microchip: square body + pins + inner die."""
    d.rectangle([cx - 0.62 * s, cy - 0.62 * s, cx + 0.62 * s, cy + 0.62 * s],
                fill=color)
    d.rectangle([cx - 0.34 * s, cy - 0.34 * s, cx + 0.34 * s, cy + 0.34 * s],
                fill=(5, 8, 16))
    d.rectangle([cx - 0.16 * s, cy - 0.16 * s, cx + 0.16 * s, cy + 0.16 * s],
                fill=color)
    for i in (-1, 0, 1):
        off = i * 0.36 * s
        d.line([cx + off, cy - s, cx + off, cy - 0.62 * s], fill=color, width=4)
        d.line([cx + off, cy + 0.62 * s, cx + off, cy + s], fill=color, width=4)
        d.line([cx - s, cy + off, cx - 0.62 * s, cy + off], fill=color, width=4)
        d.line([cx + 0.62 * s, cy + off, cx + s, cy + off], fill=color, width=4)


def draw_spark(d, cx, cy, s, color):
    """Four-point spark / star."""
    pts = [(cx, cy - s), (cx + 0.22 * s, cy - 0.22 * s), (cx + s, cy),
           (cx + 0.22 * s, cy + 0.22 * s), (cx, cy + s),
           (cx - 0.22 * s, cy + 0.22 * s), (cx - s, cy),
           (cx - 0.22 * s, cy - 0.22 * s)]
    d.polygon(pts, fill=color)
    d.ellipse([cx - 0.14 * s, cy - 0.14 * s, cx + 0.14 * s, cy + 0.14 * s],
              fill=(255, 255, 255))


def draw_lock(d, cx, cy, s, color):
    """Padlock: shackle arc + body + keyhole."""
    d.arc([cx - 0.5 * s, cy - 0.85 * s, cx + 0.5 * s, cy + 0.15 * s], 180, 360,
          fill=color, width=7)
    d.rounded_rectangle([cx - 0.62 * s, cy - 0.05 * s, cx + 0.62 * s, cy + 0.8 * s],
                        radius=8, fill=color)
    d.ellipse([cx - 0.13 * s, cy + 0.12 * s, cx + 0.13 * s, cy + 0.38 * s],
              fill=(5, 8, 16))
    d.rectangle([cx - 0.05 * s, cy + 0.34 * s, cx + 0.05 * s, cy + 0.62 * s],
                fill=(5, 8, 16))


def draw_circles(d, cx, cy, s, color):
    """Trilateral: three overlapping circles."""
    r = 0.52 * s
    cols = [(255, 200, 40), (0, 255, 170), (64, 156, 255)]
    offs = [(-0.45 * s, 0.30 * s), (0.45 * s, 0.30 * s), (0, -0.42 * s)]
    for (ox, oy), c in zip(offs, cols):
        d.ellipse([cx + ox - r, cy + oy - r, cx + ox + r, cy + oy + r],
                  fill=c, outline=(255, 255, 255), width=2)


def draw_flame(d, cx, cy, s, c1, c2=(250, 200, 80)):
    pts = [(cx, cy - s), (cx + 0.36 * s, cy - 0.44 * s), (cx + 0.64 * s, cy - 0.04 * s),
           (cx + 0.76 * s, cy + 0.44 * s), (cx + 0.56 * s, cy + 0.84 * s),
           (cx, cy + s), (cx - 0.56 * s, cy + 0.84 * s),
           (cx - 0.76 * s, cy + 0.44 * s), (cx - 0.64 * s, cy - 0.04 * s),
           (cx - 0.36 * s, cy - 0.44 * s)]
    d.polygon(pts, fill=c1)
    inner = [(cx, cy - 0.45 * s), (cx + 0.30 * s, cy - 0.10 * s),
             (cx + 0.42 * s, cy + 0.30 * s), (cx + 0.28 * s, cy + 0.62 * s),
             (cx, cy + 0.72 * s), (cx - 0.28 * s, cy + 0.62 * s),
             (cx - 0.42 * s, cy + 0.30 * s), (cx - 0.30 * s, cy - 0.10 * s)]
    d.polygon(inner, fill=c2)
    d.ellipse([cx - 0.16 * s, cy + 0.34 * s, cx + 0.16 * s, cy + 0.66 * s],
              fill=(255, 240, 180))


def draw_bridge(d, cx, cy, s, color):
    w = 4
    d.arc([cx - s, cy - 0.55 * s, cx + s, cy + 0.45 * s], 180, 360, fill=color, width=w)
    d.line([cx - s, cy + 0.55 * s, cx + s, cy + 0.55 * s], fill=color, width=w)
    for px in (-0.55, 0, 0.55):
        d.line([cx + px * s, cy - 0.10 * s, cx + px * s, cy + 0.55 * s], fill=color, width=3)


def draw_ballot(d, cx, cy, s, color):
    """Ballot box + check mark."""
    d.rounded_rectangle([cx - 0.7 * s, cy - 0.25 * s, cx + 0.7 * s, cy + 0.8 * s],
                        radius=8, fill=color)
    d.rectangle([cx - 0.4 * s, cy - 0.55 * s, cx + 0.4 * s, cy - 0.25 * s],
                fill=color)
    d.line([cx - 0.35 * s, cy + 0.28 * s, cx - 0.05 * s, cy + 0.55 * s],
           fill=(5, 8, 16), width=6)
    d.line([cx - 0.05 * s, cy + 0.55 * s, cx + 0.45 * s, cy - 0.05 * s],
           fill=(5, 8, 16), width=6)


def draw_drone(d, cx, cy, s, color):
    """Quadcopter: central body + 4 rotor discs + arms."""
    for ox, oy in ((-0.62, -0.62), (0.62, -0.62), (-0.62, 0.62), (0.62, 0.62)):
        d.line([cx, cy, cx + ox * s, cy + oy * s], fill=color, width=4)
        d.ellipse([cx + ox * s - 0.32 * s, cy + oy * s - 0.10 * s,
                   cx + ox * s + 0.32 * s, cy + oy * s + 0.10 * s], fill=color)
    d.ellipse([cx - 0.38 * s, cy - 0.28 * s, cx + 0.38 * s, cy + 0.28 * s],
              fill=color)
    d.ellipse([cx - 0.12 * s, cy - 0.10 * s, cx + 0.12 * s, cy + 0.10 * s],
              fill=(5, 8, 16))


ICONS = {"chip": draw_chip, "spark": draw_spark, "lock": draw_lock,
         "circles": draw_circles, "flame": draw_flame, "bridge": draw_bridge,
         "ballot": draw_ballot, "drone": draw_drone}


def tag_pill(d, x, y, tag, color, f_tag):
    tw = d.textlength(tag, font=f_tag) + 22
    d.rounded_rectangle([x, y, x + tw, y + 28], radius=14, fill=color)
    d.text((x + 11, y + 4), tag, font=f_tag, fill=(5, 8, 16))
    return tw


def neon_card(d, x0, y0, x1, y1, color):
    """Card fill + neon outline + bright accent bar on the left edge."""
    d.rounded_rectangle([x0, y0, x1, y1], radius=12, fill=CARD,
                        outline=color, width=2)
    d.rounded_rectangle([x0, y0, x0 + 8, y1], radius=4, fill=color)


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- faint cyber grid background ----
    for gx in range(0, W + 1, 64):
        d.line([gx, 136, gx, H], fill=(10, 22, 44), width=1)
    for gy in range(136, H + 1, 64):
        d.line([0, gy, W, gy], fill=(10, 22, 44), width=1)

    # ---- Header band ----
    d.rectangle([0, 0, W, 132], fill=HEADER_BG)
    f_mast = ImageFont.truetype(SERIF_B, 58)
    f_date = ImageFont.truetype(SANS_B, 23)
    mast = "THE WORLD IN ONE DAY"
    d.text(((W - d.textlength(mast, font=f_mast)) / 2, 22), mast, font=f_mast, fill=(255, 255, 255))
    date = "WEDNESDAY, 18 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=f_date)) / 2, 94), date, font=f_date, fill=CYAN)
    d.rectangle([36, 144, W - 36, 147], fill=CYAN)
    d.rectangle([36, 148, W - 36, 150], fill=MAGENTA)

    f_tag = ImageFont.truetype(SANS_B, 17)
    m = 36
    full_w = W - 2 * m  # 952

    # ---- Hero: NVIDIA, full width ----
    tag, color, head, sub, icon = STORIES[0]
    hx0, hy0, hh = m, 164, 196
    neon_card(d, hx0, hy0, hx0 + full_w, hy0 + hh, color)
    draw_chip(d, hx0 + full_w - 82, hy0 + hh // 2, 54, color)
    px, py = hx0 + 28, hy0 + 22
    tag_pill(d, px, py, tag, color, f_tag)
    py += 42
    f_hero = ImageFont.truetype(SANS_B, 35)
    f_hero_sub = ImageFont.truetype(SANS, 20)
    tw = full_w - 56 - 140  # leave room for the chip icon
    for line in wrap(d, head, f_hero, tw)[:2]:
        d.text((px, py), line, font=f_hero, fill=HEAD)
        py += 43
    py += 6
    for line in wrap(d, sub, f_hero_sub, tw)[:2]:
        d.text((px, py), line, font=f_hero_sub, fill=SUB)
        py += 27

    # ---- 2x3 grid: stories 1..6 ----
    cw = (full_w - 20) // 2  # 466
    ch = 156
    f_head = ImageFont.truetype(SANS_B, 24)
    f_sub = ImageFont.truetype(SANS, 17)
    for i in range(1, 7):
        tag, color, head, sub, icon = STORIES[i]
        col, row = (i - 1) % 2, (i - 1) // 2
        x0 = m + col * (cw + 20)
        y0 = 376 + row * (ch + 12)
        neon_card(d, x0, y0, x0 + cw, y0 + ch, color)
        ICONS[icon](d, x0 + cw - 42, y0 + 44, 28, color)
        px, py = x0 + 24, y0 + 14
        tag_pill(d, px, py, tag, color, f_tag)
        py += 40
        tw = cw - 48 - 62  # leave room for the icon
        for line in wrap(d, head, f_head, tw)[:2]:
            d.text((px, py), line, font=f_head, fill=HEAD)
            py += 30
        py += 4
        for line in wrap(d, sub, f_sub, tw)[:2]:
            d.text((px, py), line, font=f_sub, fill=SUB)
            py += 22

    # ---- Bottom wide: RUSSIA / DRONES ----
    tag, color, head, sub, icon = STORIES[7]
    bx0, by0, bh = m, 874, 106
    neon_card(d, bx0, by0, bx0 + full_w, by0 + bh, color)
    draw_drone(d, bx0 + full_w - 60, by0 + bh // 2 + 2, 32, color)
    px, py = bx0 + 28, by0 + 12
    tag_pill(d, px, py, tag, color, f_tag)
    py += 38
    f_wide = ImageFont.truetype(SANS_B, 26)
    tw = full_w - 56 - 92
    for line in wrap(d, head, f_wide, tw)[:1]:
        d.text((px, py), line, font=f_wide, fill=HEAD)
        py += 32
    f_wide_sub = ImageFont.truetype(SANS, 17)
    for line in wrap(d, sub, f_wide_sub, tw)[:1]:
        d.text((px, py), line, font=f_wide_sub, fill=SUB)
        py += 22

    # ---- Footer ----
    f_foot = ImageFont.truetype(SANS, 16)
    foot = "18 November 2026 \u2022 World news at a glance \u2022 Nvidia \u2022 OpenAI \u2022 Cyberattack \u2022 Shenzhen \u2022 Qeshm \u2022 Kerch \u2022 Alaska \u2022 Drones"
    d.text(((W - d.textlength(foot, font=f_foot)) / 2, 992), foot, font=f_foot, fill=FOOT)

    img.save("entry.png", "PNG", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
