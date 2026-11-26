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


def fastshot(a, b, heading, caption, assets, base, spot, color=(70, 120, 200), mood="neutral", flip=False, light=False):
    """A short, busy shot: moving character plus two independently animated props."""
    span = b - a
    x0 = 250 if not flip else 1660
    x1 = 600 if not flip else 1310
    moving = Item(
        sc(person(color, mood, lh=(-95, 75), rh=(95, 35), flip=flip), .72),
        x0, 610, a, "pop", .22, bob=7, sway=2.5,
        path=[(a, x0, 610), (a + span * .45, (x0 + x1) / 2, 590), (b - .08, x1, 610)],
    )
    items = [
        title(heading, a, INK if light else WHITE, 105, 48),
        moving,
        prop(assets[0], 820, 400, a + .12, .62, "pop"),
        prop(assets[1], 1190, 470, a + .42, .62, "slide", dx=180 if not flip else -180),
        prop(lambda: arrow(230, RED if not light else INK), 1010, 650, a + .68, .62, "wipe"),
        Item(label(caption, 48, GOLD if not light else RED), 1050, 875, a + .88, "pop", .2),
    ]
    return make_shot(a, b, "", items, base, spot, floor=(22, 26, 38) if base == NAVY2 else None, focus=(960, 540))


def fast_beats(kind):
    # Each beat is a script-specific visual pair. The list cycles with changed
    # pose/entry direction so the timeline never sits on one still scene.
    common = {
        0: [("THE HOOK", "DEALS AREN'T OVER", lambda: banner("BLACK FRIDAY", 520, 130, RED, WHITE, 60), lambda: banner("PART 2", 420, 130, GOLD, INK, 60), NAVY2, NAVY2_S, "surprised"),
            ("SHOPPERS RUSH", "TVS / TOYS / ELECTRONICS", lambda: tv(), lambda: gift(), BLUE2, BLUE2_S, "happy"),
            ("THE FIRST EVENT ENDS", "ONE CHANCE?", lambda: calendar("27", "NOV", "EVENT 1"), lambda: xmark(260), WARM2, WARM2_S, "worried"),
            ("ANOTHER WAVE", "RETURN TO WALMART", lambda: store(), lambda: phone(420, 780, app_screen), SAGE2, SAGE2_S, "think"),
            ("THE BIG QUESTION", "WHY WAIT?", lambda: money_sack(), lambda: qmark(280), NAVY2, NAVY2_S, "think")],
        2: [("STORE + SCREEN", "ONE ECOSYSTEM", lambda: store(), lambda: phone(420, 780, app_screen), SAGE2, SAGE2_S, "neutral"),
            ("THE HOLIDAY LIST", "MANY NEEDS", lambda: tv(), lambda: grocery_bag(), PEACH2, PEACH2_S, "think"),
            ("ONE TRIP", "TV / TOYS / SNACKS", lambda: gift(), lambda: grocery_bag(), SAGE2, SAGE2_S, "happy"),
            ("CHECK STOCK", "BEFORE YOU DRIVE", lambda: browser(), lambda: magnifier(), SAGE2, SAGE2_S, "think"),
            ("PHYSICAL + DIGITAL", "TWO WAYS TO SHOP", lambda: store(), lambda: laptop(), NAVY2, NAVY2_S, "happy"),
            ("PICKUP OR DELIVERY", "LESS FRICTION", lambda: cart(), lambda: package_box(), NAVY2, NAVY2_S, "happy"),
            ("THE RIGHT OPTION", "FIT THE NEED", lambda: pin(130), lambda: calendar("02", "DEC", "RETURN"), BLUE2, BLUE2_S, "think"),
            ("NOT JUST PRICE", "TIME MATTERS", lambda: clock(220, 6, 25), lambda: qmark(250), WARM2, WARM2_S, "worried")],
        3: [("THE FIRST VISIT", "BUY ONCE", lambda: calendar("27", "NOV", "VISIT 1"), lambda: tv(), BLUE2, BLUE2_S, "happy"),
            ("THE SECOND VISIT", "COME BACK", lambda: calendar("02", "DEC", "VISIT 2"), lambda: gift(), BLUE2, BLUE2_S, "happy"),
            ("CYBER MONDAY", "ANOTHER CHECK", lambda: laptop(), lambda: sparkle(45), SAGE2, SAGE2_S, "think"),
            ("PAYDAY / TIMING", "NOT READY YET", lambda: clock(220, 9, 40), lambda: money_sack(), WARM2, WARM2_S, "worried"),
            ("COMPARE FIRST", "THEN DECIDE", lambda: browser(), lambda: magnifier(), SAGE2, SAGE2_S, "think"),
            ("THE APP REMINDS", "STAY IN CONSIDERATION", lambda: phone(420, 780, app_screen), lambda: sparkle(42), BLUE2, BLUE2_S, "happy"),
            ("REPEAT ENGAGEMENT", "MORE OPPORTUNITIES", lambda: timeline(120, 880, 760), lambda: cart(), NAVY2, NAVY2_S, "happy"),
            ("THE QUESTION", "WHAT BRINGS THEM BACK?", lambda: qmark(280), lambda: hero(1, 1, 0) if False else money_sack(), WARM2, WARM2_S, "think")],
        4: [("WALMART+", "MORE THAN A TRANSACTION", lambda: wm_board(), lambda: phone(420, 780, app_screen), NAVY2, NAVY2_S, "happy"),
            ("DELIVERY", "WHEN YOU NEED IT", lambda: delivery_truck(), lambda: pin(130), SAGE2, SAGE2_S, "happy"),
            ("SHIPPING PERKS", "SUBJECT TO TERMS", lambda: package_box(), lambda: calendar("02", "DEC", "DELIVERY"), PEACH2, PEACH2_S, "neutral"),
            ("KEEP USING ONE RETAILER", "LESS SWITCHING", lambda: store(), lambda: cart(), BLUE2, BLUE2_S, "think"),
            ("CONVENIENCE", "A REASON TO RETURN", lambda: phone(420, 780, app_screen), lambda: sparkle(42), SAGE2, SAGE2_S, "happy"),
            ("NOT EVERY DEAL", "IS EXCLUSIVE", lambda: warning(), lambda: xmark(240), RED2, RED2_S, "worried"),
            ("MARGINS MATTER", "SELECTIVE DISCOUNTS", lambda: money_sack(), lambda: tag_label("SALE", 300, 100, RED, WHITE, 44), WARM2, WARM2_S, "think"),
            ("THE NEXT QUESTION", "WHICH PRODUCTS?", lambda: qmark(280), lambda: tv(), NAVY2, NAVY2_S, "think")],
        5: [("HEADLINE PRODUCT", "GET ATTENTION", lambda: tv(), lambda: tag_label("SALE", 300, 100, RED, WHITE, 44), BLUE2, BLUE2_S, "surprised"),
            ("POPULAR TOY", "A REASON TO LOOK", lambda: teddy(), lambda: gift(), WARM2, WARM2_S, "happy"),
            ("LAPTOP / GAMING", "EASY TO COMPARE", lambda: laptop(), lambda: browser(), SAGE2, SAGE2_S, "think"),
            ("ADD-ONS", "SOUNDBAR / CABLES", lambda: tv(), lambda: package_box(), NAVY2, NAVY2_S, "happy"),
            ("TOYS BRING MORE", "BATTERIES / WRAP", lambda: teddy(), lambda: gift(), PEACH2, PEACH2_S, "happy"),
            ("THE BASKET GROWS", "MORE CATEGORIES", lambda: basket(), lambda: grocery_bag(), SAGE2, SAGE2_S, "happy"),
            ("INVENTORY", "WHEN TO PROMOTE", lambda: calendar("02", "DEC", "DROP"), lambda: store(), NAVY2, NAVY2_S, "think"),
            ("THE HYPE", "WHY CHECK AGAIN?", lambda: qmark(280), lambda: phone(420, 780, app_screen), RED2, RED2_S, "worried")],
        6: [("LIMITED WINDOW", "ACT SOON", lambda: clock(220, 3, 10), lambda: tag_label("LIMITED", 330, 105, RED, WHITE, 42), RED2, RED2_S, "worried"),
            ("CHECK THE NEXT WAVE", "WHAT CHANGED?", lambda: phone(420, 780, app_screen), lambda: magnifier(), SAGE2, SAGE2_S, "think"),
            ("WAIT OR BUY", "CUSTOMERS DECIDE", lambda: clock(220, 9, 40), lambda: money_sack(), WARM2, WARM2_S, "worried"),
            ("READ REVIEWS", "COMPARE FIRST", lambda: browser(), lambda: magnifier(), PEACH2, PEACH2_S, "think"),
            ("URGENCY", "BRINGS THEM BACK", lambda: megaphone(), lambda: phone(420, 780, app_screen), BLUE2, BLUE2_S, "surprised"),
            ("BUT BE CAREFUL", "DISCOUNTS GET CHECKED", lambda: warning(), lambda: browser(), RED2, RED2_S, "worried"),
            ("AMAZON / TARGET", "SAME CUSTOMER", lambda: amazon_tile(), lambda: target_tile(), SAGE2, SAGE2_S, "think"),
            ("WHAT SEPARATES WALMART?", "THE NEXT QUESTION", lambda: wm_board(), lambda: qmark(250), NAVY2, NAVY2_S, "think")],
        7: [("AMAZON", "ONLINE SCALE", lambda: amazon_tile(), lambda: browser(), SAGE2, SAGE2_S, "think"),
            ("TARGET", "A DIFFERENT MIX", lambda: target_tile(), lambda: store(), PEACH2, PEACH2_S, "happy"),
            ("WALMART", "STORE + DIGITAL", lambda: wm_board(), lambda: phone(420, 780, app_screen), BLUE2, BLUE2_S, "happy"),
            ("COMPARE PRICES", "SWITCHING IS EASY", lambda: browser(), lambda: magnifier(), SAGE2, SAGE2_S, "think"),
            ("CHECK AVAILABILITY", "BEFORE BUYING", lambda: magnifier(), lambda: pin(130), PEACH2, PEACH2_S, "think"),
            ("REVIEWS + ASSORTMENT", "MORE THAN A DEAL", lambda: laptop(), lambda: gift(), NAVY2, NAVY2_S, "happy"),
            ("CATEGORY BY CATEGORY", "KEEP THE OPTION OPEN", lambda: tv(), lambda: teddy(), WARM2, WARM2_S, "think"),
            ("THE SAME CUSTOMER", "THE FIGHT CONTINUES", lambda: person((70, 120, 200), "worried"), lambda: qmark(250), RED2, RED2_S, "worried")],
        8: [("EARLY PROMOTIONS", "THE SEASON STARTS", lambda: calendar("01", "NOV", "EARLY"), lambda: megaphone(), NAVY2, NAVY2_S, "happy"),
            ("BLACK FRIDAY", "ONE WAVE", lambda: banner("BLACK FRIDAY", 520, 130, RED, WHITE, 60), lambda: tv(), BLUE2, BLUE2_S, "surprised"),
            ("CYBER MONDAY", "ANOTHER WAVE", lambda: laptop(), lambda: phone(420, 780, app_screen), SAGE2, SAGE2_S, "think"),
            ("WEEKS TO CHRISTMAS", "MORE DECISIONS", lambda: calendar("24", "DEC", "CHRISTMAS"), lambda: tree(), PEACH2, PEACH2_S, "happy"),
            ("STAY VISIBLE", "WHILE THEY DECIDE", lambda: store(), lambda: sparkle(45), NAVY2, NAVY2_S, "happy"),
            ("ONE ECOSYSTEM", "MANY NEEDS", lambda: cart(), lambda: grocery_bag(), SAGE2, SAGE2_S, "happy"),
            ("REPEAT SHOPPING", "THE HABIT", lambda: timeline(120, 880, 760), lambda: person((70, 120, 200), "happy"), BLUE2, BLUE2_S, "happy"),
            ("THE REAL PRIZE", "THE ENTIRE SEASON", lambda: qmark(280), lambda: wm_board(), NAVY2, NAVY2_S, "think")],
        9: [("SALE 1", "THE FIRST OPPORTUNITY", lambda: banner("SALE 1", 420, 130, RED, WHITE, 60), lambda: tv(), BLUE2, BLUE2_S, "happy"),
            ("SALE 2", "THE SECOND OPPORTUNITY", lambda: banner("SALE 2", 420, 130, GOLD, INK, 60), lambda: gift(), WARM2, WARM2_S, "happy"),
            ("THE NEXT VISIT", "ANOTHER CHANCE", lambda: calendar("02", "DEC", "RETURN"), lambda: store(), SAGE2, SAGE2_S, "think"),
            ("THE BASKET", "MORE THAN ONE PRODUCT", lambda: basket(), lambda: grocery_bag(), PEACH2, PEACH2_S, "happy"),
            ("THE CUSTOMER", "CHOOSES AGAIN", lambda: person((70, 120, 200), "happy"), lambda: phone(420, 780, app_screen), BLUE2, BLUE2_S, "happy"),
            ("NOT JUST PRICE", "CONVENIENCE + SCALE", lambda: wm_board(), lambda: sparkle(45), NAVY2, NAVY2_S, "think"),
            ("THE QUESTION", "WHY WALMART AGAIN?", lambda: qmark(300), lambda: amazon_tile(), RED2, RED2_S, "worried")],
    }
    return common[kind]


def add_fast_chapter(S, start, length, kind):
    beats = fast_beats(kind)
    count = max(len(beats), math.ceil(length / 1.9))
    step = length / count
    for i in range(count):
        a, b = start + i * step, start + (i + 1) * step
        heading, caption, p1, p2, base, spot, mood = beats[i % len(beats)]
        S.append(fastshot(a, b, heading, caption, [p1, p2], base, spot,
                          color=((70 + (i * 17) % 110), 120, 200), mood=mood,
                          flip=(i % 2 == 1), light=(base[0] > 100)))


def build():
    S = []
    # Hook is 0..72.36. Existing supplied Chapter 1 animation follows it.
    # The hook and every later chapter use short micro-shots; Chapter 1 keeps
    # the original supplied Claude scene block as the visual reference.
    add_fast_chapter(S, 0.0, AUDIO[0], 0)
    ch1_offset = AUDIO[0]
    for s in c1.build():
        shift_scene(s, ch1_offset)
        S.append(s)
    offset = AUDIO[0] + AUDIO[1]
    for idx in range(2, 10):
        add_fast_chapter(S, offset, AUDIO[idx], idx)
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
