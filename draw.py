#!/usr/bin/env python3
"""Draw entry.png for news-image-20261122: a dark night-desk front page.

The World in One Day, Sunday 22 November 2026. Everything is drawn in
code with PIL and DejaVu fonts: no photo, no copied art, no network.
"""
import math
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SERIF = FONT_DIR + "DejaVuSerif.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"

NAVY = (10, 17, 40)
PANEL = (19, 30, 66)
PANEL2 = (16, 26, 56)
GOLD = (232, 193, 90)
CREAM = (242, 234, 216)
MUTED = (154, 167, 199)
RED = (229, 87, 46)
TEAL = (46, 196, 182)
SKY = (96, 165, 220)
LINE = (43, 58, 102)
DOT = (201, 168, 106)

_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def wrap(text, fnt, width):
    """Wrap text to a pixel width, returning a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if _draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(x, y, lines, fnt, fill, spacing=3):
    for line in lines:
        _draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def hline(y, x0=24, x1=1000, fill=LINE, width=1):
    _draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- map
# Rough continent outlines in (longitude, latitude). Dots land only
# inside these shapes, which makes the world map read as a map.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-60, 60),
     (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-90, 21), (-97, 16),
     (-105, 20), (-115, 28), (-125, 40), (-125, 49), (-145, 60), (-168, 66)],
    [(-58, 64), (-45, 60), (-30, 68), (-25, 76), (-45, 80), (-60, 76),
     (-58, 64)],
    [(-80, 10), (-60, 8), (-50, 0), (-40, -5), (-35, -8), (-40, -20),
     (-48, -28), (-58, -35), (-65, -45), (-70, -55), (-75, -40),
     (-80, -20), (-80, 10)],
    [(-10, 36), (-9, 43), (0, 46), (-2, 50), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 59), (30, 60), (30, 70), (20, 70),
     (15, 68), (10, 64), (5, 60), (0, 55), (-5, 50), (-10, 36)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31),
     (35, 28), (43, 12), (51, 11), (48, 0), (40, -10), (35, -20),
     (30, -30), (20, -35), (15, -30), (12, -18), (9, -1), (9, 4),
     (-8, 5), (-17, 15)],
    [(30, 70), (40, 68), (55, 69), (70, 72), (90, 75), (110, 76),
     (140, 72), (160, 70), (180, 66), (170, 60), (162, 55), (158, 50),
     (142, 45), (140, 38), (130, 35), (127, 40), (122, 38), (120, 30),
     (110, 20), (105, 10), (100, 8), (95, 15), (90, 22), (85, 20),
     (80, 13), (77, 8), (72, 20), (65, 25), (58, 26), (52, 28),
     (48, 30), (42, 36), (35, 36), (30, 42), (30, 70)],
    [(113, -22), (114, -30), (120, -34), (130, -32), (140, -38),
     (150, -37), (153, -27), (146, -19), (142, -11), (136, -12),
     (132, -11), (126, -14), (122, -17), (113, -22)],
]


def inside_poly(lon, lat, poly):
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if (yi > lat) != (yj > lat):
            xint = (xj - xi) * (lat - yi) / (yj - yi) + xi
            if lon < xint:
                inside = not inside
        j = i
    return inside


def lonlat_to_xy(lon, lat, mx, my, mw, mh):
    x = mx + (lon + 180.0) / 360.0 * mw
    y = my + (72.0 - lat) / 130.0 * mh
    return x, y


def draw_map(mx, my, mw, mh):
    # graticule
    for gx in range(-150, 181, 30):
        x, _ = lonlat_to_xy(gx, 0, mx, my, mw, mh)
        _draw.line([(x, my), (x, my + mh)], fill=(23, 35, 68), width=1)
    for gy in range(60, -60, -30):
        _, y = lonlat_to_xy(0, gy, mx, my, mw, mh)
        _draw.line([(mx, y), (mx + mw, y)], fill=(23, 35, 68), width=1)
    # dotted land
    step = 6
    for px in range(mx, mx + mw, step):
        for py in range(my, my + mh, step):
            lon = (px - mx) / mw * 360.0 - 180.0
            lat = 72.0 - (py - my) / mh * 130.0
            if any(inside_poly(lon, lat, poly) for poly in CONTINENTS):
                _draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=DOT)


def pin(x, y, number):
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([x - 12, y - 12, x + 12, y + 12], fill=(229, 87, 46, 70))
    gd.ellipse([x - 9, y - 9, x + 9, y + 9], fill=(229, 87, 46, 255))
    _img.paste(Image.alpha_composite(_img.convert("RGBA"), glow).convert("RGB"),
               (0, 0))
    _draw.ellipse([x - 9, y - 9, x + 9, y + 9], outline=(255, 255, 255),
                  width=2)
    label = str(number)
    fnt = font(SANS_B, 11)
    tw = _draw.textlength(label, font=fnt)
    _draw.text((x - tw / 2, y - 7), label, font=fnt, fill=(255, 255, 255))


# ------------------------------------------------------------- scenes
def scene_cop31(x, y, w, h):
    _draw.rectangle([x, y, x + w, y + h], fill=(23, 48, 84))
    _draw.rectangle([x, y + h - 22, x + w, y + h], fill=(16, 34, 62))
    # long table with delegates
    _draw.rectangle([x + 20, y + h - 46, x + w - 20, y + h - 38],
                    fill=(232, 193, 90))
    for i, cx in enumerate([x + 45, x + 100, x + 155, x + 210, x + 265]):
        _draw.ellipse([cx - 11, y + h - 70, cx + 11, y + h - 48],
                      fill=(242, 234, 216))
        _draw.rectangle([cx - 12, y + h - 48, cx + 12, y + h - 44],
                        fill=[(46, 196, 182), (229, 87, 46), (96, 165, 220),
                              (232, 193, 90), (154, 167, 199)][i])
    # clock showing 03:00, top right
    cx, cy, r = x + w - 36, y + 26, 16
    _draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(242, 234, 216),
                  outline=GOLD, width=3)
    _draw.line([(cx, cy), (cx, cy - 10)], fill=NAVY, width=3)
    _draw.line([(cx, cy), (cx + 9, cy)], fill=NAVY, width=3)
    _draw.text((x + 12, y + 8), "03:00 GMT", font=font(SANS_B, 13),
               fill=GOLD)


def scene_kyiv(x, y, w, h):
    _draw.rectangle([x, y, x + w, y + h], fill=(8, 12, 30))
    # skyline
    base = y + h
    for bx, bw, bh in [(0, 34, 34), (40, 26, 52), (72, 30, 40),
                       (108, 24, 58), (138, 30, 36), (174, 26, 50),
                       (206, 30, 42), (242, 26, 56), (274, 30, 38)]:
        _draw.rectangle([x + bx, base - bh, x + bx + bw, base],
                        fill=(24, 34, 64))
        for wy in range(base - bh + 6, base - 4, 10):
            _draw.rectangle([x + bx + 5, wy, x + bx + 9, wy + 4],
                            fill=(232, 193, 90))
    # explosions
    for ex, ey, r in [(70, 62, 12), (190, 48, 14), (265, 70, 10)]:
        _draw.ellipse([x + ex - r, y + ey - r, x + ex + r, y + ey + r],
                      fill=(255, 140, 40))
        _draw.ellipse([x + ex - r // 2, y + ey - r // 2,
                       x + ex + r // 2, y + ey + r // 2], fill=(255, 220, 120))
    # drone trails
    for dx, dy in [(30, 20), (120, 12), (210, 24), (280, 14)]:
        _draw.line([(x + dx, y + dy + 18), (x + dx + 8, y + dy)],
                   fill=(255, 255, 255), width=2)
        _draw.ellipse([x + dx + 5, y + dy - 3, x + dx + 11, y + dy + 3],
                      fill=(255, 255, 255))


def scene_bahrain(x, y, w, h):
    _draw.rectangle([x, y, x + w, y + h], fill=(58, 28, 22))
    _draw.rectangle([x, y + h - 26, x + w, y + h], fill=(16, 32, 58))
    # tanker
    _draw.rectangle([x + 40, y + h - 52, x + 250, y + h - 30],
                    fill=(30, 30, 36))
    _draw.rectangle([x + 200, y + h - 70, x + 225, y + h - 52],
                    fill=(30, 30, 36))
    _draw.rectangle([x + 40, y + h - 58, x + 250, y + h - 52],
                    fill=(229, 87, 46))
    # flames
    for fx, fh in [(70, 26), (110, 34), (150, 24), (200, 30)]:
        _draw.polygon([(x + fx - 12, y + h - 52), (x + fx, y + h - 52 - fh),
                       (x + fx + 12, y + h - 52)], fill=(255, 140, 40))
        _draw.polygon([(x + fx - 6, y + h - 52), (x + fx, y + h - 52 - fh + 10),
                       (x + fx + 6, y + h - 52)], fill=(255, 220, 120))
    # smoke
    for sx, sy, sr in [(90, 26, 10), (130, 16, 13), (180, 22, 11)]:
        _draw.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr],
                      fill=(90, 90, 100))


def thumb(kind, x, y, w, h):
    _draw.rectangle([x, y, x + w, y + h], fill=PANEL2)
    cx, cy = x + w // 2, y + h // 2
    if kind == "ship":
        _draw.rectangle([x + 12, cy + 2, x + w - 12, cy + 12], fill=RED)
        _draw.polygon([(x + 30, cy + 2), (x + 38, cy - 14), (x + 46, cy + 2)],
                      fill=(255, 140, 40))
        _draw.polygon([(x + 55, cy + 2), (x + 62, cy - 10), (x + 69, cy + 2)],
                      fill=(255, 220, 120))
        _draw.line([(x + 6, cy + 16), (x + w - 6, cy + 16)], fill=SKY, width=2)
    elif kind == "quake":
        _draw.polygon([(x + 8, cy + 12), (x + 26, cy - 12), (x + 44, cy + 12),
                       (x + 62, cy - 8), (x + 80, cy + 12)], fill=(120, 110, 90))
        _draw.line([(x + 4, cy - 2), (x + 20, cy - 2), (x + 26, cy - 12),
                    (x + 34, cy + 8), (x + 44, cy - 2), (x + 60, cy - 2)],
                   fill=RED, width=2)
    elif kind == "boat":
        _draw.arc([x + 14, cy - 10, x + w - 14, cy + 14], 0, 180, fill=GOLD,
                  width=3)
        _draw.line([(x + 6, cy + 16), (x + w - 6, cy + 16)], fill=SKY, width=2)
        _draw.line([(x + 14, cy + 20), (x + w - 14, cy + 20)], fill=SKY,
                   width=2)
    elif kind == "parliament":
        _draw.rectangle([x + 14, cy - 8, x + w - 14, cy + 10], fill=GOLD)
        _draw.polygon([(x + 10, cy - 8), (cx, cy - 20), (x + w - 10, cy - 8)],
                      fill=GOLD)
        for px in (x + 22, x + 42, x + 62):
            _draw.rectangle([px, cy - 2, px + 4, cy + 10], fill=NAVY)
    elif kind == "aid":
        _draw.rectangle([x + 10, cy - 8, x + 52, cy + 8], fill=(242, 234, 216))
        _draw.rectangle([x + 52, cy - 4, x + 68, cy + 8], fill=RED)
        _draw.ellipse([x + 18, cy + 8, x + 26, cy + 16], fill=(20, 20, 26))
        _draw.ellipse([x + 56, cy + 8, x + 64, cy + 16], fill=(20, 20, 26))
    elif kind == "arrest":
        _draw.ellipse([x + 18, cy - 8, x + 38, cy + 12], outline=GOLD, width=3)
        _draw.ellipse([x + 52, cy - 8, x + 72, cy + 12], outline=GOLD, width=3)
        _draw.line([(x + 38, cy + 2), (x + 52, cy + 2)], fill=GOLD, width=3)
    elif kind == "chip":
        _draw.rectangle([x + 28, cy - 12, x + 62, cy + 12], fill=TEAL)
        _draw.rectangle([x + 40, cy - 4, x + 50, cy + 4], fill=NAVY)
        _draw.ellipse([x + 66, cy - 14, x + 84, cy + 4], outline=GOLD, width=3)
        _draw.line([(x + 80, cy + 2), (x + 88, cy + 10)], fill=GOLD, width=3)
    elif kind == "hospital":
        _draw.rectangle([x + 38, cy - 14, x + 52, cy + 14], fill=(242, 234, 216))
        _draw.rectangle([x + 28, cy - 4, x + 62, cy + 4], fill=(242, 234, 216))
        _draw.rectangle([x + 43, cy - 9, x + 47, cy + 9], fill=RED)
        _draw.rectangle([x + 33, cy - 1, x + 57, cy + 3], fill=RED)
    elif kind == "sub":
        _draw.ellipse([x + 10, cy - 8, x + 76, cy + 8], fill=(96, 165, 220))
        _draw.rectangle([x + 40, cy - 14, x + 52, cy - 8], fill=(96, 165, 220))
        _draw.line([(x + 6, cy + 12), (x + w - 6, cy + 12)], fill=SKY, width=2)
    elif kind == "protest":
        for i, px in enumerate([x + 16, x + 34, x + 52, x + 70]):
            _draw.ellipse([px - 5, cy - 12, px + 5, cy - 2], fill=CREAM)
            _draw.rectangle([px - 5, cy - 2, px + 5, cy + 12], fill=CREAM)
        _draw.rectangle([x + 12, cy - 20, x + 40, cy - 12], fill=RED)


# -------------------------------------------------------------- content
LEADS = [
    ("1  ANTALYA, TURKEY · CLIMATE",
     "COP31 climate talks close in on a final deal",
     "A new package lands after a fight over fossil fuels; delegations "
     "have until 03:00 GMT to object before a final plenary.",
     "Reuters, BBC", scene_cop31),
    ("2  KYIV, UKRAINE · WAR",
     "Russia fires 400 drones and 110 missiles at Ukraine",
     "One of the war's largest overnight attacks; at least seven people "
     "are killed in Kyiv, and a strike hits Zelensky's hometown.",
     "Al Jazeera, AP", scene_kyiv),
    ("3  MANAMA, BAHRAIN · IRAN WAR",
     "Iran strikes US bases in Bahrain",
     "An industrial site burns, no injuries reported; tankers are hit in "
     "Hormuz, and a US base in Kuwait is struck too.",
     "Al Jazeera, CNA", scene_bahrain),
]

GRID = [
    ("ship", "4", "GULF OF FINLAND",
     "Russian cargo ship burns after drone strike",
     "Sparta II ablaze; Finland says Ukraine was likely behind it.", "BBC"),
    ("quake", "5", "PERU · ANDES",
     "Magnitude 6.8 quake shakes Peru's Andes",
     "Tremor sends people fleeing in Lima; no deaths at first.",
     "Wire reports"),
    ("boat", "6", "BAYELSA, NIGERIA",
     "Boat carrying mourners capsizes",
     "24 dead as passengers head to a funeral in Bayelsa.", "DW, Sky News"),
    ("parliament", "7", "JERUSALEM",
     "Eisenkot asked to form Israel's government",
     "He invites Likud to talks, seeking the broadest government.",
     "Straits Times"),
    ("aid", "8", "GAZA",
     "Strike hits a food aid vehicle",
     "Three Palestinians die in an air attack.", "Al Jazeera, Reuters"),
    ("arrest", "9", "SINALOA, MEXICO",
     "'El Chapo Isidro' caught in Sinaloa",
     "FBI top-ten fugitive held after a shoot-out; 11 dead.", "Sky News, BBC"),
    ("chip", "10", "WASHINGTON",
     "Nvidia faces a US accounting probe",
     "The SEC inquiry is at an early stage, media report.", "Straits Times"),
    ("hospital", "11", "BRASILIA, BRAZIL",
     "Bolsonaro in intensive care",
     "Ex-president stable, breathing on his own.",
     "Al Jazeera, Reuters"),
    ("sub", "12", "CANBERRA",
     "Marles rejects US report on AUKUS subs",
     "He says the budget office is wrong.", "ABC, Reuters"),
    ("protest", "13", "FRANCE",
     "Protesters rally for a sixth weekend",
     "Crowds march over living costs and public services.", "AFP"),
]

ALSO = [
    ("14", "EU proposes a tax on Big Tech", "Guardian"),
    ("15", "Estonia to close its border with Russia", "AFP"),
    ("16", "Iran to ration electricity as grid strains", "Straits Times"),
    ("17", "Trump vows to work with Democrats to cap card interest at 10%", "AFP"),
    ("18", "Pentagon moves to restrict US-Canada defence ties", "AFP"),
    ("19", "Belgium faces air traffic shutdown from Monday's strike", "AFP"),
    ("20", "Brazil town clears rubble after a deadly storm", "AFP"),
    ("21", "Wildberries CEO steps down days after EU sanctions", "Arab News"),
    ("22", "Rohingyas hail the genocide verdict on Myanmar", "Manila Times"),
    ("23", "North Korea's Kim visits factory sites after a 'Trump snub'", "Manila Times"),
    ("24", "11 dead after drinking tainted alcohol in India's Manipur", "Manila Times"),
    ("25", "Opposition protests hit Meta offices in India", "Manila Times"),
    ("26", "Houthis launch revenge strikes on the Saudi capital", "Manila Times"),
    ("27", "KL Rahul's 136 puts India ahead against New Zealand", "Hindustan Times"),
    ("28", "England thrash the All Blacks 37-12, a record win", "Sunday Times"),
    ("29", "Verstappen takes Las Vegas pole", "Gulf Today"),
    ("30", "Arsenal held 2-2 by Chelsea", "Reuters"),
    ("31", "South Korea's Lee: speed is decisive in the AI race", "Manila Times"),
    ("32", "Japanese forces to use Indian facilities for live-fire training", "Daily Jagran"),
    ("33", "Air India extends its Jeddah suspension to 24 Nov", "Daily Jagran"),
    ("34", "Democrats' Senate leadership vote tests them early", "AP"),
    ("35", "Ex-Italian police chief De Gennaro dies by suicide", "AFP"),
]

NUMBERS = [
    ("~200", "nations at the COP31 talks"),
    ("400+", "drones fired at Ukraine"),
    ("110", "missiles in the same night"),
    ("6.8", "magnitude of the Peru quake"),
    ("24", "dead as a boat capsizes"),
]

# ---------------------------------------------------------------- draw
_img = Image.new("RGB", (W, H), NAVY)
_draw = ImageDraw.Draw(_img)

# top strip
_draw.rectangle([0, 0, W, 28], fill=(7, 12, 30))
_draw.text((24, 7), "THE WORLD IN ONE DAY  ·  NIGHT DESK EDITION",
           font=font(SANS_B, 12), fill=GOLD)
right = "SUNDAY 22 NOVEMBER 2026"
_draw.text((1000 - _draw.textlength(right, font=font(SANS_B, 12)), 7), right,
           font=font(SANS_B, 12), fill=CREAM)

# masthead
title = "Sunday 22 November 2026"
tf = font(SERIF_B, 46)
_draw.text(((W - _draw.textlength(title, font=tf)) / 2, 34), title,
           font=tf, fill=CREAM)
sub = ("COP31 near a deal  ·  Russia's 400-drone barrage  ·  "
       "Iran hits US bases in Bahrain")
sf = font(SERIF, 16)
_draw.text(((W - _draw.textlength(sub, font=sf)) / 2, 88), sub,
           font=sf, fill=GOLD)
hline(108, fill=GOLD, width=2)

# numbers strip
cell_w = 976 / 5
for i, (num, label) in enumerate(NUMBERS):
    x = 24 + i * cell_w
    nf = font(SANS_B, 28)
    _draw.text((x + 8, 118), num, font=nf, fill=GOLD)
    lf = font(SANS, 11)
    for j, line in enumerate(wrap(label, lf, cell_w - 16)):
        _draw.text((x + 8, 150 + j * 13), line, font=lf, fill=MUTED)
    if i:
        _draw.line([(x, 118), (x, 158)], fill=LINE, width=1)
hline(164)

# map label
_draw.text((24, 170), "WHERE IT HAPPENED — pins match story numbers",
           font=font(SANS_B, 11), fill=GOLD)
_draw.text((1000 - _draw.textlength("35 STORIES · 6 REGIONS",
           font=font(SANS_B, 11)), 170), "35 STORIES · 6 REGIONS",
           font=font(SANS_B, 11), fill=MUTED)

# hero map
MAP_X, MAP_Y, MAP_W, MAP_H = 24, 186, 976, 190
_draw.rectangle([MAP_X, MAP_Y, MAP_X + MAP_W, MAP_Y + MAP_H], fill=PANEL)
draw_map(MAP_X + 6, MAP_Y + 4, MAP_W - 12, MAP_H - 8)
PINS = {
    1: (30.7, 36.9), 2: (30.5, 50.45), 3: (50.6, 26.2),
    4: (24.0, 59.8), 5: (-75.0, -10.0), 6: (6.5, 5.0),
    7: (35.2, 31.8), 8: (34.5, 31.5), 9: (-107.0, 24.5),
    10: (-77.0, 38.9), 11: (-47.9, -15.8), 12: (149.0, -35.3),
    13: (2.35, 48.85),
}
# Gaza (8) sits almost on top of Jerusalem (7), and the Gulf of Finland
# (4) crowds Kyiv (2): nudge those pins aside with leader lines so every
# number stays readable.
PIN_OFFSETS = {8: (10.0, -8.0), 4: (-7.0, -7.0), 7: (2.0, 7.0)}
for num, (lon, lat) in PINS.items():
    px, py = lonlat_to_xy(lon, lat, MAP_X + 6, MAP_Y + 4, MAP_W - 12,
                          MAP_H - 8)
    if num in PIN_OFFSETS:
        dlon, dlat = PIN_OFFSETS[num]
        qx, qy = lonlat_to_xy(lon + dlon, lat + dlat, MAP_X + 6, MAP_Y + 4,
                              MAP_W - 12, MAP_H - 8)
        _draw.line([(px, py), (qx, qy)], fill=(255, 255, 255), width=1)
        px, py = qx, qy
    pin(px, py, num)
_draw.rectangle([MAP_X, MAP_Y, MAP_X + MAP_W, MAP_Y + MAP_H],
                outline=LINE, width=1)

# lead stories
lead_x = [24, 360, 696]
lead_w = 304
for (kicker, head, summ, src, scene), x in zip(LEADS, lead_x):
    y = 384
    scene(x, y, lead_w, 92)
    _draw.rectangle([x, y, x + lead_w, y + 92], outline=LINE, width=1)
    y += 102
    _draw.text((x, y), kicker, font=font(SANS_B, 11), fill=RED)
    y += 16
    hf = font(SERIF_B, 19)
    y = text_block(x, y, wrap(head, hf, lead_w), hf, CREAM, spacing=2)
    y += 2
    bf = font(SANS, 12)
    y = text_block(x, y, wrap(summ, bf, lead_w), bf, MUTED, spacing=2)
    _draw.text((x, y + 2), src, font=font(SANS, 10), fill=GOLD)

# grid label
hline(622)
_draw.text((24, 628), "TEN MORE STORIES", font=font(SANS_B, 11), fill=GOLD)

# grid of ten
gw, gh = 188, 90
gx0, gy0 = 24, 644
for idx, (kind, num, place, head, summ, src) in enumerate(GRID):
    col, row = idx % 5, idx // 5
    x = gx0 + col * (gw + 10)
    y = gy0 + row * (gh + 8)
    thumb(kind, x, y, gw, 30)
    _draw.text((x, y + 34), f"{num}  {place}", font=font(SANS_B, 9),
               fill=RED)
    hf = font(SANS_B, 11)
    head_lines = wrap(head, hf, gw)[:2]
    yy = y + 46
    for line in head_lines:
        _draw.text((x, yy), line, font=hf, fill=CREAM)
        yy += 12
    bfnt = font(SANS, 9)
    for line in wrap(f"{summ} ({src})", bfnt, gw)[:2]:
        _draw.text((x, yy), line, font=bfnt, fill=MUTED)
        yy += 10

# also list
hline(838)
_draw.text((24, 844), "ALSO ON SUNDAY — 22 MORE STORIES",
           font=font(SANS_B, 11), fill=GOLD)
col_w = 488
for i, (num, text, src) in enumerate(ALSO):
    col, row = i // 11, i % 11
    x = 24 + col * col_w
    y = 860 + row * 9.5
    _draw.text((x, y), num, font=font(SANS_B, 9), fill=GOLD)
    fnt = font(SANS, 9)
    _draw.text((x + 20, y), text, font=fnt, fill=CREAM)
    tw = _draw.textlength(text, font=fnt)
    _draw.text((x + 20 + tw + 4, y), f"({src})", font=fnt, fill=MUTED)

# footer
hline(970)
_draw.rectangle([24, 976, 1000, 1008], fill=(19, 30, 66))
_draw.text((32, 982),
           "DATE CHECK — Wires read to 01:00 UTC, Sunday 22 Nov 2026. Every "
           "story was reported or still developing on 22 Nov in at least one "
           "time zone.",
           font=font(SANS, 10), fill=CREAM)
_draw.text((24, 1014),
           "Sources: Reuters, BBC, Al Jazeera, AP, AFP, DW, Sky News, CNA, "
           "Straits Times, ABC Australia, Times of India, Guardian, Kyiv "
           "Independent. Pictures and map: original, drawn in code.",
           font=font(SANS, 9), fill=MUTED)

_img.save(OUT)
print("saved", OUT, _img.size)
