"""Volitelné kontroly Pygame 2: skutečné Sprite/Surface/Group bez okna."""
import math
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import pygame

NAMES = [
    ['Lod', 'Meteorit', 'Stit', 'Prekazka', 'Hrac'],
    ['PohyblivaLod', 'RizenaLod', 'OmezenaLod', 'ZrychlujiciLod', 'CilovaLod'],
    ['posun_skupinu', 'vykresli_skupinu', 'vyrad_mimo', 'skupina_typu', 'sloucene_skupiny'],
    ['zasahy', 'seber_bonusy', 'prvni_zasah', 'dvojice_zasahu', 'zasahy_kruhem'],
    ['HerniStav', 'Casovac', 'Zivoty', 'Rezimy', 'NovaHra'],
]


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def pixels(surface):
    return pygame.image.tobytes(surface, 'RGBA')


def close(actual, expected):
    return len(actual) == len(expected) and all(math.isclose(a, b, abs_tol=1e-9, rel_tol=1e-9) for a, b in zip(actual, expected))


class Bod(pygame.sprite.Sprite):
    """Vlastní vstup kontroly, nikoli přiložená vzorová třída studenta."""
    def __init__(self, center, color=(80, 180, 255), size=(20, 20)):
        super().__init__()
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.image.fill(color)
        self.rect = self.image.get_rect(center=center)
        self.pos = list(center)
        self.calls = []

    def update(self, dt):
        self.calls.append(dt)
        self.pos[0] += 10 * dt
        self.pos[1] -= 4 * dt
        self.rect.center = tuple(round(v) for v in self.pos)


class Zvlastni(Bod):
    pass


class Potomek(Zvlastni):
    pass


def snapshot(objects):
    return [(tuple(o.rect), pixels(o.image), list(o.calls)) for o in objects]


def sprites(ns, task, case):
    cls = ns[NAMES[0][task]]
    require(isinstance(cls, type) and issubclass(cls, pygame.sprite.Sprite), 'Vytvořte skutečnou třídu odvozenou od Sprite.')
    center = [[80, 100], [-20, 0], [520, 280]][case]
    original_center = center.copy()
    color = (80, 180, 255)
    size = (32, 24)
    group = pygame.sprite.Group(Bod((0, 0)))
    original = None
    if task == 0:
        args = (center,)
    elif task == 1:
        radius = [2, 7, 20][case]
        args = (center, radius); size = (2 * radius, 2 * radius); color = (235, 145, 75)
    elif task == 2:
        size = ([13, 7], [40, 30], [5, 60])[case]
        color = ([0, 255, 30], [150, 0, 240], [30, 90, 120])[case]
        args = (center, size, color)
    elif task == 3:
        size = (13 + case * 4, 9 + case * 2)
        original = pygame.Surface(size, pygame.SRCALPHA)
        original.fill((60, 70, 80, 170)); original.set_at((1, 1), (200, 30, 70, 255))
        args = (original, center)
    else:
        args = (center, group)
    original_pixels = pixels(original) if original is not None else None
    saved_size, saved_color = tuple(size), tuple(color)
    a, b = cls(*args), cls(*args)
    require(tuple(size) == saved_size and tuple(color) == saved_color, 'Neměňte předané rozměry ani barvu.')
    require(isinstance(a, pygame.sprite.Sprite), 'Výsledek musí být skutečný pygame.sprite.Sprite.')
    require(isinstance(a.image, pygame.Surface) and isinstance(a.rect, pygame.Rect), 'Sprite potřebuje image Surface a rect Rect.')
    require(a.image.get_size() == tuple(size) and a.rect.size == tuple(size), 'Rozměr obrázku a rect neodpovídá zadání.')
    anchor = a.rect.topleft if task == 3 else a.rect.center
    require(anchor == tuple(center), 'Záměna středu a levého horního rohu nebo špatná poloha.')
    require(center == original_center, 'Vstupní souřadnice se nesmějí změnit.')
    require(a.image is not b.image and a.rect is not b.rect, 'Každá instance potřebuje vlastní obraz i rect.')
    if task == 3:
        before = original_pixels
        require(a.image is not original and pixels(a.image) == before, 'Zachovejte pixely, ale použijte samostatnou kopii obrázku.')
    else:
        require(tuple(a.image.get_at((size[0] // 2, size[1] // 2)))[:3] == tuple(color), 'Špatná barva uvnitř obrázku.')
        if task == 1:
            require(a.image.get_at((0, 0)).a == 0, 'Meteorit má průhledné rohy, nikoli vyplněný čtverec.')
        else:
            require(tuple(a.image.get_at((0, 0)))[:3] == tuple(color), 'Celý obdélník vyplňte barvou.')
    if task == 4:
        require(a in group and b in group and len(group) == 3, 'Přidejte nové hráče do předané skupiny a zachovejte její členy.')
    untouched = pixels(b.image), tuple(b.rect)
    a.image.fill((1, 2, 3)); a.rect.x += 19
    require((pixels(b.image), tuple(b.rect)) == untouched, 'Změna jedné instance poškodila druhou.')
    if original is not None:
        require(pixels(original) == before, 'Změna překážky poškodila původní Surface.')
    return True


def motion(ns, task, case):
    cls = ns[NAMES[1][task]]
    require(isinstance(cls, type) and issubclass(cls, pygame.sprite.Sprite), 'Pohyb patří do vlastní třídy Sprite.')
    start = pygame.Vector2(100.25, 100.75)
    velocity = pygame.Vector2([(1, -.5), (-60, 30), (0, 0)][case])
    steps = [[.01] * 100, [0, .25, .25, .5], [0, 1, 2]][case]
    direction = pygame.Vector2([(3, 4), (0, 0), (-1, 1)][case])
    acceleration = pygame.Vector2(4, -2)
    bounds = pygame.Rect(40, 60, 120, 80)
    goal = pygame.Vector2([(110, 110), tuple(start), (160.25, 180.75)][case])
    if task == 0:args = (start, velocity)
    elif task == 1:args = (start, 100)
    elif task == 2:
        if case == 1:velocity.update(1000, -1000)
        args = (start, velocity, bounds)
    elif task == 3:args = (start, velocity, acceleration)
    else:args = (start, 25, goal)
    before = tuple(start), tuple(velocity), tuple(acceleration), tuple(goal), tuple(bounds), tuple(direction)
    obj, other = cls(*args), cls(*args)
    require(isinstance(obj, pygame.sprite.Sprite) and isinstance(obj.pozice, pygame.Vector2), 'Použijte Sprite a samostatnou desetinnou pozici Vector2.')
    require(obj.pozice is not start, 'Pozice musí být kopie vstupního vektoru.')
    if task in (0, 2, 3):require(isinstance(obj.rychlost, pygame.Vector2) and obj.rychlost is not velocity, 'Rychlost musí být vlastní Vector2.')
    if task == 2:require(obj.hranice is not bounds, 'Hranice zkopírujte.')
    if task == 3:require(obj.zrychleni is not acceleration, 'Zrychlení zkopírujte.')
    if task == 4:require(obj.cil is not goal, 'Cíl zkopírujte.')
    pos = list(start); speed = list(velocity)
    require(close(obj.pozice, pos) and obj.rect.center == tuple(round(v) for v in pos), 'Nezaměňte střed s rohem ani desetinnou pozici s rect.')
    for dt in steps:
        if task == 1:
            length = math.hypot(*direction)
            if length:
                pos = [p + d / length * 100 * dt for p, d in zip(pos, direction)]
            obj.update(direction, dt)
        elif task == 4:
            delta = [g - p for g, p in zip(goal, pos)]; length = math.hypot(*delta)
            if length <= 25 * dt:pos = list(goal)
            elif length:pos = [p + d / length * 25 * dt for p, d in zip(pos, delta)]
            obj.update(dt)
        else:
            if task == 3:speed = [v + a * dt for v, a in zip(speed, acceleration)]
            pos = [p + v * dt for p, v in zip(pos, speed)]
            if task == 2:
                pos[0] = max(bounds.left + 16, min(bounds.right - 16, pos[0]))
                pos[1] = max(bounds.top + 12, min(bounds.bottom - 12, pos[1]))
            obj.update(dt)
        require(close(obj.pozice, pos), 'Nesprávný pohyb, čas, normalizace či hranice; neztrácejte desetinné kroky.')
        require(obj.rect.center == tuple(round(v) for v in pos), 'Rect musí sledovat aktuální pozici přes round.')
        if task == 3:require(close(obj.rychlost, speed), 'Aktualizujte nejprve rychlost podle zrychlení.')
    require(close(other.pozice, start), 'Pohyb jedné instance změnil druhou.')
    require((tuple(start), tuple(velocity), tuple(acceleration), tuple(goal), tuple(bounds), tuple(direction)) == before, 'Neměňte vstupní vektory ani rect.')
    return True


def groups(ns, task, case):
    fn = ns[NAMES[2][task]]
    objects = [Bod((90, 70)), Zvlastni((40, 50)), Potomek((90, 70))] if case else []
    group = pygame.sprite.Group(objects)
    old = snapshot(objects)
    if task == 0:
        dt = [0, .5, 2][case]
        result = fn(group, dt)
        expected = sorted((round(rect.centerx + 10 * dt), round(rect.centery - 4 * dt)) for rect in (pygame.Rect(s[0]) for s in old))
        require(result == expected, 'Vraťte seřazené dvojice středů po aktualizaci.')
        require(all(o.calls == [dt] for o in objects), 'Předejte dt každému členu právě jednou.')
    elif task == 1:
        objects = [Bod((30, 30), (230, 100, 20)), Bod((90, 70), (50, 230, 100))] if case else []
        group = pygame.sprite.Group(objects); old = snapshot(objects)
        bg = pygame.Surface((120, 100)); bg.fill((4, 8, 12)); before = pixels(bg)
        expected = bg.copy()
        for o in objects:expected.blit(o.image, o.rect)
        result = fn(group, bg)
        require(isinstance(result, pygame.Surface) and result is not bg, 'Vraťte nový Surface, nikoli původní pozadí.')
        require(result.get_size() == bg.get_size() and pixels(result) == pixels(expected), 'Kopie musí obsahovat skutečné obrázky všech členů.')
        require(pixels(bg) == before, 'Pozadí zachovejte beze změny.')
    elif task == 2:
        objects = [Bod((20, 30)), Bod((-10, 40)), Bod((110, 40)), Bod((30, 90))] if case else []
        group = pygame.sprite.Group(objects); extra = pygame.sprite.Group(objects); old = snapshot(objects)
        bounds = pygame.Rect(0, 0, 100, 80); saved = bounds.copy()
        expected = [o for o in objects if o.rect.right <= 0 or o.rect.left >= 100 or o.rect.bottom <= 0 or o.rect.top >= 80]
        result = fn(group, bounds)
        require(type(result) is int and result == len(expected), 'Vraťte počet plně vyřazených, dotyk hrany nemá plochu průniku.')
        require(set(group) == set(objects) - set(expected) and set(extra) == set(group), 'Kill musí vyřadit objekt ze všech skupin.')
        require(all(not o.groups() for o in expected) and bounds == saved, 'Zachovejte hranice a odstraňte všechna členství vyřazených.')
    elif task == 3:
        result = fn(group, Zvlastni)
        require(isinstance(result, pygame.sprite.Group) and result is not group, 'Vraťte novou Group.')
        require(set(result) == {o for o in objects if isinstance(o, Zvlastni)}, 'Vyberte stejné objekty včetně potomků.')
    else:
        shared = objects[:1]
        second = pygame.sprite.Group(shared + objects[1:]); before_second = set(second)
        result = fn(group, second)
        require(isinstance(result, pygame.sprite.Group) and result is not group and result is not second, 'Sjednocení vytvoří novou skupinu.')
        require(set(result) == set(objects), 'Sjednocujte identitu, nikoli polohu; nevytvářejte kopie spritů.')
        require(set(second) == before_second, 'Druhou vstupní skupinu zachovejte.')
    if task != 0:require(snapshot(objects) == old, 'Neměňte obrázky, rect ani neaktualizujte objekty mimo zadání.')
    if task != 2:require(set(group) == set(objects), 'Původní skupina má zachovat členství.')
    return True


def hits(ns, task, case):
    fn = ns[NAMES[3][task]]
    player = Bod((30 - case * 40, 40))
    x, y = player.rect.center
    objects = [Bod((x + 19, y)), Bod((x + 5, y)), Bod((x + 20, y)), Bod((x + 19, y + 19))] if case != 2 else []
    group = pygame.sprite.Group(objects); extra = pygame.sprite.Group(objects)
    player_group = pygame.sprite.Group(player)
    for i, o in enumerate(objects):o.hodnota = [7, -2, 100, 0][i]
    old = snapshot([player, *objects])
    values = [o.hodnota for o in objects]
    if task == 3:
        shots = [player, Bod((x + 25, y))]; first = pygame.sprite.Group(shots)
        expected = {}
        for shot in shots:
            matches = [o for o in objects if max(shot.rect.left, o.rect.left) < min(shot.rect.right, o.rect.right) and max(shot.rect.top, o.rect.top) < min(shot.rect.bottom, o.rect.bottom)]
            if matches:expected[shot] = matches
        result = fn(first, group)
        require(isinstance(result, dict) and set(result) == set(expected), 'Slovník obsahuje jen skutečné střely se zásahem.')
        require(all(isinstance(result[k], list) and len(result[k]) == len(v) and set(result[k]) == set(v) for k, v in expected.items()), 'Každé střele přiřaďte všechny a jen její skutečné zásahy.')
        require(set(first) == set(shots), 'Střely se zde neodstraňují.')
    else:
        if task == 4:
            player.radius = 10
            for o in objects:o.radius = 10
            expected = [o for o in objects if (o.rect.centerx - x) ** 2 + (o.rect.centery - y) ** 2 <= 400]
        else:
            expected = [o for o in objects if max(player.rect.left, o.rect.left) < min(player.rect.right, o.rect.right) and max(player.rect.top, o.rect.top) < min(player.rect.bottom, o.rect.bottom)]
        result = fn(player, group)
        if task == 1:
            require(type(result) is int and result == sum(o.hodnota for o in expected), 'Sečtěte pouze hodnoty zasažených včetně nuly a záporných.')
            require(set(group) == set(objects) - set(expected) and set(extra) == set(group), 'Chycené bonusy odstraňte ze všech skupin.')
            require(all(not o.groups() for o in expected), 'Chycené bonusy už nemají mít členství.')
        elif task == 2:
            require((result is None if not expected else any(result is o for o in expected)), 'Vraťte skutečný kolidující objekt nebo None, nikoli bool či kopii.')
        else:
            require(isinstance(result, list) and len(result) == len(expected) and set(result) == set(expected), 'Vraťte skutečné zásahy správným geometrickým pravidlem.')
    require(snapshot([player, *objects]) == old, 'Kolize nemá přepisovat polohy, obrázky nebo pohyb.')
    require(player in player_group and [o.hodnota for o in objects] == values, 'Zachovejte hráče i hodnoty bonusů.')
    if task == 4:require(player.radius == 10 and all(o.radius == 10 for o in objects), 'Poloměry se nemění.')
    if task != 1:require(set(group) == set(objects) and set(extra) == set(objects), 'Tato varianta nesmí měnit členství.')
    return True


def states(ns, task, case):
    cls = ns[NAMES[4][task]]
    require(isinstance(cls, type), 'Tato varianta procvičuje vlastní třídu se stavem a metodami.')
    key = lambda value: pygame.event.Event(pygame.KEYDOWN, key=value)
    if task == 0:
        obj, other = cls(), cls(); sprite = Bod((20, 30)); group = pygame.sprite.Group(sprite)
        require(obj.bezi is True and obj.pauza is False, 'Nový stav běží a není pozastaven.')
        obj.zpracuj(pygame.event.Event(pygame.MOUSEMOTION)); obj.zpracuj(pygame.event.Event(pygame.KEYUP, key=pygame.K_p))
        obj.update(group, .25); require(sprite.calls == [.25], 'Běžící hra aktualizuje každý objekt právě jednou.')
        obj.zpracuj(key(pygame.K_p)); obj.update(group, 2)
        require(obj.pauza is True and sprite.calls == [.25], 'Pauza zastaví update, nikoli jen kreslení.')
        require(other.pauza is False and other.bezi is True, 'Instance nesmějí sdílet stav.')
        obj.zpracuj(key(pygame.K_p)); obj.update(group, 0)
        require(sprite.calls == [.25, 0], 'Druhé P zruší pauzu; dt předejte i při nule.')
        obj.zpracuj(key(pygame.K_p)); obj.zpracuj(pygame.event.Event(pygame.QUIT)); obj.update(group, 3)
        obj.zpracuj(key(pygame.K_p)); obj.zpracuj(pygame.event.Event(pygame.QUIT))
        require(obj.bezi is False and obj.pauza is True and sprite.calls == [.25, 0], 'QUIT musí fungovat i v pauze, ukončenou hru už klávesou neobnovujte.')
    elif task == 1:
        limit = [1, 2.5, .125][case]; obj, other = cls(limit), cls(limit)
        require(obj.limit == limit and obj.zbyva == limit, 'Uložte původní limit i zbývající čas.')
        expected = limit
        for dt in [0, limit / 4, limit / 4, limit * 2, 0, limit]:
            before = expected; expected = max(0, expected - dt)
            require(obj.update(dt) is (before > 0 and expected == 0), 'Signál True patří jen přechodu na nulu.')
            require(math.isclose(obj.zbyva, expected, abs_tol=1e-12), 'Zbývající čas nesmí pod nulu.')
        obj.restart(); require(obj.zbyva == limit and other.zbyva == limit, 'Restart obnoví původní limit a nepoškodí jinou instanci.')
    elif task == 2:
        count = [1, 3, 5][case]; obj, other = cls(count), cls(count)
        require(obj.pocatecni == count and obj.zbyva == count, 'Počáteční životy se zachovávají pro restart.')
        for i in range(count + 2):
            obj.zasah(); require(obj.zbyva == max(0, count - i - 1), 'Zásah ubere jeden život, nikdy pod nulu.')
        obj.restart(); require(obj.zbyva == count and other.zbyva == count, 'Restart a nezávislé instance.')
    elif task == 3:
        obj = cls(); require(obj.stav == 'menu', 'Začínáme v menu.')
        for event, expected in [(key(pygame.K_ESCAPE), 'menu'), (key(pygame.K_RETURN), 'hra'), (key(pygame.K_RETURN), 'hra'), (key(pygame.K_ESCAPE), 'pauza'), (pygame.event.Event(pygame.KEYUP, key=pygame.K_ESCAPE), 'pauza'), (key(pygame.K_RETURN), 'pauza'), (key(pygame.K_ESCAPE), 'hra'), (pygame.event.Event(pygame.QUIT), 'konec'), (key(pygame.K_RETURN), 'konec'), (key(pygame.K_ESCAPE), 'konec')]:
            obj.zpracuj(event); require(obj.stav == expected, 'Změna režimu neodpovídá tabulce přechodů.')
    else:
        made = []
        def factory():
            group = pygame.sprite.Group(Bod((20 + len(made) * 10, 40))); made.append(group); return group
        obj = cls(factory)
        require(len(made) == 1 and obj.objekty is made[0] and obj.skore == 0, 'Konstruktor zavolá předanou funkci právě jednou a uloží její skupinu.')
        for i in range(2):
            old = obj.objekty; members = set(old); data = snapshot(list(old)); obj.skore = 9
            obj.restart()
            require(len(made) == i + 2 and obj.objekty is made[-1] and obj.objekty is not old and obj.skore == 0, 'Restart vytvoří novou skupinu přes tovární funkci a vynuluje skóre.')
            require(set(old) == members and snapshot(list(old)) == data, 'Dřívější skupinu nepoškozujte.')
    return True


def over(c, ns, stage, task):
    labels = ['Sprite, obrázek, poloha a nezávislost', 'Pohyb, desetinná pozice a čas', 'Obsah a členství skupin', 'Skutečné objekty a geometrie kolizí', 'Pravidla stavu a opakované události']
    functions = [sprites, motion, groups, hits, states]
    for case in range(3):
        ok, result = c.call({'probe': lambda: functions[stage](ns or {}, task, case)}, 'probe')
        c.add(f'{labels[stage]} ({case + 1}/3)', ok and result is True, '' if ok and result is True else f'{type(result).__name__}: {result}')
