import ast
import os
import sys
sys.path.insert(0, os.getcwd())
from balik import Balik
from doprava import Kuryr
from dilna_check import check

c = check()
c.defines_class('ExpresniKuryr')
ns = c.load()
try:
    cls = ns['ExpresniKuryr']
    c.add('Expres je kurýr', issubclass(cls, Kuryr), 'Odvoďte ExpresniKuryr z připravené třídy Kuryr.')
    node = next((node for node in c.tree.body if isinstance(node, ast.ClassDef) and node.name == 'ExpresniKuryr'), None)
    for name in ('__init__', 'cena'):
        method = next((method for method in node.body if isinstance(method, ast.FunctionDef) and method.name == name), None) if node else None
        c.add('super v metodě ' + name, bool(c.calls_in(method, 'super')) if method else False, 'V této metodě navažte pomocí super() na základní implementaci.')
    init_calls = []
    original_init = Kuryr.__init__
    def init_spy(self, adresa, limit_g=10000):
        init_calls.append((self, adresa, limit_g))
        original_init(self, adresa, limit_g)
    try:
        Kuryr.__init__ = init_spy
        first = cls('  Testovací 2  ', 'dopoledne')
        second = cls('Jiná 4', 'odpoledne', 0, 8000)
        c.add('Základní inicializace téže instance právě jednou', init_calls == [(first, '  Testovací 2  ', 5000), (second, 'Jiná 4', 8000)], 'Předejte základnímu konstruktoru adresu a skutečný limit, nevytvářejte dalšího kurýra.')
    finally:
        Kuryr.__init__ = original_init
    c.add('Výchozí i vlastní údaje', (first.adresa, first.termin, first.priplatek, first.limit_g) == ('  Testovací 2  ', 'dopoledne', 50, 5000)
          and (second.adresa, second.termin, second.priplatek, second.limit_g) == ('Jiná 4', 'odpoledne', 0, 8000), 'Zachovejte všechny parametry a samostatné hodnoty instancí.')
    for attr in ('adresa', 'termin', 'priplatek', 'limit_g'):
        before = getattr(first, attr)
        ok, error = c.call({'write': setattr}, 'write', (first, attr, 'změna'))
        c.add('Údaje expresu jsou pouze pro čtení', not ok and isinstance(error, AttributeError) and getattr(first, attr) == before, 'Zachovejte připravené a zděděné property.')
    for args in [('', 'dopoledne'), (' \t', 'dopoledne'), (None, 'dopoledne'), (9, 'dopoledne'),
                 ('A', ''), ('A', 'večer'), ('A', 'Dopoledne'), ('A', None), ('A', ['dopoledne'])]:
        c.raises({'ctor': cls}, 'ctor', args, ValueError)
    for fee in (-1, True, 1.5, '50', None):
        c.raises({'ctor': cls}, 'ctor', ('A', 'dopoledne', fee), ValueError)
    for limit in (0, -1, True, 1.5, '5000', None):
        c.raises({'ctor': cls}, 'ctor', ('A', 'odpoledne', 50, limit), ValueError)
    for obj in (first, second, cls('Třetí', 'dopoledne', 75, 12000)):
        for weight in (1, 5000, 5001, 8000, 8001, 12000, 12001):
            parcel = Balik('E', weight)
            before = (dict(vars(obj)), dict(vars(parcel)))
            ok, value = c.call({'cena': obj.cena}, 'cena', (parcel,))
            expected = (99 if weight <= 5000 else 149) + obj.priplatek
            correct = ok and type(value) is int and value == expected if weight <= obj.limit_g else not ok and isinstance(value, ValueError)
            c.add('Cena rozšiřuje základ a zachová omezení', correct and before == (vars(obj), vars(parcel)) and c.last_output == '', 'Použijte základní cenu s aktuálním limitem a přičtěte příplatek.')
    original_price = Kuryr.cena
    calls = []
    parcel = Balik('SPY', 200)
    def price_spy(self, balik):
        calls.append((self, balik))
        return 237
    try:
        Kuryr.cena = price_spy
        ok, value = c.call({'cena': first.cena}, 'cena', (parcel,))
        c.add('Výsledek skutečného základního volání se použije', ok and value == 287 and calls == [(first, parcel)] and c.last_output == '', 'Navazujte právě jednou na základní metodu této instance, základní část ceny neopisujte.')
        def refuse(self, balik):
            raise ValueError('Odmítnutí základní dopravou')
        Kuryr.cena = refuse
        c.raises({'cena': first.cena}, 'cena', (parcel,), ValueError)
    finally:
        Kuryr.cena = original_price
except BaseException as exc:
    c.add('Expres lze ověřit', False, f'{type(exc).__name__}: {exc}')
r = c.run()
if c.no_error(r):
    for text in ('Termín: dopoledne', 'Cena expresu: 149', 'Expresní limit zůstal v platnosti.'):
        c.output_contains(r, text)
c.done()
