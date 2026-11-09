"""Chyť robota: nezávislé geometrické/časové vstupy a skutečný běh GUI."""
import math
import os
from pathlib import Path
import random
import struct

os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import pygame


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def near(actual, expected):
    return len(actual) == len(expected) and all(math.isclose(a, b, abs_tol=1e-8, rel_tol=1e-9) for a, b in zip(actual, expected))


def click(pos, button=1, kind=pygame.MOUSEBUTTONDOWN):
    return pygame.event.Event(kind, pos=pos, button=button)


def selection(ns):
    cls = ns['Robot']
    require(isinstance(cls, type) and issubclass(cls, pygame.sprite.Sprite), 'Robot musí dědit skutečnou třídu Sprite.')
    for radius, points in [(22, 10), (9, 0), (31, 37)]:
        source = pygame.Vector2(-40.3, 120.2)
        robot, other = cls(source, radius, points), cls(source, radius, points)
        require(robot.radius == radius and robot.body == points and isinstance(robot.pozice, pygame.Vector2), 'Uložte předaný radius, body a přesnou polohu.')
        require(robot.pozice is not source and near(robot.pozice, source) and robot.rect.center == (-40, 120), 'Kreslený střed zaokrouhlete, vlastní přesnou polohu zachovejte.')
        require(robot.image.get_size() == (2 * radius, 2 * radius) and robot.image is not other.image, 'Každý robot má vlastní obrázek velikosti 2×radius.')
        original_pixel = other.image.get_at((radius, radius))
        robot.image.set_at((radius, radius), (1, 2, 3))
        require(other.image.get_at((radius, radius)) == original_pixel, 'Instance nesmějí sdílet měnitelný obrázek.')
        for dx, dy in [(0, 0), (radius, 0), (-radius, 0), (0, -radius), (radius + .01, 0), (.9 * radius, .9 * radius), (2 * radius, 2 * radius)]:
            point = pygame.Vector2(-40 + dx, 120 + dy)
            before = tuple(point), tuple(robot.pozice), tuple(robot.rect)
            expected = dx * dx + dy * dy <= radius * radius
            require(robot.obsahuje(point) is expected, 'Zásah je kruh kolem rect.center včetně přesné hrany, nikoli celý čtverec ani desetinná poloha.')
            require((tuple(point), tuple(robot.pozice), tuple(robot.rect)) == before, 'Test bodu nesmí měnit vstup nebo robota.')
        robot.update(.7, pygame.Rect(-100, 50, 200, 200))
        require(near(robot.pozice, source) and tuple(source) == (-40.3, 120.2), 'Základní Robot stojí a nemění předanou pozici.')
    first, top, away = cls((100, 100)), cls((100, 100)), cls((200, 200))
    group = pygame.sprite.Group(first, top, away)
    before = group.sprites()
    require(ns['najdi_robota'](group, (100, 100)) is top, 'Při překrytí vraťte původní poslední zasažený objekt, nakreslený navrchu.')
    require(ns['najdi_robota'](group, (200, 200)) is away, 'Nehledejte jen na jedné pevné pozici.')
    require(ns['najdi_robota'](group, (121, 121)) is None and ns['najdi_robota'](pygame.sprite.Group(), (0, 0)) is None, 'Průhledný roh ani prázdná skupina neznamenají zásah.')
    require(group.sprites() == before, 'Výběr nemění členství ani pořadí skupiny.')
    return True


def movement(ns):
    Guard, Swing, Base = ns['Hlidac'], ns['Kyvac'], ns['Robot']
    require(isinstance(Guard, type) and isinstance(Swing, type) and issubclass(Guard, Base) and issubclass(Swing, Base), 'Oba pohyblivé typy dědí Robot.')
    bounds = pygame.Rect(-120, -90, 240, 180)
    for start, velocity, radius, steps in [((0, 0), (80, 50), 22, [0, .125]), ((0, 0), (-80, -50), 9, [10, 0]), ((0, 0), (80, 50), 22, [10, 0]), ((0, 0), (1, 0), 22, [.001] * 100), ((98, 68), (4, 9), 22, [0, .1]), ((-98, -68), (-4, -9), 22, [0, .1])]:
        point, speed = pygame.Vector2(start), pygame.Vector2(velocity)
        obj, other = Guard(point, speed, radius, 37), Guard(point, speed, radius, 37)
        require(obj.rychlost is not speed and isinstance(obj.rychlost, pygame.Vector2) and obj.body == 37 and obj.radius == radius, 'Hlídač kopíruje vektor rychlosti a zachová předané údaje rodiče.')
        expected, direction = list(start), list(velocity)
        for dt in steps:
            expected = [p + v * dt for p, v in zip(expected, direction)]
            for axis, low, high in [(0, bounds.left + radius, bounds.right - radius), (1, bounds.top + radius, bounds.bottom - radius)]:
                if expected[axis] <= low:
                    expected[axis], direction[axis] = low, abs(direction[axis])
                elif expected[axis] >= high:
                    expected[axis], direction[axis] = high, -abs(direction[axis])
            obj.update(dt, bounds)
            require(near(obj.pozice, expected) and near(obj.rychlost, direction) and obj.rect.center == tuple(round(x) for x in expected), 'Posun je rychlost×dt; všechny čtyři hrany omezují celý obraz a nastavují směr dovnitř i při přesném dosažení.')
        require(tuple(point) == start and tuple(speed) == velocity and near(other.pozice, start), 'Hlídač nemění zdroje ani jiné instance.')
    for anchor, amplitude, period, radius, steps in [((0, 0), 50, 2, 22, [0, .5, .5, .5, .5]), ((0, 0), 13, .8, 9, [.001] * 100), ((80, 60), 300, 1, 22, [.25, .5]), ((10, 12), 0, 3, 12, [1])]:
        source = pygame.Vector2(anchor)
        obj = Swing(source, amplitude, period, radius, 31)
        require(obj.kotva is not source and obj.kotva is not obj.pozice and obj.amplituda == amplitude and obj.perioda == period and obj.cas == 0 and obj.body == 31, 'Kývač má vlastní neměnnou kotvu, parametry a počáteční čas 0.')
        elapsed = 0.0
        for dt in steps:
            elapsed += dt
            x = anchor[0] + amplitude * math.sin(2 * math.pi * elapsed / period)
            expected = (max(bounds.left + radius, min(bounds.right - radius, x)), max(bounds.top + radius, min(bounds.bottom - radius, anchor[1])))
            obj.update(dt, bounds)
            require(near(obj.pozice, expected) and math.isclose(obj.cas, elapsed) and obj.rect.center == tuple(round(v) for v in expected), 'Sinus počítejte od kotvy z celkového času a periody; omezte výsledek i aktualizujte rect.')
            require(near(obj.kotva, anchor) and tuple(source) == anchor, 'Kývač nesmí posouvat kotvu ani vstupní vektor.')
    require(tuple(bounds) == (-120, -90, 240, 180), 'Pohyb nesmí přepsat předané hranice.')
    for period in [0, -1]:
        try:
            Swing((0, 0), perioda=period)
        except ValueError:
            pass
        else:
            require(False, 'Nekladnou periodu odmítněte ValueError.')
    group = pygame.sprite.Group(Base((0, 0)), Guard((0, 0), (10, 20)), Swing((0, 0)))
    group.update(.5, bounds)
    require([r.rect.center for r in group] == [(0, 0), (5, 10), (50, 0)], 'Různé typy musejí spolupracovat v jedné skutečné Group.update(dt,hranice).')
    return True


def account_state(lov):
    return lov.skore, lov.zivoty, lov.pokusy, lov.zasahy, tuple(lov.roboty)


def accounting(ns):
    Robot, cls = ns['Robot'], ns['Lov']
    first, top = Robot((100, 100)), Robot((100, 100), body=37)
    original = pygame.sprite.Group(first, top)
    extra = pygame.sprite.Group(top)
    obj, other = cls(original, 2), cls([], 0)
    require(isinstance(obj.roboty, pygame.sprite.Group) and obj.roboty is not original and obj.roboty.sprites() == [first, top], 'Lov má vlastní skupinu se stejnými původními objekty.')
    require(account_state(obj)[:4] == (0, 2, 0, 0) and obj.presnost() == 0, 'Čítače začínají na nule, nulová přesnost nedělí nulou.')
    for event in [pygame.event.Event(pygame.USEREVENT), pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE), click((100, 100), 3), click((100, 100), kind=pygame.MOUSEBUTTONUP)]:
        before = account_state(obj)
        require(obj.klik(event) is None and account_state(obj) == before, 'Jiné události, pravé tlačítko a uvolnění nemění účetnictví.')
    require(obj.klik(click((100, 100))) is top and account_state(obj)[:4] == (37, 2, 1, 1), 'Jeden stisk chytí jen horního robota a přičte jeho skutečnou hodnotu.')
    require(not top.groups() and not extra and original.sprites() == [first], 'Chycený sprite odstraňte ze všech skupin, ostatní zachovejte.')
    require(obj.klik(click((400, 400))) is None and account_state(obj)[:4] == (37, 1, 2, 1), 'Minutí je pokus a ztráta jednoho života, nikoli bod nebo zásah.')
    require(obj.klik(click((100, 100))) is first and account_state(obj)[:4] == (47, 1, 3, 2) and math.isclose(obj.presnost(), 200 / 3), 'Přesnost je nezaokrouhlený podíl zásahů a pokusů, nezávislý na bodech.')
    before = account_state(obj)
    require(obj.klik(click((400, 400))) is None and account_state(obj) == before, 'Po pochytání všech cílů další klik není pokus.')
    require(account_state(other)[:4] == (0, 0, 0, 0), 'Instance nesdílejí čítače.')
    dead = cls([Robot((200, 200))], 1)
    dead.klik(click((500, 500))); before = account_state(dead)
    require(before[:4] == (0, 0, 1, 0), 'Poslední život lze ztratit.')
    require(dead.klik(click((200, 200))) is None and account_state(dead) == before, 'Po nule není zásah ani další záporný život.')
    return True


def wave_signature(kolo):
    return [(type(r).__name__, tuple(r.rect.center), r.body, tuple(r.rychlost) if hasattr(r, 'rychlost') else r.perioda) for r in kolo.lov.roboty]


def same_wave(actual, expected):
    if len(actual) != len(expected):
        return False
    for a, b in zip(actual, expected):
        if a[:3] != b[:3]:
            return False
        if isinstance(b[3], tuple):
            if not near(a[3], b[3]):
                return False
        elif not math.isclose(a[3], b[3], abs_tol=1e-9, rel_tol=1e-9):
            return False
    return True


def oracle_wave(rng, number):
    result = []
    for index in range(min(2 + number, 6)):
        x, y = rng.randint(114, 606), rng.randint(118, 434)
        if index % 2 == 0:
            result.append(('Hlidac', (x, y), 10, (rng.choice((-1, 1)) * min(80 + 15 * (number - 1), 220), 50)))
        else:
            result.append(('Kyvac', (x, y), 20, max(.7, 2 - .15 * (number - 1))))
    return result


def rounds(ns):
    cls = ns['Kolo']
    a, b, other = cls(17, 12), cls(17, 12), cls(18, 12)
    require(a.hranice is not ns['HRANICE'] and tuple(a.hranice) == (24, 96, 672, 360) and isinstance(a.rng, random.Random), 'Kolo vlastní kopii hranic a generátor náhody.')
    require(a.zbyva == 12 and not a.konec and a.duvod == '' and a.cislo == 1 and isinstance(a.lov, ns['Lov']), 'Čistý začátek s první tříčlennou vlnou.')
    rng = random.Random(17)
    require(same_wave(wave_signature(a), oracle_wave(rng, 1)) and same_wave(wave_signature(a), wave_signature(b)) and wave_signature(a) != wave_signature(other), 'Předávejte seed a losujte x, y a případně směr přes vlastní generátor.')
    require(a.lov.roboty is not b.lov.roboty and all(x is not y for x, y in zip(a.lov.roboty, b.lov.roboty)), 'Kola nesdílejí skupiny ani sprity.')
    before = wave_signature(a), a.cislo, a.rng.getstate()
    require(a.dalsi_vlna() is False and (wave_signature(a), a.cislo, a.rng.getstate()) == before, 'Dokud cíle existují, další vlna nic nezmění ani nelosuje.')
    positions = [(r, tuple(r.pozice), tuple(r.rychlost) if hasattr(r, 'rychlost') else None) for r in a.lov.roboty]
    a.update(.125)
    for r, position, velocity in positions:
        expected = (position[0] + velocity[0] * .125, position[1] + velocity[1] * .125) if velocity else (position[0] + 50 * math.sin(2 * math.pi * .125 / 2), position[1])
        require(near(r.pozice, expected), 'Kolo musí skutečně aktualizovat oba druhy robotů s dt a hranicemi.')
    require(a.zbyva == 11.875, 'Čas odečtěte v sekundách.')
    a.lov.skore, a.lov.zivoty, a.lov.pokusy, a.lov.zasahy = 5, 2, 4, 1
    for number in range(2, 17):
        a.lov.roboty.empty()
        before = account_state(a.lov)[:4], a.zbyva
        require(a.dalsi_vlna() is True and a.cislo == number and same_wave(wave_signature(a), oracle_wave(rng, number)), 'Vlny střídají typy, pokračují v náhodě a respektují stropy počtu/rychlosti/periody.')
        require(all(r.radius == 22 and a.hranice.contains(r.rect) for r in a.lov.roboty), 'Nové vlny používají výchozí velikost robotů a vznikají uvnitř plochy.')
        require((account_state(a.lov)[:4], a.zbyva) == before, 'Nová vlna nesmí resetovat čas, životy, skóre ani přesnost.')
    a = cls(17, 12)
    a.lov.roboty.empty(); last = ns['Robot']((100, 200), body=100)
    a.lov.roboty.add(last); extra = pygame.sprite.Group(last)
    a.lov.skore, a.lov.zivoty, a.lov.pokusy, a.lov.zasahy = 5, 2, 4, 1
    require(a.klik(click((100, 200))) is last and not extra and a.cislo == 2 and len(a.lov.roboty) == 4, 'Po chycení posledního cíle hned vytvořte další vlnu, zachovejte návratový objekt.')
    require(account_state(a.lov)[:4] == (105, 2, 5, 2) and a.zbyva == 12, 'Přechod vlny zachová čítače i čas.')
    a = cls(17, .01); before = wave_signature(a)
    a.update(.02)
    require(a.konec is True and a.duvod == 'cas' and a.zbyva == 0 and wave_signature(a) == before, 'Vypršení času skončí před pohybem a před následným kliknutím.')
    frozen = account_state(a.lov), a.rng.getstate()
    a.klik(click(a.lov.roboty.sprites()[-1].rect.center)); a.update(2)
    require((account_state(a.lov), a.rng.getstate()) == frozen and a.zbyva == 0, 'Po konci model, čítače i náhoda zůstávají stejné.')
    a.lov.roboty.empty(); require(a.dalsi_vlna() is False, 'Po konci už nevytvářejte další vlnu.')
    a = cls(); a.lov.zivoty = 1
    a.klik(click((-200, -200)))
    require(a.konec is True and a.duvod == 'zivoty' and a.lov.zivoty == 0, 'Poslední minutí ukončí kolo ihned, ještě před dalším update.')
    for limit in [0, -1]:
        try:
            cls(limit=limit)
        except ValueError:
            pass
        else:
            require(False, 'Nekladný limit odmítněte ValueError.')
    return True


def frozen_world(kolo):
    return kolo.zbyva, kolo.cislo, account_state(kolo.lov), wave_signature(kolo), kolo.rng.getstate()


def game(ns):
    cls = ns['Hra']
    key = lambda code: pygame.event.Event(pygame.KEYDOWN, key=code)
    obj = cls(17)
    require(obj.seed == 17 and obj.bezi is True and obj.stav == 'nabidka' and obj.kolo is None and obj.nabidka_povolena is True, 'Nabídka má běžící okno, ale ještě žádné Kolo.')
    for event in [key(pygame.K_r), key(pygame.K_p), click((200, 200)), pygame.event.Event(pygame.KEYUP, key=pygame.K_SPACE)]:
        obj.zpracuj(event)
    obj.update(30)
    require(obj.stav == 'nabidka' and obj.kolo is None, 'Nabídka nezačne na R/P/klik/KEYUP a neodečítá čas.')
    obj.zpracuj(key(pygame.K_SPACE)); old = obj.kolo
    require(obj.stav == 'hra' and isinstance(old, ns['Kolo']) and wave_signature(old) == oracle_wave(random.Random(17), 1), 'Mezerník spustí skutečné nové Kolo s předaným seedem.')
    obj.update(.125); require(old.zbyva == 29.875, 'Hraní předá dt do kola právě jednou.')
    obj.zpracuj(key(pygame.K_p)); before = frozen_world(old)
    obj.update(10); obj.zpracuj(click((-200, -200))); obj.zpracuj(pygame.event.Event(pygame.KEYUP, key=pygame.K_p))
    require(obj.stav == 'pauza' and frozen_world(old) == before, 'Pauza zmrazí svět i kliknutí, KEYUP ji nezruší.')
    obj.zpracuj(key(pygame.K_p)); require(obj.stav == 'hra' and obj.kolo is old, 'P pokračuje ve stejném světě.')
    old.lov.skore = 77; before = frozen_world(old)
    obj.zpracuj(key(pygame.K_p)); obj.zpracuj(key(pygame.K_r))
    require(obj.kolo is not old and obj.stav == 'hra' and obj.kolo.zbyva == 30 and account_state(obj.kolo.lov)[:4] == (0, 3, 0, 0), 'R i v pauze vytvoří čisté nové kolo a přejde do hry.')
    require(frozen_world(old) == before and wave_signature(obj.kolo) == oracle_wave(random.Random(17), 1), 'Restart nevyprázdní staré skupiny a zopakuje seed.')
    obj.zpracuj(key(pygame.K_r)); require(obj.kolo is not old and obj.stav == 'hra', 'Restart funguje i při hraní.')
    obj.kolo.lov.zivoty = 1; obj.zpracuj(click((-200, -200)))
    require(obj.stav == 'vysledek' and obj.bezi is True and obj.kolo.duvod == 'zivoty', 'Poslední minutí ihned ukáže výsledek bez zavření aplikace.')
    old = obj.kolo; before = frozen_world(old)
    obj.update(10); obj.zpracuj(click((100, 100))); obj.zpracuj(key(pygame.K_p))
    require(obj.stav == 'vysledek' and frozen_world(old) == before, 'Výsledek se nehýbe, neúčtuje kliky a nemá pauzu.')
    obj.zpracuj(key(pygame.K_r)); obj.update(31)
    require(obj.stav == 'vysledek' and obj.kolo.duvod == 'cas', 'Výsledek musí následovat i po vypršení času.')
    obj.zpracuj(key(pygame.K_SPACE))
    require(obj.stav == 'nabidka' and obj.kolo is None, 'Mezerník z výsledku vrací čistou nabídku.')
    for state in ['nabidka', 'hra', 'pauza', 'vysledek']:
        obj = cls(17)
        if state != 'nabidka':
            obj.novy_lov(); obj.stav = state
        old = obj.kolo; before = frozen_world(old) if old is not None else None
        obj.zpracuj(pygame.event.Event(pygame.QUIT))
        obj.zpracuj(key(pygame.K_r)); obj.zpracuj(key(pygame.K_SPACE)); obj.update(5)
        obj.zpracuj(pygame.event.Event(pygame.QUIT))
        require(obj.bezi is False and obj.kolo is old and (frozen_world(old) if old is not None else None) == before, 'QUIT funguje všude a další vstup už ukončenou aplikaci neobnoví.')
    obj = cls(); obj.zpracuj(key(pygame.K_ESCAPE)); require(obj.bezi is False, 'Esc funguje už v nabídce.')
    return True


def over(c, ns, stage):
    operation = [selection, movement, accounting, rounds, game][stage]
    ok, result = c.call({'probe': lambda: operation(ns or {})}, 'probe')
    c.add('Pravidla nové části projektu', ok and result is True, '' if ok and result is True else f'{type(result).__name__}: {result}')
    c.add('Import neotevírá okno', pygame.display.get_surface() is None, 'Okno a smyčku spouštějte až pod __main__.')
    events = {}
    if stage == 4:
        events[0] = [{'type': 'KEYDOWN', 'key': 'K_SPACE'}]
    point = oracle_wave(random.Random(11), 1)[-1][1] if stage >= 3 else (160, 200)
    events[1] = [{'type': 'MOUSEBUTTONDOWN', 'button': 1, 'pos': list(point)}]
    events[4] = [{'type': 'QUIT'}]
    if stage == 4:
        events[2] = [{'type': 'KEYDOWN', 'key': 'K_p'}]
    r = c.pygame_run(frames=15, colors=[(55, 205, 177, 24, 96, 672, 360), (80, 170, 255, 24, 96, 672, 360)], events=events, mouse={0: (5, 5)})
    if c.pg_no_error(r):
        c.add('Skutečné okno s roboty', r.size == [720, 520] and 'Chyť robota' in (r.caption or '') and r.ended and r.frames == 5 and sum(r.color_count(color, frame=0, region=(24, 96, 672, 360)) for color in [(55, 205, 177), (80, 170, 255)]) > 100, 'Použijte připravenou smyčku 720×520; hra musí roboty skutečně kreslit a přijmout zavření.')
        c.add('Kliknutí ovládá stejný viditelný model', r.rendered('Body: 10'), 'Levé kliknutí má chytit skutečného robota podle události.pos, i když je aktuální kurzor jinde.')
        c.add('Omezená frekvence smyčky', bool(r.fps) and all(v == 60 for v in r.fps), 'Použijte společné Clock.tick(60).')
        path = Path('roboti.png')
        data = path.read_bytes() if path.is_file() else b''
        c.add('Poslední snímek při zavření', data.startswith(b'\x89PNG\r\n\x1a\n') and len(data) > 24 and struct.unpack('>II', data[16:24]) == (720, 520), 'Běžné zavření uchová poslední skutečné roboti.png, také v pauze.')
