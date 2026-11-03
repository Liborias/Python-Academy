import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'kilometry', (2,), 10)
c.returns(ns, 'kilometry', (0,), 0)
c.returns(ns, 'kilometry', (4,), 20)
if ns is not None:
    c.add("Globální konstanta zachována", ns.get('DELKA_OKRUHU') == 5, "Konstantu uvnitř funkce nepřepisujte.")
    ns['DELKA_OKRUHU'] = 6
c.returns(ns, 'kilometry', (2,), 12)

c.done()
