import os
import sys
sys.path.insert(0, os.getcwd())
from balik import Balik
from doprava import OsobniOdber, Kuryr
from expres import ExpresniKuryr
from dilna_check import check

c = check()
c.defines_class('Expedice')
ns = c.load()
try:
    cls = ns['Expedice']
    parcel = Balik('ŽK', 1200)
    pickup, courier, express = OsobniOdber('Dílna'), Kuryr('Javorová 1'), ExpresniKuryr('Javorová 1', 'odpoledne')
    originals = [(obj, dict(vars(obj))) for obj in (parcel, pickup, courier, express)]
    ok, e = c.call({'ctor': cls}, 'ctor', (parcel, pickup))
    c.add('Expedice si ponechá původní objekty', ok and e.balik is parcel and e.doprava is pickup and c.last_output == '', 'Uchovejte odkazy na předaný balík a ověřenou dopravu.')
    for attr in ('balik', 'doprava'):
        before = getattr(e, attr)
        ok, error = c.call({'write': setattr}, 'write', (e, attr, None))
        c.add('Odkazy jsou pouze pro čtení', not ok and isinstance(error, AttributeError) and getattr(e, attr) is before, 'Změna dopravy patří metodě s ověřením.')
    second_parcel = Balik('JINÝ', 7200)
    second = cls(second_parcel, courier)
    for chosen, price in ((courier, 99), (express, 149), (pickup, 0), (courier, 99)):
        ok, value = c.call({'change': e.zmen_dopravu}, 'change', (chosen,))
        quiet = c.last_output == ''
        ok_quote, quote = c.call({'quote': e.nabidka}, 'quote')
        c.add('Změna přepne dopravu a vrátí novou cenu', ok and value == price and e.doprava is chosen and e.balik is parcel and ok_quote and quote == price and quiet and c.last_output == '', 'Ověřte novou dopravu a pak uložte tentýž objekt; nabídku přepošlete aktuální dopravě.')
        c.add('Dvě expedice se neovlivní', second.balik is second_parcel and second.doprava is courier and second.nabidka() == 149, 'Každá expedice si uchová vlastní volbu a balík.')
    for invalid in (Kuryr('Nízký limit', 1000), ExpresniKuryr('Nízký limit', 'dopoledne', 50, 1000)):
        before = (e.balik, e.doprava, e.nabidka(), dict(vars(invalid)))
        ok, error = c.call({'change': e.zmen_dopravu}, 'change', (invalid,))
        c.add('Odmítnutí zachová původní volbu', not ok and isinstance(error, ValueError) and (e.balik, e.doprava, e.nabidka(), vars(invalid)) == before and c.last_output == '', 'Novou dopravu uložte až po úspěšném výpočtu ceny.')
        c.raises({'ctor': cls}, 'ctor', (parcel, invalid), ValueError)
    # Záměrně jiné vnitřní údaje, žádný společný předek dopravy.
    class VlastniDoprava:
        def __init__(self, castka):
            self.castka = castka
        def cena(self, balik):
            calls.append((self, balik))
            if self.castka < 0:
                raise ValueError('Odmítnuto')
            return self.castka
    own = VlastniDoprava(59)
    calls = []
    fresh = cls(parcel, own)
    c.add('Konstruktor ověří nabídku přes veřejné rozhraní', calls == [(own, parcel)] and fresh.balik is parcel and fresh.doprava is own, 'Před úspěšným vytvořením ověřte cenu daného balíku právě jednou.')
    own.castka = 83
    calls.clear()
    ok, value = c.call({'quote': fresh.nabidka}, 'quote')
    c.add('Nabídka se zjišťuje znovu', ok and value == 83 and calls == [(own, parcel)] and c.last_output == '', 'Volejte aktuální cena, nepoužívejte uloženou starou cenu.')
    own.castka = 71
    calls.clear()
    ok, value = c.call({'change': e.zmen_dopravu}, 'change', (own,))
    c.add('Nová doprava funguje bez změny Expedice', ok and value == 71 and e.doprava is own and calls == [(own, parcel)] and c.last_output == '', 'Použijte společné rozhraní; nevyžadujte konkrétní třídy ani jejich vnitřní atributy.')
    bad = VlastniDoprava(-1)
    calls.clear()
    ok, error = c.call({'change': e.zmen_dopravu}, 'change', (bad,))
    c.add('I nová doprava může odmítnout beze změn', not ok and isinstance(error, ValueError) and e.doprava is own and e.balik is parcel and e.nabidka() == 71, 'Ponechte původní volbu a předejte výjimku volajícímu.')
    calls.clear()
    c.raises({'ctor': cls}, 'ctor', (parcel, bad), ValueError)
    c.add('Konstruktor použije i odmítající rozhraní', calls == [(bad, parcel)], 'Kontrola nemá záviset na názvu třídy dopravy.')
    c.add('Nabídky a přepnutí nemění balíky ani dopravy', all(vars(obj) == before for obj, before in originals), 'Používejte dotaz cena; rezervace ani změny přepravních údajů sem nepatří.')
except BaseException as exc:
    c.add('Expedici lze ověřit', False, f'{type(exc).__name__}: {exc}')
r = c.run()
if c.no_error(r):
    for text in ('Osobní odběr: 0', 'Kurýr: 99', 'Expres: 149', 'Volba odmítnuta, cena zůstává: 149'):
        c.output_contains(r, text)
c.done()
