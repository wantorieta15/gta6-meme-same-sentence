#!/usr/bin/env python3
"""Build the GTA 6 meme for make.fun bounty gta6-meme-x-01 (Account 1).

Concept v2 — "SENTENCE SERVED": copies the rank-1 winning formula as
closely as possible (perintah mas Wan: salin 75% rank 1/2). Rank 1
(tak-attack, 828.964): Lucia/ghost keluar dari sel penjara menuju sunset
Vice City; teks "13 YEARS · 4,811 DAYS · SENTENCE SERVED".

Scene: full-bleed Vice City sunset + skyline. Left: prison cell — barred
window with the sunset, open doorway, tally marks + DAY 4,811 on the wall.
Lucia (orange jumpsuit) walks out of the cell toward the sun. The make.fun
ghost floats beside her, holding its star. Big text: "13 YEARS · 4,811
DAYS" (top) and "SENTENCE SERVED." (bottom). Pink strip: the make.fun
pitch in the meme's own voice.

Style: flat vector illustration (no AI art, no copied images). Bold Anton
meme type, huge and readable at 480px. 1080x1080 square for X.
Deterministic: same input -> byte-identical PNG.
"""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1080
ANTON = "/home/hatch/workspace/goals/menang-bounty-make-fun/hidden_files/meme-x-study/Anton-Regular.ttf"

# ---- palette ------------------------------------------------------------
BLACK = (10, 10, 12)
WHITE = (255, 255, 255)
PINK = (230, 0, 126)        # make.fun magenta
PINK_SOFT = (255, 94, 138)
ORANGE = (255, 158, 79)
SUNSET_TOP = (255, 94, 138)
SUNSET_MID = (255, 158, 79)
SUNSET_BOT = (123, 47, 190)
SKYLINE = (43, 16, 66)
PRISON_TOP = (48, 52, 66)
PRISON_BOT = (24, 27, 38)
JUMPSUIT = (255, 122, 26)
SKIN = (232, 178, 140)
SKIN_DARK = (214, 158, 118)
HAIR = (26, 18, 24)
GREEN = (74, 222, 128)


def vgrad(w, h, stops):
    """Vertical gradient through color stops (0..1). Returns RGB image."""
    arr = np.zeros((h, w, 3), dtype=np.uint8)
    ys = np.linspace(0, 1, h)
    for i in range(len(stops) - 1):
        c0, c1 = np.array(stops[i], dtype=float), np.array(stops[i + 1], dtype=float)
        t0, t1 = i / (len(stops) - 1), (i + 1) / (len(stops) - 1)
        m = (ys >= t0) & (ys <= t1)
        t = np.clip((ys[m] - t0) / max(t1 - t0, 1e-9), 0, 1)[:, None, None]
        arr[m] = (c0 * (1 - t) + c1 * t).astype(np.uint8)
    return Image.fromarray(arr, "RGB")


def sparkle(draw, cx, cy, r, fill):
    """4-point star (sparkle) centered at cx,cy with radius r."""
    pts = []
    for k in range(8):
        ang = math.pi / 2 + k * math.pi / 4
        rr = r if k % 2 == 0 else r * 0.28
        pts.append((cx + rr * math.cos(ang), cy - rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def star5(draw, cx, cy, r, fill):
    """5-point star."""
    pts = []
    for k in range(10):
        ang = -math.pi / 2 + k * math.pi / 5
        rr = r if k % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def palm(draw, x, y, s, color):
    """Palm-tree silhouette: trunk + 5 fronds. (x,y) = base of trunk."""
    pts = []
    for i in range(9):
        t = i / 8
        pts.append((x + 14 * s * t * t, y - 95 * s * t))
    draw.line(pts, fill=color, width=max(3, int(9 * s)))
    tx, ty = pts[-1]
    for ang in (-160, -125, -90, -55, -20):
        a = math.radians(ang)
        ex = tx + 52 * s * math.cos(a)
        ey = ty + 30 * s * math.sin(a) + 14 * s
        mx = tx + 26 * s * math.cos(a)
        my = ty + 26 * s * math.sin(a) - 12 * s
        draw.line([(tx, ty), (mx, my), (ex, ey)], fill=color,
                  width=max(2, int(5 * s)))


def skyline(draw, box, sun_xy, sun_r):
    """Sunset view: gradient sky, sun, skyline blocks, palm. box=(x0,y0,x1,y1)."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    sky = vgrad(w, h, [SUNSET_TOP, SUNSET_MID, SUNSET_BOT])
    draw_img = sky.copy()
    d = ImageDraw.Draw(draw_img)
    sx, sy = sun_xy[0] - x0, sun_xy[1] - y0
    d.ellipse([sx - sun_r, sy - sun_r, sx + sun_r, sy + sun_r],
              fill=(255, 236, 170))
    base = h
    bx = 0
    heights = [0.42, 0.30, 0.55, 0.36, 0.48, 0.28, 0.40]
    bw = w // len(heights)
    for i, hf in enumerate(heights):
        bh = int(h * hf)
        d.rectangle([bx, base - bh, bx + bw - 3, base], fill=SKYLINE)
        for wy in range(base - bh + 8, base - 6, 14):
            for wx in range(bx + 5, bx + bw - 8, 11):
                if (wx * 7 + wy * 13) % 5 == 0:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 120))
        bx += bw
    palm(d, int(w * 0.68), base, 0.85, SKYLINE)
    return draw_img


def tally(draw, x, y, groups, s=1.0, color=(235, 235, 235)):
    """Prison tally marks: groups of 5 (4 vertical + 1 diagonal)."""
    gx = x
    for _ in range(groups):
        for i in range(4):
            lx = gx + i * int(9 * s)
            draw.line([(lx, y), (lx, y + int(26 * s))], fill=color,
                      width=max(2, int(3 * s)))
        draw.line([(gx - 2, y + int(24 * s)), (gx + int(32 * s), y + 2)],
                  fill=color, width=max(2, int(3 * s)))
        gx += int(44 * s)


def meme_text(draw, cx, y, text, font, fill=WHITE, stroke=BLACK, sw=6):
    draw.text((cx, y), text, font=font, fill=fill, anchor="ma",
              stroke_width=sw, stroke_fill=stroke)


def ghost(draw, cx, cy, s):
    """The make.fun ghost: white body, sparkle eyes, smile, star badge.
    (cx,cy) = center of body. s = scale (1.0 -> ~200px tall)."""
    w, h = int(190 * s), int(210 * s)
    x0, y0 = cx - w // 2, cy - h // 2
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([cx - int(150 * s), cy - int(150 * s),
                cx + int(150 * s), cy + int(150 * s)],
               fill=(230, 0, 126, 60))
    glow = glow.filter(ImageFilter.GaussianBlur(30))
    body = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(body)
    bd.rounded_rectangle([x0 - 7, y0 - 7, x0 + w + 7, y0 + h + 7],
                         radius=int(95 * s), fill=(12, 10, 16, 255))
    for i, fx in enumerate([0.06, 0.30, 0.54, 0.78]):
        wx = x0 + int(w * fx)
        bd.ellipse([wx - int(24 * s), y0 + h - int(52 * s),
                    wx + int(24 * s), y0 + h + 7], fill=(12, 10, 16, 255))
    bd.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=int(88 * s),
                         fill=(255, 255, 255, 255))
    for i, fx in enumerate([0.06, 0.30, 0.54, 0.78]):
        wx = x0 + int(w * fx)
        bd.ellipse([wx - int(21 * s), y0 + h - int(48 * s),
                    wx + int(21 * s), y0 + h - int(4 * s)],
                   fill=(255, 255, 255, 255))
    sparkle(bd, cx - int(42 * s), cy - int(38 * s), int(22 * s), (12, 10, 16, 255))
    sparkle(bd, cx + int(42 * s), cy - int(38 * s), int(22 * s), (12, 10, 16, 255))
    bd.arc([cx - int(22 * s), cy + int(8 * s), cx + int(22 * s), cy + int(44 * s)],
           start=15, end=165, fill=(12, 10, 16, 255), width=max(3, int(6 * s)))
    bx, by = x0 + w - int(6 * s), cy + int(34 * s)
    bd.ellipse([bx - int(42 * s), by - int(42 * s), bx + int(42 * s), by + int(42 * s)],
               fill=(230, 0, 126, 255), outline=(12, 10, 16, 255),
               width=max(3, int(6 * s)))
    star5(bd, bx, by, int(24 * s), (255, 255, 255, 255))
    return glow, body


# ---- scene --------------------------------------------------------------
def cell_panel(img, d):
    """Left: prison cell. Wall x 0..330, y 150..830."""
    wall = vgrad(330, 680, [PRISON_TOP, PRISON_BOT])
    img.paste(wall, (0, 150))
    # barred window: the same Vice City sunset seen through bars
    wx0, wy0, wx1, wy1 = 24, 180, 196, 540
    view = skyline(d, (wx0, wy0, wx1, wy1), (wx0 + 90, wy0 + 160), 26)
    img.paste(view, (wx0, wy0))
    d.rectangle([wx0, wy0, wx1, wy1], outline=(14, 14, 18), width=8)
    for bx in (66, 110, 154):
        d.line([(bx, wy0), (bx, wy1)], fill=(14, 14, 18), width=10)
    for by in (300, 420):
        d.line([(wx0, by), (wx1, by)], fill=(14, 14, 18), width=10)
    # open doorway: sunset through the open door (she walks out here)
    dx0, dx1 = 216, 330
    door = vgrad(dx1 - dx0, 680, [SUNSET_TOP, SUNSET_MID, SUNSET_BOT])
    img.paste(door, (dx0, 150))
    d.line([(dx0, 150), (dx0, 830)], fill=(14, 14, 18), width=10)
    d.line([(dx1 - 5, 150), (dx1 - 5, 830)], fill=(14, 14, 18), width=10)
    # tally marks + DAY on the wall below the window
    d.text((30, 566), "DAY 4,811", font=ImageFont.truetype(ANTON, 34),
           fill=(235, 235, 235))
    tally(d, 30, 616, 4, s=0.9)
    tally(d, 30, 660, 4, s=0.9)
    tally(d, 30, 704, 3, s=0.9)


def lucia(d, cx):
    """Lucia in her orange jumpsuit, walking out of the cell toward the sun.
    Feet at y~770, head at y~390."""
    # legs in stride
    d.rounded_rectangle([cx - 48, 630, cx - 6, 770], radius=12, fill=JUMPSUIT)
    d.rounded_rectangle([cx + 6, 630, cx + 48, 770], radius=12, fill=JUMPSUIT)
    d.rectangle([cx - 52, 758, cx - 2, 776], fill=(30, 30, 34))
    d.rectangle([cx + 2, 758, cx + 52, 776], fill=(30, 30, 34))
    # torso
    d.rounded_rectangle([cx - 58, 492, cx + 58, 656], radius=26, fill=JUMPSUIT)
    d.line([(cx - 58, 556), (cx + 58, 556)], fill=(214, 90, 10), width=4)
    # arms: right arm raised toward the sun
    d.line([(cx + 50, 514), (cx + 112, 448)], fill=JUMPSUIT, width=28)
    d.ellipse([cx + 100, 432, cx + 128, 460], fill=SKIN)
    d.line([(cx - 50, 514), (cx - 84, 596)], fill=JUMPSUIT, width=28)
    d.ellipse([cx - 98, 584, cx - 70, 612], fill=SKIN)
    # head + dark hair in a bun
    d.ellipse([cx - 36, 414, cx + 36, 486], fill=SKIN)
    d.ellipse([cx - 38, 404, cx + 38, 454], fill=HAIR)
    d.ellipse([cx + 8, 386, cx + 46, 424], fill=HAIR)


def build():
    img = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(img)
    # full-bleed Vice City sunset + skyline + sun
    view = skyline(d, (0, 150, 1080, 830), (880, 400), 75)
    img.paste(view, (0, 150))
    cell_panel(img, d)
    # ground strip
    d.rectangle([0, 770, 1080, 830], fill=(20, 16, 26))
    d.line([(0, 770), (1080, 770)], fill=(70, 74, 92), width=3)
    # Lucia walking out of the cell toward the sun
    lucia(d, 430)
    # ghost beside her, bridging to freedom
    glow, body = ghost(d, 660, 470, 1.15)
    img.paste(Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB"), (0, 0))
    img.paste(body, (0, 0), body)
    d = ImageDraw.Draw(img)
    # top + bottom bands: rank 1's own words
    d.rectangle([0, 0, W, 150], fill=BLACK)
    d.rectangle([0, 830, W, 950], fill=BLACK)
    meme_text(d, W // 2, 30, "13 YEARS · 4,811 DAYS",
              ImageFont.truetype(ANTON, 72))
    meme_text(d, W // 2, 842, "SENTENCE SERVED.",
              ImageFont.truetype(ANTON, 88))
    # pink strip: the make.fun pitch, in the meme's own voice
    d.rectangle([0, 950, W, H], fill=PINK)
    f = ImageFont.truetype(ANTON, 42)
    meme_text(d, W // 2, 990, "MY AGENT MADE THIS ON make.fun — AND GOT PAID",
              f, fill=BLACK, stroke=BLACK, sw=0)
    return img


if __name__ == "__main__":
    out = build()
    out.save("/home/hatch/workspace/goals/menang-bounty-make-fun/hidden_files/gta6-meme-x-01-akun1/meme.png")
    print("saved meme.png", out.size)
