import os
import sys
sys.path.insert(0, os.getcwd())
import sklad
from skladova_karta import SkladovaKarta
from nakupni_objednavka import NakupniObjednavka
from dilna_check import check

c = check()
c.defines_class('RezervacniSklad')
made, calls = [], []
class VerejnaKarta:
    def __init__(self, nazev, celkem=0):
        self._model = SkladovaKarta(nazev, celkem)
        made.append(self)
    @property
    def dostupne(self):
        return self._model.dostupne
    def rezervuj(self, pocet):
        calls.append(('rezervuj', self, pocet))
        return self._model.rezervuj(pocet)
    def uvolni(self, pocet):
        calls.append(('uvolni', self, pocet))
        return self._model.uvolni(pocet)
original_card = sklad.SkladovaKarta
sklad.SkladovaKarta = VerejnaKarta
ns = c.load()
def order(code, request):
    value = NakupniObjednavka(code)
    for key, count in request.items():
        value.pridej(key, key, 10, count)
    return value
try:
    cls = ns['RezervacniSklad']
    c.add('Rozšíření původního skladu', issubclass(cls, sklad.Sklad), 'Odvoďte třídu z původního Sklad.')
    store = cls()
    store.pridej('K', 'Kniha', 8)
    store.pridej('O', 'Obal', 2)
    store.rezervuj({'K': 1})  # Anonymní rezervace se při stornu nesmí uvolnit.
    a, b = order('A', {'K': 3, 'O': 1}), order('B', {'K': 2, 'O': 1})
    for item, expected in [(a, {'K': 4, 'O': 1}), (b, {'K': 2, 'O': 0})]:
        ok, value = c.call({'reserve': store.rezervuj_objednavku}, 'reserve', (item,))
        c.add('Úplná rezervace uzavře příslušný nákup', ok and value == expected and store.prehled() == expected and item.uzavrena and store.stav(item.cislo) == 'rezervovana' and c.last_output == '', 'Využijte základní rezervaci, teprve po úspěchu nákup uzavřete a zaevidujte.')
        value['K'] = 999
        c.add('Vrácený přehled je kopie', store.prehled() == expected, 'Nesdílejte interní přehled.')
    bad = [order('C', {'K': 1, 'O': 1}), order('C', {'K': 1, 'CHYBÍ': 1}), order('A', {'K': 1}), a, order('PRÁZDNÁ', {})]
    closed = order('UZAVŘENÁ', {'K': 1}); closed.uzavri(); bad.append(closed)
    for item in bad:
        before, was_closed = store.prehled(), item.uzavrena
        calls.clear()
        ok, error = c.call({'reserve': store.rezervuj_objednavku}, 'reserve', (item,))
        c.add('Odmítnutí nemění sklad ani nákup', not ok and isinstance(error, ValueError) and store.prehled() == before and item.uzavrena == was_closed and not calls, 'Ověřte identitu, otevření a celý požadavek před rezervací.')
    c.raises({'state': store.stav}, 'state', ('C',), ValueError)
    calls.clear()
    ok, value = c.call({'cancel': store.storno}, 'cancel', ('A',))
    c.add('Storno uvolní jen vlastní kusy přes karty', ok and value == {'K': 5, 'O': 1} and store.stav('A') == 'stornovana' and store.stav('B') == 'rezervovana'
          and sorted((kind, count) for kind, _, count in calls) == [('uvolni', 1), ('uvolni', 3)] and a.uzavrena and c.last_output == '', 'Uvolněte uložené počty A, rezervaci B i anonymní ponechte.')
    for code in ('A', 'NEZNÁMÁ'):
        before = store.prehled(); calls.clear()
        c.raises({'cancel': store.storno}, 'cancel', (code,), ValueError)
        c.add('Další storno nic neuvolní', store.prehled() == before and not calls, 'Stav ověřte před prvním uvolněním.')
    c.raises({'reserve': store.rezervuj_objednavku}, 'reserve', (order('A', {'K': 1}),), ValueError)
    ok, value = c.call({'cancel': store.storno}, 'cancel', ('B',))
    c.add('I po obou stornech zůstává anonymní rezervace', ok and value == {'K': 7, 'O': 2}, 'Nepřepisujte rezervované počty na nulu.')
    c.add('Fyzický počet se nemění', [card._model.celkem for card in made] == [8, 2], 'Rezervace a storno mění rezervované množství, nikoli fyzický celkový počet.')
    other = cls(); other.pridej('K', 'Jiná', 9)
    other.rezervuj_objednavku(order('A', {'K': 2}))
    c.add('Evidence patří každému skladu zvlášť', other.prehled() == {'K': 7} and store.stav('A') == 'stornovana' and store.prehled() == {'K': 7, 'O': 2}, 'Slovník evidence patří instanci, ne společné třídě.')
except BaseException as exc:
    c.add('Rezervace lze ověřit', False, f'{type(exc).__name__}: {exc}')
finally:
    sklad.SkladovaKarta = original_card
r = c.run()
if c.no_error(r):
    for text in ('Po první rezervaci:', 'Po stornu první:', 'Druhé storno odmítnuto:', 'Druhá objednávka: rezervovana'):
        c.output_contains(r, text)
c.done()
