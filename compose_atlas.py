#!/usr/bin/env python3
"""THE TUESDAY ATLAS - compose engine for Akun 10 (@sindyariana115203),
news-image-20261124, Wave 1. Written fresh in this build session.

Renders the Tuesday 24 November 2026 front page wide (3900 px), then fits
the winning variant whole onto a 1024x1024 page-coloured canvas and
quantises to 256 colours. Usage: python3 compose_atlas.py A|B
Writes compose_<V>.png (wide) and entry_<V>.png (1024x1024, the entry).

Palette: navy / cream, red + gold accents. Layout A: 3 lead cards in a row,
12 mini cards in 4x3, dotted world map bottom-left, ALSO ON bottom-right.
All facts come from the locked NI24 pool (ni24-pool.md + 07:00 refresh);
no invented numbers, no Monday times presented as Tuesday times.
"""
import sys

from PIL import Image, ImageDraw, ImageFont

FONT_DIR = "/home/hatch/workspace/makefun/ni22-stage/fonts"

# ---------------------------------------------------------------- palette
PAGE = (247, 241, 227)      # cream paper
PAPER = (255, 253, 246)     # card paper
INK = (20, 38, 74)          # navy ink
INK_SOFT = (43, 63, 105)
RED = (179, 39, 30)
GOLD = (196, 154, 60)
GOLD_SOFT = (232, 205, 130)
TEAL = (47, 107, 122)
GREEN = (46, 107, 79)
BROWN = (107, 91, 46)
GREY = (90, 90, 84)
DATE_BG = (246, 226, 224)
WHITE = (255, 255, 255)
BLACK = (12, 12, 12)

REGION_COLORS = {
    "EUROPE": (31, 58, 110),
    "MIDDLE EAST": (140, 47, 38),
    "AMERICAS": (46, 107, 79),
    "OCEANIA": (47, 107, 122),
    "WORLD": (107, 91, 46),
}

# ---------------------------------------------------------------- fonts
def _font(name, size):
    try:
        return ImageFont.truetype(FONT_DIR + "/" + name, size)
    except OSError:
        return ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)


def fonts():
    return {
        "mast": _font("PlayfairDisplay-Black.ttf", 330),
        "date": _font("PlayfairDisplay-Black.ttf", 138),
        "head_lead": _font("Archivo-Bold.ttf", 62),
        "head_mini": _font("Archivo-Bold.ttf", 46),
        "deck_lead": _font("Archivo.ttf", 35),
        "deck_mini": _font("Archivo.ttf", 32),
        "body": _font("Archivo.ttf", 32),
        "brief": _font("Archivo.ttf", 30),
        "mono": _font("IBMPlexMono-Bold.ttf", 34),
        "mono_sm": _font("IBMPlexMono-Bold.ttf", 29),
        "mono_lg": _font("IBMPlexMono-Bold.ttf", 76),
        "chip": _font("IBMPlexMono-Bold.ttf", 30),
        "label": _font("IBMPlexMono-Bold.ttf", 27),
        "pin": _font("IBMPlexMono-Bold.ttf", 36),
        "num": _font("IBMPlexMono-Bold.ttf", 88),
    }


F = fonts()

# ---------------------------------------------------------------- data
# Cards: (num, region, place, topic, headline, deck, chip, source, reported, scene)
CARDS = [
    (1, "EUROPE", "BENGHAZI, LIBYA", "WAR",
     "Ukraine sinks Russian warship Merkury off Libya",
     "7 sea drones launched at the Steregushchiy-class corvette; a Ka-27 "
     "combat helicopter was destroyed aboard and the cargo vessel MV Angara "
     "was hit. Zelenskyy announced the sinking on Monday.",
     "7 SEA DRONES", "CNN / Times / WSJ / AP", "REPORTED 23 NOV", "merkury"),
    (4, "WORLD", "ANTALYA, TURKIYE", "CLIMATE",
     "COP31 ends with no deal - first since 2000",
     "The Antalya Pact cover decision was not adopted and the final text "
     "dropped every mention of fossil fuels. 44 hours overtime, the longest "
     "COP ever; talks carry to COP32 in Addis Ababa, November 2027.",
     "NO DEAL", "Times / Guardian", "REPORTED 23 NOV", "cop31"),
    (11, "OCEANIA", "WELLINGTON", "CRICKET",
     "New Zealand bat out draw with India",
     "NZ 239/5 - Mitchell 49* off 186 balls, Phillips 26* off 126, a "
     "63-run stand over 258 balls. India 720/9d (Rahul 136, Pant 128, "
     "Gill 98); NZ 368 (Nicholls 175*, Phillips 118). 2nd Test Christchurch "
     "27 Nov-1 Dec.",
     "DRAW 239/5", "HS / WicketPulse", "REPORTED 23 NOV", "cricket"),
    (2, "EUROPE", "GULF OF FINLAND", "SEA",
     "Russian cargo ship Sparta II hit, towed clear",
     "Hit by 2 drones on Saturday; Finland led the Loviisa rescue and all "
     "16 crew were taken off. The 121 m ship was towed out of Finnish "
     "waters on Sunday night.",
     "121 M SHIP", "Reuters / Times / WSJ", "REPORTED 22-23 NOV", "sparta"),
    (3, "EUROPE", "KYIV REGION, UKRAINE", "WAR",
     "Russian strikes kill at least 15 near Kyiv",
     "Kyiv strikes kill at least 15 near the capital: 11 killed in a block "
     "of flats in Dymer; a drone hit a 6-floor building in Kyiv on Monday, "
     "5 injured. Zelenskyy to CNN on Putin: for us, he is a killer.",
     "15 KILLED", "Times / AP", "REPORTED 23 NOV", "kyiv"),
    (5, "MIDDLE EAST", "WASHINGTON", "SANCTIONS",
     "US sanctions about 30 Iran-linked exchange houses",
     "Iran sanctions hit about 30 exchange houses and executives on Monday, "
     "the core of shadow banking evading sanctions on Iranian banks.",
     "ABOUT 30 HIT", "AP / Treasury", "REPORTED 23 NOV", "bank"),
    (6, "MIDDLE EAST", "GAZA CITY", "CONFLICT",
     "Israeli strikes kill 3 in Gaza",
     "3 killed on Monday in separate strikes, including a UNRWA employee. "
     "Shifa Hospital and the agency confirm the deaths.",
     "3 KILLED", "AP", "REPORTED 23 NOV", "gaza"),
    (7, "MIDDLE EAST", "WESTERN YEMEN", "WAR",
     "Strike kills 11 in western Yemen",
     "Houthis say a Saudi-backed forces strike on Monday killed 11 and "
     "wounded 19 in western Yemen.",
     "11 KILLED", "AP", "REPORTED 23 NOV", "yemen"),
    (8, "AMERICAS", "MARKETS", "GOLD",
     "Gold rebounds 1.5% to $3,588",
     "Bullion rose 1.5% on Monday after its worst week in 8 months, off a "
     "14-month low. Traders await the US PCE inflation report due 25 Nov; "
     "the 10-year yield sits near 4.96%.",
     "$3,588 / OZ", "Reuters", "REPORTED 23 NOV", "gold"),
    (9, "WORLD", "CRYPTO", "MARKETS",
     "Bitcoin steadies near $61,284",
     "Quoted $61,284 on Monday at 12:52 UTC, up 1.1% in 24 hours and down "
     "4.5% in 7 days; the weekend low was about $55,100 as leveraged "
     "liquidations eased.",
     "$61,284", "CoinPaprika", "REPORTED 23 NOV", "bitcoin"),
    (10, "AMERICAS", "LOS ANGELES", "BUSINESS",
     "GTA VI takes $3.8bn on day one",
     "The biggest entertainment launch on record - past every game launch "
     "and single-day film box office. $3.8 billion in the first day.",
     "$3.8BN DAY ONE", "ActiveInvestorMag", "REPORTED 23 NOV", "gta"),
    (12, "EUROPE", "LIVERPOOL", "FOOTBALL",
     "Liverpool 4-0 Man Utd; Pochettino debut disaster",
     "Yoro was sent off in the 8th minute and United played with 10 men. "
     "The loss leaves United 19th in the Premier League, on 8 points.",
     "4-0", "Mint / NextSportsWeb", "REPORTED 23 NOV", "football"),
    (13, "AMERICAS", "WASHINGTON", "POLITICS",
     "Trump: work with Democrats to cap card rates",
     "Trump says he would work with Democrats to cap credit-card rates. "
     "Van Hollen challenges Schumer for Senate leader; secret ballot 1 Dec.",
     "RATE CAP", "ActiveInvestorMag", "REPORTED 23 NOV", "capitol"),
    (14, "AMERICAS", "WASHINGTON", "POLITICS",
     "Democrats take both chambers",
     "Democrats 258-173: largest House majority since 1992, after the North "
     "Carolina pickup. Democrats hold both chambers of Congress.",
     "258-173", "BBC / ActiveInvestorMag", "REPORTED 23 NOV", "tally"),
    (20, "AMERICAS", "NEW YORK", "MARKETS",
     "Nvidia brings back Jensen Huang as CEO",
     "The board reinstated Huang effective immediately on Monday. Shares "
     "jumped 31%; the Nasdaq rose 6%, the S and P 500 5%, the chip index 12%.",
     "+31% HUANG BACK", "Reuters", "REPORTED 23 NOV", "chip"),
]

LEAD_NUMS = (1, 4, 11)
MINI_NUMS = (2, 3, 5, 6, 7, 8, 9, 10, 12, 13, 14, 20)

# Briefs 16-42: (text, source)
BRIEFS = [
    ("Nepal PM Balendra Shah ends Delhi state visit; met Modi Monday", "IANS"),
    ("Thousands march in Lisbon over cost of living", "JagranJosh"),
    ("UK-EU Brexit reset deal: Burnham calls it landmark to parliament", "BBC"),
    ("India-EU free-trade pact likely signed 16 Dec in Brussels", "JagranJosh"),
    ("Tata Steel sells pipe business to APL Apollo, Rs 28,000 crore", "ObserverVoice"),
    ("SpiceJet pilot seeks urgent financial + safety audit; IndiGo holds 65.9% domestic", "ObserverVoice"),
    ("IFFI 2026 hosts BRICS Roundtable in Goa", "ObserverVoice"),
    ("Modi inaugurates AI Centre at IIT Patna + Rs 400 crore research projects", "ObserverVoice"),
    ("Amit Shah launches Rs 4,000 crore infra push in Arunachal Pradesh", "ObserverVoice"),
    ("JEE Main 2027 Session 1 registration closes today", "JagranJosh"),
    ("NEET PG 2026: 10,105 medical seats flagged blocked", "JagranJosh"),
    ("Google invests $5m in AI research at IIT Kharagpur", "JagranJosh"),
    ("US stocks fall again as AI shares swing; Nasdaq 100 futures +3% Monday", "AP"),
    ("Morgan Stanley Wilson most bullish on stocks since April: sell-off a fat pitch", "ActiveInvestorMag"),
    ("Goldman sees +18% S and P 500 through 2027, Brent $88, gold $4,650", "ActiveInvestorMag"),
    ("KOSPI falls about 3% Monday to 10-month low; Taiwan steadies", "Reuters"),
    ("Miley Cyrus marries Maxx Morando in California", "BBC"),
    ("FBI probes hack of its crime database; Washington State pauses van-dealer checks", "AP"),
    ("Solana launches solana.ai, a platform for autonomous AI agents to transact", "Gadgets360"),
    ("Chainflip offers attacker behind $12m theft a 10% bounty; deadline 23 Nov", "Gadgets360"),
    ("Kraken CAD flash crash to about $17,000 equivalent on Saturday; trades stand", "BitcoinWorld"),
    ("HKMA explores AI agents to trace crypto crime as stablecoins dominate illicit flows", "HK News TV"),
    ("Hong Kong CPI rises 2.2% year on year in October", "HK News TV"),
    ("UN AI weapons talks continue; states agree to keep negotiating lethal autonomous weapons", "salonvision"),
    ("North Korea weighs shutting Swiss office in Pyongyang", "Reuters, Tue 04:24 WIB"),
    ("Congo halts cobalt exports from 30 Nov until further notice", "Reuters"),
    ("Indonesia: 24 killed in factory blaze, rescuers search for dozens missing", "Reuters"),
]

# Numbers strip: (big, small)
NUMBERS = [
    ("7", "SEA DRONES - MERKURY SUNK"),
    ("NO DEAL", "COP31 - FIRST SINCE 2000"),
    ("44 H", "COP OVERTIME - LONGEST EVER"),
    ("$3,588", "GOLD 3588 +1.5% MON"),
    ("$61,284", "BITCOIN 61284 12:52 UTC"),
    ("+31%", "NVIDIA - HUANG RETURNS"),
    ("$3.8BN", "GTA VI DAY ONE"),
    ("239/5", "NZ DRAW WELLINGTON"),
]

# Timeline: (time, text) - times as reported, zones written out.
TIMELINE = [
    ("04:24 WIB TUE", "KCNA: North Korea weighs closing its Swiss office in Pyongyang - Reuters"),
    ("21:39 HKT MON", "Hong Kong sets airspace curbs for the Interpol summit, 30 Nov-3 Dec - HK News TV"),
    ("12:52 UTC MON", "Bitcoin quoted $61,284 as leveraged liquidations ease - CoinPaprika"),
    ("MON EVENING", "Zelenskyy announces the Merkury sinking; US Treasury sanctions about 30 Iran exchange houses"),
    ("SUN NIGHT", "Sparta II towed out of Finnish waters; COP31 closing plenary ends with no deal"),
    ("00:02 UTC MON", "UN states agree to keep negotiating lethal AI weapons - salonvision"),
]

# DATE CHECK: named, dated discards - NOT Tuesday's news.
DATECHECK = [
    ("186-drone night over Ukraine, 161 downed", "Fri 21-Sun 22 Nov"),
    ("Hong Kong Election Committee: 856 candidates, 723 seats", "Sun 22 Nov"),
    ("Alcaraz beats Zverev 6-2, 7-6(9-7), first ATP Finals title", "Sun 22 Nov"),
    ("Verstappen wins Las Vegas Grand Prix", "Sun 22 Nov"),
    ("Wembanyama scores 50, Spurs 114-91 Pelicans", "Sun 22 Nov"),
    ("India declare 720/9 - the DRAW is Monday's news", "Sun 22 Nov"),
    ("Nvidia CEO Jensen Huang resigns after affair admission", "Thu 12 Nov"),
]

# Map pins: (card num, lon, lat)
PINS = [
    (1, 20.0, 32.1), (2, 25.0, 60.0), (3, 30.5, 50.5), (4, 30.7, 36.9),
    (5, -77.5, 38.8), (6, 34.5, 31.5), (7, 44.0, 15.0), (8, -0.1, 51.5),
    (9, -122.0, 37.8), (10, -118.2, 34.0), (11, 174.8, -41.3),
    (12, -3.0, 53.4), (13, -76.0, 40.0), (14, -78.6, 35.8), (20, -74.0, 40.7),
]

# ---------------------------------------------------------------- helpers
def wrap(draw, text, font, width):
    """Greedy word wrap to pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_center(draw, cx, y, text, font, fill):
    draw.text((cx - draw.textlength(text, font=font) / 2, y), text,
              font=font, fill=fill)


def star(draw, cx, cy, r, fill):
    pts = []
    import math
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def waves(draw, x0, y0, x1, y1, color, n=5):
    import math
    for k in range(n):
        yy = y0 + (y1 - y0) * (k + 0.5) / n
        pts = []
        for xx in range(int(x0), int(x1) + 1, 24):
            pts.append((xx, yy + 10 * math.sin((xx - x0) / 90.0 + k)))
        draw.line(pts, fill=color, width=7)


def skyline(draw, x0, ybase, x1, color, seed=0):
    import random
    rnd = random.Random(seed)
    x = x0
    while x < x1 - 30:
        w = rnd.randint(46, 110)
        h = rnd.randint(60, 190)
        draw.rectangle([x, ybase - h, x + w, ybase], fill=color)
        x += w + 14


# ---------------------------------------------------------------- scenes
def scene(draw, kind, x, y, w, h, variant):
    """Flat layered scene strip inside box (x, y, w, h)."""
    bg = {
        "merkury": (23, 52, 96), "cop31": (122, 62, 32),
        "cricket": (34, 96, 58), "sparta": (52, 74, 110),
        "kyiv": (58, 58, 66), "bank": (88, 66, 32),
        "gaza": (96, 66, 44), "yemen": (110, 74, 40),
        "gold": (146, 110, 32), "bitcoin": (196, 122, 24),
        "gta": (74, 42, 96), "football": (26, 92, 52),
        "capitol": (44, 66, 104), "tally": (36, 58, 96),
        "chip": (24, 68, 66),
    }[kind]
    if variant == "B":
        bg = tuple(max(0, c - 18) for c in bg)
    draw.rectangle([x, y, x + w, y + h], fill=bg)
    cx, cy = x + w / 2, y + h / 2
    if kind == "merkury":
        waves(draw, x, y + h * 0.55, x + w, y + h * 0.95, (150, 190, 235))
        draw.polygon([(x + w * 0.28, y + h * 0.62), (x + w * 0.72, y + h * 0.62),
                      (x + w * 0.62, y + h * 0.38), (x + w * 0.38, y + h * 0.38)],
                     fill=(16, 28, 54))
        draw.rectangle([x + w * 0.44, y + h * 0.18, x + w * 0.50, y + h * 0.40],
                       fill=(16, 28, 54))
        star(draw, x + w * 0.74, y + h * 0.30, 46, (255, 176, 32))
        for i in range(7):
            dx = x + w * (0.12 + 0.11 * i)
            dy = y + h * (0.14 + (0.06 if i % 2 else 0.0))
            draw.ellipse([dx - 12, dy - 8, dx + 12, dy + 8], fill=(230, 230, 230))
            draw.line([dx, dy + 8, dx, dy + 26], fill=(230, 230, 230), width=4)
    elif kind == "cop31":
        draw.ellipse([cx - 150, cy - 150, cx + 150, cy + 150], fill=(232, 176, 64))
        draw.rectangle([x + w * 0.08, y + h * 0.72, x + w * 0.92, y + h * 0.78],
                       fill=(232, 205, 130))
        for i in range(5):
            bx = x + w * (0.14 + 0.17 * i)
            draw.rectangle([bx, y + h * 0.52, bx + 70, y + h * 0.72],
                           fill=(247, 241, 227))
            draw.rectangle([bx + 8, y + h * 0.44, bx + 62, y + h * 0.52],
                           fill=(247, 241, 227))
        draw.line([x + w * 0.30, y + h * 0.30, x + w * 0.70, y + h * 0.66],
                  fill=(179, 39, 30), width=26)
        draw.line([x + w * 0.70, y + h * 0.30, x + w * 0.30, y + h * 0.66],
                  fill=(179, 39, 30), width=26)
    elif kind == "cricket":
        draw.ellipse([x + w * 0.06, y + h * 0.10, x + w * 0.94, y + h * 0.92],
                     fill=(64, 140, 84))
        draw.ellipse([x + w * 0.30, y + h * 0.26, x + w * 0.70, y + h * 0.76],
                     fill=(232, 205, 130))
        draw.rectangle([cx - 8, y + h * 0.30, cx + 8, y + h * 0.62],
                       fill=(247, 241, 227))
        draw.rectangle([cx - 34, y + h * 0.30, cx - 26, y + h * 0.62],
                       fill=(247, 241, 227))
        draw.rectangle([cx + 26, y + h * 0.30, cx + 34, y + h * 0.62],
                       fill=(247, 241, 227))
        draw.ellipse([x + w * 0.72, y + h * 0.66, x + w * 0.72 + 34,
                      y + h * 0.66 + 34], fill=(179, 39, 30))
        draw.line([x + w * 0.14, y + h * 0.78, x + w * 0.30, y + h * 0.46],
                  fill=(120, 70, 20), width=14)
    elif kind == "sparta":
        waves(draw, x, y + h * 0.55, x + w, y + h * 0.95, (150, 190, 235))
        draw.polygon([(x + w * 0.16, y + h * 0.60), (x + w * 0.84, y + h * 0.60),
                      (x + w * 0.76, y + h * 0.34), (x + w * 0.26, y + h * 0.34)],
                     fill=(40, 40, 44))
        draw.rectangle([x + w * 0.30, y + h * 0.16, x + w * 0.44, y + h * 0.36],
                       fill=(40, 40, 44))
        star(draw, x + w * 0.62, y + h * 0.28, 52, (255, 120, 32))
        star(draw, x + w * 0.78, y + h * 0.22, 30, (255, 176, 32))
        draw.line([x + w * 0.84, y + h * 0.58, x + w * 0.97, y + h * 0.58],
                  fill=(232, 205, 130), width=8)
    elif kind == "kyiv":
        skyline(draw, x + 20, y + h * 0.82, x + w - 20, (30, 30, 36), seed=3)
        star(draw, x + w * 0.68, y + h * 0.30, 56, (255, 120, 32))
        star(draw, x + w * 0.30, y + h * 0.22, 30, (255, 176, 32))
        draw.rectangle([x, y + h * 0.82, x + w, y + h], fill=(20, 20, 24))
    elif kind == "bank":
        draw.rectangle([x + w * 0.30, y + h * 0.30, x + w * 0.70, y + h * 0.78],
                       fill=(247, 241, 227))
        draw.polygon([(x + w * 0.26, y + h * 0.32), (x + w * 0.74, y + h * 0.32),
                      (cx, y + h * 0.10)], fill=(179, 39, 30))
        for i in range(4):
            px = x + w * (0.34 + 0.11 * i)
            draw.rectangle([px, y + h * 0.40, px + 22, y + h * 0.72],
                           fill=(88, 66, 32))
        draw.ellipse([x + w * 0.72, y + h * 0.08, x + w * 0.94, y + h * 0.42],
                     outline=(255, 255, 255), width=10)
        draw.line([x + w * 0.76, y + h * 0.36, x + w * 0.90, y + h * 0.14],
                  fill=(255, 255, 255), width=10)
    elif kind == "gaza":
        skyline(draw, x + 20, y + h * 0.80, x + w - 20, (60, 44, 34), seed=7)
        draw.rectangle([x + w * 0.40, y + h * 0.18, x + w * 0.60, y + h * 0.62],
                       fill=(247, 241, 227))
        draw.rectangle([x + w * 0.47, y + h * 0.26, x + w * 0.53, y + h * 0.54],
                       fill=(179, 39, 30))
        draw.rectangle([x + w * 0.43, y + h * 0.36, x + w * 0.57, y + h * 0.44],
                       fill=(179, 39, 30))
    elif kind == "yemen":
        draw.polygon([(x, y + h), (x + w * 0.30, y + h * 0.18),
                      (x + w * 0.55, y + h), (x + w * 0.55, y + h * 0.42),
                      (x + w * 0.80, y + h * 0.10), (x + w, y + h)],
                     fill=(70, 52, 34))
        star(draw, x + w * 0.62, y + h * 0.30, 48, (255, 176, 32))
        draw.rectangle([x, y + h * 0.86, x + w, y + h], fill=(52, 38, 26))
    elif kind == "gold":
        for i, (bx, by, bh) in enumerate([(0.14, 0.62, 0.20), (0.30, 0.52, 0.30),
                                          (0.46, 0.42, 0.40), (0.62, 0.34, 0.48)]):
            draw.rectangle([x + w * bx, y + h * by, x + w * (bx + 0.13),
                            y + h * (by + bh)], fill=(232, 205, 130))
            draw.rectangle([x + w * bx, y + h * by, x + w * (bx + 0.13),
                            y + h * (by + 0.06)], fill=(255, 236, 170))
        draw.line([(x + w * 0.10, y + h * 0.70), (x + w * 0.34, y + h * 0.52),
                   (x + w * 0.58, y + h * 0.58), (x + w * 0.86, y + h * 0.22)],
                  fill=(255, 255, 255), width=12)
        draw.polygon([(x + w * 0.86, y + h * 0.22), (x + w * 0.78, y + h * 0.22),
                      (x + w * 0.86, y + h * 0.34)], fill=(255, 255, 255))
    elif kind == "bitcoin":
        draw.ellipse([cx - 85, cy - 85, cx + 85, cy + 85],
                     fill=(232, 205, 130))
        draw.text((cx - 34, cy - 72), "B", font=F["num"], fill=(120, 70, 10))
        draw.line([(x + w * 0.08, y + h * 0.74), (x + w * 0.30, y + h * 0.60),
                   (x + w * 0.52, y + h * 0.66), (x + w * 0.80, y + h * 0.34)],
                  fill=(255, 255, 255), width=10)
    elif kind == "gta":
        skyline(draw, x + 20, y + h * 0.82, x + w - 20, (40, 24, 56), seed=11)
        draw.ellipse([x + w * 0.70, y + h * 0.10, x + w * 0.92, y + h * 0.44],
                     fill=(232, 176, 64))
        star(draw, x + w * 0.30, y + h * 0.30, 44, (232, 205, 130))
        draw.rectangle([x, y + h * 0.82, x + w, y + h], fill=(30, 18, 44))
    elif kind == "football":
        draw.ellipse([x + w * 0.06, y + h * 0.08, x + w * 0.94, y + h * 0.94],
                     fill=(52, 140, 76))
        draw.ellipse([x + w * 0.06, y + h * 0.08, x + w * 0.94, y + h * 0.94],
                     outline=(255, 255, 255), width=8)
        draw.line([cx, y + h * 0.08, cx, y + h * 0.94], fill=(255, 255, 255),
                  width=8)
        draw.ellipse([cx - 66, cy - 66, cx + 66, cy + 66],
                     outline=(255, 255, 255), width=8)
        draw.ellipse([x + w * 0.66, y + h * 0.60, x + w * 0.66 + 64,
                      y + h * 0.60 + 64], fill=(247, 241, 227))
        draw.ellipse([x + w * 0.66, y + h * 0.60, x + w * 0.66 + 64,
                      y + h * 0.60 + 64], outline=(20, 38, 74), width=6)
    elif kind in ("capitol", "tally"):
        draw.polygon([(cx - 170, y + h * 0.72), (cx - 170, y + h * 0.46),
                      (cx - 60, y + h * 0.46), (cx - 60, y + h * 0.30),
                      (cx, y + h * 0.14), (cx + 60, y + h * 0.30),
                      (cx + 60, y + h * 0.46), (cx + 170, y + h * 0.46),
                      (cx + 170, y + h * 0.72)], fill=(247, 241, 227))
        draw.rectangle([x, y + h * 0.72, x + w, y + h * 0.80], fill=(247, 241, 227))
        if kind == "tally":
            draw.rectangle([x + w * 0.10, y + h * 0.86, x + w * 0.62, y + h * 0.94],
                           fill=(46, 107, 79))
            draw.rectangle([x + w * 0.64, y + h * 0.86, x + w * 0.90, y + h * 0.94],
                           fill=(179, 39, 30))
        else:
            draw.rectangle([x + w * 0.36, y + h * 0.84, x + w * 0.64, y + h * 0.96],
                           fill=(232, 205, 130))
    elif kind == "chip":
        draw.rectangle([cx - 105, cy - 80, cx + 105, cy + 80],
                       fill=(20, 38, 74), outline=(232, 205, 130), width=10)
        draw.rectangle([cx - 48, cy - 48, cx + 48, cy + 48],
                       fill=(232, 205, 130))
        for i in range(4):
            yy = cy - 60 + i * 40
            draw.line([cx - 148, yy, cx - 105, yy], fill=(232, 205, 130), width=10)
            draw.line([cx + 105, yy, cx + 148, yy], fill=(232, 205, 130), width=10)
        draw.line([(x + w * 0.08, y + h * 0.82), (x + w * 0.40, y + h * 0.62),
                   (x + w * 0.66, y + h * 0.68), (x + w * 0.92, y + h * 0.30)],
                  fill=(120, 220, 120), width=12)
        draw.polygon([(x + w * 0.92, y + h * 0.30), (x + w * 0.84, y + h * 0.30),
                      (x + w * 0.92, y + h * 0.42)], fill=(120, 220, 120))


# ---------------------------------------------------------------- world map
# Simplified continent outlines (lon, lat), authored for this page.
POLYS = [
    [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66),
     (-80, 62), (-70, 62), (-65, 60), (-60, 55), (-55, 52), (-55, 47),
     (-60, 45), (-65, 44), (-70, 43), (-75, 39), (-76, 35), (-80, 32),
     (-81, 26), (-84, 30), (-89, 29), (-97, 26), (-97, 16), (-92, 15),
     (-87, 13), (-83, 9), (-79, 9), (-83, 10), (-87, 14), (-90, 14),
     (-92, 15), (-97, 18), (-102, 18), (-105, 20), (-110, 23), (-114, 28),
     (-117, 32), (-122, 37), (-124, 42), (-125, 49), (-130, 55), (-135, 58),
     (-145, 60), (-155, 58), (-162, 58), (-168, 66)],
    [(-58, 64), (-52, 60), (-43, 60), (-40, 65), (-32, 68), (-25, 70),
     (-20, 74), (-22, 77), (-30, 80), (-45, 81), (-58, 80), (-60, 76),
     (-62, 72), (-58, 64)],
    [(-79, 9), (-77, 7), (-75, 10), (-72, 12), (-71, 12), (-64, 10),
     (-62, 9), (-59, 8), (-54, 6), (-51, 4), (-50, 0), (-44, -3), (-41, -5),
     (-37, -8), (-35, -9), (-37, -13), (-39, -17), (-40, -22), (-42, -23),
     (-48, -27), (-52, -32), (-53, -35), (-58, -38), (-62, -41), (-65, -45),
     (-67, -50), (-69, -52), (-71, -54), (-73, -50), (-73, -45), (-73, -40),
     (-72, -35), (-71, -30), (-70, -23), (-70, -18), (-75, -15), (-77, -12),
     (-80, -6), (-81, -3), (-80, 1), (-79, 9)],
    [(-17, 15), (-16, 20), (-10, 31), (-5, 35), (0, 36), (10, 37), (11, 34),
     (20, 32), (30, 31), (32, 31), (35, 28), (36, 36), (39, 21), (43, 12),
     (48, 11), (51, 12), (48, 10), (44, 5), (41, 0), (40, -5), (40, -10),
     (39, -17), (36, -22), (32, -28), (28, -33), (20, -35), (17, -32),
     (15, -27), (12, -18), (13, -12), (12, -5), (9, 4), (8, 5), (4, 6),
     (-3, 5), (-8, 4), (-13, 8), (-16, 12), (-17, 15)],
    [(-10, 36), (-9, 43), (-2, 48), (-4, 49), (0, 50), (2, 51), (5, 53),
     (8, 57), (10, 59), (5, 58), (5, 62), (10, 64), (13, 66), (18, 69),
     (25, 71), (30, 70), (35, 68), (40, 67), (45, 68), (55, 69), (65, 69),
     (75, 72), (85, 74), (95, 76), (105, 77), (115, 76), (125, 74),
     (135, 72), (145, 72), (155, 70), (162, 68), (170, 66), (178, 65),
     (178, 62), (170, 60), (162, 60), (158, 56), (156, 52), (150, 59),
     (142, 55), (140, 50), (138, 46), (135, 43), (132, 43), (130, 42),
     (127, 40), (127, 35), (130, 33), (132, 34), (135, 34), (137, 35),
     (140, 37), (141, 40), (141, 45), (140, 39), (137, 37), (135, 35),
     (133, 34), (131, 33), (130, 31), (127, 35), (126, 38), (122, 39),
     (120, 35), (120, 30), (121, 28), (118, 25), (112, 22), (109, 20),
     (108, 18), (106, 10), (105, 9), (103, 8), (100, 8), (98, 10),
     (95, 15), (92, 21), (89, 22), (86, 20), (83, 17), (80, 13), (77, 8),
     (75, 11), (72, 20), (68, 23), (66, 25), (61, 25), (58, 26), (56, 27),
     (54, 26), (52, 25), (50, 29), (48, 30), (44, 29), (42, 15), (40, 15),
     (39, 21), (37, 32), (36, 36), (33, 36), (30, 36), (27, 37), (23, 36),
     (22, 37), (19, 40), (16, 38), (12, 44), (8, 44), (3, 43), (0, 40),
     (-2, 37), (-6, 36), (-9, 37), (-10, 36)],
    [(113, -22), (114, -30), (115, -35), (118, -35), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (150, -22), (146, -19), (142, -15), (142, -11),
     (140, -17), (136, -15), (135, -12), (132, -11), (130, -13), (126, -14),
     (122, -17), (118, -20), (113, -22)],
    [(167, -45), (170, -43), (173, -41), (175, -38), (177, -38), (178, -37),
     (174, -41), (172, -43), (168, -46), (167, -45)],
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51),
     (-3, 50), (-5, 50)],
    [(130, 31), (132, 33), (134, 34), (136, 35), (138, 35), (140, 36),
     (141, 39), (141, 42), (142, 44), (143, 43), (141, 40), (139, 38),
     (137, 37), (135, 35), (133, 34), (131, 33), (130, 31)],
    [(95, 5), (100, 0), (104, -3), (106, -6), (103, -5), (99, 1), (95, 5)],
    [(109, 1), (113, 4), (117, 6), (119, 1), (117, -3), (113, -4),
     (110, -3), (109, 1)],
    [(105, -6), (110, -7), (114, -8), (114, -9), (108, -8), (105, -6)],
    [(131, -1), (136, -2), (141, -3), (146, -6), (147, -9), (143, -8),
     (138, -8), (134, -4), (131, -1)],
    [(44, -16), (47, -15), (50, -16), (50, -20), (47, -25), (44, -25),
     (43, -20), (44, -16)],
    [(-22, 64), (-18, 63), (-15, 64), (-14, 66), (-18, 66), (-22, 65)],
]


def _inside(lon, lat, poly):
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


def draw_map(draw, x, y, w, h, variant):
    """Dotted world map from the polygons above, with numbered pins."""
    draw.rectangle([x, y, x + w, y + h], fill=(233, 230, 214))
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=4)
    lon0, lon1, lat0, lat1 = -180.0, 180.0, 84.0, -56.0
    sx = w / (lon1 - lon0)
    sy = h / (lat0 - lat1)
    s = min(sx, sy)
    ox = x + (w - (lon1 - lon0) * s) / 2
    oy = y + (h - (lat0 - lat1) * s) / 2
    dot = INK if variant == "A" else (30, 48, 84)
    lon = -178.5
    while lon < 180:
        lat = 82.5
        while lat > -58:
            if any(_inside(lon, lat, p) for p in POLYS):
                px = ox + (lon - lon0) * s
                py = oy + (lat0 - lat) * s
                draw.ellipse([px - 5, py - 5, px + 5, py + 5], fill=dot)
            lat -= 2.5
        lon += 3.0
    # Pins with leader offsets where true spots collide (US east coast,
    # London/Liverpool, SF/LA, Antalya/Gaza): circle at the offset point,
    # thin red leader to the true location, red dot on the true spot.
    OFFSETS = {5: (-18, 5), 13: (6, 6), 14: (-10, -6), 20: (10, -5),
               8: (7, -4), 9: (-7, 6), 6: (6, -6)}
    for num, plon, plat in PINS:
        px = ox + (plon - lon0) * s
        py = oy + (lat0 - plat) * s
        qx, qy = px, py
        if num in OFFSETS:
            dlon, dlat = OFFSETS[num]
            qx = px + dlon * s
            qy = py - dlat * s
            draw.line([px, py, qx, qy], fill=RED, width=5)
            draw.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED)
        draw.ellipse([qx - 30, qy - 30, qx + 30, qy + 30], fill=RED,
                     outline=WHITE, width=5)
        label = str(num)
        tw = draw.textlength(label, font=F["pin"])
        draw.text((qx - tw / 2, qy - 26), label, font=F["pin"], fill=WHITE)
    return

# ---------------------------------------------------------------- page
W = 4200
M = 100
CW = W - 2 * M


def card_by_num(num):
    for c in CARDS:
        if c[0] == num:
            return c
    raise KeyError(num)


def draw_card(draw, card, x, y, w, h, lead, variant):
    num, region, place, topic, head, deck, chip, src, rep, kind = card
    rc = REGION_COLORS[region]
    draw.rectangle([x, y, x + w, y + h], fill=PAPER, outline=INK, width=4)
    sh = int(h * 0.36) if lead else int(h * 0.32)
    scene(draw, kind, x + 4, y + 4, w - 8, sh, variant)
    # number badge over the scene, top-left
    draw.rectangle([x + 4, y + 4, x + 68, y + 68], fill=RED)
    num_txt = str(num)
    tw = draw.textlength(num_txt, font=F["mono"])
    draw.text((x + 36 - tw / 2, y + 12), num_txt, font=F["mono"], fill=WHITE)
    # data chip band at the bottom of the scene
    cy0 = y + 4 + sh - 52
    draw.rectangle([x + 4, cy0, x + w - 4, cy0 + 52], fill=GOLD)
    draw.text((x + 26, cy0 + 8), chip, font=F["chip"], fill=INK)
    ty = y + 4 + sh + 18
    label = "%s - %s - %s" % (place, region, topic)
    draw.text((x + 26, ty), label, font=F["label"], fill=rc)
    ty += 48
    hf = F["head_lead"] if lead else F["head_mini"]
    lh = 76 if lead else 58
    max_lines = 3
    for line in wrap(draw, head, hf, w - 52)[:max_lines]:
        draw.text((x + 26, ty), line, font=hf, fill=INK)
        ty += lh
    ty += 10
    df = F["deck_lead"] if lead else F["deck_mini"]
    dlh = 46 if lead else 42
    for line in wrap(draw, deck, df, w - 52)[:4 if lead else 3]:
        draw.text((x + 26, ty), line, font=df, fill=(38, 38, 38))
        ty += dlh
    src_line = "%s - %s" % (rep, src)
    draw.text((x + 26, y + h - 52), src_line, font=F["mono_sm"], fill=GREY)


def draw_numbers(draw, x, y, w, variant):
    bg = INK if variant == "A" else (96, 32, 28)
    cell_w, cell_h = w // 4, 168
    draw.rectangle([x, y, x + w, y + cell_h * 2], fill=bg)
    for i, (big, small) in enumerate(NUMBERS):
        cx0 = x + (i % 4) * cell_w
        cy0 = y + (i // 4) * cell_h
        bf = F["mono_lg"]
        while draw.textlength(big, font=bf) > cell_w - 60 and bf.size > 44:
            bf = _font("IBMPlexMono-Bold.ttf", bf.size - 6)
        text_center(draw, cx0 + cell_w / 2, cy0 + 16, big, bf, GOLD_SOFT)
        text_center(draw, cx0 + cell_w / 2, cy0 + 108, small, F["mono_sm"], WHITE)
    return cell_h * 2


def draw_regions(draw, x, y, w):
    counts = [("EUROPE", 4), ("MIDDLE EAST", 3), ("AMERICAS", 5),
              ("OCEANIA", 1), ("WORLD", 2)]
    total = sum(c for _, c in counts)
    cx = x
    for name, count in counts:
        bw = int(w * count / total)
        draw.rectangle([cx, y, cx + bw, y + 84], fill=REGION_COLORS[name])
        text_center(draw, cx + bw / 2, y + 22, "%s %d" % (name, count),
                    F["mono"], WHITE)
        cx += bw
    return 84


def draw_timeline(draw, x, y, w, variant):
    draw.text((x, y), "THE DAY IN TIME - FROM MONDAY EVENING INTO TUESDAY MORNING",
              font=F["mono"], fill=RED)
    y += 56
    cell_w, cell_h = w // 3, 158
    for i, (when, what) in enumerate(TIMELINE):
        cx0 = x + (i % 3) * cell_w
        cy0 = y + (i // 3) * cell_h
        draw.rectangle([cx0 + 6, cy0, cx0 + cell_w - 6, cy0 + cell_h - 14],
                       outline=INK, width=3)
        draw.text((cx0 + 26, cy0 + 14), when, font=F["mono_sm"], fill=RED)
        for j, line in enumerate(wrap(draw, what, F["body"], cell_w - 52)[:2]):
            draw.text((cx0 + 26, cy0 + 52 + j * 42), line, font=F["body"],
                      fill=INK)
    note = ("Times as reported, zones written out. Monday-evening wires marked "
            "MON were carried into Tuesday's edition.")
    draw.text((x, y + cell_h * 2 + 6), note, font=F["mono_sm"], fill=GREY)
    return 56 + cell_h * 2 + 44


def draw_also_on(draw, x, y, w, h):
    draw.text((x, y), "ALSO ON - 16 TO 42", font=F["mono"], fill=RED)
    draw.line([x, y + 52, x + w, y + 52], fill=INK, width=3)
    yy = y + 66
    for i, (text, src) in enumerate(BRIEFS):
        num = 16 + i
        draw.text((x, yy), "%d." % num, font=F["mono_sm"], fill=RED)
        lines = wrap(draw, "%s  (%s)" % (text, src), F["brief"], w - 78)
        for line in lines[:2]:
            draw.text((x + 78, yy), line, font=F["brief"], fill=INK)
            yy += 40
        yy += 8
    return yy - y


def draw_datecheck(draw, x, y, w):
    draw.rectangle([x, y, x + w, y + 400], fill=DATE_BG, outline=RED, width=5)
    draw.text((x + 30, y + 18),
              "DATE CHECK - NOT TUESDAY'S NEWS: named, dated, left out on purpose",
              font=F["mono"], fill=RED)
    col_w = (w - 60) // 2
    for i, (what, when) in enumerate(DATECHECK):
        cx0 = x + 30 + (i % 2) * col_w
        cy0 = y + 76 + (i // 2) * 78
        draw.text((cx0, cy0), "X  %s" % what, font=F["body"], fill=INK)
        draw.text((cx0, cy0 + 40), "     %s" % when, font=F["mono_sm"],
                  fill=RED)
    return 400


def render(variant):
    lead_order = (1, 4, 11) if variant == "A" else (4, 1, 11)
    img = Image.new("RGB", (W, 6800), PAGE)
    d = ImageDraw.Draw(img)
    y = 64
    # kicker
    d.line([M, y, W - M, y], fill=INK, width=4)
    text_center(d, W / 2, y + 18,
                "42 STORIES  |  5 REGIONS  |  TUESDAY 24 NOVEMBER 2026",
                F["mono"], INK)
    d.line([M, y + 78, W - M, y + 78], fill=INK, width=4)
    y += 96
    # masthead
    if variant == "A":
        text_center(d, W / 2, y, "THE TUESDAY ATLAS", F["mast"], INK)
        y += 400
        d.line([M, y, W - M, y], fill=RED, width=8)
        y += 26
    else:
        d.rectangle([M, y, W - M, y + 350], fill=INK)
        text_center(d, W / 2, y + 25, "THE TUESDAY ATLAS", F["mast"], PAGE)
        y += 376
        d.line([M, y, W - M, y], fill=RED, width=8)
        y += 26
    # date line
    text_center(d, W / 2, y, "Tuesday 24 November 2026", F["date"], RED)
    y += 190
    text_center(d, W / 2, y,
                "THE WORLD IN ONE IMAGE - EVERY STORY DATED, EVERY NUMBER CHECKED",
                F["mono"], INK_SOFT)
    y += 62
    deck = ("Seven drones sink a Russian warship off Libya. COP31 collapses "
            "with no deal. New Zealand bats out a draw. Tuesday, in full.")
    for line in wrap(d, deck, F["body"], CW - 400):
        text_center(d, W / 2, y, line, F["body"], INK)
        y += 44
    y += 26
    # numbers strip
    y += draw_numbers(d, M, y, CW, variant)
    y += 24
    # region strip
    y += draw_regions(d, M, y, CW)
    y += 24
    # timeline
    y += draw_timeline(d, M, y, CW, variant)
    y += 26
    # leads
    lead_w = (CW - 2 * 50) // 3
    lead_h = 960
    for i, num in enumerate(lead_order):
        draw_card(d, card_by_num(num), M + i * (lead_w + 50), y, lead_w,
                  lead_h, True, variant)
    y += lead_h + 30
    # minis 4x3
    mini_w = (CW - 3 * 40) // 4
    mini_h = 600
    for r in range(3):
        for c in range(4):
            num = MINI_NUMS[r * 4 + c]
            draw_card(d, card_by_num(num), M + c * (mini_w + 40),
                      y + r * (mini_h + 30), mini_w, mini_h, False, variant)
    y += 3 * mini_h + 2 * 30 + 30
    # bottom: map + also on (A: map left; B: flipped)
    bottom_y = y
    map_w, also_w = 2200, 1720
    if variant == "A":
        map_x, also_x = M, M + map_w + 80
    else:
        also_x, map_x = M, M + also_w + 80
    d.text((map_x, bottom_y), "WHERE IT HAPPENED - PINS MATCH STORY NUMBERS",
           font=F["mono"], fill=RED)
    d.text((also_x, bottom_y), "ALSO ON - 16 TO 42", font=F["mono"], fill=RED)
    draw_map(d, map_x, bottom_y + 56, map_w, 1060, variant)
    d.text((map_x, bottom_y + 56 + 1060 + 18),
           "Dots: land, drawn from coast outlines in code. Red pins are numbered by story.",
           font=F["mono_sm"], fill=GREY)
    d.line([also_x, bottom_y + 52, also_x + also_w, bottom_y + 52], fill=INK,
           width=3)
    yy = bottom_y + 66
    for i, (text, src) in enumerate(BRIEFS):
        num = 16 + i
        d.text((also_x, yy), "%d." % num, font=F["mono_sm"], fill=RED)
        for line in wrap(d, "%s  (%s)" % (text, src), F["brief"], also_w - 78)[:2]:
            d.text((also_x + 78, yy), line, font=F["brief"], fill=INK)
            yy += 40
        yy += 8
    briefs_bottom = yy
    map_bottom = bottom_y + 56 + 1060 + 18 + 40
    y = max(briefs_bottom, map_bottom) + 10
    # date check
    y += draw_datecheck(d, M, y, CW)
    y += 30
    # footer
    d.line([M, y, W - M, y], fill=INK, width=4)
    y += 18
    foot1 = ("SOURCES: CNN - Times - WSJ - AP - Reuters - Guardian - BBC - "
             "Treasury - CoinPaprika - ActiveInvestorMag - HS - WicketPulse - "
             "Mint - Gadgets360 - HK News TV - IANS - JagranJosh - ObserverVoice.")
    for line in wrap(d, foot1, F["mono_sm"], CW):
        d.text((M, y), line, font=F["mono_sm"], fill=INK_SOFT)
        y += 40
    d.text((M, y), "CERTAINTY: REPORTED = reported by the sources named on the card.",
           font=F["mono_sm"], fill=INK_SOFT)
    y += 40
    d.text((M, y), "Pictures and map: original, drawn in code. Original drawings.",
           font=F["mono_sm"], fill=INK_SOFT)
    y += 56
    return img.crop((0, 0, W, y + 40))


def fit_entry(compose):
    canvas = Image.new("RGB", (1024, 1024), PAGE)
    scale = min(1024 / compose.width, 1024 / compose.height)
    nw, nh = int(compose.width * scale), int(compose.height * scale)
    small = compose.resize((nw, nh), Image.LANCZOS)
    canvas.paste(small, ((1024 - nw) // 2, (1024 - nh) // 2))
    return canvas.quantize(colors=256, method=Image.MEDIANCUT).convert("RGB")


def main():
    variant = sys.argv[1] if len(sys.argv) > 1 else "A"
    compose = render(variant)
    compose.save("compose_%s.png" % variant)
    entry = fit_entry(compose)
    entry.save("entry_%s.png" % variant, optimize=True)
    import os
    print("variant %s compose %dx%d entry_%s.png %d bytes" % (
        variant, compose.width, compose.height, variant,
        os.path.getsize("entry_%s.png" % variant)))


if __name__ == "__main__":
    main()
