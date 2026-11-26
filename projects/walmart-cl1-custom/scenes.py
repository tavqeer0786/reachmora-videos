import math, sys
import numpy as np, cv2
from PIL import Image, ImageFilter
from lib import *

FPS = 30
DUR = 87.95


def sc(img, s):
    return img.resize((max(1, int(img.width * s)), max(1, int(img.height * s))), Image.LANCZOS)


def ease_out(p):
    return 1 - (1 - p) ** 3


def ease_back(p):
    c1, c3 = 1.9, 2.9
    return 1 + c3 * (p - 1) ** 3 + c1 * (p - 1) ** 2


def smooth(p):
    return p * p * (3 - 2 * p)


class Item:
    def __init__(s, spr, x, y, t0, anim="pop", dur=0.4, end=None, dx=0, dy=0, bob=0, sway=0, path=None, amax=1.0,
                 scale=1.0, rot=0):
        s.spr, s.x, s.y, s.t0, s.anim, s.dur, s.end = spr, x, y, t0, anim, dur, end
        s.dx, s.dy, s.bob, s.sway, s.path, s.amax, s.scale, s.rot = dx, dy, bob, sway, path, amax, scale, rot
        s.cache = {}

    def state(s, t):
        if t < s.t0:
            return None
        if s.end is not None and t > s.end + 0.2:
            return None
        p = min(1.0, (t - s.t0) / s.dur)
        a, sca, x, y = 1.0, s.scale, s.x, s.y
        crop = 1.0
        if s.anim == "pop":
            sca *= max(0.001, ease_back(p))
            a = min(1, p * 4)
        elif s.anim == "fade":
            a = p
        elif s.anim == "slide":
            e = 1 - ease_out(p)
            x += s.dx * e
            y += s.dy * e
            a = min(1, p * 3)
        elif s.anim == "wipe":
            crop = ease_out(p)
        if s.path:
            ts = [q[0] for q in s.path]
            if t <= ts[0]:
                x, y = s.path[0][1], s.path[0][2]
            elif t >= ts[-1]:
                x, y = s.path[-1][1], s.path[-1][2]
            else:
                for i in range(len(ts) - 1):
                    if ts[i] <= t <= ts[i + 1]:
                        q = smooth((t - ts[i]) / (ts[i + 1] - ts[i]))
                        x = s.path[i][1] + (s.path[i + 1][1] - s.path[i][1]) * q
                        y = s.path[i][2] + (s.path[i + 1][2] - s.path[i][2]) * q
                        break
        if s.bob:
            y += s.bob * math.sin(2 * math.pi * (t - s.t0) / 2.4)
        rot = s.rot
        if s.sway:
            rot += s.sway * math.sin(2 * math.pi * (t - s.t0) / 0.5)
        if s.end is not None and t > s.end:
            a *= max(0, 1 - (t - s.end) / 0.2)
        return sca, a * s.amax, x, y, rot, crop

    def draw(s, base, t):
        st = s.state(t)
        if st is None:
            return
        sca, a, x, y, rot, crop = st
        if a <= 0.01:
            return
        key = (round(sca, 2), int(rot), round(crop, 2))
        spr = s.cache.get(key)
        if spr is None:
            spr = s.spr
            if crop < 0.999:
                cw = max(1, int(spr.width * crop))
                spr = spr.crop((0, 0, cw, spr.height))
            if abs(sca - 1) > 0.005:
                spr = sc(spr, sca)
            if rot:
                spr = spr.rotate(rot, resample=Image.BICUBIC, expand=True)
            if len(s.cache) > 60:
                s.cache.clear()
            s.cache[key] = spr
        w0 = s.spr.width * sca
        px = int(x - w0 / 2) if crop >= 0.999 else int(x - w0 / 2)
        if rot:
            px = int(x - spr.width / 2)
        py = int(y - spr.height / 2)
        if a < 0.99:
            al = spr.getchannel("A").point(lambda v: int(v * a))
            spr = spr.copy()
            spr.putalpha(al)
        base.paste(spr, (px, py), spr)


class Scene:
    def __init__(s, t0, t1, bgimg, items, cam=(1.0, 1.05, 960, 540)):
        s.t0, s.t1, s.bg, s.items, s.cam = t0, t1, bgimg, items, cam

    def render(s, t):
        base = s.bg.copy()
        for it in s.items:
            it.draw(base, t)
        arr = np.asarray(base)
        z0, z1, fx, fy = s.cam
        p = min(1, max(0, (t - s.t0) / (s.t1 - s.t0)))
        z = z0 + (z1 - z0) * p
        if abs(z - 1) < 1e-3:
            return arr
        cw, ch = W / z, H / z
        cx = min(max(fx, cw / 2), W - cw / 2)
        cy = min(max(fy, ch / 2), H - ch / 2)
        x0, y0 = int(cx - cw / 2), int(cy - ch / 2)
        crop = arr[y0:y0 + int(ch), x0:x0 + int(cw)]
        return cv2.resize(crop, (W, H), interpolation=cv2.INTER_LINEAR)


# ------------------------------------------------------------- extra props
def arrow(w=300, col=WHITE):
    cv = Cv(w, 80)
    x = 10
    while x < w - 90:
        cv.line([(x, 40), (x + 34, 40)], 10, col)
        x += 56
    cv.poly([(w - 90, 8), (w - 10, 40), (w - 90, 72)], col, 0)
    return cv.out()


def bubble_text(txt, w=420, h=300, size=54, col=INK, tail="left"):
    b = bubble(w, h, tail)
    cv = Cv(w, h)
    cv.text((w / 2, (h - 70) / 2 + 4), txt, size, col, HAND)
    b.alpha_composite(cv.out())
    return b


def glow(s=700, col=(255, 210, 90), a=150):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    ImageDraw.Draw(im).ellipse([s * 0.25, s * 0.25, s * 0.75, s * 0.75], fill=col + (a,))
    return im.filter(ImageFilter.GaussianBlur(s * 0.09))


def wm_board(w=520, h=300):
    cv = Cv(w, h)
    cv.rect((w / 2 - 16, 140, w / 2 + 16, h - 6), (120, 124, 134), 6)
    cv.rr((10, 10, w - 10, 170), 24, WM_BLUE, 8)
    lg = wm_logo(78, WHITE)
    cv.im.alpha_composite(lg.resize((lg.width * SS, lg.height * SS), Image.LANCZOS),
                          (int((w - lg.width) / 2 * SS), int(34 * SS)))
    return cv.out()


def circle_node(d=120, col=GOLD, txt=None, size=36, fg=INK):
    cv = Cv(d + 8, d + 8)
    cv.ell((4, 4, d + 4, d + 4), col, 7)
    if txt:
        cv.text(((d + 8) / 2, (d + 8) / 2 + 2), txt, size, fg, HAND)
    return cv.out()


def timeline(x0, x1, y, w=14, col=INK):
    cv = Cv(x1 - x0 + 60, 90)
    cv.line([(10, 45), (x1 - x0 + 10, 45)], w, col)
    cv.poly([(x1 - x0 - 10, 12), (x1 - x0 + 46, 45), (x1 - x0 - 10, 78)], col, 0)
    return cv.out()


def pw(txt, size, col, w=None):
    return label(txt, size, col)


# ------------------------------------------------------------- scenes
NAVY, NAVY_S = (28, 34, 48), (52, 62, 86)
SAGE, SAGE_S = (168, 190, 190), (196, 214, 212)
WARM, WARM_S = (60, 44, 44), (98, 72, 64)
CHAR, CHAR_S = (36, 36, 42), (62, 64, 74)
BLUEB, BLUEB_S = (26, 66, 124), (48, 100, 176)
PEACH, PEACH_S = (222, 200, 172), (240, 224, 200)
SLATE, SLATE_S = (46, 58, 80), (74, 90, 120)

P_BLUE = person((70, 120, 200), "neutral")


def build():
    S = []

    # ---- S1 one event = one chance
    items = [
        Item(calendar("27", "NOV", "BLACK FRIDAY"), 560, 500, 0.3, scale=1.5, bob=6),
        Item(label("ONE EVENT", 76), 560, 930, 1.7, "fade"),
        Item(arrow(360), 960, 500, 3.0, "wipe", 0.5),
        Item(money_sack(), 1380, 500, 3.7, scale=1.5, bob=6),
        Item(label("ONE MAJOR CHANCE", 70, GOLD), 1380, 930, 4.5, "fade"),
        Item(label("CHAPTER 1  |  THE PROBLEM WITH ONE BIG BLACK FRIDAY", 34, (200, 206, 220)), 600, 70, 0.1, "fade",
             end=3.2),
    ]
    S.append(Scene(0, 7.0, bg(NAVY, NAVY_S), items, (1.0, 1.06, 960, 540)))

    # ---- S2 season is longer
    bar = Cv(1620, 190)
    segc = [(236, 228, 210), (222, 214, 196)]
    for i in range(8):
        x0 = 10 + i * 200
        bar.rr((x0, 20, x0 + 200, 150), 10, segc[i % 2], 6)
    bar_img = bar.out()
    items = [
        Item(bar_img, 960, 600, 7.3, "wipe", 1.6),
        Item(label("NOV", 54), 220, 740, 7.6, "fade"),
        Item(sc(tree(), 0.42), 1700, 440, 8.9, scale=1.0),
        Item(label("DEC 25", 54), 1700, 740, 8.9, "fade"),
        Item(pin(130), 946, 470, 7.9, "slide", 0.45, dy=-120),
        Item(label("ONE DAY", 60, RED), 946, 350, 8.4, "fade"),
        Item(label("THE WHOLE HOLIDAY SEASON", 84, WHITE), 960, 880, 9.2, "fade"),
    ]
    S.append(Scene(7.0, 10.8, bg(NAVY, NAVY_S), items, (1.0, 1.05, 960, 560)))

    # ---- S3 think about Christmas shopping
    items = [
        Item(sc(person((200, 90, 80), "think", lh=(-95, 75), rh=(60, -60)), 1.7), 600, 540, 10.95, "slide", 0.5, dx=-300),
        Item(bubble(620, 440), 1330, 400, 11.7, scale=1.45),
        Item(sc(tree(), 0.9), 1440, 360, 12.1),
        Item(sc(gift(), 0.85), 1170, 430, 12.5),
        Item(label("HOW DO PEOPLE REALLY SHOP FOR CHRISTMAS?", 64, WHITE), 960, 960, 11.2, "fade"),
    ]
    S.append(Scene(10.8, 13.7, bg(WARM, WARM_S, floor=(44, 32, 32), floor_y=840), items, (1.0, 1.05, 700, 540)))

    # ---- S4 not everything at once
    ghosts = [
        Item(sc(tv(), 0.75), 900, 250, 13.95, "fade", amax=0.35),
        Item(sc(gift(), 0.7), 1130, 290, 13.95, "fade", amax=0.35),
        Item(sc(tree(), 0.62), 1380, 270, 13.95, "fade", amax=0.35),
        Item(sc(grocery_bag(), 0.7), 1020, 170, 13.95, "fade", amax=0.35),
    ]
    items = ghosts + [
        Item(sc(person((70, 120, 200), "neutral", lh=(-60, 60), rh=(140, 60)), 1.6), 520, 560, 13.9, "slide", 0.4, dx=-300),
        Item(sc(cart(), 1.3), 1130, 700, 14.1, "slide", 0.4, dx=300),
        Item(sc(gift(col=(70, 120, 200)), 0.55), 1170, 640, 14.4),
        Item(xmark(360), 1130, 250, 14.9, end=None),
        Item(label("NOT EVERYTHING AT ONCE", 78, WHITE), 1050, 960, 15.0, "fade"),
    ]
    S.append(Scene(13.7, 16.2, bg(CHAR, CHAR_S, floor=(26, 26, 30), floor_y=820), items, (1.0, 1.05, 900, 560)))

    # ---- S5 timeline: tv, toy, decorations, groceries
    nodes = [320, 750, 1180, 1610]
    items = [Item(timeline(140, 1790, 700), 965, 700, 16.1, "wipe", 0.8)]
    ico = [(sc(tv(), 0.8), 16.3), (sc(teddy(), 0.85), 18.9), (sc(ornaments(), 0.78), 20.5), (sc(grocery_bag(), 0.8), 22.3)]
    t1s = ["NOVEMBER", "LATER", "A WEEK LATER", "BEFORE CHRISTMAS"]
    t2s = ["buys a TV", "waits for a toy deal", "buys decorations", "back for groceries"]
    cols = [(90, 150, 220), GOLD, RED, GREEN]
    for i, n in enumerate(nodes):
        t0 = ico[i][1]
        items.append(Item(circle_node(48, cols[i]), n, 700, t0, "pop", 0.3))
        items.append(Item(ico[i][0], n, 290, t0 + 0.1, bob=5))
        items.append(Item(label(t1s[i], 38, INK), n, 800, t0 + 0.3, "fade"))
        items.append(Item(label(t2s[i], 34, (60, 64, 76)), n, 860, t0 + 0.45, "fade"))
    wk = sc(person((70, 120, 200), "happy", lh=(-70, 60), rh=(70, 60)), 0.45)
    items.append(Item(wk, 320, 562, 16.2, "pop", 0.3,
                      path=[(16.2, 320, 562), (18.7, 320, 562), (19.3, 750, 562), (20.3, 750, 562), (20.9, 1180, 562),
                            (22.1, 1180, 562), (22.7, 1610, 562)]))
    S.append(Scene(16.0, 25.3, bg(SAGE, SAGE_S), items, (1.0, 1.04, 960, 540)))

    # ---- S6 different needs, different times
    items = [
        Item(label("DIFFERENT NEEDS", 78, INK), 520, 250, 25.6, "fade"),
        Item(label("DIFFERENT TIMES", 78, INK), 1400, 250, 26.5, "fade"),
        Item(sc(gift(), 0.95), 330, 590, 25.8, bob=5),
        Item(sc(tv(), 0.7), 590, 600, 26.0, bob=5),
        Item(sc(grocery_bag(), 0.72), 830, 600, 26.2, bob=5),
        Item(sc(clock(220, 3, 10), 1.25), 1190, 600, 26.7),
        Item(sc(clock(220, 9, 40), 1.25), 1470, 600, 26.9),
        Item(sc(clock(220, 6, 25), 1.25), 1750, 600, 27.1),
    ]
    S.append(Scene(25.3, 28.2, bg(PEACH, PEACH_S), items, (1.0, 1.05, 960, 540)))

    # ---- S7 focus on one day, miss shoppers
    items = [
        Item(glow(1500), 560, 580, 28.3, "fade", 0.8),
        Item(sc(store(), 1.15), 560, 620, 28.4, "slide", 0.5, dy=200),
        Item(sc(banner("BLACK FRIDAY", 560, 140, RED, WHITE, 62), 1.25), 560, 190, 29.3),
        Item(label("ALL ATTENTION ON ONE DAY", 62, WHITE), 560, 975, 30.0, "fade"),
    ]
    xs = [1200, 1430, 1660]
    for i, x in enumerate(xs):
        t0 = 31.6 + i * 0.45
        items.append(Item(sc(person((120, 120, 140), "worried", lh=(-70, 60), rh=(70, 60)), 0.62), x, 700, t0, "slide", 0.5, dx=300))
        items.append(Item(sc(bubble_text("not yet...", 420, 300, 54), 0.72), x - 10, 420, t0 + 0.4))
    items.append(Item(label("MISSED?", 120, RED), 1500, 190, 34.0, "pop", 0.4, sway=4))
    S.append(Scene(28.2, 35.25, bg(NAVY, NAVY_S, spot_pos=(520, 560), rx=520, ry=420), items, (1.0, 1.06, 900, 560)))

    # ---- S8 second event
    items = [
        Item(sc(banner("BLACK FRIDAY", 640, 150, RED, WHITE, 70), 1.25), 540, 470, 35.3),
        Item(label("+", 160, WHITE), 960, 470, 36.0, "pop"),
        Item(sc(banner("PART 2", 520, 150, GOLD, INK, 84), 1.25), 1400, 470, 36.15, "slide", 0.45, dx=500),
        Item(sparkle(46), 1700, 380, 36.6), Item(sparkle(30), 1000, 600, 36.75), Item(sparkle(38), 1250, 340, 36.9),
        Item(label("A SECOND EVENT CHANGES THAT", 84, WHITE), 960, 820, 36.7, "fade"),
    ]
    S.append(Scene(35.25, 37.9, bg(BLUEB, BLUEB_S), items, (1.0, 1.06, 960, 540)))

    # ---- S9 another reason to check Walmart
    items = [
        Item(sc(phone(420, 780, app_screen), 1.2), 560, 540, 38.1, bob=6),
        Item(sc(magnifier(), 1.6), 900, 700, 40.6, "slide", 0.5, dx=300, dy=100),
        Item(label("PRICES", 92, INK), 1360, 260, 39.2, "fade"),
        Item(label("PRODUCTS", 92, INK), 1360, 430, 40.0, "fade"),
        Item(label("A REASON TO CHECK", 78, RED), 1360, 620, 41.0, "fade"),
        Item(sc(sparkle(50), 1), 1650, 300, 39.4), Item(sparkle(40), 1700, 450, 40.2),
    ]
    S.append(Scene(37.9, 42.8, bg(SAGE, SAGE_S), items, (1.0, 1.05, 700, 540)))

    # ---- S10 not only Black Friday
    items = [
        Item(label("THIS ISN'T ONLY ABOUT", 90, WHITE), 960, 250, 42.9, "fade"),
        Item(sc(tag_label("BLACK FRIDAY", 760, 170, RED, WHITE, 84), 1.35), 960, 520, 43.3),
        Item(label("THE WHOLE SEASON", 108, GOLD), 960, 820, 44.3, "pop", 0.4),
    ]
    S.append(Scene(42.8, 45.6, bg(CHAR, CHAR_S), items, (1.0, 1.05, 960, 540)))

    # ---- S11 compete across the season
    blocks = [("EARLY PROMOS", (214, 100, 60), 285, 45.7, megaphone_icon(260), 0.9),
              ("BLACK FRIDAY", RED, 725, 48.9, bag_shop(260), 0.9),
              ("CYBER MONDAY", (70, 120, 200), 1165, 50.9, laptop(), 0.62),
              ("TO CHRISTMAS", GREEN, 1605, 51.7, tree(), 0.62)]
    items = [Item(label("RETAILERS COMPETE ACROSS THE SEASON", 72, WHITE), 960, 130, 45.7, "fade")]
    for txt, col, x, t0, icon, s in blocks:
        items.append(Item(chevron_block(430, 150, col, txt, 38), x, 740, t0, "slide", 0.4, dx=-120))
        items.append(Item(sc(icon, s * 1.3), x, 430, t0 + 0.15, bob=5))
    S.append(Scene(45.6, 52.6, bg(SLATE, SLATE_S), items, (1.0, 1.0, 960, 540)))

    # ---- S12 series of opportunities, not one giant moment
    items = [Item(label("A SERIES OF OPPORTUNITIES", 100, GOLD), 960, 250, 53.4, "fade", end=56.5)]
    for i in range(7):
        x = 330 + i * 210
        t0 = 53.7 + i * 0.35
        items.append(Item(circle_node(150, (240, 190, 70)), x, 560, t0, end=56.5))
        items.append(Item(sparkle(38, WHITE), x, 560, t0 + 0.1, end=56.5))
    giant = Cv(520, 520)
    giant.ell((10, 10, 510, 510), RED, 9)
    pass
    items += [Item(giant.out(), 960, 500, 56.7, scale=1.3), Item(label("ONE GIANT MOMENT", 96, WHITE), 960, 900, 56.9, "fade"), Item(xmark(380), 960, 500, 57.3)]
    S.append(Scene(53.2, 58.4, bg(WARM, WARM_S), items, (1.0, 1.05, 960, 540)))

    # ---- S13 remain visible while decisions happen
    items = [Item(sc(calendar("27", "NOV", None, 420, 460), 1.3), 560, 540, 58.5, end=64.4)]
    dec = [sc(tv(), 0.55), sc(gift(), 0.6), sc(teddy(), 0.65), sc(grocery_bag(), 0.55), sc(tree(), 0.55)]
    for i, d in enumerate(dec):
        items.append(Item(d, 1150 + (i % 3) * 160, 460 + (i // 3) * 210, 58.8 + i * 0.3, "pop", end=64.4,
                          path=[(58.8 + i * 0.3, 1150 + (i % 3) * 160, 460 + (i // 3) * 210),
                                (61.0 + i * 0.25, 560 + (i - 2) * 22, 560 + (i % 2) * 40)]))
    items.append(Item(label("EVERY DECISION ON ONE DAY?", 76, WHITE), 1250, 200, 60.0, "fade", end=64.4))
    items.append(Item(xmark(480), 560, 540, 63.0, end=64.4))
    # part B
    items += [
        Item(timeline(100, 1100, 800), 640, 830, 64.6, "wipe", 0.5),
        Item(sc(person((70, 120, 200), "think", lh=(-70, 60), rh=(70, 60)), 0.8), 300, 590, 64.6, "pop", 0.3,
             path=[(64.6, 300, 590), (67.4, 1000, 590)]),
        Item(bubble_text("?", 200, 190, 70), 520, 330, 65.2), Item(bubble_text("?", 200, 190, 70), 760, 330, 65.7),
        Item(glow(900), 1500, 500, 64.8, "fade", 0.9),
        Item(sc(wm_board(), 1.35), 1500, 520, 64.8),
        Item(label("STAYS VISIBLE", 90, GOLD), 1500, 200, 65.6, "fade"),
    ]
    S.append(Scene(58.4, 67.4, bg(NAVY, NAVY_S), items, (1.0, 1.05, 960, 540)))

    # ---- S14 but there's a problem
    items = [
        Item(sc(warning(), 1.35), 640, 500, 68.2, sway=4),
        Item(sc(person((120, 90, 160), "worried", lh=(-60, -40), rh=(60, -40)), 1.6), 1350, 520, 68.25, "slide", 0.3, dx=300),
        Item(label("BUT...", 120, WHITE), 640, 900, 68.5, "pop"),
    ]
    S.append(Scene(68.0, 69.65, bg((58, 26, 30), (110, 44, 50)), items, (1.0, 1.04, 960, 540)))

    # ---- S15 customers can shop anywhere
    items = [
        Item(sc(person((70, 120, 200), "neutral", lh=(-70, 60), rh=(70, 30)), 1.3), 960, 570, 69.65, end=74.7),
        Item(sc(phone(420, 780, app_screen), 0.24), 1095, 590, 69.9, end=74.7),
        Item(pin(130), 380, 300, 69.9), Item(pin(110, GREEN), 1560, 280, 70.4), Item(pin(120, GOLD), 1500, 800, 70.9),
        Item(pin(100, (70, 120, 200)), 430, 790, 71.1),
        Item(label("SHOP ALMOST ANYWHERE", 84, INK), 960, 140, 69.8, "fade"),
        Item(sc(amazon_tile(), 1.05), 400, 500, 72.0, end=74.7),
        Item(sc(target_tile(), 1.05), 1520, 500, 73.3, end=74.7),
        Item(sc(browser(), 1.4), 960, 520, 74.9),
        Item(label("COMPARE PRICES", 90, RED), 960, 960, 75.6, "fade"),
    ]
    S.append(Scene(69.65, 77.3, bg(SAGE, SAGE_S), items, (1.0, 1.05, 960, 540)))

    # ---- S16 sale doesn't guarantee return
    items = [
        Item(sc(store(), 1.05), 560, 620, 77.4, "slide", 0.4, dy=200),
        Item(sc(megaphone(), 1.3), 1160, 400, 77.7, sway=5),
        Item(sc(banner("ANOTHER SALE!", 560, 140, RED, WHITE, 60), 1.2), 620, 170, 78.4),
    ]
    for i in range(3):
        items.append(Item(sc(person((110 + i * 30, 120, 140 + i * 20), "neutral", lh=(-60, 60), rh=(60, 60), flip=True), 0.6),
                          700, 760, 79.4 + i * 0.3, "pop", 0.3,
                          path=[(79.4 + i * 0.3, 700, 760), (81.8, 1050 + i * 270, 760)]))
    items += [
        Item(qmark(300), 1560, 360, 80.6),
        Item(label("NO GUARANTEE", 110, RED), 1300, 960, 80.9, "pop", 0.4, sway=3),
    ]
    S.append(Scene(77.3, 82.1, bg(NAVY, NAVY_S, floor=(22, 26, 38), floor_y=840), items, (1.0, 1.05, 900, 540)))

    # ---- S17 closing question
    lines = ["What does Walmart offer", "that can make a customer", "choose it again, even when", "competing retailers are", "offering deals too?"]
    hl = {"Walmart": WM_YELLOW, "choose": GOLD, "it": GOLD, "again,": GOLD, "competing": (255, 130, 120), "retailers": (255, 130, 120)}
    allw = [w for l in lines for w in l.split()]
    tot = sum(len(w) + 1 for w in allw)
    items = [Item(wm_logo(90), 960, 170, 82.1, "fade"), Item(glow(600), 1600, 740, 86.2, "fade", 0.7), Item(qmark(360), 1600, 740, 86.2, bob=6)]
    cum, size = 0, 84
    for li, line in enumerate(lines):
        y = 330 + li * 118
        lw = text_w(line, size)
        left = 960 - lw / 2 - 80
        words = line.split()
        for wi, wd in enumerate(words):
            pre = " ".join(words[:wi]) + (" " if wi else "")
            wx = left + text_w(pre, size)
            ww = text_w(wd, size)
            c = Cv(int(ww + 20), 130)
            c.text((ww / 2 + 10, 68), wd, size, hl.get(wd, WHITE), HAND)
            t0 = 82.2 + (cum / tot) * 5.2
            items.append(Item(c.out(), wx + ww / 2, y, t0, "fade", 0.18))
            cum += len(wd) + 1
    S.append(Scene(82.1, DUR + 0.2, bg(NAVY, NAVY_S), items, (1.0, 1.04, 960, 540)))
    return S


def make_renderer():
    scenes = build()

    def at(t):
        for i, s in enumerate(scenes):
            if s.t0 <= t < s.t1 + 1e-6:
                return i
        return len(scenes) - 1

    def frame(t):
        i = at(t)
        s = scenes[i]
        f = s.render(t)
        dt = t - s.t0
        if i > 0 and 0 <= dt < 0.14:
            prev = scenes[i - 1].render(s.t0 - 1e-3)
            p = dt / 0.14
            f = (prev.astype(np.float32) * (1 - p) + f.astype(np.float32) * p).astype(np.uint8)
        if t > DUR - 0.35:
            q = max(0, (DUR - t) / 0.35)
            f = (f.astype(np.float32) * q).astype(np.uint8)
        return f
    return frame, scenes
