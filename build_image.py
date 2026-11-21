#!/usr/bin/env python3
"""Draw the entry image: one 1024x1024 newspaper-style summary of the
world news of Saturday 21 November 2026.

Stories (each cross-checked in at least two independent sources on
2026-11-21):
1. Russia's massive overnight strike on Ukraine (400+ drones, 110
   missiles, Kyiv deaths) with missiles / a drone coming down in
   Poland; PM Tusk called it a deliberate provocation.
2. AI stock rout: Nasdaq -5.3%, S&P 500 -3.7% into correction,
   Nikkei -5.1%, Nvidia about -14%.
3. Trump-Xi-Putin first three-way summit in Shenzhen and their
   joint peace declaration; Trump defended it on 21 Nov.
4. ICJ found Myanmar committed genocide against the Rohingya
   (historic first ruling against a state); Myanmar rejected it.
5. COP31 in Antalya, Turkey ran into overtime over fossil fuels.
6. Pancreatic-cancer pill daraxonrasib: tumours undetectable on
   scans in about 1 in 12 trial patients.

Only stdlib + Pillow are used, and only at build time. The shipped
entrypoint (main.py) is stdlib-only and simply copies entry.png.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (13, 17, 26)
PANEL = (24, 31, 46)
WHITE = (245, 247, 250)
MUTED = (178, 188, 205)
RED = (235, 64, 52)
ORANGE = (245, 166, 35)
BLUE = (64, 156, 255)
GREEN = (52, 199, 123)
PURPLE = (167, 139, 250)
TEAL = (45, 212, 191)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def panel(draw, box, accent, kicker, headline, body, head_size=40):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=18, fill=PANEL)
    draw.rectangle([x0, y0, x0 + 10, y1], fill=accent)
    tx = x0 + 28
    draw.text((tx, y0 + 14), kicker, font=font(BOLD, 23), fill=accent)
    y = y0 + 48
    for line in wrap(draw, headline, font(BOLD, head_size), x1 - tx - 20):
        draw.text((tx, y), line, font=font(BOLD, head_size), fill=WHITE)
        y += head_size + 5
    y += 2
    for line in wrap(draw, body, font(REG, 25), x1 - tx - 20):
        draw.text((tx, y), line, font=font(REG, 25), fill=MUTED)
        y += 33


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Header
    d.text((36, 26), "THE WORLD IN ONE DAY", font=font(BOLD, 62), fill=WHITE)
    d.text((36, 102), "SATURDAY  21 NOVEMBER 2026", font=font(BOLD, 44), fill=ORANGE)
    d.line([(36, 168), (988, 168)], fill=ORANGE, width=5)

    # 1. Ukraine / Poland (top, full width)
    panel(
        d, (36, 188, 988, 402), RED,
        "UKRAINE WAR  -  KYIV & POLAND",
        "RUSSIA'S HUGE STRIKE: 400+ DRONES, 110 MISSILES",
        "Kyiv hit overnight, at least 8 killed. Missiles & a drone came "
        "down in POLAND - PM Tusk: \"deliberate provocation.\"",
        head_size=36,
    )

    # 2. Markets (left) and 3. Summit (right)
    panel(
        d, (36, 422, 504, 662), BLUE,
        "MARKETS  -  AI ROUT",
        "NASDAQ -5.3%  S&P 500 -3.7%",
        "AI sell-off pushes S&P into correction. "
        "Nikkei -5.1%, Nvidia -14%.",
        head_size=32,
    )
    panel(
        d, (520, 422, 988, 662), PURPLE,
        "SUMMIT  -  SHENZHEN",
        "TRUMP - XI - PUTIN MEET",
        "First US-China-Russia summit issues a joint "
        "peace declaration. Europe sceptical.",
        head_size=32,
    )

    # 4. ICJ (left) and 5. COP31 (right)
    panel(
        d, (36, 682, 504, 922), TEAL,
        "UN COURT  -  THE HAGUE",
        "MYANMAR: GENOCIDE",
        "ICJ: Myanmar committed genocide against the "
        "Rohingya - a historic first. Myanmar rejects it.",
        head_size=32,
    )
    panel(
        d, (520, 682, 988, 922), GREEN,
        "CLIMATE  -  COP31, TURKEY",
        "TALKS RUN OVERTIME",
        "200 nations deadlocked over fossil fuels in "
        "Antalya. Cancer pill: tumours vanish in 1 in 12.",
        head_size=32,
    )

    # Footer (wrapped to fit the 1024 width)
    fy = 942
    for line in wrap(
        d,
        "21 NOV 2026 - WAR WIDENS, AI STOCKS CRASH, SUPERPOWERS MEET, "
        "A LANDMARK VERDICT, CLIMATE TALKS STALL",
        font(BOLD, 24), 952,
    ):
        d.text((36, fy), line, font=font(BOLD, 24), fill=WHITE)
        fy += 32

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
