#!/usr/bin/env python3
"""news-image-20261120-cand-b — "ONE DAY IN UTC".
Broadsheet front page summing up Friday 20 November 2026 in 50 stories.
All text is exact programmatic PIL text; all illustrations are flat
vector-style drawings made with PIL primitives. No photos, no AI images.
Canvas 1600x2640, target < 1 MiB PNG.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1600, 2820
PAPER = (248, 242, 223)
INK = (20, 20, 20)
RED = (179, 32, 44)
NAVY = (29, 58, 95)
BLUE = (47, 111, 178)
GOLD = (180, 138, 40)
GREY = (107, 107, 96)
LIGHT = (239, 231, 207)
SEA = (207, 224, 232)
LAND = (232, 217, 184)
WHITE = (255, 255, 255)

FD = "/usr/share/fonts/truetype/dejavu/"

def font(name, size):
    return ImageFont.truetype(FD + name, size)

SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def wrap(text, fnt, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def text_block(x, y, text, fnt, fill, maxw, lh=None, align="left"):
    lh = lh or int(fnt.size * 1.22)
    for ln in wrap(text, fnt, maxw):
        if align == "center":
            d.text((x + (maxw - d.textlength(ln, font=fnt)) / 2, y), ln, font=fnt, fill=fill)
        else:
            d.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y

def rule(y, x0=24, x1=1576, wdt=3, fill=INK):
    d.line([(x0, y), (x1, y)], fill=fill, width=wdt)

def section_head(y, label):
    d.line([(24, y + 14), (24 + 0, y + 14)], fill=INK, width=2)
    rule(y + 2, 24, 300, 2)
    d.text((312, y - 8), label, font=SANS_B(26), fill=INK)
    rule(y + 2, 312 + d.textlength(label, font=SANS_B(26)) + 12, 1576, 2)
    return y + 34

# ---------------- masthead ----------------
name = "THE DAILY GLOBE  ·  ONE DAY, THE WHOLE WORLD"
d.text(((W - d.textlength(name, font=SANS_B(20))) / 2, 16), name, font=SANS_B(20), fill=GREY)
rule(48, 24, 1576, 4)
hl = "Friday 20 November 2026"
d.text(((W - d.textlength(hl, font=SERIF_B(92))) / 2, 58), hl, font=SERIF_B(92), fill=INK)
sub = "Three leaders declare peace in Shenzhen  ·  A bridge falls silent  ·  A missile over Riyadh  ·  A cyclone comes ashore"
text_block(80, 168, sub, SERIF(27), RED, 1440, lh=34, align="center")
rule(244, 24, 1576, 2)

# ---------------- timeline strip: THE DAY IN UTC ----------------
ty = 256
d.text((24, ty), "THE DAY IN UTC", font=SANS_B(22), fill=RED)
tl = [
    ("OVERNIGHT", "Crimean Bridge hit a third time"),
    ("~06:00 UTC", "APEC leaders meet in Shenzhen"),
    ("~10:00 UTC", "Trilateral declaration issued"),
    ("~14:00 UTC", "Houthi missile hits Riyadh KAFD"),
    ("EVENING", "Akvan makes landfall in Odisha"),
    ("LATE", "Wall Street slides, Dow −1,100"),
]
cw = (1552 - 5 * 8) / 6
for i, (t, s) in enumerate(tl):
    x = 24 + i * (cw + 8)
    d.rectangle([x, ty + 30, x + cw, ty + 96], fill=LIGHT, outline=INK, width=2)
    d.text((x + 10, ty + 36), t, font=SANS_B(19), fill=RED)
    text_block(x + 10, ty + 60, s, SANS(16), INK, cw - 20, lh=19)
rule(ty + 108, 24, 1576, 2)

# ---------------- stats strip ----------------
sy = 384
stats = [
    ("300,000", "evacuated ahead of Cyclone Akvan"),
    ("9–6", "ICJ vote: Myanmar guilty of genocide"),
    ("$1.8bn", "GTA VI day-one sales"),
    ("25.9bn km", "Voyager 1 now from Earth"),
    ("−1,100", "Dow points lost on Friday"),
]
sw = 1552 / 5
for i, (n, lab) in enumerate(stats):
    x = 24 + i * sw
    d.text((x + (sw - d.textlength(n, font=SERIF_B(44))) / 2, sy), n, font=SERIF_B(44), fill=RED)
    text_block(x + 8, sy + 54, lab, SANS(15), INK, sw - 16, lh=18, align="center")
    if i:
        d.line([(x, sy + 6), (x, sy + 84)], fill=GREY, width=1)
rule(sy + 100, 24, 1576, 2)

# ---------------- lead illustrations ----------------
def draw_summit(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 58, 95))
    # sky glow + round table
    d.ellipse([x + w / 2 - 150, y + h - 130, x + w / 2 + 150, y + h - 10], fill=(210, 170, 90))
    d.ellipse([x + w / 2 - 120, y + h - 105, x + w / 2 + 120, y + h - 25], fill=(120, 70, 40))
    # three flags on poles
    flags = [("US", (178, 34, 52)), ("CN", (222, 41, 16)), ("RU", (255, 255, 255))]
    fw, fh = 120, 74
    xs = [x + 60, x + w / 2 - fw / 2, x + w - 60 - fw]
    for (code, col), fx in zip(flags, xs):
        d.line([(fx + fw / 2, y + 8), (fx + fw / 2, y + fh + 8)], fill=(240, 230, 200), width=4)
        d.rectangle([fx, y + 8, fx + fw, y + 8 + fh], fill=col, outline=INK, width=2)
        if code == "US":
            for s in range(7):
                d.rectangle([fx, y + 8 + s * 10, fx + fw, y + 8 + s * 10 + 5],
                            fill=(178, 34, 52) if s % 2 == 0 else WHITE)
            d.rectangle([fx, y + 8, fx + 48, y + 8 + 34], fill=(30, 58, 95))
            for sx in (fx + 8, fx + 22, fx + 36):
                for sy2 in (y + 12, y + 26):
                    d.ellipse([sx, sy2, sx + 5, sy2 + 5], fill=WHITE)
        elif code == "CN":
            d.text((fx + 8, y + 12), "★", font=SANS_B(26), fill=(255, 220, 0))
        else:
            d.rectangle([fx, y + 8 + 24, fx + fw, y + 8 + 50], fill=(0, 90, 170))
            d.rectangle([fx, y + 8 + 50, fx + fw, y + 8 + fh], fill=(200, 30, 30))
    d.text((x + 12, y + h - 30), "SHENZHEN", font=SANS_B(18), fill=WHITE)

def draw_bridge(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(170, 205, 225))
    d.rectangle([x, y + h - 55, x + w, y + h], fill=(40, 90, 130))  # sea
    for i in range(6):
        d.arc([x + 30 + i * 120, y + h - 70, x + 130 + i * 120, y + h - 30], 180, 360, fill=WHITE, width=3)
    # deck with a broken gap in the middle
    d.rectangle([x + 10, y + 95, x + w / 2 - 55, y + 112], fill=(60, 60, 60))
    d.rectangle([x + w / 2 + 55, y + 95, x + w - 10, y + 112], fill=(60, 60, 60))
    for tx in (x + 120, x + w - 170):
        d.rectangle([tx, y + 30, tx + 16, y + 95], fill=(90, 90, 90))
        d.line([(tx + 8, y + 30), (tx + 8, y + 95)], fill=(60, 60, 60), width=2)
    # sagging cables
    d.line([(x + 128, y + 30), (x + w / 2 - 55, y + 100)], fill=(40, 40, 40), width=3)
    d.line([(x + w - 162, y + 30), (x + w / 2 + 55, y + 100)], fill=(40, 40, 40), width=3)
    # smoke + fire at the gap
    for cx, cy, r, col in [(x + w / 2 - 20, y + 70, 26, (90, 90, 90)),
                           (x + w / 2 + 15, y + 55, 32, (120, 120, 120)),
                           (x + w / 2, y + 40, 22, (150, 150, 150))]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    d.polygon([(x + w / 2 - 18, y + 108), (x + w / 2, y + 78), (x + w / 2 + 18, y + 108)],
              fill=(230, 120, 20))
    d.text((x + w - 170, y + 8), "KERCH STRAIT", font=SANS_B(18), fill=NAVY)

def draw_riyadh(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(38, 44, 66))  # night sky
    for sx, sy in [(x + 40, y + 20), (x + 200, y + 35), (x + 420, y + 18), (x + 620, y + 30), (x + 700, y + 15)]:
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=WHITE)
    # skyline
    towers = [(x + 30, 90, 70, 150), (x + 130, 60, 64, 180), (x + 220, 100, 70, 140),
              (x + 480, 70, 72, 170), (x + 580, 95, 66, 145), (x + 660, 110, 60, 130)]
    for tx, ty2, tw, th in towers:
        d.rectangle([tx, y + h - th, tx + tw, y + h], fill=(90, 100, 130), outline=(150, 160, 190), width=2)
        for wy in range(y + h - th + 12, y + h - 8, 18):
            for wx in range(tx + 8, tx + tw - 8, 16):
                d.rectangle([wx, wy, wx + 6, wy + 8], fill=(255, 220, 120))
    # damaged twisted tower (centre)
    tx = x + 320
    d.polygon([(tx, y + h - 190), (tx + 90, y + h - 190), (tx + 70, y + h - 90),
               (tx + 95, y + h), (tx + 10, y + h), (tx + 25, y + h - 90)], fill=(150, 60, 50), outline=INK)
    for wy in range(y + h - 175, y + h - 8, 20):
        d.rectangle([tx + 30, wy, tx + 55, wy + 8], fill=(255, 200, 100))
    # missile streak + blast
    d.line([(x + 700, y + 12), (x + 400, y + 60)], fill=(255, 180, 60), width=5)
    d.polygon([(x + 380, y + 30), (x + 420, y + 55), (x + 395, y + 80)], fill=(255, 140, 40))
    for ang in range(0, 360, 45):
        import math
        r1 = 26
        ex = x + 400 + int(r1 * math.cos(math.radians(ang)))
        ey = y + 55 + int(r1 * math.sin(math.radians(ang)))
        d.line([(x + 400, y + 55), (ex, ey)], fill=(255, 200, 80), width=4)
    d.ellipse([x + 388, y + 43, x + 412, y + 67], fill=(255, 220, 120))
    d.text((x + 440, y + 8), "KAFD, RIYADH", font=SANS_B(18), fill=WHITE)

def draw_cyclone(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(120, 160, 190))
    # coastline + land
    d.polygon([(x, y + h), (x + w, y + h), (x + w, y + 110), (x + w * 0.55, y + 150), (x, y + 120)],
              fill=(200, 180, 130))
    d.rectangle([x + 30, y + h - 60, x + 90, y + h - 18], fill=(140, 70, 50))
    d.polygon([(x + 25, y + h - 60), (x + 60, y + h - 85), (x + 95, y + h - 60)], fill=(90, 40, 30))
    d.rectangle([x + 620, y + h - 55, x + 680, y + h - 18], fill=(140, 70, 50))
    d.polygon([(x + 615, y + h - 55), (x + 650, y + h - 80), (x + 685, y + h - 55)], fill=(90, 40, 30))
    # spiral
    import math
    cx, cy = x + w * 0.55, y + 75
    for turn in range(3):
        pts = []
        for a in range(0, 361, 6):
            r = 12 + turn * 26 + a * 0.09
            pts.append((cx + r * math.cos(math.radians(a + turn * 40)),
                        cy + r * math.sin(math.radians(a + turn * 40)) * 0.85))
        d.line(pts, fill=WHITE, width=6)
    d.ellipse([cx - 12, cy - 10, cx + 12, cy + 10], fill=NAVY)
    # rain
    for i in range(14):
        rx = x + 20 + i * 52
        d.line([(rx, y + 130), (rx - 8, y + 158)], fill=(220, 235, 245), width=3)
    d.text((x + w - 190, y + 8), "BAY OF BENGAL", font=SANS_B(18), fill=WHITE)

LEADS = [
    ("1", "SHENZHEN · SUMMIT", "Three leaders, one declaration",
     "Trump, Xi and Putin issue a joint peace declaration in Shenzhen — four points: nukes, the UN, oil, the ICC. Trump defers the Iran war decision to 2027.",
     draw_summit),
    ("2", "CRIMEA · WAR", "Bridge hit, rail halted",
     "A Ukrainian attack on the Crimean Bridge halts railway traffic between Russia and Crimea — the third strike on the crossing.",
     draw_bridge),
    ("3", "RIYADH · MISSILE", "Missile hits Riyadh's KAFD",
     "A Houthi missile strikes the King Abdullah Financial District; the Saudi sovereign-wealth-fund tower is damaged. No casualties reported.",
     draw_riyadh),
    ("4", "ODISHA · CYCLONE", "Cyclone Akvan comes ashore",
     "Akvan makes landfall near Gopalpur around noon. 300,000 people evacuated, 423 rescue teams deployed, winds 90–100 km/h gusting to 110.",
     draw_cyclone),
]

y = section_head(504, "THE FOUR BIG STORIES")
lead_y = [538, 880]
for idx, (num, kick, head, body, draw_fn) in enumerate(LEADS):
    lx = 24 + (idx % 2) * 784
    ly = lead_y[idx // 2]
    d.rectangle([lx, ly, lx + 768, ly + 330], outline=INK, width=2)
    d.rectangle([lx, ly, lx + 768, ly + 330], fill=PAPER)
    d.rectangle([lx, ly, lx + 768, ly + 330], outline=INK, width=2)
    d.ellipse([lx + 14, ly + 14, lx + 54, ly + 54], fill=RED)
    d.text((lx + 24, ly + 18), num, font=SANS_B(24), fill=WHITE)
    draw_fn(lx + 10, ly + 10, 748, 168)
    d.ellipse([lx + 14, ly + 14, lx + 54, ly + 54], fill=RED)
    d.text((lx + 24, ly + 18), num, font=SANS_B(24), fill=WHITE)
    d.text((lx + 14, ly + 190), kick, font=SANS_B(17), fill=RED)
    text_block(lx + 14, ly + 214, head, SERIF_B(32), INK, 740, lh=36)
    text_block(lx + 14, ly + 254, body, SANS(18), INK, 740, lh=22)

# ---------------- secondary grid ----------------
def icon_scales(x, y, s=96):
    d.rectangle([x, y, x + s, y + s], fill=(29, 58, 95))
    d.line([(x + s / 2, y + 14), (x + s / 2, y + 78)], fill=WHITE, width=4)
    d.line([(x + 18, y + 28), (x + s - 18, y + 28)], fill=WHITE, width=4)
    d.polygon([(x + 12, y + 62), (x + 34, y + 30), (x + 48, y + 62)], outline=WHITE, width=3)
    d.polygon([(x + s - 48, y + 62), (x + s - 34, y + 30), (x + s - 12, y + 62)], outline=WHITE, width=3)
    d.line([(x + 18, y + 82), (x + s - 18, y + 82)], fill=WHITE, width=4)

def icon_game(x, y, s=96):
    d.rectangle([x, y, x + s, y + s], fill=(120, 30, 90))
    d.rounded_rectangle([x + 14, y + 30, x + s - 14, y + 66], radius=14, fill=WHITE)
    d.text((x + 24, y + 36), "+", font=SANS_B(26), fill=(120, 30, 90))
    d.ellipse([x + 58, y + 40, x + 68, y + 50], fill=(120, 30, 90))
    d.ellipse([x + 70, y + 40, x + 80, y + 50], fill=(120, 30, 90))

def icon_sat(x, y, s=96):
    d.rectangle([x, y, x + s, y + s], fill=(20, 40, 70))
    d.rectangle([x + 16, y + 40, x + 34, y + 56], fill=(70, 130, 200), outline=WHITE, width=2)
    d.rectangle([x + 62, y + 40, x + 80, y + 56], fill=(70, 130, 200), outline=WHITE, width=2)
    d.ellipse([x + 40, y + 38, x + 56, y + 58], fill=WHITE)
    d.arc([x + 30, y + 10, x + 66, y + 30], 200, 340, fill=(255, 220, 80), width=3)
    d.arc([x + 24, y + 4, x + 72, y + 30], 200, 340, fill=(255, 220, 80), width=3)

def icon_talk(x, y, s=96):
    d.rectangle([x, y, x + s, y + s], fill=(40, 110, 90))
    d.rounded_rectangle([x + 14, y + 22, x + 62, y + 52], radius=10, fill=WHITE)
    d.rounded_rectangle([x + 34, y + 50, x + 82, y + 80], radius=10, fill=(255, 220, 120))
    d.text((x + 22, y + 28), "···", font=SANS_B(18), fill=(40, 110, 90))
    d.text((x + 42, y + 56), "···", font=SANS_B(18), fill=(40, 110, 90))

def icon_gavel(x, y, s=96):
    d.rectangle([x, y, x + s, y + s], fill=(90, 60, 20))
    d.rectangle([x + 22, y + 30, x + 74, y + 46], fill=WHITE)
    d.line([(x + 48, y + 46), (x + 48, y + 76)], fill=WHITE, width=6)
    d.rectangle([x + 26, y + 76, x + 70, y + 84], fill=WHITE)

def icon_atom(x, y, s=96):
    d.rectangle([x, y, x + s, y + s], fill=(100, 40, 40))
    d.ellipse([x + 44, y + 44, x + 52, y + 52], fill=(255, 220, 80))
    d.ellipse([x + 14, y + 28, x + 82, y + 68], outline=WHITE, width=3)
    d.ellipse([x + 14, y + 28, x + 82, y + 68], outline=WHITE, width=3)
    d.line([(x + 20, y + 72), (x + 76, y + 24)], fill=WHITE, width=3)
    d.line([(x + 20, y + 24), (x + 76, y + 72)], fill=WHITE, width=3)

def icon_link(x, y, s=96):
    d.rectangle([x, y, x + s, y + s], fill=(60, 60, 110))
    d.ellipse([x + 16, y + 30, x + 52, y + 66], outline=WHITE, width=5)
    d.ellipse([x + 44, y + 30, x + 80, y + 66], outline=WHITE, width=5)

def icon_sun(x, y, s=96):
    d.rectangle([x, y, x + s, y + s], fill=(200, 140, 30))
    d.ellipse([x + 34, y + 34, x + 62, y + 62], fill=(255, 240, 160))
    for a in range(0, 360, 45):
        import math
        x1 = x + 48 + int(22 * math.cos(math.radians(a)))
        y1 = y + 48 + int(22 * math.sin(math.radians(a)))
        x2 = x + 48 + int(32 * math.cos(math.radians(a)))
        y2 = y + 48 + int(32 * math.sin(math.radians(a)))
        d.line([(x1, y1), (x2, y2)], fill=WHITE, width=4)

def icon_crown(x, y, s=96):
    d.rectangle([x, y, x + s, y + s], fill=(140, 30, 60))
    d.polygon([(x + 18, y + 66), (x + 18, y + 38), (x + 34, y + 52), (x + 48, y + 28),
               (x + 62, y + 52), (x + 78, y + 38), (x + 78, y + 66)], fill=(255, 215, 90), outline=INK)

def icon_chart(x, y, s=96):
    d.rectangle([x, y, x + s, y + s], fill=(150, 30, 30))
    d.line([(x + 16, y + 80), (x + 16, y + 18)], fill=WHITE, width=4)
    d.line([(x + 16, y + 80), (x + 82, y + 80)], fill=WHITE, width=4)
    d.line([(x + 22, y + 30), (x + 42, y + 46), (x + 58, y + 40), (x + 78, y + 66)], fill=(255, 220, 80), width=5)
    d.polygon([(x + 78, y + 66), (x + 70, y + 60), (x + 82, y + 56)], fill=(255, 220, 80))

def icon_rocket(x, y, s=96):
    d.rectangle([x, y, x + s, y + s], fill=(30, 60, 110))
    d.polygon([(x + 48, y + 14), (x + 62, y + 44), (x + 58, y + 66), (x + 38, y + 66), (x + 34, y + 44)],
              fill=WHITE, outline=INK)
    d.ellipse([x + 44, y + 44, x + 52, y + 52], fill=(30, 60, 110))
    d.polygon([(x + 40, y + 66), (x + 48, y + 84), (x + 56, y + 66)], fill=(255, 140, 40))

def icon_boat(x, y, s=96):
    d.rectangle([x, y, x + s, y + s], fill=(20, 90, 110))
    d.polygon([(x + 22, y + 58), (x + 74, y + 58), (x + 64, y + 74), (x + 32, y + 74)], fill=(200, 120, 60))
    d.line([(x + 48, y + 58), (x + 48, y + 26)], fill=WHITE, width=3)
    d.polygon([(x + 50, y + 28), (x + 50, y + 54), (x + 72, y + 54)], fill=WHITE)
    for wy in (82, 88):
        d.line([(x + 14, wy), (x + 82, wy)], fill=(160, 210, 230), width=3)

SECOND = [
    ("5", "MYANMAR · ICJ", "Myanmar guilty of genocide",
     "ICJ rules 9–6: Myanmar committed genocide against the Rohingya in 2017 — the first state ever convicted of genocide.", icon_scales),
    ("6", "GAMING", "GTA VI: $1.8bn on day one",
     "Day-one sales pass The Odyssey's $1.80bn global run. Peak viewers: 7.91m.", icon_game),
    ("7", "SPACE", "Voyager 1, one light-day out",
     "NASA confirms the 1977 probe is now 25.9bn km — 16bn miles — from Earth.", icon_sat),
    ("8", "EUROPE", "Europe ready to talk to Russia",
     "European leaders say they are ready for talks on ending the war in Ukraine.", icon_talk),
    ("9", "SEOUL", "Ex-PM Han cleared",
     "South Korea's top court clears ex-PM Han Duck-soo over the 2024 martial-law case.", icon_gavel),
    ("10", "PYONGYANG", "Yongbyon grows",
     "North Korea is expanding uranium enrichment at Yongbyon, the UN watchdog reports.", icon_atom),
    ("11", "CARACAS", "US–Venezuela restore military ties",
     "The two countries agree to restore military cooperation.", icon_link),
    ("12", "FIJI", "Fiji declares national disaster",
     "Severe drought and El Niño water shortages grip the islands.", icon_sun),
    ("13", "DELHI", "Modi meets the Waleses",
     "Modi meets the Prince and Princess of Wales in Delhi.", icon_crown),
    ("14", "MARKETS", "Wall Street slides",
     "Dow −1,100; S&P 500 −2.02%, Nasdaq −2.25% on Friday.", icon_chart),
    ("15", "SPACE · JAPAN", "Hayabusa2 landing scrapped",
     "Engine trouble forces Japan to scrap the asteroid landing; the mission is replanned.", icon_rocket),
    ("16", "SENEGAL", "Migrant boat capsizes",
     "Dozens missing after a boat carrying about 100 people capsizes off Senegal.", icon_boat),
]

y = section_head(1228, "MORE FROM FRIDAY")
gy = 1262
for idx, (num, kick, head, body, ic) in enumerate(SECOND):
    gx = 24 + (idx % 3) * 524
    gyy = gy + (idx // 3) * 168
    d.rectangle([gx, gyy, gx + 504, gyy + 158], outline=INK, width=2)
    ic(gx + 12, gyy + 12)
    d.ellipse([gx + 12, gyy + 12, gx + 40, gyy + 40], fill=RED)
    d.text((gx + 21, gyy + 15), num, font=SANS_B(15), fill=WHITE)
    tx = gx + 120
    d.text((tx, gyy + 12), kick, font=SANS_B(14), fill=RED)
    text_block(tx, gyy + 32, head, SERIF_B(21), INK, 372, lh=24)
    text_block(tx, gyy + 82, body, SANS(15), INK, 372, lh=18)

# ---------------- world map ----------------
y = section_head(gy + 4 * 168 + 8, "WHERE IT HAPPENED")
my = y + 8
d.rectangle([24, my, 1576, my + 320], fill=SEA, outline=INK, width=2)
CONTINENTS = [
    [(60, 60), (180, 30), (300, 45), (330, 90), (280, 120), (230, 150), (150, 140), (80, 110)],  # N America
    [(300, 170), (350, 165), (380, 200), (360, 260), (320, 270), (295, 220)],  # S America
    [(700, 110), (790, 95), (860, 120), (880, 180), (830, 250), (760, 240), (710, 180)],  # Africa
    [(700, 55), (770, 40), (800, 70), (760, 95), (710, 85)],  # Europe
    [(810, 45), (1050, 30), (1250, 50), (1420, 70), (1400, 140), (1250, 160), (1100, 150), (950, 140), (870, 110)],  # Asia
    [(1230, 230), (1360, 225), (1390, 260), (1300, 275), (1230, 260)],  # Australia
]
for poly in CONTINENTS:
    d.polygon([(24 + px, my + py) for px, py in poly], fill=LAND, outline=(120, 100, 60))
PINS = {
    1: (1290, 120), 2: (830, 80), 3: (900, 140), 4: (1130, 145), 5: (1200, 158),
    6: (180, 90), 7: (250, 80), 8: (745, 62), 9: (1345, 100), 10: (1322, 72),
    11: (330, 175), 12: (1490, 250), 13: (1090, 122), 14: (255, 105), 15: (1400, 95),
    16: (692, 152),
}
for n, (px, py) in PINS.items():
    cx, cy = 24 + px, my + py
    d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=RED, outline=WHITE, width=2)
    s = str(n)
    d.text((cx - d.textlength(s, font=SANS_B(13)) / 2, cy - 8), s, font=SANS_B(13), fill=WHITE)
d.text((36, my + 292), "Pins 1–16 match the stories above.  7 = Voyager 1, tracked from California.",
       font=SANS(15), fill=NAVY)

# ---------------- ALSO list ----------------
y = section_head(my + 332, "ALSO ON FRIDAY 20 NOVEMBER  —  17 TO 50")
ALSO = [
    "COP31 final day in Antalya: $120bn adaptation goal on the table",
    "Test cricket: Nicholls 113*, New Zealand 243/5 v India",
    "APEC leaders meet in Shenzhen; Xi urges open trade",
    "Fire at the ancestral home of Muhammad Yunus",
    "Sensex 83,021.75; Nifty crosses 25,500",
    "Trump invites Putin to the G20 in Miami",
    "US jobless claims: 203,000",
    "EU–UK summit opens in Brussels",
    "India beat Malaysia at the Hong Kong Open",
    "Women's Asian Hockey Champions Trophy begins",
    "Amur falcons cross the Arabian Sea",
    "NATO assembly opens its 72nd session",
    "Argentina 0–2 Australia at the U17 World Cup",
    "EU gas storage rules; methane rules in 24 months",
    "Modi pitches India at the FICCI centenary",
    "COP31: India pushes climate resilience",
    "Google's Gemini 4 enters the AI race (reported)",
    "India launches its own H5N1 bird-flu vaccine",
    "Pakistan PM to lead the SCO delegation",
    "Kenya's IEBC visits Nigeria on election readiness",
    "UK consumer sentiment edges up; GfK index −22",
    "Trump defers the Iran war decision to 2027",
    "Anthropic shares close 17% higher on day one",
    "US pulls military aircraft from a UK air base",
    "South Africa beat Bangladesh on day five",
    "Railways cancel 10 trains, divert 23 for Akvan",
    "ISRO names four astronaut candidates for Gaganyaan",
    "UGC-NET December exams set for 14–21 December",
    "World Children's Day marked around the globe",
    "NDRF sends 31 teams to five states for Akvan",
    "IFFI opens in Goa; Cherry Blossom Festival in Shillong",
    "S&P 500 −2.02%, Nasdaq −2.25% in the slide",
    "India and Japan fast-track UNICORN defence deals",
    "EPFO raises PF withdrawal limit to 90%",
]
assert len(ALSO) == 34, len(ALSO)
ay = y + 8
for i, item in enumerate(ALSO):
    n = 17 + i
    col = i // 17
    row = i % 17
    ax = 24 + col * 788
    ayy = ay + row * 18
    d.text((ax, ayy), f"{n}.", font=SANS_B(15), fill=RED)
    d.text((ax + 34, ayy), item, font=SANS(15), fill=INK)

# ---------------- DATE CHECK + footer ----------------
dy = ay + 17 * 18 + 12
d.rectangle([24, dy, 1576, dy + 78], fill=LIGHT, outline=RED, width=2)
d.text((40, dy + 8), "DATE CHECK — LEFT OUT, BECAUSE THEY HAPPENED EARLIER:",
       font=SANS_B(17), fill=RED)
text_block(40, dy + 32, "Van Gogh's record $190.4m sale (reported 19 Nov)  ·  The Crimean Bridge span that fell on 17–18 Nov — today's news is the new strike that halted rail  ·  Anthropic's $83 IPO price (set 19 Nov; today its shares closed 17% higher).",
           SANS(16), INK, 1520, lh=20)
fy = dy + 92
rule(fy, 24, 1576, 2)
foot = "Every story here happened or was first reported on Friday 20 November 2026.  Sources: Reuters, AP, AFP, BBC, The Hindu, Space.com, NDTV.  ·  THE DAILY GLOBE — 50 stories, one page."
text_block(24, fy + 10, foot, SANS(15), GREY, 1552, lh=19, align="center")

img.save("/home/hatch/workspace/makefun/news-image-20261120-cand-b/entry.png",
         optimize=True)
print("saved", img.size)
