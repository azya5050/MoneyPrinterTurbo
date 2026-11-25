"""Sahne görsellerini PIL ile üretir (1920x1080 noir / dosya estetiği)."""

from __future__ import annotations

import math
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1920, 1080

BG = (11, 13, 16)
PAPER = (226, 218, 200)
INK = (28, 26, 24)
WHITE = (236, 230, 218)
GREY = (140, 140, 140)
RED = (200, 36, 36)

FONT_BLACK = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
FONT_BOLD = "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"
FONT_MONO = "/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf"
FONT_SERIF = "/usr/share/fonts/truetype/freefont/FreeSerifBoldItalic.ttf"


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def _rng(seed: int) -> random.Random:
    return random.Random(seed)


def background(seed: int, base=BG) -> Image.Image:
    """Koyu, hafif dokulu ve ortası aydınlık bir arka plan."""
    img = Image.new("RGB", (W, H), base)
    glow = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(glow)
    d.ellipse((W * 0.15, H * 0.05, W * 0.85, H * 0.95), fill=55)
    glow = glow.filter(ImageFilter.GaussianBlur(220))
    lift = Image.new("RGB", (W, H), (60, 58, 56))
    img = Image.composite(lift, img, glow)
    # ince toz / doku
    r = _rng(seed)
    d = ImageDraw.Draw(img)
    for _ in range(900):
        x, y = r.randrange(W), r.randrange(H)
        c = r.randrange(18, 40)
        d.point((x, y), fill=(c, c, c))
    return img


def header(img: Image.Image, label: str = "DOSYA: NORJAK · 1971") -> None:
    d = ImageDraw.Draw(img)
    f = font(FONT_MONO, 26)
    d.rectangle((60, 52, 72, 64), fill=RED)
    d.text((88, 44), label, font=f, fill=(170, 165, 155))
    f2 = font(FONT_MONO, 26)
    t = "ÇÖZÜLMEDİ"
    tw = d.textlength(t, font=f2)
    d.text((W - 60 - tw, 44), t, font=f2, fill=RED)


def center_text(d, y, text, f, fill, spacing=10):
    lines = text.split("\n")
    for line in lines:
        bbox = d.textbbox((0, 0), line, font=f)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        d.text(((W - w) / 2 - bbox[0], y - bbox[1]), line, font=f, fill=fill)
        y += h + spacing
    return y


def fit_font(d, text, path, max_w, start, min_size=40):
    size = start
    while size > min_size:
        f = font(path, size)
        widest = max(d.textlength(line, font=f) for line in text.split("\n"))
        if widest <= max_w:
            return f
        size -= 4
    return font(path, min_size)


def stamp(img: Image.Image, text: str, xy, angle=-12, size=70, color=RED) -> None:
    f = font(FONT_BLACK, size)
    tmp = Image.new("RGBA", (1, 1))
    tw = int(ImageDraw.Draw(tmp).textlength(text, font=f))
    layer = Image.new("RGBA", (tw + 60, size + 60), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rectangle((6, 6, tw + 54, size + 54), outline=color + (210,), width=7)
    d.text((30, 18), text, font=f, fill=color + (210,))
    layer = layer.rotate(angle, expand=True, resample=Image.BICUBIC)
    img.paste(layer, (int(xy[0]), int(xy[1])), layer)


def paper(size, seed, color=PAPER) -> Image.Image:
    w, h = size
    p = Image.new("RGB", (w, h), color)
    r = _rng(seed)
    d = ImageDraw.Draw(p)
    for _ in range(int(w * h / 180)):
        x, y = r.randrange(w), r.randrange(h)
        v = r.randrange(-18, 8)
        c = tuple(max(0, min(255, ch + v)) for ch in color)
        d.point((x, y), fill=c)
    # kenarlarda eskime
    edge = Image.new("L", (w, h), 0)
    ImageDraw.Draw(edge).rectangle((0, 0, w, h), outline=255, width=30)
    edge = edge.filter(ImageFilter.GaussianBlur(25))
    dark = Image.new("RGB", (w, h), tuple(int(c * 0.72) for c in color))
    return Image.composite(dark, p, edge)


def paste_rotated(img, layer, center, angle, shadow=True):
    layer = layer.convert("RGBA").rotate(angle, expand=True, resample=Image.BICUBIC)
    x = int(center[0] - layer.width / 2)
    y = int(center[1] - layer.height / 2)
    if shadow:
        sh = Image.new("RGBA", layer.size, (0, 0, 0, 0))
        sh.putalpha(layer.split()[3].point(lambda a: int(a * 0.7)))
        sh = sh.filter(ImageFilter.GaussianBlur(18))
        img.paste((0, 0, 0), (x + 18, y + 24), sh)
    img.paste(layer, (x, y), layer)


# ----------------------------------------------------------------- sahneler


def scene_title(s, seed):
    img = background(seed)
    d = ImageDraw.Draw(img)
    f = fit_font(d, s["title"], FONT_BLACK, W - 300, 190)
    y = center_text(d, 300, s["title"], f, WHITE, spacing=24)
    d.rectangle((W / 2 - 160, y + 30, W / 2 + 160, y + 40), fill=RED)
    center_text(d, y + 80, s["subtitle"], font(FONT_MONO, 52), (190, 185, 175))
    header(img)
    return img


def scene_chapter(s, seed):
    img = background(seed, base=(8, 8, 10))
    d = ImageDraw.Draw(img)
    center_text(d, 360, s["num"], font(FONT_MONO, 60), RED)
    f = fit_font(d, s["title"], FONT_BLACK, W - 300, 230)
    y = center_text(d, 460, s["title"], f, WHITE)
    d.rectangle((W / 2 - 90, y + 40, W / 2 + 90, y + 48), fill=RED)
    header(img)
    return img


def scene_date(s, seed):
    img = background(seed)
    d = ImageDraw.Draw(img)
    f = fit_font(d, s["big"], FONT_BLACK, W - 280, 240)
    y = center_text(d, 340, s["big"], f, WHITE)
    # konum pini
    cx, cy = W / 2, y + 90
    d.ellipse((cx - 16, cy - 16, cx + 16, cy + 16), fill=RED)
    center_text(d, cy + 50, s["small"], fit_font(d, s["small"], FONT_MONO, W - 200, 48, 28), (190, 185, 175))
    header(img)
    return img


def scene_ticket(s, seed):
    img = background(seed)
    tw, th = 1300, 560
    t = paper((tw, th), seed, color=(232, 222, 196))
    d = ImageDraw.Draw(t)
    d.rectangle((0, 0, tw, 110), fill=(150, 30, 30))
    d.text((40, 26), "YOLCU BİLETİ · UÇUŞ KUPONU", font=font(FONT_BOLD, 54), fill=(245, 235, 220))
    # delikli ayrım çizgisi
    for yy in range(130, th, 28):
        d.ellipse((960, yy, 972, yy + 12), fill=(60, 55, 50))
    mono = font(FONT_MONO, 40)
    small = font(FONT_MONO, 28)
    rows = [("YOLCU ADI", s["name"]), ("GÜZERGAH", s["route"]), ("SEFER", s["flight"]), ("ÜCRET / NAKİT", s["price"])]
    y = 150
    for k, v in rows:
        d.text((50, y), k, font=small, fill=(110, 100, 90))
        d.text((50, y + 32), v, font=mono, fill=INK)
        y += 100
    d.text((1000, 160), "TEK YÖN", font=font(FONT_BOLD, 52), fill=INK)
    d.text((1000, 240), "KİMLİK", font=small, fill=(110, 100, 90))
    d.text((1000, 275), "SORULMADI", font=font(FONT_MONO, 36), fill=RED)
    d.text((1000, 360), "24.11.1971", font=font(FONT_MONO, 36), fill=INK)
    paste_rotated(img, t, (W / 2, H / 2 + 30), -4)
    header(img)
    return img


def silhouette(size=(520, 640)):
    w, h = size
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rectangle((0, 0, w, h), fill=(52, 52, 54, 255))
    col = (18, 18, 20, 255)
    d.ellipse((w * 0.30, h * 0.14, w * 0.70, h * 0.58), fill=col)  # baş
    d.rectangle((w * 0.42, h * 0.52, w * 0.58, h * 0.66), fill=col)  # boyun
    d.ellipse((w * 0.04, h * 0.62, w * 0.96, h * 1.40), fill=col)  # omuzlar
    # gömlek yakası + kravat
    d.polygon([(w * 0.42, h * 0.64), (w * 0.5, h * 0.74), (w * 0.58, h * 0.64)], fill=(220, 220, 215, 255))
    d.polygon([(w * 0.48, h * 0.72), (w * 0.52, h * 0.72), (w * 0.55, h * 1.0), (w * 0.45, h * 1.0)], fill=(5, 5, 5, 255))
    d.text((w * 0.43, h * 0.22), "?", font=font(FONT_BLACK, 200), fill=(70, 70, 72, 255))
    for x in range(0, w, 1):
        pass
    # boy cetveli çizgileri
    for i, yy in enumerate(range(20, h, 60)):
        d.line((0, yy, 24, yy), fill=(120, 120, 120, 255), width=2)
    return layer


def scene_profile(s, seed):
    img = background(seed)
    folder = paper((1600, 820), seed, color=(205, 180, 130))
    d = ImageDraw.Draw(folder)
    sil = silhouette((480, 600))
    folder.paste(sil, (70, 120), sil)
    d.rectangle((70, 120, 550, 720), outline=(60, 50, 40), width=4)
    d.text((640, 110), s["name"], font=fit_font(d, s["name"], FONT_BLACK, 900, 80, 40), fill=INK)
    d.line((640, 215, 1520, 215), fill=(90, 70, 50), width=4)
    y = 260
    for line in s["lines"]:
        d.text((640, y), "▪", font=font(FONT_MONO, 40), fill=(150, 30, 30))
        d.text((690, y), line, font=fit_font(d, line, FONT_MONO, 840, 40, 26), fill=INK)
        y += 80
    paste_rotated(img, folder, (W / 2, H / 2 + 40), 1.5)
    stamp(img, "ŞÜPHELİ", (1430, 800), angle=-10, size=64)
    header(img)
    return img


def scene_note(s, seed):
    img = background(seed)
    n = paper((900, 640), seed + 3, color=(238, 233, 220))
    d = ImageDraw.Draw(n)
    for yy in range(140, 640, 72):
        d.line((40, yy, 860, yy), fill=(170, 190, 215), width=2)
    d.line((110, 0, 110, 640), fill=(220, 140, 140), width=2)
    f = font(FONT_SERIF, 70)
    y = 70
    for line in s["lines"]:
        d.text((140, y), line, font=f, fill=(30, 40, 90))
        y += 140 if line.endswith(",") else 120
    # katlama izi
    d.line((0, 320, 900, 320), fill=(205, 198, 182), width=3)
    paste_rotated(img, n, (W / 2, H / 2 + 30), 3)
    header(img)
    return img


def scene_bomb(s, seed):
    img = background(seed)
    d = ImageDraw.Draw(img)
    # açık evrak çantası
    x0, y0, x1, y1 = 360, 300, 1560, 880
    d.rounded_rectangle((x0, y0, x1, y1), radius=30, fill=(26, 24, 22), outline=(70, 66, 60), width=8)
    d.rounded_rectangle((x0 + 40, y0 + 40, x1 - 40, y1 - 40), radius=16, fill=(48, 40, 34))
    # kırmızı silindirler
    for i in range(8):
        cx = x0 + 120 + i * 90
        d.rounded_rectangle((cx, y0 + 90, cx + 66, y1 - 150), radius=28, fill=(170, 30, 28), outline=(90, 10, 10), width=3)
        d.rectangle((cx + 4, y0 + 140, cx + 62, y0 + 160), fill=(120, 18, 18))
    # pil
    d.rectangle((x1 - 330, y0 + 110, x1 - 110, y0 + 420), fill=(30, 30, 30), outline=(110, 110, 110), width=4)
    d.rectangle((x1 - 290, y0 + 90, x1 - 250, y0 + 110), fill=(150, 150, 150))
    d.rectangle((x1 - 190, y0 + 90, x1 - 150, y0 + 110), fill=(150, 150, 150))
    d.text((x1 - 300, y0 + 240), "6V", font=font(FONT_BLACK, 90), fill=(200, 170, 40))
    # kablolar
    r = _rng(seed)
    for col in [(200, 40, 40), (220, 200, 60), (40, 120, 220), (230, 230, 230)]:
        pts = []
        sx, sy = x0 + 160 + r.randrange(500), y0 + 120
        ex, ey = x1 - 240 + r.randrange(-60, 60), y0 + 100
        for t in range(0, 21):
            tt = t / 20
            px = sx + (ex - sx) * tt
            py = sy + (ey - sy) * tt + math.sin(tt * math.pi) * (90 + r.randrange(160))
            pts.append((px, py))
        d.line(pts, fill=col, width=7, joint="curve")
    header(img)
    stamp(img, "GERÇEK MİYDİ?", (1260, 860), angle=-8, size=56)
    return img


def scene_list(s, seed):
    img = background(seed)
    d = ImageDraw.Draw(img)
    d.text((220, 200), s["title"], font=font(FONT_BLACK, 110), fill=WHITE)
    d.rectangle((222, 340, 400, 350), fill=RED)
    y = 420
    for i, item in enumerate(s["items"]):
        d.text((220, y), f"{i + 1:02d}", font=font(FONT_MONO, 52), fill=RED)
        d.text((340, y), item, font=fit_font(d, item, FONT_BOLD, 1400, 58, 36), fill=(225, 220, 210))
        y += 110
    header(img)
    return img


def scene_fact(s, seed):
    img = background(seed)
    d = ImageDraw.Draw(img)
    f = fit_font(d, s["big"], FONT_BLACK, W - 300, 360)
    y = center_text(d, 280, s["big"], f, RED)
    d.rectangle((W / 2 - 120, y + 40, W / 2 + 120, y + 48), fill=WHITE)
    center_text(d, y + 90, s["small"], fit_font(d, s["small"], FONT_MONO, W - 240, 52, 28), (200, 195, 185))
    header(img)
    return img


def banknote(seed, size=(520, 222)):
    w, h = size
    n = paper(size, seed, color=(178, 190, 168))
    d = ImageDraw.Draw(n)
    d.rectangle((10, 10, w - 10, h - 10), outline=(60, 80, 60), width=5)
    d.rectangle((22, 22, w - 22, h - 22), outline=(90, 110, 90), width=2)
    d.ellipse((w / 2 - 70, h / 2 - 80, w / 2 + 70, h / 2 + 80), fill=(150, 165, 140), outline=(60, 80, 60), width=3)
    d.text((40, 30), "20", font=font(FONT_BLACK, 60), fill=(40, 60, 40))
    d.text((w - 110, h - 95), "20", font=font(FONT_BLACK, 60), fill=(40, 60, 40))
    r = _rng(seed)
    serial = f"L{r.randrange(10**7, 10**8)}{chr(65 + r.randrange(26))}"
    d.text((w - 260, 34), serial, font=font(FONT_MONO, 28), fill=(40, 70, 40))
    d.text((40, h - 60), serial, font=font(FONT_MONO, 28), fill=(40, 70, 40))
    return n


def scene_money(s, seed):
    img = background(seed)
    r = _rng(seed)
    for i in range(16):
        bn = banknote(seed + i)
        cx = 260 + (i % 4) * 470 + r.randrange(-40, 40)
        cy = 220 + (i // 4) * 220 + r.randrange(-30, 30)
        paste_rotated(img, bn, (cx, cy), r.uniform(-14, 14))
    d = ImageDraw.Draw(img)
    d.rectangle((0, H - 250, W, H - 110), fill=(8, 8, 10))
    center_text(d, H - 230, "10.000 × $20  ·  TÜM SERİ NUMARALARI KAYDEDİLDİ", font(FONT_MONO, 50), WHITE)
    header(img)
    return img


def scene_quote(s, seed):
    img = background(seed)
    d = ImageDraw.Draw(img)
    f = fit_font(d, s["quote"], FONT_SERIF, W - 320, 150)
    y = center_text(d, 380, s["quote"], f, WHITE)
    center_text(d, y + 60, s["who"], fit_font(d, s["who"], FONT_MONO, W - 260, 40, 26), (175, 170, 160))
    header(img)
    return img


def scene_map(s, seed):
    img = background(seed, base=(10, 14, 18))
    d = ImageDraw.Draw(img)
    lat0, lat1 = 38.6, 48.4
    lon0, lon1 = -125.5, -117.0

    def P(lat, lon):
        x = 300 + (lon - lon0) / (lon1 - lon0) * 1320
        y = 110 + (lat1 - lat) / (lat1 - lat0) * 900
        return (x, y)

    # ızgara
    for la in range(39, 49):
        d.line((P(la, lon0), P(la, lon1)), fill=(28, 36, 44), width=1)
    for lo in range(-125, -116):
        d.line((P(lat0, lo), P(lat1, lo)), fill=(28, 36, 44), width=1)
    # kabaca Pasifik kıyı çizgisi
    coast = [(48.4, -124.7), (47.0, -124.2), (46.2, -124.0), (45.0, -124.0), (44.0, -124.1), (43.0, -124.5),
             (42.0, -124.3), (41.0, -124.1), (40.0, -124.2), (39.0, -123.7), (38.6, -123.4)]
    sea = [P(*c) for c in coast] + [P(38.6, lon0), P(48.4, lon0)]
    d.polygon(sea, fill=(14, 24, 34))
    d.line([P(*c) for c in coast], fill=(70, 90, 110), width=3)
    # Columbia nehri
    river = [(46.25, -124.0), (46.2, -123.4), (46.1, -123.0), (45.75, -122.78), (45.6, -122.4), (45.7, -121.5), (45.6, -120.9)]
    d.line([P(*c) for c in river], fill=(60, 110, 160), width=5)
    # rota
    sea_tac, pdx, reno = (47.45, -122.31), (45.59, -122.60), (39.50, -119.77)
    route = [sea_tac, (46.6, -122.6), (45.95, -122.55), pdx, (44.0, -121.9), (42.0, -121.0), reno]
    pts = [P(*c) for c in route]
    for a, b in zip(pts, pts[1:]):
        steps = int(math.dist(a, b) / 24)
        for i in range(0, steps, 2):
            p1 = (a[0] + (b[0] - a[0]) * i / steps, a[1] + (b[1] - a[1]) * i / steps)
            p2 = (a[0] + (b[0] - a[0]) * (i + 1) / steps, a[1] + (b[1] - a[1]) * (i + 1) / steps)
            d.line((p1, p2), fill=(230, 225, 210), width=5)
    # atlayış bölgesi
    jx, jy = P(45.95, -122.55)
    for rr, a in [(110, 40), (75, 70), (40, 120)]:
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(ov).ellipse((jx - rr, jy - rr, jx + rr, jy + rr), fill=(200, 36, 36, a))
        img.paste(ov, (0, 0), ov)
    d = ImageDraw.Draw(img)
    d.line((jx - 22, jy - 22, jx + 22, jy + 22), fill=WHITE, width=6)
    d.line((jx - 22, jy + 22, jx + 22, jy - 22), fill=WHITE, width=6)
    d.text((jx + 170, jy - 70), "TAHMİNİ ATLAYIŞ\nBÖLGESİ · 20:13", font=font(FONT_MONO, 34), fill=(255, 120, 110), spacing=8)
    tx, ty = P(45.72, -122.77)
    d.rectangle((tx - 9, ty - 9, tx + 9, ty + 9), fill=(250, 200, 60))
    d.text((tx - 330, ty + 40), "TENA BAR (1980)", font=font(FONT_MONO, 30), fill=(250, 200, 60))
    for name, c, off in [("SEATTLE", sea_tac, (24, -20)), ("PORTLAND", pdx, (30, 40)), ("RENO", reno, (24, -10))]:
        x, y = P(*c)
        d.ellipse((x - 14, y - 14, x + 14, y + 14), fill=WHITE)
        d.text((x + off[0], y + off[1] - 10), name, font=font(FONT_BOLD, 46), fill=WHITE)
    d.text((340, 960), "PASİFİK OKYANUSU", font=font(FONT_MONO, 30), fill=(70, 100, 130))
    header(img, "UÇUŞ 305 · ROTA")
    return img


def plane_layer(scale=1.0):
    w, h = int(1400 * scale), int(480 * scale)
    L = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    k = scale
    col = (6, 7, 9, 255)
    # gövde
    d.rounded_rectangle((60 * k, 200 * k, 1260 * k, 290 * k), radius=int(45 * k), fill=col)
    d.polygon([(1240 * k, 200 * k), (1360 * k, 236 * k), (1240 * k, 290 * k)], fill=col)  # burun
    d.polygon([(60 * k, 210 * k), (0, 190 * k), (10 * k, 260 * k), (60 * k, 285 * k)], fill=col)  # kuyruk konisi
    # T-kuyruk
    d.polygon([(40 * k, 210 * k), (110 * k, 30 * k), (190 * k, 30 * k), (170 * k, 210 * k)], fill=col)
    d.polygon([(70 * k, 40 * k), (250 * k, 25 * k), (250 * k, 45 * k), (70 * k, 60 * k)], fill=col)
    # arka motorlar (727: 3 motor)
    d.rounded_rectangle((150 * k, 170 * k, 330 * k, 215 * k), radius=int(20 * k), fill=col)
    # kanat
    d.polygon([(600 * k, 270 * k), (820 * k, 270 * k), (520 * k, 420 * k), (440 * k, 420 * k)], fill=col)
    # açık arka merdiven
    d.polygon([(70 * k, 285 * k), (130 * k, 285 * k), (40 * k, 410 * k), (10 * k, 400 * k)], fill=col)
    # pencereler
    for x in range(380, 1180, 38):
        d.rectangle((x * k, 228 * k, (x + 14) * k, 242 * k), fill=(200, 170, 90, 255))
    return L


def scene_plane(s, seed):
    img = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        c = (int(10 + 22 * t), int(14 + 24 * t), int(22 + 28 * t))
        d.line((0, y, W, y), fill=c)
    # bulutlar
    r = _rng(seed)
    cl = Image.new("L", (W, H), 0)
    cd = ImageDraw.Draw(cl)
    for _ in range(60):
        x, y = r.randrange(-200, W), r.randrange(int(H * 0.45), H + 100)
        rw, rh = r.randrange(200, 600), r.randrange(60, 160)
        cd.ellipse((x, y, x + rw, y + rh), fill=r.randrange(40, 110))
    cl = cl.filter(ImageFilter.GaussianBlur(40))
    img = Image.composite(Image.new("RGB", (W, H), (70, 78, 90)), img, cl)
    pl = plane_layer(0.95)
    img.paste(pl, (int(W / 2 - pl.width / 2), 250), pl)
    # yağmur
    d = ImageDraw.Draw(img)
    for _ in range(700):
        x, y = r.randrange(W), r.randrange(H)
        ln = r.randrange(20, 55)
        g = r.randrange(80, 150)
        d.line((x, y, x - ln * 0.25, y + ln), fill=(g, g, g + 10), width=1)
    # şimşek parıltısı
    flash = Image.new("L", (W, H), 0)
    ImageDraw.Draw(flash).ellipse((W * 0.6, -300, W * 1.3, 400), fill=70)
    flash = flash.filter(ImageFilter.GaussianBlur(160))
    img = Image.composite(Image.new("RGB", (W, H), (180, 190, 210)), img, flash)
    d = ImageDraw.Draw(img)
    d.rectangle((0, H - 210, W, H - 120), fill=(0, 0, 0))
    center_text(d, H - 195, s["caption"], font(FONT_MONO, 52), WHITE)
    header(img)
    return img


def scene_tie(s, seed):
    img = background(seed, base=(30, 30, 32))
    d = ImageDraw.Draw(img)
    cx = W / 2 - 200
    col = (8, 8, 10)
    d.rounded_rectangle((cx - 70, 170, cx + 70, 260), radius=14, fill=(70, 70, 75))  # klips
    d.polygon([(cx - 60, 250), (cx + 60, 250), (cx + 40, 330), (cx - 40, 330)], fill=col)  # düğüm
    d.polygon([(cx - 38, 330), (cx + 38, 330), (cx + 95, 880), (cx, 960), (cx - 95, 880)], fill=col)
    d.line((cx - 80, 520, cx + 80, 520), fill=(190, 170, 120), width=12)  # kravat iğnesi
    d.ellipse((cx - 14, 508, cx + 14, 532), fill=(235, 230, 220))
    # kanıt etiketi
    tag = paper((600, 360), seed, color=(240, 236, 226))
    td = ImageDraw.Draw(tag)
    td.rectangle((0, 0, 600, 80), fill=(150, 30, 30))
    td.text((30, 14), "KANIT #1", font=font(FONT_BLACK, 52), fill=WHITE)
    for i, line in enumerate(["Siyah klipsli kravat", "Bulunduğu yer: Koltuk 18", "Kısmi DNA profili", "Titanyum parçacıkları"]):
        td.text((30, 110 + i * 60), line, font=font(FONT_MONO, 34), fill=INK)
    paste_rotated(img, tag, (W / 2 + 380, H / 2), -6)
    header(img)
    return img


RENDERERS = {
    "title": scene_title,
    "chapter": scene_chapter,
    "date": scene_date,
    "ticket": scene_ticket,
    "profile": scene_profile,
    "note": scene_note,
    "bomb": scene_bomb,
    "list": scene_list,
    "fact": scene_fact,
    "money": scene_money,
    "quote": scene_quote,
    "map": scene_map,
    "plane": scene_plane,
    "tie": scene_tie,
}


def render_scene(scene: dict, seed: int) -> Image.Image:
    return RENDERERS[scene["type"]](scene, seed)


def thumbnail() -> Image.Image:
    img = scene_plane({"caption": ""}, 7).resize((1280, 720), Image.LANCZOS)
    d = ImageDraw.Draw(img)
    d.rectangle((0, 520, 1280, 720), fill=(0, 0, 0))
    ov = Image.new("RGBA", (1280, 720), (0, 0, 0, 0))
    ImageDraw.Draw(ov).rectangle((0, 0, 1280, 720), fill=(0, 0, 0, 90))
    img.paste(ov, (0, 0), ov)
    d = ImageDraw.Draw(img)
    d.text((50, 470), "UÇAKTAN ATLADI", font=font(FONT_BLACK, 112), fill=WHITE, stroke_width=6, stroke_fill=(0, 0, 0))
    d.text((50, 600), "VE HİÇ BULUNAMADI", font=font(FONT_BLACK, 84), fill=RED, stroke_width=5, stroke_fill=(0, 0, 0))
    bf = font(FONT_BLACK, 74)
    bw = d.textlength("$200.000", font=bf)
    d.rounded_rectangle((1240 - bw - 56, 40, 1240, 150), radius=14, fill=RED)
    d.text((1240 - bw - 28, 52), "$200.000", font=bf, fill=WHITE)
    d.text((50, 40), "D.B. COOPER", font=font(FONT_MONO, 60), fill=(240, 220, 120), stroke_width=3, stroke_fill=(0, 0, 0))
    return img
