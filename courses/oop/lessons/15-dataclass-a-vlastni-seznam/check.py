import ast
import os
import sys
from dataclasses import fields, is_dataclass, MISSING
sys.path.insert(0, os.getcwd())
from adresa import Adresa
from dilna_check import check

c = check()
c.defines_class('ExpedicniStitek')
ns = c.load()
try:
    cls = ns['ExpedicniStitek']
    c.add('Štítek je dataclass', isinstance(cls, type) and is_dataclass(cls), 'Použijte dekorátor dataclass na třídě.')
    node = next((n for n in c.tree.body if isinstance(n, ast.ClassDef) and n.name == 'ExpedicniStitek'), None)
    own = {n.name for n in node.body if isinstance(n, ast.FunctionDef)} if node else set()
    c.add('Běžné metody vytváří dataclass', not own.intersection({'__init__', '__eq__', '__repr__'}), 'Konstruktor, porovnání a repr nechte vygenerovat.')
    metadata = {field.name: field for field in fields(cls)}
    c.add('Poznámky mají továrnu na výchozí hodnotu', set(metadata) == {'kod', 'adresa', 'poznamky'} and metadata['poznamky'].default is MISSING
          and callable(metadata['poznamky'].default_factory), 'Definujte tři pole a u poznamky použijte field(default_factory=list).')
    address = Adresa('  Žlutá 8  ', 'Nové Město', '01234')
    address_before = dict(vars(address))
    a, b = cls(' E-1 ', address), cls('E-2', address)
    c.add('Nové štítky mají vlastní prázdné seznamy', a.kod == ' E-1 ' and a.adresa is address and b.adresa is address
          and isinstance(a.poznamky, list) and a.poznamky == [] and b.poznamky == [] and a.poznamky is not b.poznamky,
          'Zachovejte původní kód/adresu, výchozí seznam vytvořte pro každou instanci.')
    for index, text in enumerate(['Opatrně s obalem.', 'Opatrně s obalem.', '  Žlutý štítek  '], 1):
        ok, value = c.call({'add': a.pridej_poznamku}, 'add', (text,))
        c.add('Poznámky zachovají pořadí a opakování', ok and type(value) is int and value == index and c.last_output == ''
              and a.poznamky == ['Opatrně s obalem.', 'Opatrně s obalem.', '  Žlutý štítek  '][:index] and b.poznamky == [],
              'Připojte původní text na konec a vraťte počet; druhý štítek se nemění.')
    late = cls('POZDĚJI', address)
    c.add('I pozdější štítek začíná vlastním seznamem', late.poznamky == [] and late.poznamky is not a.poznamky, 'Továrna musí pokaždé vrátit nový seznam.')
    supplied = ['Vlastní seznam']
    explicit = cls(kod='VLASTNÍ', adresa=address, poznamky=supplied)
    ok, value = c.call({'add': explicit.pridej_poznamku}, 'add', ('Druhá',))
    c.add('Výslovně předané objekty se nekopírují', ok and value == 2 and explicit.poznamky is supplied and supplied == ['Vlastní seznam', 'Druhá']
          and explicit.adresa is address, 'Použijte předaný seznam a adresu jako původní odkazy.')
    equal = cls(' E-1 ', Adresa('  Žlutá 8  ', 'Nové Město', '01234'), list(a.poznamky))
    before = (dict(vars(a)), list(a.poznamky), dict(vars(equal)), list(equal.poznamky))
    c.add('Datová rovnost využívá hodnotu adresy i poznámek', a is not equal and a == equal and equal == a, 'Rovnost zahrnuje všechna pole, i hodnotově stejnou samostatnou adresu.')
    text = repr(a)
    c.add('Generovaný repr ukazuje názvy a hodnoty polí', text.startswith('ExpedicniStitek(') and all(label in text for label in ('kod=', 'adresa=', 'poznamky='))
          and repr(a.kod) in text and repr(a.poznamky) in text and before == (vars(a), a.poznamky, vars(equal), equal.poznamky), 'Repr i porovnávání jsou dotazy bez změn stavu.')
    for attr, changed in [('kod', 'JINÝ'), ('adresa', Adresa('Jiná', 'Nové Město', '01234')), ('poznamky', [])]:
        old = getattr(equal, attr)
        setattr(equal, attr, changed)
        c.add('Každé pole ovlivňuje rovnost', a != equal and equal != a, 'Nevylučujte pole z generovaného porovnání.')
        setattr(equal, attr, old)
    c.add('Adresa se při práci s poznámkami nemění', vars(address) == address_before, 'Přidávání poznámek nezasahuje do adresy.')
except BaseException as exc:
    c.add('Dataclass lze ověřit', False, f'{type(exc).__name__}: {exc}')
r = c.run()
if c.no_error(r):
    for text in ('Poznámek po zápisu: 1', 'První poznámky:', 'Druhý štítek: []', 'Shodná data: True'):
        c.output_contains(r, text)
c.done()
