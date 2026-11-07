import ast
import os
import sys
sys.path.insert(0, os.getcwd())
from balik import Balik
from dilna_check import check

c = check()
c.defines_class('PopsanyBalik')
ns = c.load()

def describes(text, code, weight):
    try:
        node = ast.parse(text, mode='eval').body
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name) or node.func.id != 'PopsanyBalik':
            return False
        args = [ast.literal_eval(arg) for arg in node.args]
        if len(args) > 2 or any(kw.arg not in ('kod', 'hmotnost_g') for kw in node.keywords):
            return False
        values = dict(zip(('kod', 'hmotnost_g'), args))
        for kw in node.keywords:
            if kw.arg in values:
                return False
            values[kw.arg] = ast.literal_eval(kw.value)
        return values == {'kod': code, 'hmotnost_g': weight} and type(values['hmotnost_g']) is int
    except (ValueError, SyntaxError, TypeError):
        return False

try:
    cls = ns['PopsanyBalik']
    c.add('Popsaný balík dědí původní rozhraní', issubclass(cls, Balik), 'Odvoďte třídu z připraveného Balik.')
    for code, weight in [('B-8', 1), ("ŽK'9\n\\konec", 12500)]:
        item = cls(code, weight)
        for current in (code, 'NOVÝ "kód"'):
            item.kod = current
            before = dict(vars(item))
            ok, value = c.call({'str': str}, 'str', (item,))
            c.add('Str vrací aktuální popis bez výpisu a změn', ok and value == f'Balík {current}, {weight} g' and c.last_output == '' and vars(item) == before,
                  'Vraťte aktuální popis(), nevypisujte jej a neukládejte zastaralou kopii.')
            ok, value = c.call({'repr': repr}, 'repr', (item,))
            c.add('Repr bezpečně zachová údaje balíku', ok and describes(value, current, weight) and c.last_output == '' and vars(item) == before,
                  'Vraťte zápis PopsanyBalik(kód, hmotnost) s řádně zapsaným textovým kódem, například přes !r.')
        old = Balik.popis
        try:
            Balik.popis = lambda self: 'Aktuální veřejný popis'
            c.add('Str skutečně deleguje na popis', str(item) == 'Aktuální veřejný popis', 'Použijte veřejné popis(), neopisujte jeho výpočet.')
        finally:
            Balik.popis = old
    for weight in (0, -1, True, 1.5, '8'):
        c.raises({'ctor': cls}, 'ctor', ('B', weight), ValueError)
    item = cls('B', 30)
    c.raises({'write': setattr}, 'write', (item, 'hmotnost_g', 99), AttributeError)
    c.add('Property hmotnosti zůstala zachována', item.hmotnost_g == 30, 'Nedovolte změnit zděděnou hmotnost.')
except BaseException as exc:
    c.add('Výpisy lze ověřit', False, f'{type(exc).__name__}: {exc}')
r = c.run()
if c.no_error(r):
    c.output_contains(r, 'Pro zákazníka: Balík B-001, 1200 g')
c.done()
