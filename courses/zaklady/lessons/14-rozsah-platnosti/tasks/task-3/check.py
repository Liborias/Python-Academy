import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'vstupne', (3,), 240)
c.returns(ns, 'vstupne', (0,), 0)
c.returns(ns, 'vstupne', (1,), 80)
if ns is not None:
    c.add("Globální konstanta zachována", ns.get('CENA_LISTKU') == 80, "Konstantu uvnitř funkce nepřepisujte.")
    ns['CENA_LISTKU'] = 81
c.returns(ns, 'vstupne', (2,), 162)

c.done()
