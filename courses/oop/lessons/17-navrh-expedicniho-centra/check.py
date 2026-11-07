import os
import sys
sys.path.insert(0, os.getcwd())
from objednavka import Objednavka
from dilna_check import check

c = check()
c.defines_class('NakupniObjednavka')
ns = c.load()
try:
    cls = ns['NakupniObjednavka']
    for code in ('', ' \t', None, 7):
        c.raises({'ctor': cls}, 'ctor', (code,), ValueError)
    a, b = cls(' A-Ž '), cls('B')
    c.add('Nový nákup je samostatný a otevřený', a.cislo == ' A-Ž ' and a.uzavrena is False and a.celkem() == 0 and a.pozadavek() == {}, 'Zachovejte číslo a vlastní prázdný nákup.')
    c.raises({'close': a.uzavri}, 'close', (), ValueError)
    for attr in ('cislo', 'uzavrena'):
        value = getattr(a, attr)
        c.raises({'write': setattr}, 'write', (a, attr, None), AttributeError)
        c.add('Property nákupu jsou jen pro čtení', getattr(a, attr) == value, 'Použijte připravené property.')
    expected, total = {}, 0
    for index, args in enumerate([('K', '  Žlutá kniha  ', 170, 2), ('O', 'Obal', 30, 1), ('K', '  Žlutá kniha  ', 170, 3), ('ZDARMA', 'Dárek', 0, 1)], 1):
        ok, value = c.call({'add': a.pridej}, 'add', args)
        expected[args[0]] = expected.get(args[0], 0) + args[3]
        total += args[2] * args[3]
        c.add('Řádky a počty se nezaměňují', ok and value == index and a.celkem() == total and a.pozadavek() == expected and c.last_output == '', 'Vraťte počet řádků, množství stejných kódů sečtěte.')
    ok, value = c.call({'add': b.pridej}, 'add', ('J', 'Jiná', 7))
    c.add('Výchozí počet je jeden a nákupy se neovlivní', ok and value == 1 and b.celkem() == 7 and b.pozadavek() == {'J': 1} and a.pozadavek() == expected, 'Každý nákup používá vlastní objednávku a požadavek.')
    invalid = [('', 'N', 2, 1), ('  ', 'N', 2, 1), (None, 'N', 2, 1), ('X', '', 2, 1), ('X', 3, 2, 1)]
    invalid += [('X', 'N', value, 1) for value in (-1, True, 1.5, '2', None)]
    invalid += [('X', 'N', 2, value) for value in (0, -1, True, 1.5, '2', None)]
    for args in invalid:
        ok, error = c.call({'add': a.pridej}, 'add', args)
        c.add('Neplatný řádek nemění nákup', not ok and isinstance(error, ValueError) and a.celkem() == total and a.pozadavek() == expected and not a.uzavrena, 'Vše ověřte před přidáním položky nebo skladového množství.')
    copy = a.pozadavek()
    copy['K'] = 999
    c.add('Požadavek je samostatná kopie', a.pozadavek() == expected and a.pozadavek() is not a.pozadavek(), 'Vraťte nový slovník počtů.')
    for name, expected_value in [('celkem', total), ('pozadavek', expected)]:
        ok, value = c.call({name: getattr(a, name)}, name)
        c.add('Dotaz nic nevypisuje', ok and value == expected_value and c.last_output == '', 'Dotazy vracejí hodnotu bez print.')
    original_add = Objednavka.pridej
    delegated = []
    def watched_add(self, polozka):
        delegated.append((polozka.nazev, polozka.cena_za_kus, polozka.pocet))
        return original_add(self, polozka)
    try:
        Objednavka.pridej = watched_add
        probe = cls('DELEGACE')
        probe.pridej('P', '  Předaný název  ', 12, 3)
        c.add('Položku převezme původní objednávka', delegated == [('  Předaný název  ', 12, 3)], 'Vytvořte Polozka s původními údaji a předejte ji veřejné pridej.')
    finally:
        Objednavka.pridej = original_add
    original = Objednavka.celkem
    try:
        Objednavka.celkem = lambda self: 4321
        c.add('Cena se skutečně deleguje', a.celkem() == 4321, 'Využijte veřejné celkem původní objednávky.')
    finally:
        Objednavka.celkem = original
    ok, value = c.call({'close': a.uzavri}, 'close')
    c.add('Úspěšné uzavření', ok and value is None and a.uzavrena is True and c.last_output == '', 'Uzavřete neprázdný otevřený nákup.')
    for name, args in [('close', ()), ('add', ('K', 'Kniha', 1, 1))]:
        method = a.uzavri if name == 'close' else a.pridej
        c.raises({name: method}, name, args, ValueError)
        c.add('Po uzavření se data nemění', a.uzavrena and a.pozadavek() == expected and a.celkem() == total, 'Druhé uzavření a přidání odmítněte před změnou.')
except BaseException as exc:
    c.add('Nákup lze ověřit', False, f'{type(exc).__name__}: {exc}')
r = c.run()
if c.no_error(r):
    c.output_contains(r, 'Zboží celkem: 780')
c.done()
