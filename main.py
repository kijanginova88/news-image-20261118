#!/usr/bin/env python3
"""World news of Wednesday 18 November 2026, summed up in one image.

Deterministic: no network, no clock, no randomness. Draws a 1024x1024
PNG with Pillow from the fixed story list below and writes it to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).

Stories were researched on 18 Nov 2026 from Reuters, AP, NASA and
ScienceAlert reporting of 18 Nov 2026; full sources are in SOURCES.md.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (247, 243, 234)
NAVY = (11, 37, 69)
GOLD = (232, 184, 75)
INK = (17, 24, 39)
GREY = (71, 85, 105)
CARD = (255, 255, 255)
LINE = (216, 210, 196)

FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
]


def font(bold, size):
    for p in FONT_PATHS:
        if bold and "Bold" in p and os.path.exists(p):
            return ImageFont.truetype(p, size)
        if not bold and "Bold" not in p and os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


STORIES = [
    {
        "kicker": "MIDDLE EAST  •  GULF",
        "color": (180, 35, 24),
        "headline": "Iran Strikes Back at U.S. Bases in Gulf",
        "fact": "Iran fired drones at Ali Al Salem air base in Kuwait; Bahrain intercepted a third attack this week. No confirmed damage reported.",
        "icon": "rocket",
    },
    {
        "kicker": "AFRICA  •  HORN",
        "color": (180, 83, 9),
        "headline": "Ethiopia, Eritrea Mass Troops at Border",
        "fact": "Forces amass within striking distance near Badme, raising fears of open war between the old rivals.",
        "icon": "flags",
    },
    {
        "kicker": "UKRAINE  •  ENERGY",
        "color": (29, 78, 216),
        "headline": "Ukraine Drones Halve Russia's Oil Refining",
        "fact": "Refining down 45% since late October; 15 of 35 big refineries hit or halted, incl. Ryazan and Kirishi.",
        "icon": "refinery",
    },
    {
        "kicker": "SPACE  •  NASA",
        "color": (124, 58, 237),
        "headline": "Voyager 1 Reaches One Light-Day Away",
        "fact": "First human-made object 25.9 billion km from Earth; a radio signal now takes 24 hours one way.",
        "icon": "satellite",
    },
    {
        "kicker": "UNITED STATES  •  POLITICS",
        "color": (21, 128, 61),
        "headline": "Peltola Wins Alaska, Democrats Take Senate",
        "fact": "AP called the final Senate race on 18 Nov: Peltola 50.1% beats Sullivan 45.8%; Democrats lead 56-44.",
        "icon": "capitol",
    },
    {
        "kicker": "UNITED KINGDOM  •  ECONOMY",
        "color": (14, 116, 144),
        "headline": "UK Inflation Hits One-Year High",
        "fact": "CPI rose to 3.6% in October; petrol at 174.7p a litre, diesel at a record 199.5p a litre.",
        "icon": "chart",
    },
]


def draw_icon(d, kind, x, y, s, color):
    if kind == "rocket":
        # Rocket body pointing up-right with a flame trail
        d.polygon([(x + 34, y + 2), (x + 52, y + 26), (x + 44, y + 40),
                   (x + 24, y + 40), (x + 16, y + 26)], fill=color)
        d.ellipse([x + 28, y + 18, x + 40, y + 30], fill=(255, 255, 255))
        d.polygon([(x + 16, y + 26), (x + 24, y + 40), (x + 12, y + 44)],
                  fill=color)
        d.polygon([(x + 52, y + 26), (x + 44, y + 40), (x + 56, y + 44)],
                  fill=color)
        d.polygon([(x + 26, y + 44), (x + 34, y + 62), (x + 42, y + 44)],
                  fill=(245, 158, 11))
        for i, (sx, sy) in enumerate([(x + 58, y + 8), (x + 64, y + 22),
                                      (x + 8, y + 52)]):
            d.ellipse([sx, sy, sx + 6, sy + 6], fill=(245, 158, 11))
    elif kind == "flags":
        # Two crossed flag poles, red and blue
        d.line([x + 20, y + 8, x + 20, y + 66], fill=NAVY, width=5)
        d.line([x + 48, y + 8, x + 48, y + 66], fill=NAVY, width=5)
        d.polygon([(x + 20, y + 8), (x + 46, y + 14), (x + 20, y + 26)],
                  fill=(180, 35, 24))
        d.polygon([(x + 48, y + 8), (x + 22, y + 14), (x + 48, y + 26)],
                  fill=(29, 78, 216))
        d.rectangle([x + 8, y + 62, x + 60, y + 70], fill=NAVY)
    elif kind == "refinery":
        # Towers and a flame
        d.rectangle([x + 10, y + 26, x + 24, y + 66], fill=color)
        d.rectangle([x + 30, y + 14, x + 44, y + 66], fill=color)
        d.rectangle([x + 48, y + 36, x + 62, y + 66], fill=color)
        d.polygon([(x + 52, y + 2), (x + 62, y + 18), (x + 58, y + 30),
                   (x + 66, y + 20), (x + 70, y + 34), (x + 56, y + 40),
                   (x + 46, y + 34), (x + 50, y + 20), (x + 44, y + 26)],
                  fill=(245, 158, 11))
        d.rectangle([x + 6, y + 62, x + 66, y + 70], fill=NAVY)
    elif kind == "satellite":
        # Dish body, panels and a signal star
        d.rectangle([x + 6, y + 30, x + 22, y + 40], fill=color)
        d.rectangle([x + 46, y + 30, x + 62, y + 40], fill=color)
        d.ellipse([x + 24, y + 22, x + 44, y + 48], fill=color)
        d.line([x + 34, y + 48, x + 34, y + 62], fill=color, width=5)
        d.line([x + 34, y + 8, x + 34, y + 20], fill=color, width=4)
        d.polygon([(x + 52, y + 2), (x + 57, y + 11), (x + 67, y + 4),
                   (x + 60, y + 13), (x + 67, y + 21), (x + 56, y + 19),
                   (x + 54, y + 29), (x + 49, y + 19), (x + 39, y + 21),
                   (x + 46, y + 12), (x + 40, y + 5), (x + 49, y + 10)],
                  fill=(245, 158, 11))
    elif kind == "capitol":
        # Dome, columns and base
        d.pieslice([x + 16, y + 6, x + 52, y + 34], 180, 360, fill=color)
        d.rectangle([x + 32, y + 2, x + 36, y + 10], fill=color)
        d.rectangle([x + 10, y + 34, x + 58, y + 40], fill=color)
        for cx in [x + 14, x + 26, x + 38, x + 50]:
            d.rectangle([cx, y + 40, cx + 4, y + 58], fill=color)
        d.rectangle([x + 6, y + 58, x + 62, y + 66], fill=NAVY)
        d.ellipse([x + 28, y + 42, x + 40, y + 56], fill=(255, 255, 255))
    elif kind == "chart":
        # Rising bars with an arrow
        bars = [(x + 6, 44), (x + 22, 34), (x + 38, 24), (x + 54, 12)]
        for bx, bh in bars:
            d.rectangle([bx, y + 66 - bh, bx + 12, y + 66], fill=color)
        d.line([x + 4, y + 66, x + 66, y + 66], fill=NAVY, width=4)
        d.line([x + 8, y + 52, x + 26, y + 40, x + 44, y + 28, x + 62, y + 12],
               fill=(245, 158, 11), width=5)
        d.polygon([(x + 62, y + 12), (x + 54, y + 10), (x + 58, y + 20)],
                  fill=(245, 158, 11))


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Header
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.rectangle([0, 148, W, 156], fill=GOLD)
    f_date = font(True, 46)
    f_sub = font(True, 28)
    d.text((W // 2, 52), "WEDNESDAY 18 NOVEMBER 2026", font=f_date,
           fill=(255, 255, 255), anchor="mm")
    d.text((W // 2, 112), "THE WORLD IN ONE DAY  •  SIX STORIES",
           font=f_sub, fill=GOLD, anchor="mm")

    # Story grid: 2 columns x 3 rows
    gx, gy = 16, 168
    pw, ph, gap = 490, 262, 12
    f_kick = font(True, 17)
    f_head = font(True, 27)
    f_fact = font(False, 18)
    for i, s in enumerate(STORIES):
        x = gx + (i % 2) * (pw + gap)
        y = gy + (i // 2) * (ph + gap)
        d.rounded_rectangle([x, y, x + pw, y + ph], radius=10,
                            fill=CARD, outline=LINE, width=2)
        d.rectangle([x, y, x + pw, y + 8], fill=s["color"])
        d.text((x + 18, y + 26), s["kicker"], font=f_kick, fill=s["color"])
        draw_icon(d, s["icon"], x + pw - 88, y + 18, 68, s["color"])
        tx = x + 18
        tw = pw - 36
        lines = wrap(d, s["headline"], f_head, tw - 96)
        ly = y + 56
        for ln in lines[:3]:
            d.text((tx, ly), ln, font=f_head, fill=INK)
            ly += 33
        flines = wrap(d, s["fact"], f_fact, tw)
        ly += 6
        for ln in flines[:3]:
            d.text((tx, ly), ln, font=f_fact, fill=GREY)
            ly += 23

    # Footer
    f_foot = font(False, 16)
    d.text((W // 2, 1002),
           "Sources: Reuters  •  AP  •  NASA  •  ScienceAlert  —  All events reported on 18 November 2026",
           font=f_foot, fill=GREY, anchor="mm")

    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, "entry.png")
    img.save(out, "PNG", compress_level=6)
    print("wrote", out)


if __name__ == "__main__":
    main()
