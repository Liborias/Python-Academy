import os
import sys
sys.path.insert(0, os.getcwd())
from balik import Balik
from dilna_check import check

c = check()
for name in ('Doprava', 'OsobniOdber', 'Kuryr'):
    c.defines_class(name)
ns = c.load()
try:
    base, pickup, courier = (ns[name] for name in ('Doprava', 'OsobniOdber', 'Kuryr'))
    c.add('Dopravy přepisují společnou metodu', issubclass(pickup, base) and issubclass(courier, base), 'Obě konkrétní třídy dědí z Doprava.')
    c.raises({'cena': base().cena}, 'cena', (Balik('B', 1),), NotImplementedError)
    for cls in (pickup, courier):
        for text in ('', ' \t ', None, 7):
            ok, error = c.call({'ctor': cls}, 'ctor', (text,))
            c.add('Místo či adresa musí obsahovat text', not ok and isinstance(error, ValueError), 'Odmítněte prázdný text, mezery i jiné typy.')
    for limit in (0, -1, True, 1.5, '10000', None):
        c.raises({'ctor': courier}, 'ctor', ('Ulice 9', limit), ValueError)
    a, b = pickup('  Dílna Žďár  '), courier('  Ulice 9  ')
    c.add('Původní údaje a výchozí limit', a.misto == '  Dílna Žďár  ' and b.adresa == '  Ulice 9  ' and b.limit_g == 10000, 'Kontrola textu nemění jeho uloženou podobu; výchozí limit je 10000 g.')
    for obj, attr in ((a, 'misto'), (b, 'adresa'), (b, 'limit_g')):
        before = getattr(obj, attr)
        ok, error = c.call({'write': setattr}, 'write', (obj, attr, 'přepsáno'))
        c.add('Údaje jsou pouze pro čtení', not ok and isinstance(error, AttributeError) and getattr(obj, attr) == before, 'Použijte připravené property.')
    for obj, limit in ((b, 10000), (courier('Jiná 2', 3000), 3000), (courier('Těžká 3', 14000), 14000)):
        for weight in (1, 3000, 3001, 5000, 5001, 10000, 10001, 14000):
            parcel = Balik('K-8', weight)
            before = (dict(vars(obj)), dict(vars(parcel)))
            ok, result = c.call({'cena': obj.cena}, 'cena', (parcel,))
            expected = 99 if weight <= 5000 else 149
            correct = ok and type(result) is int and result == expected if weight <= limit else not ok and isinstance(result, ValueError)
            c.add('Cena respektuje pásmo i konkrétní limit', correct and before == (vars(obj), vars(parcel)) and c.last_output == '', 'Nejprve odmítněte hmotnost nad limit; pak vraťte 99 nebo 149 Kč bez změny stavu.')
    parcel = Balik('TĚŽKÝ', 99999)
    before = (dict(vars(a)), dict(vars(parcel)))
    ok, value = c.call({'cena': a.cena}, 'cena', (parcel,))
    c.add('Osobní odběr nemá limit ani poplatek', ok and type(value) is int and value == 0 and before == (vars(a), vars(parcel)) and c.last_output == '', 'Odběr vrací nulu i pro těžký balík.')
    # Tyto možnosti mají pouze společné veřejné rozhraní, ne společného předka.
    class Nabidka:
        def __init__(self, castka):
            self.castka = castka
        def cena(self, balik):
            calls.append((self, balik))
            return self.castka
    x, y = Nabidka(37), Nabidka(82)
    calls = []
    parcel = Balik('V-3', 720)
    for options, expected in (([x, y, x], [37, 82, 37]), ([y, x], [82, 37]), ([], []), ([b, a], [99, 0])):
        before = list(options)
        calls.clear()
        ok, value = c.call(ns, 'ceny_dopravy', (options, parcel))
        c.add('Polymorfní výpočet zachová pořadí i opakování', ok and isinstance(value, list) and value == expected and value is not options and options == before and c.last_output == '', 'Vraťte seznam výsledků cena v pořadí vstupu, bez větvení podle typu.')
        if all(isinstance(obj, Nabidka) for obj in options):
            c.add('Každá možnost oceňuje tentýž balík', calls == [(obj, parcel) for obj in options], 'Volejte cenu každého předaného objektu se stejným balíkem právě jednou.')
    c.raises(ns, 'ceny_dopravy', ([a, b], Balik('LIMIT', 10001)), ValueError)
except BaseException as exc:
    c.add('Dopravy lze ověřit', False, f'{type(exc).__name__}: {exc}')
r = c.run()
if c.no_error(r):
    for text in ('Lehký balík: [0, 99]', 'Těžší balík: [0, 149]', 'Nadlimitní balík kurýr odmítl.'):
        c.output_contains(r, text)
c.done()
