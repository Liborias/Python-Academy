import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'minuty', (2,), 90)
c.returns(ns, 'minuty', (0,), 0)
c.returns(ns, 'minuty', (6,), 270)
if ns is not None:
    c.add("Globální konstanta zachována", ns.get('DELKA_HODINY') == 45, "Konstantu uvnitř funkce nepřepisujte.")
    ns['DELKA_HODINY'] = 46
c.returns(ns, 'minuty', (2,), 92)

c.done()
