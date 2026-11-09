"""Kontroly navazující hry: reálný pygame model a skutečná SDL smyčka."""
import math
import os
import random
from pathlib import Path
import struct
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import pygame


def require(ok, message):
    if not ok:raise AssertionError(message)


def near(actual, expected):
    return len(actual) == len(expected) and all(math.isclose(a, b, abs_tol=1e-9, rel_tol=1e-9) for a, b in zip(actual, expected))


class Keys:
    def __init__(self, *pressed):self.pressed = set(pressed)
    def __getitem__(self, key):return key in self.pressed


class Rng:
    """Kontrolovaný zdroj, který současně ověřuje interval každého losování."""
    def __init__(self):self.calls = []
    def randint(self, low, high):
        require(low <= high, 'Neplatné meze losování.')
        self.calls.append((low, high))
        return low if len(self.calls) % 2 else high


def ship(ns):
    cls = ns['Hrac']
    require(isinstance(cls, type) and issubclass(cls, pygame.sprite.Sprite), 'Hrac musí být skutečná třída Sprite.')
    for keys, expected in [(Keys(), (0, 0)), (Keys(pygame.K_LEFT), (-1, 0)), (Keys(pygame.K_RIGHT, pygame.K_UP), (1, -1)), (Keys(pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN), (0, 0))]:
        direction = ns['precti_smer'](keys)
        require(isinstance(direction, pygame.Vector2) and tuple(direction) == expected, 'Přečtěte čtyři šipky, protější směry se ruší.')
    for start, vector, speed, steps in [((320, 420), (3, -4), 240, [0, .25, .25]), ((100.25, 120.75), (1, 0), 1, [.01] * 100), ((320, 420), (-1, 1), 240, [5]), ((320,420),(1,-1),240,[5]), ((320, 420), (0, 0), 240, [3])]:
        source = pygame.Vector2(start); bounds = pygame.Rect(20, 70, 600, 390); direction = pygame.Vector2(vector)
        before = tuple(source), tuple(bounds), tuple(direction)
        obj, other = cls(source, bounds), cls(source, bounds)
        require(obj.radius == 14 and obj.image.get_size() == (40, 32) and isinstance(obj.rect, pygame.Rect), 'Použijte dodaný obrázek 40×32 a radius 14.')
        require(obj.pozice is not source and obj.hranice is not bounds and isinstance(obj.pozice, pygame.Vector2), 'Vektor a hranice potřebují vlastní kopie.')
        require(obj.rychlost == 240, 'Výchozí rychlost je 240 px/s.')
        obj.rychlost = speed; position = list(start); length = math.hypot(*vector)
        for dt in steps:
            if length:position = [p + v / length * speed * dt for p, v in zip(position, vector)]
            position = [max(40, min(600, position[0])), max(86, min(444, position[1]))]
            obj.update(direction, dt)
            require(near(obj.pozice, position) and obj.rect.center == tuple(round(p) for p in position), 'Normalizujte směr, použijte rychlost × dt a uchovejte desetinnou pozici; celá loď zůstane uvnitř.')
        require(near(other.pozice, start), 'Instance nesmějí sdílet polohu.')
        require((tuple(source), tuple(bounds), tuple(direction)) == before, 'Neměňte vstupní vektory ani hranice.')
    for bounds in [pygame.Rect(0,0,80,64),pygame.Rect(-100,-80,80,64)]:
        obj=cls(bounds.center,bounds);obj.update((1,1),1)
        require(near(obj.pozice,(bounds.right-20,bounds.bottom-16)) and bounds.contains(obj.rect), 'Respektujte skutečně předané hranice, ne pevnou velikost okna.')
    return True


def stream(ns):
    Meteor, Stream = ns['Meteorit'], ns['ProudMeteoritu']
    require(isinstance(Meteor, type) and issubclass(Meteor, pygame.sprite.Sprite) and isinstance(Stream, type), 'Meteorit je Sprite, ProudMeteoritu samostatná třída se skupinou.')
    source = pygame.Vector2(101.25, -15.3)
    rock = Meteor(source, 13, 1)
    require(rock.radius == 13 and rock.image.get_size() == (26, 26) and rock.pozice is not source, 'Uložte poloměr, správný obraz a vlastní přesnou pozici.')
    for _ in range(100):rock.update(.01)
    require(near(rock.pozice, (101.25, -14.3)) and rock.rect.center == (round(101.25), round(-14.3)), 'Neztrácejte malé kroky pádu ani původní x.')
    require(tuple(source) == (101.25, -15.3), 'Pád nesmí změnit předaný vektor.')
    fast = Meteor((20, 10.25), 13, 80); fast.update(.25)
    require(near(fast.pozice, (20, 30.25)), 'Použijte předanou rychlost, nejen samotné dt.')
    for bounds in [pygame.Rect(20, 70, 600, 390), pygame.Rect(-80, -30, 160, 90)]:
        rng = Rng(); obj = Stream(rng, .5); other = Stream(Rng(), .5)
        require(obj.rng is rng and obj.cas == 0 and obj.minulo == 0 and isinstance(obj.objekty, pygame.sprite.Group) and not obj.objekty, 'Proud začíná s prázdnou vlastní skupinou a nulovými čítači.')
        r = obj.vytvor(bounds)
        require(isinstance(r, Meteor) and r in obj.objekty and len(obj.objekty) == 1, 'Vytvor musí vrátit a přidat tentýž nový meteorit.')
        require(rng.calls == [(12, 26), (bounds.left + 12, bounds.right - 12), (90, 160)], 'Losujte poloměr, potom dosažitelný střed x a rychlost přes předaný randint.')
        require(r.radius == 12 and r.rect.bottom == bounds.top and r.rect.centerx == bounds.right - 12 and r.rychlost == 90, 'Nový kámen má být celý nad plochou, v jejích vodorovných mezích.')
        require(not other.objekty, 'Proudy nesmějí sdílet skupinu.')
        obj.objekty.empty(); rng.calls.clear()
        # Za dva kroky vzniknou tři kameny. Nové kameny se v témž kroku nepohnou.
        obj.update(.25, bounds); require(not obj.objekty and obj.cas == .25, 'Zachovejte zbytek času, před intervalem nevytvářejte.')
        obj.update(1.5, bounds)
        require(len(obj.objekty) == 3 and math.isclose(obj.cas, .25), 'Dohánějte všechny celé intervaly a ponechte zbytek, nestačí jediné if.')
        require(all(r.rect.bottom == bounds.top for r in obj.objekty), 'Nové kameny se aktualizují až v příštím kroku.')
        before_positions = [(r, tuple(r.pozice), r.rychlost) for r in obj.objekty]
        obj.update(.125, bounds)
        require(len(obj.objekty) == 3 and all(near(r.pozice, (p[0], p[1] + speed * .125)) for r, p, speed in before_positions), 'Proud musí v dalším kroku skutečně aktualizovat existující kameny.')
        obj.objekty.empty()
        out = Meteor((bounds.centerx, bounds.bottom + 12), 12, 0)
        edge = Meteor((bounds.centerx, bounds.bottom + 11), 12, 0)
        obj.objekty.add(out, edge); extra = pygame.sprite.Group(out, edge)
        saved = tuple(bounds); obj.update(0, bounds)
        require(obj.minulo == 1 and out not in obj.objekty and not out.groups() and edge in obj.objekty and edge in extra, 'Kámen s top >= bottom už minul plochu. Vyřaďte jej ze všech skupin právě jednou.')
        obj.update(0, bounds); require(obj.minulo == 1 and tuple(bounds) == saved, 'Jeden průlet počítejte jen jednou a neměňte hranice.')
        edge.pozice.y = bounds.bottom + edge.radius
        obj.update(0, bounds); require(obj.minulo == 2 and not edge.groups(), 'Průlety se sčítají i v dalších krocích.')
    for interval in [0, -1]:
        try:Stream(Rng(), interval)
        except ValueError:pass
        else:require(False, 'Nekladný interval odmítněte ValueError.')
    return True


def health(ns):
    cls = ns['Zdravi']; require(isinstance(cls, type), 'Zdravi je vlastní třída.')
    obj, other = cls(3, .75), cls(3, .75)
    require(obj.zivoty == 3 and obj.ochrana == .75 and obj.nezranitelnost == 0, 'Uložte životy, délku ochrany a nulový počáteční odpočet.')
    require(obj.zasah() is True and obj.zivoty == 2 and obj.nezranitelnost == .75, 'První zásah ubere jeden život a zapne ochranu.')
    require(obj.zasah() is False and obj.zivoty == 2, 'Ochrana brání opakované ztrátě života.')
    obj.tick(.25); require(obj.nezranitelnost == .5, 'Tick odečítá sekundy, nikoli snímky.')
    require(obj.zasah() is False and obj.nezranitelnost == .5, 'Odmítnutý zásah nesmí odpočet prodloužit.')
    obj.tick(2); require(obj.nezranitelnost == 0, 'Odpočet nesmí pod nulu.')
    require(obj.zasah() is True and obj.zivoty == 1, 'Po vypršení ochrany lze znovu přijmout zásah.')
    obj.tick(1); require(obj.zasah() is True and obj.zivoty == 0, 'Poslední život lze odečíst.')
    obj.tick(4); require(obj.zasah() is False and obj.zivoty == 0, 'Životy nesmějí pod nulu.')
    require(other.zivoty == 3 and other.nezranitelnost == 0, 'Nezávislý zdravotní stav.')
    player = ns['Hrac']((200, 200), ns['HRANICE'])
    proud = ns['ProudMeteoritu'](Rng())
    obj = cls()
    require(ns['zpracuj_zasahy'](player, proud, obj) is False and obj.zivoty == 3, 'Bez kolize se život neodečítá.')
    hits = [ns['Meteorit']((200, 200), 20, 0), ns['Meteorit']((234, 200), 20, 0)]
    miss = ns['Meteorit']((300, 200), 20, 0)
    diagonal = ns['Meteorit']((230, 230), 20, 0)
    proud.objekty.add(*hits, miss, diagonal); extra = pygame.sprite.Group(*hits, miss, diagonal)
    require(ns['zpracuj_zasahy'](player, proud, obj) is True and obj.zivoty == 2, 'Jedna dávka kolizí ubere nejvýše jeden život; dotyk kruhů se počítá.')
    require(set(proud.objekty) == {miss,diagonal} and set(extra) == {miss,diagonal} and all(not h.groups() for h in hits), 'Použijte kruhy, odstraňte všechny zasažené a nezasažené ponechte.')
    proud.objekty.add(ns['Meteorit']((200, 200), 20, 0))
    require(ns['zpracuj_zasahy'](player, proud, obj) is False and obj.zivoty == 2 and set(proud.objekty) == {miss,diagonal}, 'I během ochrany odstraňte zasažené, ale neodečítejte život.')
    return True


class QuietStream:
    def __init__(self):self.objekty = pygame.sprite.Group(); self.minulo = 7; self.calls = []
    def update(self, dt, bounds):self.calls.append((dt, tuple(bounds)))


def round_model(ns):
    cls = ns['Kolo']; require(isinstance(cls, type), 'Kolo je vlastní třída skládající herní objekty.')
    obj, other = cls(17), cls(17)
    require(isinstance(obj.hrac, ns['Hrac']) and isinstance(obj.proud, ns['ProudMeteoritu']) and isinstance(obj.zdravi, ns['Zdravi']), 'Sestavte hráče, proud a zdraví z předchozích ověřených částí.')
    require(obj.hrac.rect.center == (320, 420) and obj.zdravi.zivoty == 3 and obj.skore == 0 and obj.stit is False and obj.bonus_cas == 0 and not obj.bonusy, 'Čistý začátek kola.')
    require(obj.hranice is not ns['HRANICE'] and obj.proud.objekty is not other.proud.objekty and obj.bonusy is not other.bonusy, 'Kola nesmějí sdílet proměnlivý svět.')
    require(not obj.proud.objekty and isinstance(obj.proud.rng,random.Random) and obj.proud.rng.getstate() == random.Random(17).getstate(), 'Prázdný proud musí dostat vlastní generátor se skutečně předaným seedem.')
    a, b = obj.proud.vytvor(obj.hranice), other.proud.vytvor(other.hranice)
    require((a.radius, a.rect.center, a.rychlost) == (b.radius, b.rect.center, b.rychlost), 'Seed se musí dostat do vlastního generátoru proudu.')
    obj.proud = QuietStream()
    obj.update((0, 0), 0)
    require(obj.skore == 7 and obj.proud.calls == [(0, tuple(obj.hranice))], 'Skóre přebírá počet minutých kamenů a dt předává proudu.')
    obj.update((0, 0), 0); require(obj.skore == 7, 'Stejný počet průletů se nepřičítá znovu za každý snímek.')
    meteor = ns['Meteorit'](obj.hrac.rect.center, 20, 0)
    bonus = ns['BonusStitu'](obj.hrac.rect.center)
    obj.proud.objekty.add(meteor); obj.bonusy.add(bonus); extra = pygame.sprite.Group(meteor, bonus)
    obj.update((0, 0), 0)
    require(obj.zdravi.zivoty == 3 and obj.stit is False and obj.zdravi.nezranitelnost == obj.zdravi.ochrana, 'Bonus se sbírá před zásahem; štít pohltí dávku a zapne ochranu.')
    require(not extra and not obj.bonusy and not obj.proud.objekty and obj.proud.minulo == 7, 'Zásah není minutý kámen ani bod, odstranění platí pro všechna členství.')
    obj.stit = True; obj.proud.objekty.add(ns['Meteorit'](obj.hrac.rect.center, 20, 0))
    obj.update((0, 0), .25)
    require(obj.stit is True and obj.zdravi.zivoty == 3 and obj.zdravi.nezranitelnost == .75, 'Během nezranitelnosti se štít nespotřebuje ani odpočet neprodlouží.')
    obj.stit = False; obj.zdravi.nezranitelnost = .125
    obj.proud.objekty.add(ns['Meteorit'](obj.hrac.rect.center, 20, 0)); obj.update((0, 0), .125)
    require(obj.zdravi.zivoty == 2, 'Nejprve aktualizujte odpočet, pak vyhodnoťte nové zásahy.')
    obj = cls(); obj.proud = QuietStream(); obj.update((0, 0), 12)
    require(len(obj.bonusy) == 2 and obj.bonus_cas == 0, 'Za 12 sekund vytvořte dva bonusy; nově vytvořené se v témž kroku nepohnou.')
    require(all(isinstance(b, ns['BonusStitu']) and b.rect.center == (obj.hranice.centerx, obj.hranice.top - 12) for b in obj.bonusy), 'Bonus vzniká každých 6 sekund nad středem plochy.')
    obj.update((0,0),.25)
    require(len(obj.bonusy)==2 and all(b.rect.centery==obj.hranice.top+8 for b in obj.bonusy), 'Existující bonusy musejí v dalším kroku padat rychlostí 80 px/s.')
    out = ns['BonusStitu']((obj.hranice.centerx,obj.hranice.bottom+12)); obj.bonusy.add(out); extra=pygame.sprite.Group(out)
    obj.update((0,0),0); require(not out.groups() and not extra, 'Bonusy mimo plochu odstraňujte ze všech skupin.')
    obj.zdravi.zivoty = 0; before = tuple(obj.hrac.pozice), obj.skore, obj.bonus_cas, len(obj.proud.calls), [tuple(b.rect) for b in obj.bonusy]
    obj.update((1, 0), 9)
    require((tuple(obj.hrac.pozice), obj.skore, obj.bonus_cas, len(obj.proud.calls), [tuple(b.rect) for b in obj.bonusy]) == before, 'Konec kola zmrazí čas, objekty, skóre i bonusy.')
    return True


def game(ns):
    cls = ns['Hra']; require(isinstance(cls, type), 'Hra je vlastní třída.')
    obj = cls(17); other = cls(17)
    require(obj.bezi is True and obj.pauza is False and obj.restart_povolen is True and obj.seed == 17 and isinstance(obj.kolo, ns['Kolo']), 'Vytvořte běžící hru s vlastním kolem, seedem a povoleným restartem.')
    key = lambda k:pygame.event.Event(pygame.KEYDOWN, key=k)
    start = tuple(obj.kolo.hrac.pozice)
    obj.zpracuj(pygame.event.Event(pygame.USEREVENT)); obj.zpracuj(pygame.event.Event(pygame.KEYUP, key=pygame.K_p))
    obj.update((1, 0), .125)
    require(near(obj.kolo.hrac.pozice, (start[0] + 30, start[1])), 'Běžící hra předá vstup a čas do kola právě jednou.')
    obj.zpracuj(key(pygame.K_p)); frozen = tuple(obj.kolo.hrac.pozice), obj.kolo.proud.cas, obj.kolo.bonus_cas
    obj.update((1, 0), 2)
    require(obj.pauza is True and (tuple(obj.kolo.hrac.pozice), obj.kolo.proud.cas, obj.kolo.bonus_cas) == frozen and other.pauza is False, 'Pauza zmrazí herní čas a neovlivní jinou instanci.')
    obj.zpracuj(key(pygame.K_p)); require(obj.pauza is False, 'Druhé P zruší pauzu.')
    old = obj.kolo; old.skore = 19
    old.proud.vytvor(old.hranice); old.bonusy.add(ns['BonusStitu']((320,100)))
    old_groups = set(old.proud.objekty), set(old.bonusy)
    obj.zpracuj(key(pygame.K_p)); obj.zpracuj(key(pygame.K_r))
    require(obj.kolo is not old and obj.pauza is False and obj.kolo.skore == 0 and obj.kolo.zdravi.zivoty == 3 and obj.kolo.stit is False, 'R vytvoří čisté nové kolo a zruší pauzu.')
    require(old.skore == 19 and near(old.hrac.pozice, (start[0] + 30, start[1])), 'Starý svět se při restartu nesmí přepsat ani vyprázdnit.')
    require((set(old.proud.objekty),set(old.bonusy)) == old_groups, 'Restart nesmí vyprazdňovat staré skupiny.')
    initial = obj.kolo.proud.vytvor(obj.kolo.hranice)
    signature = initial.radius, initial.rect.center, initial.rychlost
    obj.zpracuj(key(pygame.K_r)); repeated = obj.kolo.proud.vytvor(obj.kolo.hranice)
    require((repeated.radius, repeated.rect.center, repeated.rychlost) == signature, 'Restart s týmž seedem zopakuje začátek náhodné posloupnosti.')
    obj.kolo.zdravi.zivoty = 0; obj.zpracuj(key(pygame.K_p)); require(obj.pauza is False, 'Po konci kola už P nezapíná pauzu.')
    before = tuple(obj.kolo.hrac.pozice); obj.update((1, 0), 1); require(tuple(obj.kolo.hrac.pozice) == before, 'Po konci kola se svět nehýbe.')
    obj.zpracuj(key(pygame.K_r)); require(obj.kolo.zdravi.zivoty == 3, 'R funguje také po ztrátě posledního života.')
    obj.zpracuj(key(pygame.K_p)); obj.zpracuj(pygame.event.Event(pygame.QUIT))
    last = obj.kolo; before = tuple(last.hrac.pozice); obj.update((1, 0), 1); obj.zpracuj(key(pygame.K_r)); obj.zpracuj(pygame.event.Event(pygame.QUIT))
    require(obj.bezi is False and obj.kolo is last and tuple(last.hrac.pozice) == before, 'QUIT funguje i v pauze; ukončenou hru R ani update neobnoví.')
    obj = cls(); obj.zpracuj(key(pygame.K_ESCAPE)); require(obj.bezi is False, 'Escape ukončí hru.')
    return True


def over(c, ns, stage):
    operation = [ship, stream, health, round_model, game][stage]
    ok, result = c.call({'probe':lambda:operation(ns or {})}, 'probe')
    c.add('Pravidla nové části projektu', ok and result is True, '' if ok and result is True else f'{type(result).__name__}: {result}')
    c.add('Model se načítá bez herního okna', pygame.display.get_surface() is None, 'Okno a smyčku spouštějte až v bloku __main__.')
    # Stejná řešení musí skutečně řídit loď a vykreslit dodané herní okno.
    r = c.pygame_run(frames=8, pixels=[(351, 420)], held={0:['K_RIGHT']})
    if c.pg_no_error(r):
        c.add('Skutečná herní smyčka a ovládání', r.size == [640,480] and 'Meteority' in (r.caption or '') and r.frames == 8 and r.pixel((351,420)) == (80,180,255), 'Program má zobrazit Meteority 640×480 a řídit viditelnou loď podle šipek a dt.')
        c.add('Omezená frekvence smyčky', bool(r.fps) and all(v == 60 for v in r.fps), 'Použijte společnou smyčku s Clock.tick(60).')
    events = {3:[{'type':'QUIT'}]}
    if stage == 4:events = {1:[{'type':'KEYDOWN','key':'K_p'}], 3:[{'type':'QUIT'}]}
    r = c.pygame_run(frames=20, events=events)
    if c.pg_no_error(r):
        c.add('Okno reaguje na zavření', r.ended and r.frames < 20, 'QUIT musí ukončit smyčku také v pauze.')
        path = Path('meteority.png')
        data = path.read_bytes() if path.is_file() else b''
        c.add('Poslední skutečný snímek', data.startswith(b'\x89PNG\r\n\x1a\n') and len(data)>24 and struct.unpack('>II',data[16:24]) == (640,480), 'Při zavření zachovejte poslední snímek přes společnou smyčku.')
