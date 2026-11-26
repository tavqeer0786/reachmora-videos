"""Full Walmart documentary timeline using the supplied flat-puppet scene style."""
import math
import scenes as c1
from scenes import *

FPS = 30
AUDIO = [72.364082, 87.906100, 94.765737, 91.199615, 95.055986, 98.665556, 79.945828, 103.086825, 85.125737, 86.905782]
DUR = sum(AUDIO)

NAVY2, NAVY2_S = (28, 34, 48), (52, 62, 86)
SAGE2, SAGE2_S = (168, 190, 190), (196, 214, 212)
WARM2, WARM2_S = (60, 44, 44), (98, 72, 64)
BLUE2, BLUE2_S = (26, 66, 124), (48, 100, 176)
PEACH2, PEACH2_S = (222, 200, 172), (240, 224, 200)
RED2, RED2_S = (58, 26, 30), (110, 44, 50)


# Small aliases keep the new chapter vocabulary readable while reusing the
# supplied prop library.
def package_box():
    return gift(300, (70, 120, 200))


def truck():
    return bag_shop(340, (70, 120, 200))


def delivery_truck():
    return bag_shop(360, (62, 160, 90))


def basket():
    return cart(480, 380)


def shift_scene(s, off):
    s.t0 += off
    s.t1 += off
    for it in s.items:
        it.t0 += off
        if it.end is not None:
            it.end += off
        if it.path:
            it.path = [(t + off, x, y) for t, x, y in it.path]


def hero(x, y, t, color=(70, 120, 200), mood="neutral", scale=1.1, flip=False):
    return Item(sc(person(color, mood, lh=(-70, 60), rh=(70, 60), flip=flip), scale), x, y, t, "pop", .35, bob=5)


def prop(fn, x, y, t, scale=1.0, anim="pop", dx=0, dy=0, end=None):
    image = fn() if callable(fn) else fn
    return Item(sc(image, scale), x, y, t, anim, .4, dx=dx, dy=dy, end=end, bob=4 if anim == "pop" else 0)


def title(txt, t, color=WHITE, y=145, size=72):
    return Item(label(txt, size, color), 960, y, t, "fade", .35)


def make_shot(t0, t1, heading, items, base=NAVY2, spot=NAVY2_S, floor=None, focus=(960, 540)):
    all_items = [title(heading, t0, WHITE if base[0] < 100 else INK, 130, 70)] + items
    return Scene(t0, t1, bg(base, spot, floor=floor, floor_y=840), all_items, (1.0, 1.05, focus[0], focus[1]))


def add_chapter(S, start, length, heading, specs):
    step = length / len(specs)
    for i, make in enumerate(specs):
        a, b = start + i * step, start + (i + 1) * step
        S.append(make(a, b, heading if i == 0 else ""))


def build_hook(start, length):
    def s1(a, b, h):
        return make_shot(a, b, "BLACK FRIDAY ISN'T OVER", [
            prop(lambda: banner("BLACK FRIDAY", 620, 150, RED, WHITE, 70), 620, 470, a + .2, 1.2),
            hero(1450, 610, a + .5, (70, 120, 200), "surprised", 1.15),
            prop(lambda: sparkle(48), 1700, 260, a + 1.0),
        ], BLUE2, BLUE2_S)
    def s2(a, b, h):
        return make_shot(a, b, "CUSTOMERS RUSH IN", [
            hero(390, 650, a + .2, (70, 120, 200), "happy", .8),
            hero(840, 650, a + .55, (200, 90, 80), "happy", .8),
            hero(1290, 650, a + .9, (120, 90, 160), "happy", .8),
            prop(lambda: tv(), 520, 300, a + .8, .72), prop(lambda: gift(), 940, 300, a + 1.1, .7),
            prop(lambda: laptop(), 1360, 300, a + 1.4, .55),
        ], NAVY2, NAVY2_S, floor=(22, 26, 38))
    def s3(a, b, h):
        return make_shot(a, b, "THEN THE FIRST EVENT ENDS", [
            prop(lambda: calendar("27", "NOV", "EVENT 1"), 520, 560, a + .2, .92),
            prop(lambda: xmark(360), 1030, 520, a + 1.0, .8),
            hero(1510, 620, a + 1.3, (120, 120, 140), "worried", 1.0),
        ], WARM2, WARM2_S)
    def s4(a, b, h):
        return make_shot(a, b, "A SECOND WAVE", [
            prop(lambda: banner("BLACK FRIDAY", 520, 130, RED, WHITE, 60), 500, 390, a + .2, 1.0),
            prop(lambda: banner("PART 2", 480, 130, GOLD, INK, 65), 1110, 390, a + .7, 1.0, "slide", dx=300),
            prop(lambda: sparkle(55), 1530, 260, a + 1.2),
            title("ANOTHER REASON TO RETURN", a + 1.5, GOLD, 820, 62),
        ], BLUE2, BLUE2_S)
    def s5(a, b, h):
        return make_shot(a, b, "THE REAL STRATEGY", [
            prop(lambda: phone(420, 780, app_screen), 520, 550, a + .2, 1.0),
            prop(lambda: store(), 1130, 590, a + .6, 1.0),
            prop(lambda: timeline(160, 1660, 760), 960, 760, a + 1.1, .95, "wipe"),
            hero(1600, 600, a + 1.5, (70, 120, 200), "think", .8),
        ], SAGE2, SAGE2_S)
    def s6(a, b, h):
        return make_shot(a, b, "WHY WAIT FOR THE NEXT SALE?", [
            hero(520, 600, a + .1, (200, 90, 80), "think", 1.0),
            prop(lambda: qmark(330), 960, 470, a + .7, .9, "pop", end=b - .2),
            prop(lambda: money_sack(), 1430, 560, a + 1.1, .85),
            title("THE QUESTION", a + 1.5, GOLD, 870, 88),
        ], NAVY2, NAVY2_S)
    return [s1, s2, s3, s4, s5, s6]


def chapter_specs(kind):
    def ch2(a, b, h):
        return make_shot(a, b, "STORE + SCREEN", [prop(lambda: store(), 470, 570, a + .2, .95), prop(lambda: phone(420, 780, app_screen), 1130, 540, a + .7, .85), hero(1580, 610, a + 1.1, (70, 120, 200), "happy", .8)], SAGE2, SAGE2_S)
    def ch3(a, b, h):
        return make_shot(a, b, "MANY NEEDS. ONE ECOSYSTEM.", [hero(430, 640, a + .1, (70, 120, 200), "think", .75), prop(lambda: tv(), 840, 300, a + .5, .6), prop(lambda: gift(), 1120, 300, a + .8, .6), prop(lambda: grocery_bag(), 1390, 300, a + 1.1, .65), title("CONVENIENCE + SCALE", a + 1.5, GOLD, 850, 64)], PEACH2, PEACH2_S)
    def ch4(a, b, h):
        return make_shot(a, b, "CHECK AVAILABILITY", [prop(lambda: browser(), 560, 520, a + .2, .9), prop(lambda: magnifier(), 1080, 600, a + .7, .9), prop(lambda: pin(130), 1500, 400, a + 1.2, .9), title("THE RIGHT FULFILLMENT", a + 1.5, INK, 850, 60)], SAGE2, SAGE2_S)
    def ch5(a, b, h):
        return make_shot(a, b, "PICKUP OR DELIVERY", [prop(lambda: cart(), 500, 650, a + .1, 1.0), prop(lambda: package_box(), 1000, 520, a + .6, .85), prop(lambda: truck(), 1500, 560, a + 1.0, .85), title("LESS FRICTION", a + 1.5, GOLD, 850, 78)], NAVY2, NAVY2_S, floor=(22, 26, 38))
    def ch6(a, b, h):
        return make_shot(a, b, "THE SECOND VISIT", [hero(420, 650, a + .1, (70, 120, 200), "happy", .8), prop(lambda: calendar("27", "NOV", "VISIT 1"), 840, 420, a + .5, .65), prop(lambda: calendar("02", "DEC", "VISIT 2"), 1260, 420, a + .9, .65), prop(lambda: arrow(300), 1030, 620, a + 1.1, .7, "wipe"), title("REPEAT ENGAGEMENT", a + 1.5, GOLD, 850, 66)], BLUE2, BLUE2_S)
    def ch7(a, b, h):
        return make_shot(a, b, "WALMART+ CHANGES THE RELATIONSHIP", [prop(lambda: wm_board(), 520, 520, a + .1, .9), prop(lambda: phone(420, 780, app_screen), 1070, 530, a + .6, .8), prop(lambda: delivery_truck(), 1530, 560, a + 1.1, .8), title("MORE REASONS TO RETURN", a + 1.5, WHITE, 850, 64)], NAVY2, NAVY2_S)
    def ch8(a, b, h):
        return make_shot(a, b, "SELECTIVE DISCOUNTS", [prop(lambda: tv(), 440, 360, a + .1, .7), prop(lambda: laptop(), 890, 370, a + .5, .55), prop(lambda: teddy(), 1300, 370, a + .9, .72), prop(lambda: basket(), 980, 720, a + 1.3, .8), title("NOT EVERY DEAL HAS THE SAME JOB", a + 1.7, GOLD, 900, 56)], WARM2, WARM2_S)
    def ch9(a, b, h):
        return make_shot(a, b, "THE NEXT DEAL", [prop(lambda: clock(220, 3, 10), 500, 500, a + .2, 1.0), prop(lambda: megaphone(), 1040, 520, a + .7, .9), prop(lambda: phone(420, 780, app_screen), 1530, 530, a + 1.1, .8), title("CHECK BACK", a + 1.6, RED, 850, 90)], RED2, RED2_S)
    def ch10(a, b, h):
        return make_shot(a, b, "THE COMPETITION", [prop(lambda: amazon_tile(), 430, 470, a + .1, .85), prop(lambda: target_tile(), 970, 470, a + .6, .85), prop(lambda: wm_board(), 1510, 470, a + 1.1, .85), prop(lambda: browser(), 970, 760, a + 1.5, .7), title("COMPARE PRICES. CHECK STOCK.", a + 1.8, INK, 930, 54)], SAGE2, SAGE2_S)
    def ch11(a, b, h):
        return make_shot(a, b, "THE WHOLE HOLIDAY SEASON", [prop(lambda: calendar("27", "NOV", "START"), 400, 500, a + .1, .7), prop(lambda: calendar("01", "DEC", "MORE"), 840, 500, a + .5, .7), prop(lambda: calendar("24", "DEC", "FINISH"), 1280, 500, a + .9, .7), hero(1660, 620, a + 1.2, (70, 120, 200), "happy", .75), title("STAY VISIBLE", a + 1.6, GOLD, 850, 84)], NAVY2, NAVY2_S)
    def ch12(a, b, h):
        return make_shot(a, b, "A HABIT, NOT A SINGLE SALE", [hero(420, 630, a + .1, (70, 120, 200), "happy", .85), prop(lambda: cart(), 910, 650, a + .6, .8), prop(lambda: timeline(120, 1650, 760), 960, 760, a + 1.1, .9, "wipe"), prop(lambda: sparkle(50), 1530, 300, a + 1.4), title("REPEAT SHOPPING", a + 1.7, GOLD, 880, 76)], BLUE2, BLUE2_S)
    def ch13(a, b, h):
        return make_shot(a, b, "THE SECOND SALE IS THE OPPORTUNITY", [prop(lambda: banner("SALE 1", 420, 130, RED, WHITE, 65), 430, 430, a + .1, .9), prop(lambda: banner("SALE 2", 420, 130, GOLD, INK, 65), 1060, 430, a + .7, .9), prop(lambda: arrow(280), 760, 650, a + 1.0, .7, "wipe"), prop(lambda: qmark(300), 1550, 430, a + 1.4, .8), title("THE REAL PRIZE: THE NEXT VISIT", a + 1.8, WHITE, 850, 60)], NAVY2, NAVY2_S)
    return {
        2: [ch2, ch3, ch4, ch5, ch6],
        3: [ch6, ch8, ch9, ch11, ch12],
        4: [ch7, ch4, ch5, ch6, ch12],
        5: [ch8, ch3, ch5, ch10, ch12],
        6: [ch9, ch6, ch11, ch10, ch12],
        7: [ch10, ch4, ch7, ch11, ch12],
        8: [ch11, ch12, ch10, ch6, ch13],
        9: [ch13, ch6, ch11, ch12, ch13],
    }[kind]


def build():
    S = []
    # Hook is 0..72.36. Existing supplied Chapter 1 animation follows it.
    hook_start = 0.0
    add_chapter(S, hook_start, AUDIO[0], "", build_hook(hook_start, AUDIO[0]))
    ch1_offset = AUDIO[0]
    for s in c1.build():
        shift_scene(s, ch1_offset)
        S.append(s)
    offset = AUDIO[0] + AUDIO[1]
    for idx in range(2, 10):
        specs = chapter_specs(idx)
        add_chapter(S, offset, AUDIO[idx], "", specs)
        offset += AUDIO[idx]
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
