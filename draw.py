#!/usr/bin/env python3
"""news-23 b138 heroes-scene: draw THE WORLD TODAY front page, 1024x1024.

Fresh implementation for make.fun news-image-20261123 (23 Nov 2026).
Heroes are BIG drawn scenes; skeleton: masthead, kicker, number strip,
region bar, UTC strip, 3 hero scenes, 10 cards, map + ALSO, DATE CHECK.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 10  # outer margin
RIGHT = W - M

FD = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FD, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FD, "DejaVuSans.ttf")
SANS_B = os.path.join(FD, "DejaVuSans-Bold.ttf")

PAPER = (247, 243, 232)
INK = (26, 26, 26)
RED = (139, 26, 26)
DARKRED = (110, 18, 18)
GOLD = (176, 132, 16)
GOLD_L = (212, 175, 55)
NAVY = (31, 58, 95)
NAVY_D = (22, 35, 63)
GREEN = (30, 107, 52)
TEAL = (0, 110, 110)
PURPLE = (96, 60, 140)
GRAY = (90, 90, 90)
LIGHT = (242, 236, 217)
CREAM2 = (238, 231, 210)


def F(path, size):
    return ImageFont.truetype(path, size)


def tw(draw, text, font):
    """Text width in px."""
    b = draw.textbbox((0, 0), text, font=font)
    return b[2] - b[0]


def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(draw, t, font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_font(draw, text, path, size, max_w, min_size=8):
    """Largest font size <= size that fits text in max_w."""
    s = size
    while s > min_size:
        f = F(path, s)
        if tw(draw, text, f) <= max_w:
            return f
        s -= 1
    return F(path, min_size)


def draw_wrapped(draw, x, y, text, font, fill, max_w, lh=None):
    lines = wrap(draw, text, font, max_w)
    if lh is None:
        lh = font.size + 3
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def chip(draw, x, y, text, fill):
    """Small pill chip; returns right edge."""
    f = F(SANS_B, 8)
    w = tw(draw, text, f) + 10
    h = 13
    draw.rounded_rectangle([x, y, x + w, y + h], radius=6, fill=fill)
    draw.text((x + 5, y + 2), text, font=f, fill=(255, 255, 255))
    return x + w


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------- masthead ----------
    d.text((M, 6), "THE WORLD TODAY", font=F(SERIF_B, 46), fill=INK)
    d.text((RIGHT, 24), "MONDAY 23 NOVEMBER 2026",
           font=F(SANS_B, 16), fill=GOLD, anchor="ra")
    d.line([(M, 58), (RIGHT, 58)], fill=INK, width=2)

    # ---------- kicker ----------
    d.rectangle([M, 62, RIGHT, 86], fill=RED)
    kick = ("AI rout hits Asia  \u00b7  UN chief urges AI rules  \u00b7  "
            "US lead over China at record low  \u00b7  Anthropic IPO $107.3B")
    d.text((M + 8, 68), kick, font=F(SANS_B, 13), fill=(255, 255, 255))

    # ---------- number strip (2 rows x 5) ----------
    nums = [
        ("-3.3%", "KOSPI"), ("5.3", "US-CHINA POWER GAP"),
        ("11,762", "EBOLA CASES, DRC"), ("10T won", "SEOUL STABILISATION FUND"),
        ("2%", "BILLIONAIRE TAX IN PARIS"),
        ("$450M", "SKUBAL DEAL"), ("165", "RUSSIAN MISSILES/WEEK"),
        ("12,000", "CLEARED IN MANCHESTER"), ("264 kg", "EXPLOSIVES SEIZED"),
        ("$107.3B", "ANTHROPIC IPO"),
    ]
    col_w = (RIGHT - M) / 5.0
    for i, (val, lab) in enumerate(nums):
        r, c = divmod(i, 5)
        x = M + c * col_w + 4
        yv = 88 + r * 24
        d.text((x, yv), val, font=F(SANS_B, 18), fill=INK)
        d.text((x, yv + 18), lab, font=F(SANS_B, 8), fill=GRAY)
        if c:
            d.line([(M + c * col_w, 90), (M + c * col_w, 138)], fill=(200, 192, 172))

    # ---------- region bar ----------
    segs = [("ASIA-PACIFIC 7", 226, NAVY), ("AMERICAS 8", 259, RED),
            ("MIDDLE EAST 6", 194, PURPLE), ("EUROPE 5", 162, TEAL),
            ("AFRICA 3", 97, GREEN), ("WORLD 2", 66, GOLD)]
    x = M
    for label, wseg, col in segs:
        d.rectangle([x, 146, x + wseg - 1, 164], fill=col)
        f = fit_font(d, label, SANS_B, 11, wseg - 6)
        d.text((x + wseg / 2, 150), label, font=f, fill=(255, 255, 255),
               anchor="ma")
        x += wseg

    # ---------- UTC strip ----------
    d.text((M, 168),
           "THE DAY IN UTC   ~00:00 Kospi dives   ~05:30 Guterres opens   "
           "~09:00 Power Index   ~12:00 Paris 2% tax   ~15:00 Kyiv missiles",
           font=F(SANS, 10), fill=GRAY)
    d.text((RIGHT, 168), "~ APPROX", font=F(SANS, 10), fill=GRAY, anchor="ra")

    # ---------- hero scenes ----------
    cols = [M, 348, 686]
    cw = 328
    sy, sh = 186, 144  # scene top, scene height
    band_y = sy + sh - 18  # caption band top

    # --- scene 1: Kospi skyline + falling chart ---
    x0 = cols[0]
    d.rectangle([x0, sy, x0 + cw, sy + sh], fill=NAVY_D)
    # buildings along the bottom (below chart, above caption band)
    import random
    rnd = random.Random(23)
    bx = x0 + 4
    while bx < x0 + cw - 14:
        bw = rnd.randint(18, 30)
        bh = rnd.randint(28, 62)
        by = band_y - bh
        d.rectangle([bx, by, bx + bw, band_y], fill=(38, 58, 96))
        for wy in range(by + 6, band_y - 4, 10):
            for wx in range(bx + 4, bx + bw - 3, 8):
                if rnd.random() < 0.55:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 90))
        bx += bw + 3
    # falling orange chart, starting right of the big number
    pts = [(x0 + 168, 226), (x0 + 198, 238), (x0 + 228, 244),
           (x0 + 258, 262), (x0 + 288, 274), (x0 + 316, 292)]
    d.line(pts, fill=(255, 140, 40), width=3)
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 255, 255))
    d.text((x0 + 10, sy + 6), "-3.3%", font=F(SANS_B, 40), fill=(255, 255, 255))
    d.rectangle([x0, band_y, x0 + cw, sy + sh], fill=(0, 0, 0))
    d.text((x0 + 6, band_y + 4),
           "KOSPI 4,708.54 \u00b7 -161 PTS \u00b7 SAMSUNG -3.1% \u00b7 HYNIX -2.5%",
           font=F(SANS_B, 9), fill=(255, 255, 255))

    # --- scene 2: Guterres globe ---
    x1 = cols[1]
    d.rectangle([x1, sy, x1 + cw, sy + sh], fill=GREEN)
    # globe on its own masked layer, right side
    gl = Image.new("RGBA", (cw, sh), (0, 0, 0, 0))
    gd = ImageDraw.Draw(gl)
    cx, cy, r = 258, 66, 52
    gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(200, 230, 190, 255))
    for k in range(-2, 3):
        gd.arc([cx - r + 12 * k, cy - r, cx + r + 12 * k, cy + r],
               start=270, end=90, fill=(90, 160, 100, 255), width=2)
        gd.arc([cx - r, cy - r + 14 * k, cx + r, cy + r + 14 * k],
               start=180, end=360, fill=(90, 160, 100, 255), width=2)
    mask = Image.new("L", (cw, sh), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    img.paste(gl, (x1, sy), mask)
    # gold text, left of the globe, clear of the caption band
    d.text((x1 + 10, sy + 4), "150", font=F(SANS_B, 40), fill=GOLD_L)
    d.text((x1 + 10, sy + 50), "DELEGATES", font=F(SANS_B, 15), fill=GOLD_L)
    d.text((x1 + 10, sy + 69), "BACK A RISK", font=F(SANS_B, 15), fill=GOLD_L)
    d.text((x1 + 10, sy + 88), "FRAMEWORK", font=F(SANS_B, 15), fill=GOLD_L)
    d.rectangle([x1, band_y, x1 + cw, sy + sh], fill=(0, 0, 0))
    d.text((x1 + 6, band_y + 4), "BRIDGETOWN SUMMIT, BARBADOS",
           font=F(SANS_B, 9), fill=GOLD_L)

    # --- scene 3: Power Index bars ---
    x2 = cols[2]
    d.rectangle([x2, sy, x2 + cw, sy + sh], fill=LIGHT)
    d.rectangle([x2, sy, x2 + cw, sy + sh], outline=(190, 182, 160))
    d.text((x2 + 8, sy + 6), "NARROWEST SINCE 2018",
           font=F(SANS_B, 12), fill=INK)
    d.text((x2 + cw - 8, sy + 6), "GAP 5.3", font=F(SANS_B, 12),
           fill=RED, anchor="ra")
    bars = [("78.9", "US", 250, NAVY), ("73.6", "CHINA", 233, RED),
            ("40.5", "INDIA", 129, GOLD)]
    by = sy + 34
    for val, lab, bw, col in bars:
        d.text((x2 + 8, by + 3), val, font=F(SANS_B, 12), fill=INK)
        bx = x2 + 52
        d.rectangle([bx, by, bx + bw, by + 20], fill=col)
        # label INSIDE the right end of the bar (white on colour)
        lf = F(SANS_B, 11)
        d.text((bx + bw - 4, by + 4), lab, font=lf, fill=(255, 255, 255),
               anchor="ra")
        by += 26
    d.text((x2 + 8, band_y + 4), "ASIA POWER INDEX 2026 \u00b7 LOWY INSTITUTE",
           font=F(SANS, 9), fill=GRAY)

    # --- hero headlines / bodies / sources (below scenes, clear of strip) ---
    heroes = [
        ("AI ROUT HITS ASIA",
         "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. "
         "Samsung -3.1%, SK Hynix -2.5%.",
         "KOREA EXCHANGE"),
        ("GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
         "UN chief urges global AI safety rules at the Bridgetown summit; "
         "150 back a risk framework.",
         "UNITED NATIONS"),
        ("US LEAD OVER CHINA AT RECORD LOW",
         "Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, "
         "narrowest since 2018. India third at 40.5.",
         "LOWY INSTITUTE"),
    ]
    hy = sy + sh + 8
    for (hl, body, src), x in zip(heroes, cols):
        y = draw_wrapped(d, x, hy, hl, F(SANS_B, 19), INK, cw, lh=22)
        y = draw_wrapped(d, x, y + 2, body, F(SANS, 10), INK, cw, lh=13)
        d.text((x, y + 4), src, font=F(SANS, 9), fill=GRAY)
        chip(d, x + cw - 62, y + 3, "REPORTED", NAVY)

    # ---------- black strip: more of the day ----------
    d.rectangle([M, 440, RIGHT, 460], fill=INK)
    d.text((M + 6, 445), "MORE OF THE DAY  \u2014  10 STORIES",
           font=F(SANS_B, 12), fill=(255, 255, 255))

    # ---------- 10 cards ----------
    cards = [
        ("AMERICAS", "BESSENT: NVIDIA ANSWERS", "Treasury wants answers.",
         "WSJ", "REPORTED"),
        ("AMERICAS", "FBI PROBES NCIC HACK", "NCIC database hacked.",
         "AP", "REPORTED"),
        ("WHITE HOUSE", "IRAN STRIKES MAY RESUME", "May resume in New Year.",
         "Reuters", "REPORTED"),
        ("MARKETS", "US FUTURES JUMP 3%", "Holiday rally lifts 3%.",
         "Bloomberg", "REPORTED"),
        ("SPORT", "SKUBAL'S $450M METS DEAL", "Nine-year, largest ever.",
         "AP", "REPORTED"),
        ("SPORT", "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice.",
         "ESPN", "REPORTED"),
        ("LEGAL", "STATES SUE SPACEX", "Ten states sue over AI.",
         "AP", "REPORTED"),
        ("TECH", "ANTHROPIC IPO: $107.3B", "Raised $83; closes $97.17.",
         "WSJ", "REPORTED"),
        ("EUROPE", "3 MISSILES CROSSED AIRSPACE", "Kyiv: 3 Kh-101s crossed.",
         "AP", "CLAIM"),
        ("SPACE", "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.",
         "Reuters", "CLAIM"),
    ]
    cat_col = {"AMERICAS": RED, "WHITE HOUSE": PURPLE, "MARKETS": TEAL,
               "SPORT": RED, "LEGAL": NAVY, "TECH": TEAL, "EUROPE": RED,
               "SPACE": NAVY}
    card_w, card_h, gap = 194, 64, 8
    for i, (cat, hl, body, src, tag) in enumerate(cards):
        r, c = divmod(i, 5)
        cx = M + c * (card_w + gap)
        cy = 464 + r * (card_h + 4)
        nf = F(SANS_B, 10)
        d.text((cx, cy), f"{i + 1}", font=nf, fill=RED)
        d.text((cx + tw(d, str(i + 1), nf) + 5, cy), cat,
               font=F(SANS_B, 9), fill=cat_col[cat])
        hf = fit_font(d, hl, SANS_B, 12, card_w)
        d.text((cx, cy + 14), hl, font=hf, fill=INK)
        d.text((cx, cy + 31), body, font=F(SANS, 9), fill=INK)
        d.text((cx, cy + 48), src, font=F(SANS, 8), fill=GRAY)
        chip(d, cx + card_w - 58, cy + 47, tag,
             NAVY if tag == "REPORTED" else RED)

    # ---------- black strip: where it happened ----------
    d.rectangle([M, 602, RIGHT, 622], fill=INK)
    d.text((M + 6, 607), "WHERE IT HAPPENED",
           font=F(SANS_B, 12), fill=(255, 255, 255))

    # ---------- map ----------
    mx0, my0, mw, mh = M, 626, 420, 202
    blob = (214, 228, 190)
    # Americas blob
    d.polygon([(30, 640), (120, 632), (150, 660), (140, 740), (110, 800),
               (60, 806), (34, 760), (24, 700)], fill=blob)
    # Eurasia blob
    d.polygon([(180, 648), (300, 636), (392, 652), (398, 700), (360, 748),
               (300, 756), (220, 748), (182, 700)], fill=blob)
    # Africa blob
    d.polygon([(268, 752), (330, 748), (336, 790), (310, 818), (276, 812),
               (262, 780)], fill=blob)
    pins = [
        (1, 360, 700), (2, 60, 780), (3, 345, 690), (4, 95, 720),
        (5, 120, 700), (6, 265, 680), (7, 235, 700), (8, 225, 680),
        (9, 275, 700), (10, 215, 665), (11, 300, 730), (12, 295, 750),
        (13, 290, 775),
    ]
    pf = F(SANS_B, 9)
    for n, px, py in pins:
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                  outline=(255, 255, 255), width=1)
        d.text((px, py), str(n), font=pf, fill=(255, 255, 255), anchor="mm")
    d.text((mx0, 796), "Pins 1\u201313: 1 Seoul \u00b7 2 Bridgetown \u00b7 3 Beijing \u00b7 4 Washington",
           font=F(SANS, 9), fill=INK)
    d.text((mx0, 808), "5 New York \u00b7 6 Kyiv \u00b7 7 Paris \u00b7 8 London \u00b7 9 Warsaw \u00b7 10 Manchester",
           font=F(SANS, 9), fill=INK)
    d.text((mx0, 820), "11 Beirut \u00b7 12 Gaza \u00b7 13 Khartoum",
           font=F(SANS, 9), fill=INK)

    # ---------- ALSO ----------
    ax = 440
    d.text((ax, 626), "ALSO ON MONDAY", font=F(SANS_B, 12), fill=INK)
    also = [
        ("14. Paris: 100+ back 2% billionaire tax", False),
        ("15. Manchester: 12,000 cleared", False),
        ("16. Zelenskyy: 165 missiles in a week", False),
        ("17. COP31: the day after Antalya pact rejected", False),
        ("18. Israel unity talks resume", False),
        ("19. Gaza: two killed in Israeli strike", False),
        ("20. West Bank settler attacks", False),
        ("21. Iran war: no deal in sight", False),
        ("22. Lebanon seizes 264 kg explosives", False),
        ("23. Bahrain: strike hits plant, 2 hurt", False),
        ("24. Benghazi: UN demands probe [CLAIM]", True),
        ("25. Sudan: defences down drones [CLAIM]", True),
        ("26. DRC: fighting traps Ebola teams", False),
        ("27. Bangladesh: Hasina jailed if she returns", False),
        ("28. Seoul minister quits over AI exam row", False),
        ("29. SK Telecom -7.3% as hype cools", False),
        ("30. China eases margin rules", False),
        ("31. Seoul readies 10T-won fund", False),
    ]
    af = F(SANS, 10)
    for i, (txt, is_claim) in enumerate(also):
        col = i // 9
        row = i % 9
        x = ax + col * 295
        y = 646 + row * 20
        if is_claim:
            base = txt.replace(" [CLAIM]", "")
            d.text((x, y), base, font=af, fill=INK)
            d.text((x + tw(d, base, af) + 3, y), "[CLAIM]",
                   font=F(SANS_B, 10), fill=RED)
        else:
            d.text((x, y), txt, font=af, fill=INK)

    # ---------- DATE CHECK ----------
    d.rectangle([M, 836, RIGHT, 918], outline=RED, width=2, fill=(253, 238, 238))
    d.text((M + 8, 842),
           "DATE CHECK  \u2014  READ 23 NOV 2026, 23:59 UTC  \u00b7  "
           "STORIES DATED 23 NOV ONLY",
           font=F(SANS_B, 12), fill=RED)
    draw_wrapped(d, M + 8, 862,
                 "LEFT OUT \u2014 NOT 23 NOV: Dems reach 258 (22 Nov) \u00b7 "
                 "Sparta II fire (22 Nov) \u00b7 El Chapo Isidro captured "
                 "(22 Nov) \u00b7 EU\u2013Indonesia pact (21 Nov) \u00b7 "
                 "Nigeria boat (21 Nov) \u00b7 ICJ Myanmar ruling (19 Nov)",
                 F(SANS, 10), INK, RIGHT - M - 16, lh=13)
    draw_wrapped(d, M + 8, 892,
                 "NOT YET \u2014 Dymer search continues (14 missing) \u00b7 "
                 "4 House races uncalled \u00b7 COP32 venue not set \u00b7 "
                 "WHO evacuating trapped Ebola staff",
                 F(SANS, 10), INK, RIGHT - M - 16, lh=13)

    # ---------- footer ----------
    d.text((M, 926),
           "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 Yonhap \u00b7 BBC \u00b7 "
           "WSJ \u00b7 ESPN \u00b7 Lowy Institute (Asia Power Index 2026).",
           font=F(SANS, 9), fill=GRAY)
    d.text((M, 940),
           "CHIPS: REPORTED = confirmed by wires \u00b7 CLAIM = one side's claim, "
           "independently unconfirmed \u00b7 ONGOING = still developing.",
           font=F(SANS, 9), fill=GRAY)
    d.text((M, 954),
           "All times UTC. Figures as reported 23 Nov 2026. "
           "Scenes are drawn illustrations, not photographs.",
           font=F(SANS, 9), fill=GRAY)
    d.line([(M, 972), (RIGHT, 972)], fill=GOLD, width=2)
    d.text((W // 2, 982),
           "THE WORLD TODAY  \u00b7  Monday 23 November 2026  \u00b7  "
           "31 stories  \u00b7  6 regions",
           font=F(SANS_B, 12), fill=GOLD, anchor="ma")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")
    print("saved", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
