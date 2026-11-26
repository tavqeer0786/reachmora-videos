import math
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080
SS = 2
INK = (17, 17, 17)
WHITE = (244, 244, 240)
GREY = (190, 192, 196)
_HERE = os.path.dirname(os.path.abspath(__file__))
_FONT_DIR = os.path.join(_HERE, "fonts")
def _font(*candidates):
    for p in candidates:
        if os.path.exists(p):
            return p
    raise FileNotFoundError("No usable font found; add ComicRelief-Bold.ttf and Poppins-Bold.ttf to ./fonts")

HAND = _font(
    os.path.join(_FONT_DIR, "ComicRelief-Bold.ttf"),
    "/usr/share/fonts/truetype/google-fonts/ofl/comicrelief/ComicRelief-Bold.ttf",
    r"C:\Windows\Fonts\arialbd.ttf",
)
POP = _font(
    os.path.join(_FONT_DIR, "Poppins-Bold.ttf"),
    "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf",
    r"C:\Windows\Fonts\segoeuib.ttf",
)

WM_BLUE = (0, 113, 206)
WM_YELLOW = (255, 194, 32)
RED = (219, 56, 52)
GREEN = (62, 160, 90)
GOLD = (236, 184, 64)
BROWN = (150, 98, 60)

_fc = {}
def font(path, size):
    k = (path, int(size * SS))
    if k not in _fc:
        _fc[k] = ImageFont.truetype(path, int(size * SS))
    return _fc[k]


class Cv:
    def __init__(s, w, h):
        s.w, s.h = w, h
        s.im = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
        s.d = ImageDraw.Draw(s.im)

    def _b(s, box):
        return [c * SS for c in box]

    def ell(s, box, fill=None, ow=6, outline=INK):
        s.d.ellipse(s._b(box), fill=fill, outline=outline if ow else None, width=ow * SS)

    def rr(s, box, r=14, fill=None, ow=6, outline=INK):
        s.d.rounded_rectangle(s._b(box), radius=r * SS, fill=fill, outline=outline if ow else None, width=ow * SS)

    def rect(s, box, fill=None, ow=6, outline=INK):
        s.d.rectangle(s._b(box), fill=fill, outline=outline if ow else None, width=ow * SS)

    def poly(s, pts, fill=None, ow=6, outline=INK):
        p = [(x * SS, y * SS) for x, y in pts]
        s.d.polygon(p, fill=fill)
        if ow:
            s.d.line(p + [p[0]], fill=outline, width=ow * SS, joint="curve")
            for x, y in p:
                r = ow * SS / 2
                s.d.ellipse([x - r, y - r, x + r, y + r], fill=outline)

    def line(s, pts, w=6, fill=INK, cap=True):
        p = [(x * SS, y * SS) for x, y in pts]
        s.d.line(p, fill=fill, width=int(w * SS), joint="curve")
        if cap:
            r = w * SS / 2
            for x, y in (p[0], p[-1]):
                s.d.ellipse([x - r, y - r, x + r, y + r], fill=fill)

    def arc(s, box, a0, a1, w=5, fill=INK):
        s.d.arc(s._b(box), a0, a1, fill=fill, width=int(w * SS))

    def pie(s, box, a0, a1, fill):
        s.d.pieslice(s._b(box), a0, a1, fill=fill)

    def text(s, xy, t, size, fill=WHITE, f=HAND, anchor="mm", stroke=0, stroke_fill=INK):
        s.d.text((xy[0] * SS, xy[1] * SS), t, font=font(f, size), fill=fill, anchor=anchor,
                 stroke_width=int(stroke * SS), stroke_fill=stroke_fill)

    def out(s):
        return s.im.resize((s.w, s.h), Image.LANCZOS)


def text_w(t, size, f=HAND):
    return font(f, size).getlength(t) / SS


# ---------------------------------------------------------------- backgrounds
def bg(base, spot=None, spot_pos=(960, 540), rx=820, ry=470, floor=None, floor_y=800):
    img = Image.new("RGB", (W, H), base)
    if spot:
        m = Image.new("L", (W, H), 0)
        ImageDraw.Draw(m).ellipse([spot_pos[0] - rx, spot_pos[1] - ry, spot_pos[0] + rx, spot_pos[1] + ry], fill=255)
        m = m.filter(ImageFilter.GaussianBlur(90))
        img.paste(Image.new("RGB", (W, H), spot), (0, 0), m)
    if floor:
        ImageDraw.Draw(img).rectangle([0, floor_y, W, H], fill=floor)
    return img


# ---------------------------------------------------------------- sparkle / spark
def spark(cv, cx, cy, R, fill=WM_YELLOW, n=6, rot=0):
    w = R * 0.26
    for i in range(n):
        a = math.radians(rot + i * 360 / n - 90)
        x1, y1 = cx + math.cos(a) * R * 0.2, cy + math.sin(a) * R * 0.2
        x2, y2 = cx + math.cos(a) * R, cy + math.sin(a) * R
        cv.line([(x1, y1), (x2, y2)], w=w, fill=fill)


def wm_logo(h=80, fg=WHITE):
    t = "Walmart"
    tw = text_w(t, h * 0.9, POP)
    cv = Cv(int(tw + h * 1.3), int(h * 1.3))
    cv.text((tw / 2 + 4, h * 0.65), t, h * 0.9, fg, POP)
    spark(cv, tw + h * 0.62, h * 0.55, h * 0.5)
    return cv.out()


def star4(cv, cx, cy, R, fill=GOLD, ow=0):
    pts = []
    for i in range(8):
        a = math.radians(i * 45 - 90)
        r = R if i % 2 == 0 else R * 0.28
        pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    cv.poly(pts, fill=fill, ow=ow)


def sparkle(R=40, fill=GOLD):
    cv = Cv(R * 2 + 4, R * 2 + 4)
    star4(cv, R + 2, R + 2, R, fill)
    return cv.out()


# ---------------------------------------------------------------- person
def person(body=(70, 120, 200), mood="neutral", lh=(-95, 75), rh=(95, 75), flip=False):
    cv = Cv(420, 560)
    # legs
    cv.line([(178, 395), (172, 520)], 13)
    cv.line([(244, 395), (250, 520)], 13)
    cv.ell((148, 510, 196, 540), INK, 0)
    cv.ell((226, 510, 274, 540), INK, 0)
    # arms
    for (sx, sy), (dx, dy) in (((148, 238), lh), ((274, 238), rh)):
        ex, ey = sx + dx, sy + dy
        cv.line([(sx, sy), (ex, ey)], 12)
        cv.ell((ex - 15, ey - 15, ex + 15, ey + 15), WHITE, 5)
    # body
    cv.rr((140, 205, 282, 398), 42, body, 6)
    cv.rr((140, 205, 282, 398), 42, None, 0)
    # head
    cv.ell((130, 40, 292, 202), WHITE, 6)
    cv.pie((133, 43, 289, 199), 20, 130, GREY)
    cv.ell((130, 40, 292, 202), None, 6)
    ex = (186, 240)
    for x in ex:
        cv.ell((x - 6, 108, x + 6, 122), INK, 0)
    if mood == "neutral":
        cv.line([(196, 158), (232, 158)], 5)
    elif mood == "happy":
        cv.arc((190, 128, 236, 176), 15, 165, 5)
    elif mood == "worried":
        cv.arc((196, 154, 232, 186), 195, 345, 5)
        cv.line([(172, 96), (200, 90)], 5)
        cv.line([(256, 96), (228, 90)], 5)
    elif mood == "think":
        cv.line([(200, 160), (236, 154)], 5)
        cv.line([(226, 92), (254, 88)], 5)
    elif mood == "surprised":
        cv.ell((203, 146, 224, 172), INK, 0)
    elif mood == "sad":
        cv.arc((196, 156, 232, 188), 200, 340, 5)
    img = cv.out()
    return img.transpose(Image.FLIP_LEFT_RIGHT) if flip else img


# ---------------------------------------------------------------- props
def calendar(day="27", top="NOV", tag=None, w=420, h=460, accent=RED):
    cv = Cv(w, h)
    cv.rr((10, 30, w - 10, h - 10), 24, (246, 244, 236), 7)
    cv.rr((10, 30, w - 10, 140), 24, accent, 7)
    cv.rect((14, 100, w - 14, 140), accent, 0)
    cv.line([(10, 140), (w - 10, 140)], 7)
    for x in (110, w - 110):
        cv.rr((x - 10, 6, x + 10, 62), 10, (90, 90, 96), 5)
    cv.text((w / 2, 92), top, 54, WHITE, HAND)
    cv.text((w / 2, 272), day, 150, INK, HAND)
    if tag:
        cv.text((w / 2, 392), tag, 38, accent, HAND)
    return cv.out()


def tv(w=380, h=320):
    cv = Cv(w, h)
    cv.rr((10, 10, w - 10, h - 60), 18, (40, 44, 54), 7)
    cv.rr((30, 30, w - 30, h - 80), 8, (90, 150, 220), 4)
    cv.poly([(50, h - 100), (130, 70), (190, h - 100)], (70, 130, 200), 0)
    cv.poly([(150, h - 100), (240, 90), (w - 50, h - 100)], (50, 105, 175), 0)
    cv.ell((w - 110, 48, w - 70, 88), (255, 226, 130), 0)
    cv.rect((30, 30, w - 30, h - 80), None, 4)
    cv.line([(w / 2 - 70, h - 25), (w / 2 + 70, h - 25)], 12)
    cv.line([(w / 2, h - 60), (w / 2, h - 28)], 10)
    return cv.out()


def teddy(s=300):
    cv = Cv(s, s)
    c = (176, 120, 70)
    cv.ell((38, 20, 108, 90), c, 6)
    cv.ell((s - 108, 20, s - 38, 90), c, 6)
    cv.ell((70, 150, s - 70, s - 12), c, 6)
    cv.ell((52, 150, 112, 216), c, 6)
    cv.ell((s - 112, 150, s - 52, 216), c, 6)
    cv.ell((56, 46, s - 56, 190), c, 6)
    cv.ell((s / 2 - 42, 112, s / 2 + 42, 172), (228, 196, 150), 5)
    cv.ell((s / 2 - 14, 118, s / 2 + 14, 138), INK, 0)
    cv.ell((100, 96, 116, 112), INK, 0)
    cv.ell((s - 116, 96, s - 100, 112), INK, 0)
    cv.poly([(s / 2 - 28, 190), (s / 2, 230), (s / 2 + 28, 190)], RED, 5)
    cv.poly([(s / 2, 196), (s / 2 - 24, 216), (s / 2 - 24, 176)], None, 0)
    return cv.out()


def ornaments(w=380, h=330):
    cv = Cv(w, h)
    cv.line([(20, 30), (w - 20, 30)], 5)
    cols = [RED, GREEN, GOLD, (70, 120, 200)]
    xs = [70, 150, 235, 315]
    ys = [150, 215, 160, 205]
    for x, y, c in zip(xs, ys, cols):
        cv.line([(x, 30), (x, y - 56)], 4)
        cv.rr((x - 14, y - 66, x + 14, y - 48), 4, (200, 200, 206), 4)
        cv.ell((x - 52, y - 52, x + 52, y + 52), c, 6)
        cv.arc((x - 34, y - 34, x + 34, y + 34), 200, 260, 6, (255, 255, 255))
    return cv.out()


def grocery_bag(w=300, h=360):
    cv = Cv(w, h)
    cv.line([(110, 100), (90, 40)], 14, (60, 140, 60))
    cv.poly([(100, 110), (120, 40), (150, 40), (150, 110)], (222, 190, 120), 5)
    cv.ell((170, 30, 250, 110), RED, 6)
    cv.line([(210, 32), (222, 8)], 6, (60, 120, 50))
    cv.poly([(40, 120), (260, 120), (245, h - 14), (55, h - 14)], (190, 140, 90), 7)
    cv.line([(40, 120), (260, 120)], 7)
    cv.text((150, 245), "FOOD", 56, (255, 240, 210), HAND)
    return cv.out()


def gift(s=260, col=RED):
    cv = Cv(s, s)
    cv.rr((20, 90, s - 20, s - 14), 12, col, 7)
    cv.rr((10, 62, s - 10, 108), 10, col, 7)
    cv.rect((s / 2 - 20, 62, s / 2 + 20, s - 14), GOLD, 5)
    cv.ell((s / 2 - 70, 8, s / 2, 64), None, 7, GOLD)
    cv.ell((s / 2, 8, s / 2 + 70, 64), None, 7, GOLD)
    return cv.out()


def tree(w=300, h=400):
    cv = Cv(w, h)
    cv.rect((w / 2 - 24, h - 70, w / 2 + 24, h - 10), BROWN, 6)
    for y, half in ((h - 60, 130), (h - 150, 105), (h - 240, 78)):
        cv.poly([(w / 2 - half, y), (w / 2, y - 120), (w / 2 + half, y)], GREEN, 6)
    star4(cv, w / 2, 34, 34, GOLD, 4)
    for x, y, c in ((110, h - 100, RED), (200, h - 180, GOLD), (150, h - 250, RED), (190, h - 90, (70, 120, 200))):
        cv.ell((x - 11, y - 11, x + 11, y + 11), c, 4)
    return cv.out()


def clock(s=220, hh=0, mm=0):
    cv = Cv(s, s)
    cv.ell((8, 8, s - 8, s - 8), (246, 244, 236), 7)
    for i in range(12):
        a = math.radians(i * 30)
        c = s / 2
        cv.line([(c + math.sin(a) * (s * 0.38), c - math.cos(a) * (s * 0.38)),
                 (c + math.sin(a) * (s * 0.44), c - math.cos(a) * (s * 0.44))], 4)
    c = s / 2
    ha = math.radians((hh % 12) * 30 + mm * 0.5)
    ma = math.radians(mm * 6)
    cv.line([(c, c), (c + math.sin(ha) * s * 0.24, c - math.cos(ha) * s * 0.24)], 8)
    cv.line([(c, c), (c + math.sin(ma) * s * 0.36, c - math.cos(ma) * s * 0.36)], 5)
    cv.ell((c - 8, c - 8, c + 8, c + 8), INK, 0)
    return cv.out()


def money_sack(w=300, h=340):
    cv = Cv(w, h)
    cv.poly([(100, 80), (60, 20), (130, 50), (150, 10), (170, 50), (240, 20), (200, 80)], (176, 150, 90), 6)
    cv.ell((30, 70, w - 30, h - 10), (196, 168, 104), 7)
    cv.rr((90, 70, w - 90, 100), 10, RED, 5)
    cv.text((w / 2, 200), "$", 150, (60, 80, 40), POP)
    return cv.out()


def tag_label(txt, w=520, h=130, col=RED, fg=WHITE, size=62, hole=True):
    cv = Cv(w, h)
    cv.poly([(60, 8), (w - 10, 8), (w - 10, h - 8), (60, h - 8), (10, h / 2)], col, 7)
    if hole:
        cv.ell((44, h / 2 - 12, 68, h / 2 + 12), (250, 250, 250), 5)
    cv.text((w / 2 + 28, h / 2 + 2), txt, size, fg, HAND)
    return cv.out()


def banner(txt, w=640, h=150, col=RED, fg=WHITE, size=70):
    cv = Cv(w, h)
    cv.poly([(0, 36), (50, 36), (50, 12), (w - 50, 12), (w - 50, 36), (w, 36), (w - 40, h / 2 + 18), (w, h - 14),
             (w - 50, h - 14), (w - 50, h - 6), (50, h - 6), (50, h - 14), (0, h - 14), (40, h / 2 + 18)], col, 7)
    cv.text((w / 2, h / 2 + 4), txt, size, fg, HAND)
    return cv.out()


def bubble(w=520, h=360, tail="left"):
    cv = Cv(w, h)
    cv.ell((20, 10, w - 20, h - 80), (246, 246, 242), 7)
    if tail == "left":
        cv.ell((20, h - 66, 60, h - 28), (246, 246, 242), 6)
        cv.ell((0, h - 30, 22, h - 8), (246, 246, 242), 5)
    else:
        cv.ell((w - 60, h - 66, w - 20, h - 28), (246, 246, 242), 6)
        cv.ell((w - 22, h - 30, w, h - 8), (246, 246, 242), 5)
    return cv.out()


def cart(w=480, h=380, item=None):
    cv = Cv(w, h)
    cv.line([(20, 40), (80, 40), (130, 250), (400, 250)], 12)
    cv.poly([(95, 90), (440, 90), (400, 232), (125, 232)], (200, 204, 212), 7)
    for x in (170, 250, 330):
        cv.line([(x - 14, 92), (x - 6, 230)], 4)
    cv.line([(110, 160), (420, 160)], 4)
    cv.ell((140, 290, 200, 350), (60, 60, 66), 7)
    cv.ell((340, 290, 400, 350), (60, 60, 66), 7)
    return cv.out()


def store(w=760, h=520, sign=True):
    cv = Cv(w, h)
    cv.rect((20, 120, w - 20, h - 20), (220, 222, 228), 7)
    cv.rect((20, 120, w - 20, 240), WM_BLUE, 7)
    lg = wm_logo(78, WHITE)
    cv.im.alpha_composite(lg.resize((lg.width * SS, lg.height * SS), Image.LANCZOS),
                          (int((w - lg.width) / 2 * SS), int(142 * SS)))
    cv.rect((300, h - 230, 460, h - 20), (130, 190, 230), 7)
    cv.line([(380, h - 230), (380, h - 20)], 5)
    for x in (70, 520):
        cv.rect((x, h - 220, x + 180, h - 110), (140, 196, 232), 6)
    cv.rect((10, 100, w - 10, 126), (150, 152, 160), 6)
    return cv.out()


def phone(w=420, h=780, content=None):
    cv = Cv(w, h)
    cv.rr((10, 10, w - 10, h - 10), 50, (34, 36, 44), 8)
    cv.rr((34, 50, w - 34, h - 44), 22, (246, 246, 244), 4)
    cv.rr((w / 2 - 50, 22, w / 2 + 50, 36), 7, (70, 72, 80), 0)
    if content:
        content(cv, 34, 50, w - 34, h - 44)
    return cv.out()


def app_screen(cv, x0, y0, x1, y1):
    cv.rect((x0, y0, x1, y0 + 120), WM_BLUE, 0)
    lg = wm_logo(52, WHITE)
    cv.im.alpha_composite(lg.resize((lg.width * SS, lg.height * SS), Image.LANCZOS),
                          (int(((x0 + x1) / 2 - lg.width / 2) * SS), int((y0 + 24) * SS)))
    cv.rr((x0 + 20, y0 + 135, x1 - 20, y0 + 185), 24, (225, 228, 235), 3)
    cv.text(((x0 + x1) / 2, y0 + 160), "Black Friday deals", 24, (90, 96, 110), HAND)
    cw = (x1 - x0 - 60) / 2
    for r in range(2):
        for c in range(2):
            ax = x0 + 20 + c * (cw + 20)
            ay = y0 + 215 + r * 205
            cv.rr((ax, ay, ax + cw, ay + 185), 14, (236, 238, 244), 3)
            cols = [(90, 150, 220), (210, 120, 90), (110, 180, 120), (230, 190, 80)]
            cv.rr((ax + 20, ay + 14, ax + cw - 20, ay + 100), 10, cols[r * 2 + c], 0)
            cv.rr((ax + 20, ay + 116, ax + 96, ay + 154), 8, RED, 0)
            cv.text((ax + 58, ay + 136), ["$199", "$49", "$89", "$29"][r * 2 + c], 24, WHITE, HAND)


def magnifier(s=260):
    cv = Cv(s, s)
    cv.line([(150, 150), (s - 24, s - 24)], 28, INK)
    cv.line([(150, 150), (s - 24, s - 24)], 16, (120, 82, 50))
    cv.ell((14, 14, 170, 170), (210, 232, 250), 9)
    cv.arc((40, 40, 144, 144), 200, 260, 7, (255, 255, 255))
    return cv.out()


def amazon_tile(w=380, h=300):
    cv = Cv(w, h)
    cv.rr((8, 8, w - 8, h - 8), 26, (246, 246, 242), 7)
    cv.text((w / 2, 125), "amazon", 78, (30, 30, 34), POP)
    cv.arc((60, 100, w - 60, 215), 20, 160, 10, (255, 153, 0))
    cv.poly([(w - 92, 196), (w - 62, 192), (w - 76, 170)], (255, 153, 0), 0)
    return cv.out()


def target_tile(w=380, h=300):
    cv = Cv(w, h)
    cv.rr((8, 8, w - 8, h - 8), 26, (246, 246, 242), 7)
    cx, cy = w / 2, 120
    cv.ell((cx - 78, cy - 78, cx + 78, cy + 78), (214, 30, 40), 0)
    cv.ell((cx - 52, cy - 52, cx + 52, cy + 52), (250, 250, 250), 0)
    cv.ell((cx - 28, cy - 28, cx + 28, cy + 28), (214, 30, 40), 0)
    cv.text((w / 2, 240), "Target", 46, (214, 30, 40), POP)
    return cv.out()


def browser(w=640, h=440):
    cv = Cv(w, h)
    cv.rr((8, 8, w - 8, h - 8), 18, (246, 246, 244), 7)
    cv.rr((8, 8, w - 8, 60), 18, (214, 218, 226), 7)
    for i, c in enumerate((RED, GOLD, GREEN)):
        cv.ell((30 + i * 30, 26, 46 + i * 30, 42), c, 3)
    cv.rr((140, 22, w - 30, 48), 12, (246, 246, 244), 3)
    rows = [("Store A", "$199", False), ("Store B", "$189", True), ("Store C", "$195", False)]
    for i, (n, p, best) in enumerate(rows):
        y = 90 + i * 110
        cv.rr((30, y, w - 30, y + 90), 12, (226, 244, 230) if best else (236, 238, 244), 4)
        cv.rr((46, y + 16, 106, y + 74), 8, (150, 170, 210), 0)
        cv.text((200, y + 45), n, 34, INK, HAND)
        cv.text((w - 120, y + 45), p, 44, RED if best else INK, HAND)
    return cv.out()


def warning(s=380):
    cv = Cv(s, s)
    cv.poly([(s / 2, 20), (s - 20, s - 40), (20, s - 40)], (240, 80, 70), 10)
    cv.text((s / 2, s * 0.62), "!", 190, WHITE, POP)
    return cv.out()


def qmark(s=300, fill=WM_YELLOW):
    cv = Cv(s, s)
    cv.text((s / 2, s / 2), "?", s * 0.95, fill, POP, stroke=8)
    return cv.out()


def xmark(s=240, col=RED):
    cv = Cv(s, s)
    cv.line([(30, 30), (s - 30, s - 30)], 36, INK)
    cv.line([(s - 30, 30), (30, s - 30)], 36, INK)
    cv.line([(30, 30), (s - 30, s - 30)], 22, col)
    cv.line([(s - 30, 30), (30, s - 30)], 22, col)
    return cv.out()


def label(txt, size=64, fill=WHITE, f=HAND, stroke=0):
    tw = int(text_w(txt, size, f)) + 40
    cv = Cv(tw, int(size * 1.5))
    cv.text((tw / 2, size * 0.75), txt, size, fill, f, stroke=stroke)
    return cv.out()


def megaphone(w=340, h=260):
    cv = Cv(w, h)
    cv.poly([(60, 100), (190, 40), (190, 210), (60, 160)], (240, 190, 60), 7)
    cv.poly([(190, 20), (300, 6), (300, 244), (190, 230)], RED, 7)
    cv.rr((20, 100, 80, 160), 14, (60, 60, 66), 6)
    cv.rr((80, 158, 120, 236), 12, (60, 60, 66), 6)
    return cv.out()


def pin(s=150, col=RED):
    cv = Cv(s, int(s * 1.3))
    cv.poly([(s / 2, s * 1.25), (14, s * 0.5), (s - 14, s * 0.5)], col, 7)
    cv.ell((12, 10, s - 12, s - 14), col, 7)
    cv.ell((s / 2 - 22, s / 2 - 36, s / 2 + 22, s / 2 + 8), WHITE, 5)
    return cv.out()


def day_cell(w=64, h=72, fill=(246, 244, 236), ow=4, txt=None, col=INK):
    cv = Cv(w, h)
    cv.rr((4, 4, w - 4, h - 4), 10, fill, ow)
    if txt:
        cv.text((w / 2, h / 2), txt, 32, col, HAND)
    return cv.out()


def chevron_block(w, h, col, txt, size=40, fg=WHITE):
    cv = Cv(w, h)
    cv.poly([(8, 8), (w - 50, 8), (w - 8, h / 2), (w - 50, h - 8), (8, h - 8), (46, h / 2)], col, 7)
    cv.text((w / 2 + 6, h / 2 + 2), txt, size, fg, HAND)
    return cv.out()


def bag_shop(s=300, col=(210, 70, 80)):
    cv = Cv(s, s)
    cv.arc((s / 2 - 70, 20, s / 2 + 70, 150), 180, 360, 12)
    cv.poly([(40, 90), (s - 40, 90), (s - 20, s - 14), (20, s - 14)], col, 7)
    cv.text((s / 2, 190), "%", 110, WHITE, POP)
    return cv.out()


def laptop(w=420, h=320):
    cv = Cv(w, h)
    cv.rr((60, 20, w - 60, h - 90), 14, (40, 44, 54), 7)
    cv.rect((80, 40, w - 80, h - 110), (110, 170, 230), 4)
    cv.text((w / 2, 112), "SALE", 60, WHITE, HAND)
    cv.poly([(20, h - 90), (w - 20, h - 90), (w - 4, h - 40), (4, h - 40)], (150, 154, 164), 7)
    return cv.out()


def megaphone_icon(s=260):
    return megaphone(s, int(s * 0.76))
