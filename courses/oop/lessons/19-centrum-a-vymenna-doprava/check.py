import os
import sys
sys.path.insert(0, os.getcwd())
from adresa import Adresa
from balik import Balik
from doprava import OsobniOdber, Kuryr
from expedice import Expedice
from stitek import ExpedicniStitek
from nakupni_objednavka import NakupniObjednavka
from rezervacni_sklad import RezervacniSklad
from dilna_check import check

c = check()
for name in ('Cyklodoprava', 'ExpedicniCentrum'):
    c.defines_class(name)
ns = c.load()
def order(code, books=1, wraps=0):
    value = NakupniObjednavka(code)
    if books:
        value.pridej('K', 'Kniha', 250, books)
    if wraps:
        value.pridej('O', 'Obal', 30, wraps)
    return value
try:
    cycle, cls = ns['Cyklodoprava'], ns['ExpedicniCentrum']
    for zone in ('', ' \t', None, 7):
        c.raises({'ctor': cycle}, 'ctor', (zone,), ValueError)
    bike = cycle('  Střed  ')
    c.add('Zóna zůstává původním textem', bike.zona == '  Střed  ', 'Ponechte původní neprázdný text zóny.')
    c.raises({'write': setattr}, 'write', (bike, 'zona', 'Jiná'), AttributeError)
    for weight in (1, 2000, 2001, 10000):
        parcel = Balik('K', weight); before = (dict(vars(parcel)), dict(vars(bike)))
        ok, value = c.call({'price': bike.cena}, 'price', (parcel,))
        valid = ok and type(value) is int and value == 59 if weight <= 2000 else not ok and isinstance(value, ValueError)
        c.add('Hranice cyklodopravy', valid and c.last_output == '' and before == (vars(parcel), vars(bike)), 'Do 2000 g včetně vraťte 59, nad limit ValueError bez změny.')
    store = RezervacniSklad(); store.pridej('K', 'Kniha', 5); store.pridej('O', 'Obal', 2)
    center = cls(store)
    c.add('Centrum má původní sklad', center.sklad is store, 'Uložte původní sklad a zpřístupněte ho property.')
    c.raises({'write': setattr}, 'write', (center, 'sklad', None), AttributeError)
    address = Adresa('Javorová 1', 'Brno', '01234')
    a, b = order('A', 2, 1), order('B', 3)
    for item, parcel, transport in [(order('VÁHA'), Balik('BAD', 2001), bike), (order('ZÁSOBY', 1, 3), Balik('BAD', 900), OsobniOdber('Dílna'))]:
        before = store.prehled()
        c.raises({'accept': center.prijmi}, 'accept', (item, parcel, transport, address), ValueError)
        c.add('Odmítnuté přijetí nic nezarezervuje ani neuzavře', store.prehled() == before and not item.uzavrena, 'Ověřte dopravu před rezervací a záznam uložte až po úspěchu skladu.')
        c.raises({'summary': center.souhrn}, 'summary', (item.cislo,), ValueError)
    parcel_a, parcel_b = Balik('BA', 1200), Balik('BB', 8000)
    for item, parcel, transport, expected in [(a, parcel_a, OsobniOdber('Dílna'), {'K': 3, 'O': 1}), (b, parcel_b, Kuryr('Javorová 1'), {'K': 0, 'O': 1})]:
        ok, value = c.call({'accept': center.prijmi}, 'accept', (item, parcel, transport, address))
        c.add('Přijetí propojí nákup a rezervaci', ok and value == item.cislo and store.prehled() == expected and item.uzavrena and c.last_output == '', 'Vraťte číslo úspěšně přijatého nákupu.')
    expected_a = {'cislo': 'A', 'stav': 'rezervovana', 'zbozi': 530, 'doprava': 0, 'celkem': 530, 'balik': 'BA', 'adresa': 'Javorová 1, 01234 Brno', 'poznamky': []}
    ok, value = c.call({'summary': center.souhrn}, 'summary', ('A',))
    c.add('Souhrn má dohodnuté údaje', ok and value == expected_a and c.last_output == '', 'Vraťte nový slovník cen, stavu, balíku, adresy a poznámek.')
    class NovaDoprava:
        def __init__(self):
            self.castka = 37
            self.calls = []
        def cena(self, balik):
            self.calls.append(balik)
            return self.castka
    own = NovaDoprava()
    original_change = Expedice.zmen_dopravu
    delegated = []
    def watched(self, nova):
        delegated.append((self.balik, nova))
        return original_change(self, nova)
    try:
        Expedice.zmen_dopravu = watched
        ok, value = c.call({'change': center.zmen_dopravu}, 'change', ('B', own))
        c.add('Změnu provádí Expedice přes společné rozhraní', ok and value == 37 and delegated == [(parcel_b, own)] and own.calls == [parcel_b] and c.last_output == '', 'Delegujte změnu původního balíku a nové dopravy, nevybírejte podle typu.')
    finally:
        Expedice.zmen_dopravu = original_change
    own.castka = 88
    c.add('Nabídka se zjišťuje aktuálně', center.souhrn('B')['doprava'] == 88 and center.souhrn('B')['celkem'] == 838, 'Nevracíte uloženou starou cenu.')
    before = center.souhrn('B')
    c.raises({'change': center.zmen_dopravu}, 'change', ('B', Kuryr('Limit', 1000)), ValueError)
    c.add('Chybná změna zachová nabídku i zásoby', center.souhrn('B') == before and store.prehled() == {'K': 0, 'O': 1}, 'Využijte bezpečné přepnutí v Expedice.')
    original_note = ExpedicniStitek.pridej_poznamku
    notes = []
    def watched_note(self, text):
        notes.append((self.kod, text))
        return original_note(self, text)
    try:
        ExpedicniStitek.pridej_poznamku = watched_note
        for count in (1, 2):
            ok, value = c.call({'note': center.pridej_poznamku}, 'note', ('A', '  Nezvonit  '))
            c.add('Poznámky zpracuje štítek', ok and value == count and c.last_output == '', 'Zachovejte pořadí i opakování přes metodu štítku.')
        c.add('Poznámky patří správné objednávce', notes == [('A', '  Nezvonit  ')] * 2 and center.souhrn('B')['poznamky'] == [], 'Nesdílejte poznámky různých štítků.')
    finally:
        ExpedicniStitek.pridej_poznamku = original_note
    summary = center.souhrn('A'); summary['poznamky'].append('Cizí'); summary['celkem'] = 0
    c.add('Souhrn nemění vnitřní údaje', center.souhrn('A')['poznamky'] == ['  Nezvonit  '] * 2 and center.souhrn('A')['celkem'] == 530, 'Vraťte nový slovník i seznam poznámek.')
    c.raises({'accept': center.prijmi}, 'accept', (order('A'), Balik('JINÁ', 1), bike, address), ValueError)
    ok, value = c.call({'cancel': center.storno}, 'cancel', ('A',))
    c.add('Storno přes centrum ponechá rezervaci B', ok and value == {'K': 2, 'O': 2} and center.souhrn('A')['stav'] == 'stornovana' and center.souhrn('B')['stav'] == 'rezervovana' and c.last_output == '', 'Delegujte storno na vlastnickou evidenci skladu.')
    for method, args in [(center.storno, ('A',)), (center.zmen_dopravu, ('A', bike)), (center.pridej_poznamku, ('A', 'Pozdě')),
                         (center.souhrn, ('NEZNÁMÁ',)), (center.storno, ('NEZNÁMÁ',)), (center.zmen_dopravu, ('NEZNÁMÁ', bike)), (center.pridej_poznamku, ('NEZNÁMÁ', 'N'))]:
        c.raises({'operation': method}, 'operation', args, ValueError)
    c.add('Odmítnuté operace zachovají stav', store.prehled() == {'K': 2, 'O': 2} and center.souhrn('A')['poznamky'] == ['  Nezvonit  '] * 2, 'Stornovanou objednávku neměňte a neznámou nevytvářejte.')
    outsider = cls(store)
    c.raises({'cancel': outsider.storno}, 'cancel', ('B',), ValueError)
    c.add('Centrum neruší cizí záznam téhož skladu', center.souhrn('B')['stav'] == 'rezervovana' and store.prehled() == {'K': 2, 'O': 2}, 'Před stornem ověřte vlastní záznam centra.')
    empty = RezervacniSklad(); second = cls(empty)
    c.raises({'summary': second.souhrn}, 'summary', ('A',), ValueError)
    c.add('Další centrum má vlastní záznamy', center.souhrn('B')['cislo'] == 'B', 'Evidence centra nesmí být společný atribut třídy.')
except BaseException as exc:
    c.add('Centrum lze ověřit', False, f'{type(exc).__name__}: {exc}')
r = c.run()
if c.no_error(r):
    for text in ('Kurýr: 99', 'Cyklodoprava: 59', 'Nabídka: 559', 'Stornovanou objednávku již neměníme.'):
        c.output_contains(r, text)
c.done()
