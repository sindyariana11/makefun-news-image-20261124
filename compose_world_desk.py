# THE WORLD DESK — NI24 wave 2, account 10. Fresh compose, written in this session.
# Palette: charcoal grey + electric blue. Layout B (wide lead).
import sys
from PIL import Image, ImageDraw, ImageFont

FD = "/home/hatch/workspace/tools/bedah-19nov/news-image/fonts/"
def F(name, size):
    return ImageFont.truetype(FD + name, size)
PLAY = "PlayfairDisplay-Black.ttf"
ARCH = "Archivo.ttf"
ARCHB = "Archivo-Bold.ttf"

CHAR = (34, 38, 46)        # charcoal
CHAR2 = (48, 54, 64)
PAPER = (233, 236, 239)    # grey paper
CARD = (250, 251, 252)
INK = (24, 27, 32)
BLUE = (0, 110, 235)       # electric blue
BLUE_L = (64, 169, 255)
GREY = (96, 104, 114)
RED = (178, 32, 32)

REGION_COLORS = {
    "EUROPE": (0, 110, 235), "MIDDLE EAST": (196, 120, 10), "AFRICA": (150, 60, 160),
    "AMERICAS": (178, 32, 32), "ASIA": (0, 140, 120), "SOUTH ASIA": (90, 130, 20),
    "ASIA-PACIFIC": (20, 130, 170), "OCEANIA": (30, 160, 90), "WORLD": (70, 70, 120),
}

# num, label, scene, headline, deck, tag, chip  (all facts from ni24 pool + 07:00 refresh)
LEADS = [
    (1, "KYIV REGION, UKRAINE - EUROPE - WAR", "city",
     "KYIV STRIKES KILL AT LEAST 15 NEAR THE CAPITAL",
     "11 killed in a block of flats in Dymer; a drone hit a 6-floor Kyiv building on Monday, 5 injured. Zelenskyy to CNN on Putin: 'for us, he's a killer'.",
     "REPORTED - Times / AP", "15 KILLED / 11 IN DYMER"),
    (2, "NEW YORK, USA - AMERICAS - MARKETS", "chip",
     "NVIDIA BRINGS BACK JENSEN HUANG AS CEO",
     "The board reinstates Huang effective immediately on Monday, after Trump intervened; Huang had resigned on 12 Nov. Shares +31% Mon; Nasdaq +6%, chip index +12%.",
     "REPORTED - Reuters", "+31% / HUANG BACK"),
    (3, "WASHINGTON, USA - MIDDLE EAST - SANCTIONS", "bank",
     "IRAN SANCTIONS HIT ~30 EXCHANGE HOUSES",
     "The US Treasury on Monday targets ~30 Iran-linked exchange houses and executives - the core of the shadow banking network evading sanctions on Iranian banks.",
     "REPORTED - AP / Treasury", "~30 SANCTIONED"),
]
GRID = [
    (4, "BENGHAZI, LIBYA - EUROPE - WAR", "ship",
     "UKRAINE SINKS RUSSIAN WARSHIP MERKURY OFF LIBYA",
     "7 sea drones launched at the corvette Merkury at Benghazi; a Ka-27 helicopter was destroyed aboard and the cargo vessel MV Angara was hit.",
     "REPORTED - CNN / AP", "7 SEA DRONES"),
    (5, "GULF OF FINLAND - EUROPE - SEA", "ship",
     "RUSSIAN CARGO SHIP SPARTA II HIT, TOWED CLEAR",
     "Sparta II, 121 m long, took 2 drone hits; all 16 crew came off in the Finland-led Loviisa rescue and the ship was towed out on Sunday night.",
     "REPORTED - Reuters / Times", "121 M / 16 CREW SAFE"),
    (6, "ANTALYA, TURKIYE - WORLD - CLIMATE", "globe",
     "COP31 ENDS WITH NO DEAL - FIRST SINCE 2000",
     "The Antalya Pact was not adopted and the final text dropped every mention of fossil fuels; 44 h overtime, the longest ever; >90 countries signed a side pledge.",
     "REPORTED - Times / Guardian", "NO DEAL / SINCE 2000"),
    (7, "GAZA CITY - MIDDLE EAST - CONFLICT", "city",
     "ISRAELI STRIKES KILL 3 IN GAZA",
     "3 killed on Monday in separate strikes, including a UNRWA employee; Shifa Hospital and the agency both confirm the deaths.",
     "REPORTED - AP", "3 KILLED"),
    (8, "NEW YORK, USA - AMERICAS - MARKETS", "chart",
     "GOLD 3588: BULLION REBOUNDS 1.5% IN A DAY",
     "Gold +1.5% on Monday after its worst week in 8 months; the 10-year yield sits near 4.96% and traders await the US PCE inflation report due 25 Nov.",
     "REPORTED - Reuters", "GOLD 3588 / OZ"),
    (9, "GLOBAL - WORLD - CRYPTO", "coin",
     "BITCOIN 61284 AS LEVERAGED SELL-OFF EASES",
     "Bitcoin quoted $61,284 Mon 12:52 UTC, +1.1% in 24 h and -4.5% in 7 days; weekend low near $55,100; the Kraken CAD flash-crash trades stand.",
     "REPORTED - CoinPaprika", "BITCOIN 61284"),
    (10, "LOS ANGELES, USA - AMERICAS - BUSINESS", "chart",
     "GTA VI TAKES $3.8BN ON DAY ONE",
     "GTA VI posts the biggest entertainment launch on record - past every game launch and every single-day film box office in history.",
     "REPORTED - ActiveInvestorMag", "$3.8BN DAY ONE"),
    (11, "WELLINGTON, NZ - OCEANIA - CRICKET", "stadium",
     "WELLINGTON TEST DRAWN AS NZ BAT OUT THE DAY",
     "NZ 239/5: Mitchell 49* off 186 balls, Phillips 26* off 126; India 720/9d (Rahul 136, Pant 128, Gill 98); India lead 352; 2nd Test Christchurch 27 Nov.",
     "REPORTED - HS / WicketPulse", "DRAWN / 239/5"),
    (12, "LIVERPOOL, ENGLAND - EUROPE - FOOTBALL", "stadium",
     "LIVERPOOL 4-0 MAN UTD; POCHETTINO DEBUT DISASTER",
     "Yoro was sent off in the 8th minute and United played with 10 men; the loss leaves United 19th in the Premier League, on 8 points.",
     "REPORTED - Mint / NextSportsWeb", "4-0 / YORO OFF 8'"),
    (13, "WASHINGTON, USA - AMERICAS - POLITICS", "capitol",
     "DEMOCRATS 258-173 TAKE BOTH CHAMBERS",
     "The largest House majority since 1992, sealed by the North Carolina pickup; Van Hollen challenges Schumer for Senate leader, secret ballot 1 Dec.",
     "REPORTED - BBC / ActiveInvestorMag", "258-173"),
]
BRIEFS = [
    "14 Congo halts cobalt exports from 30 Nov until further notice - Reuters",
    "15 KCNA: North Korea weighs closing its Swiss office in Pyongyang - Reuters",
    "16 Indonesia factory blaze kills 24, dozens missing - Reuters",
    "17 Hong Kong sets Interpol-summit curbs, 30 Nov-3 Dec - HK News TV",
    "18 Nepal PM Balendra Shah ends Delhi state visit; met Modi Mon - IANS",
    "19 India weighs rice export duties as domestic prices rise - Reuters",
    "20 Tata Steel-APL Apollo pipe deal, Rs28,000 cr - ObserverVoice",
    "21 Modi opens AI Centre at IIT Patna, Rs400 cr - ObserverVoice",
    "22 Thousands march in Lisbon over the cost of living - JagranJosh",
    "23 UK-EU reset deal: Burnham calls it 'landmark' - BBC",
    "24 India-EU trade pact likely signed 16 Dec - JagranJosh",
    "25 US discusses training Syrian forces, demining focus - Reuters",
    "26 CrowdStrike snaps up Zscaler in a $44bn deal - Reuters",
    "27 US Army to detonate Iowa lead stockpile, 68 barrels - Reuters",
    "28 Euro zone PMI 51.7, fifth month of growth - Reuters",
    "29 Miley Cyrus marries Maxx Morando in California - BBC",
    "30 Solana launches solana.ai for AI agents - Gadgets360",
    "31 UN AI weapons talks: states agree to keep negotiating - salonvision",
    "32 FBI probe opens into hack of FBI crime database - AP",
    "33 Trump: cap card rates with Democrats - ActiveInvestorMag",
    "34 Yemen: Houthi say strike kills 11, wounds 19 - AP",
    "35 KOSPI falls ~3% Monday to a 10-month low - Reuters",
    "36 Mets and A.J. Ewing agree a $95m, 8-year deal - AP",
    "37 Hong Kong CPI +2.2% year on year in Oct - HK News TV",
]
NUMBERS = [("7", "SEA DRONES - MERKURY SUNK"), ("15", "KILLED NEAR KYIV"),
           ("NO DEAL", "COP31 - FIRST SINCE 2000"), ("+31%", "NVIDIA - HUANG RETURNS"),
           ("$3,588", "GOLD +1.5% MON"), ("$61,284", "BITCOIN MON 12:52 UTC"),
           ("$3.8BN", "GTA VI DAY ONE"), ("258-173", "US HOUSE RESULT")]
REGIONS = [("EUROPE", 7), ("MIDDLE EAST", 4), ("AFRICA", 1), ("AMERICAS", 10),
           ("ASIA", 2), ("SOUTH ASIA", 5), ("ASIA-PACIFIC", 3), ("OCEANIA", 1), ("WORLD", 4)]
TIMELINE = [
    ("21:24 UTC MON", "KCNA: North Korea weighs closing Swiss office (= 04:24 WIB TUE)"),
    ("12:52 UTC MON", "Bitcoin quoted $61,284 as liquidations ease - CoinPaprika"),
    ("MON EVENING", "Zelenskyy announces the Merkury sinking off Benghazi"),
    ("MON EVENING", "US Treasury announces Iran sanctions on ~30 houses"),
    ("21:39 HKT MON", "Hong Kong announces Interpol-summit curbs, 30 Nov-3 Dec"),
]
DATECHECK = [
    "X 186-drone night over Ukraine, 161 downed - Fri 21-Sun 22 Nov",
    "X Alcaraz beats Zverev 6-2, 7-6 - first ATP Finals title, Sun 22 Nov",
    "X Verstappen wins the Las Vegas Grand Prix - Sun 22 Nov",
    "X Wembanyama scores 50, Spurs 114-91 Pelicans - Sun 22 Nov",
    "X Ukraine strike on the Kerch Bridge - reported Sun 22 Nov",
    "X Nvidia SEC probe first reported - Fri 20 Nov",
    "X Jensen Huang resigns as Nvidia CEO - Thu 12 Nov (his return is the news)",
    "X Myanmar ICJ genocide ruling - Thu 19 Nov",
]
MAPROWS = [
    "..............................................................",
    "..#####.......................................................",
    ".########..........##..####..#####............................",
    "##########........#######################..#####..............",
    ".#########.........######################..########...........",
    "..#######...........################.....##########..........",
    "...#####.............##############.......########...........",
    "....####..............############.........######............",
    "....###................########...........#####..............",
    ".....##.............##########.............###................",
    ".....#...............########..............##.................",
    "......................######..................................",
    ".......................####...........##......................",
    ".......................###...........####.....................",
    "......................##............######....................",
    ".....................................####.....................",
    "......................................##.......##.............",
    "..............................................................",
]
PINS = [(4, 29, 6), (1, 31, 3), (6, 32, 5), (7, 33, 6), (2, 11, 4),
        (13, 10, 5), (10, 6, 5), (12, 26, 2), (11, 56, 16), (9, 45, 4)]

def wrap(d, text, font, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def scene(d, x, y, w, h, kind, seed):
    sky = [(38, 70, 130), (70, 40, 90), (20, 90, 110), (120, 60, 30), (30, 100, 60)][seed % 5]
    d.rectangle([x, y, x + w, y + h], fill=sky)
    d.rectangle([x, y + h * 0.45, x + w, y + h * 0.72], fill=(sky[0] + 30, sky[1] + 30, sky[2] + 30))
    d.ellipse([x + w * 0.78, y + 4, x + w * 0.78 + 16, y + 20], fill=(250, 220, 90))
    base = y + h - 14
    if kind in ("city", "bank", "capitol"):
        n = max(3, w // 34)
        for i in range(n):
            bw = w // n - 6
            bh = h * (0.35 + ((i * 37 + seed * 11) % 30) / 100.0)
            bx = x + 4 + i * (bw + 6)
            d.rectangle([bx, base - bh, bx + bw, base], fill=(18, 22, 30))
            for wy in range(int(base - bh) + 5, int(base) - 4, 8):
                for wx in range(bx + 4, bx + bw - 3, 9):
                    if (wx * 7 + wy * 13 + seed) % 3:
                        d.rectangle([wx, wy, wx + 3, wy + 3], fill=(255, 214, 90))
        if kind == "capitol":
            d.polygon([(x + w / 2 - 16, base - h * 0.62), (x + w / 2 + 16, base - h * 0.62),
                       (x + w / 2, base - h * 0.8)], fill=(230, 235, 240))
    elif kind == "ship":
        d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(16, 60, 110))
        for i in range(6):
            d.line([x + i * w / 6, y + h * 0.78, x + i * w / 6 + 14, y + h * 0.78], fill=(140, 200, 255), width=2)
        hx = x + w * 0.18
        d.polygon([(hx, base - 8), (hx + w * 0.6, base - 8), (hx + w * 0.5, base + 2), (hx + 8, base + 2)], fill=(20, 24, 32))
        d.rectangle([hx + w * 0.22, base - 24, hx + w * 0.4, base - 8], fill=(52, 60, 72))
        d.rectangle([hx + w * 0.3, base - 34, hx + w * 0.34, base - 24], fill=(52, 60, 72))
    elif kind == "chip":
        for i in range(5):
            d.line([x + 8, y + 8 + i * (h - 16) / 4, x + w - 8, y + 8 + i * (h - 16) / 4], fill=(0, 200, 160), width=1)
        d.rectangle([x + w * 0.32, y + h * 0.2, x + w * 0.68, y + h * 0.8], outline=(0, 255, 190), width=3)
        d.rectangle([x + w * 0.42, y + h * 0.35, x + w * 0.58, y + h * 0.65], fill=(0, 255, 190))
    elif kind == "coin":
        d.ellipse([x + w * 0.36, y + h * 0.08, x + w * 0.64, y + h * 0.92], fill=(245, 170, 30))
        d.ellipse([x + w * 0.40, y + h * 0.16, x + w * 0.60, y + h * 0.84], outline=(160, 100, 0), width=3)
        d.text((x + w * 0.47, y + h * 0.28), "B", font=F(ARCHB, int(h * 0.45)), fill=(120, 70, 0))
    elif kind == "stadium":
        d.rectangle([x, y + h * 0.5, x + w, y + h], fill=(24, 130, 60))
        d.ellipse([x + w * 0.2, y + h * 0.42, x + w * 0.8, y + h * 0.98], outline=(240, 240, 240), width=2)
        d.rectangle([x + 6, y + h * 0.3, x + w - 6, y + h * 0.5], fill=(18, 22, 30))
        for wx in range(x + 10, x + w - 10, 10):
            d.rectangle([wx, y + h * 0.36, wx + 4, y + h * 0.42], fill=(255, 214, 90))
    elif kind == "globe":
        d.ellipse([x + w * 0.3, y + h * 0.05, x + w * 0.7, y + h * 0.95], outline=(120, 220, 255), width=3)
        d.ellipse([x + w * 0.42, y + h * 0.05, x + w * 0.58, y + h * 0.95], outline=(120, 220, 255), width=1)
        d.line([x + w * 0.3, y + h * 0.5, x + w * 0.7, y + h * 0.5], fill=(120, 220, 255), width=1)
    elif kind == "chart":
        pts = [(x + 8 + i * (w - 16) / 5, y + h - 10 - ((i * 29 + seed * 7) % int(h * 0.6))) for i in range(6)]
        d.line(pts, fill=(0, 255, 160), width=3)
        for px, py in pts:
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 220, 80))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(14, 17, 22))

def card(d, bx, by, bw, bh, item, big):
    num, label, kind, head, deck, tag, chip = item
    d.rectangle([bx, by, bx + bw, by + bh], fill=CARD, outline=(170, 178, 188), width=1)
    sh = 104 if big else 40
    scene(d, bx + 3, by + 3, bw - 6, sh, kind, num)
    d.rectangle([bx + 3, by + 3, bx + 30, by + 23], fill=BLUE)
    d.text((bx + 8, by + 6), str(num), font=F(ARCHB, 13), fill=(255, 255, 255))
    d.rectangle([bx + 3, by + 3 + sh - 14, bx + 3 + min(bw - 6, int(d.textlength(chip, font=F(ARCHB, 10))) + 12), by + 3 + sh], fill=(14, 17, 22))
    d.text((bx + 9, by + 3 + sh - 12), chip, font=F(ARCHB, 10), fill=(255, 220, 80))
    yy = by + 6 + sh
    hf = F(ARCHB, 16 if big else 12)
    for ln in wrap(d, head, hf, bw - 12)[:2]:
        d.text((bx + 6, yy), ln, font=hf, fill=INK)
        yy += 19 if big else 14
    yy += 2
    df = F(ARCH, 11 if big else 9)
    maxd = 4 if big else 4
    for ln in wrap(d, deck, df, bw - 12)[:maxd]:
        d.text((bx + 6, yy), ln, font=df, fill=(52, 58, 66))
        yy += 13 if big else 11
    d.text((bx + 6, by + bh - 15), tag, font=F(ARCHB, 8), fill=BLUE)
    d.text((bx + 6, by + bh - 26), label, font=F(ARCH, 7), fill=GREY)

def build(variant, out):
    img = Image.new("RGB", (1024, 1024), PAPER)
    d = ImageDraw.Draw(img)
    M, W = 14, 996
    # header band
    d.rectangle([0, 0, 1024, 110], fill=CHAR)
    d.text((512, 7), "37 STORIES - 9 REGIONS - EVERY ONE DATED TUESDAY 24 NOVEMBER 2026",
           font=F(ARCHB, 13), fill=(190, 200, 214), anchor="ma")
    d.text((512, 24), "THE WORLD DESK", font=F(PLAY, 40), fill=(255, 255, 255), anchor="ma")
    d.text((512, 70), "TUESDAY 24 NOVEMBER 2026", font=F(ARCHB, 33), fill=BLUE_L, anchor="ma")
    # numbers strip
    y = 114
    cw = W // 8
    for i, (big, small) in enumerate(NUMBERS):
        x = M + i * cw
        d.rectangle([x, y, x + cw - 3, y + 34], fill=CHAR2)
        d.text((x + 6, y + 3), big, font=F(ARCHB, 15), fill=(255, 220, 80))
        d.text((x + 6, y + 21), small, font=F(ARCH, 7), fill=(220, 226, 233))
    # region strip (equal segments so every bucket name stays readable)
    y = 152
    segw = W // 9
    for i, (name, c) in enumerate(REGIONS):
        x = M + i * segw
        d.rectangle([x, y, x + segw - 3, y + 20], fill=REGION_COLORS[name])
        d.text((x + 5, y + 5), "%s %d" % (name, c), font=F(ARCHB, 8), fill=(255, 255, 255))
    # timeline
    y = 176
    d.rectangle([M, y, M + W, y + 38], fill=(255, 255, 255), outline=(170, 178, 188))
    d.text((M + 6, y + 2), "THE ROAD INTO TUESDAY - TIMES AS REPORTED, ZONES NAMED; MONDAY TIMES ARE NOT SHOWN AS TUESDAY",
           font=F(ARCHB, 9), fill=BLUE)
    tw = W // 5
    for i, (t, ev) in enumerate(TIMELINE):
        x = M + i * tw
        d.text((x + 6, y + 13), t, font=F(ARCHB, 8), fill=INK)
        for j, ln in enumerate(wrap(d, ev, F(ARCH, 8), tw - 12)[:2]):
            d.text((x + 6, y + 21 + j * 9), ln, font=F(ARCH, 8), fill=GREY)
    # leads
    y = 218
    leads = list(LEADS)
    if variant == "B":
        leads = [LEADS[1], LEADS[0], LEADS[2]]
        widths = [332, 332, 332]
    else:
        widths = [400, 298, 298]
    x = M
    for item, bw in zip(leads, widths):
        card(d, x, y, bw - 6, 226, item, True)
        x += bw
    # grid
    y = 448
    grid = list(GRID)
    if variant == "B":
        grid = GRID[5:] + GRID[:5]
    gw = W // 5
    for r in range(2):
        for cix in range(5):
            card(d, M + cix * gw, y + r * 148, gw - 6, 144, grid[r * 5 + cix], False)
    # also on
    y = 748
    d.rectangle([M, y, M + W, y + 118], fill=(255, 255, 255), outline=(170, 178, 188))
    d.text((M + 6, y + 4), "ALSO ON THE WORLD DESK - BRIEFS 14 TO 37", font=F(ARCHB, 11), fill=BLUE)
    colw = W // 3
    for i, b in enumerate(BRIEFS):
        cx = M + (i // 8) * colw
        cy = y + 24 + (i % 8) * 12
        for j, ln in enumerate(wrap(d, b, F(ARCH, 9), colw - 14)[:1]):
            d.text((cx + 6, cy), ln, font=F(ARCH, 9), fill=INK)
    # bottom: map + date check
    y = 868
    d.rectangle([M, y, M + 500, y + 96], fill=CHAR)
    d.text((M + 6, y + 3), "WHERE IT HAPPENED - PINS MATCH STORY NUMBERS", font=F(ARCHB, 9), fill=(255, 255, 255))
    ox, oy, cell = M + 10, y + 18, 8
    for r, row in enumerate(MAPROWS):
        for cix, ch in enumerate(row):
            if ch == "#":
                d.ellipse([ox + cix * cell, oy + r * 4, ox + cix * cell + 3, oy + r * 4 + 3], fill=(140, 190, 255))
    for num, gx, gy in PINS:
        px, py = ox + gx * cell, oy + gy * 4
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED)
        d.text((px, py - 6), str(num), font=F(ARCHB, 8), fill=(255, 255, 255), anchor="ma")
    dx = M + 508
    d.rectangle([dx, y, dx + 488, y + 96], fill=(252, 238, 238), outline=RED, width=2)
    d.text((dx + 6, y + 3), "DATE CHECK - NOT TUESDAY'S NEWS: NAMED, DATED, LEFT OUT ON PURPOSE", font=F(ARCHB, 9), fill=RED)
    for i, line in enumerate(DATECHECK):
        d.text((dx + 6, y + 17 + i * 9), line, font=F(ARCH, 8), fill=(90, 30, 30))
    d.text((dx + 6, y + 86), "Tonight's real count: 7 sea drones, at the top of this page.", font=F(ARCHB, 8), fill=RED)
    # footer
    y = 968
    d.line([M, y, M + W, y], fill=CHAR, width=2)
    d.text((M, y + 5), "SOURCES: Reuters - AP - BBC - CNN - Times - Guardian - Treasury - CoinPaprika - HS - WicketPulse - Mint - HK News TV - IANS - JagranJosh - ObserverVoice - Gadgets360 - salonvision - ActiveInvestorMag",
           font=F(ARCH, 9), fill=INK)
    d.text((M, y + 19), "CERTAINTY: REPORTED = confirmed by the named source. Every story on this page is dated Tuesday 24 November 2026 or the Monday-evening wires carried into Tuesday's edition, as labelled.",
           font=F(ARCH, 9), fill=GREY)
    d.text((M, y + 33), "Pictures and map: original, drawn in code.", font=F(ARCHB, 10), fill=BLUE)
    img.save(out, optimize=True)
    return out

if __name__ == "__main__":
    variant = sys.argv[1] if len(sys.argv) > 1 else "A"
    out = sys.argv[2]
    build(variant, out)
    print("wrote", out)
