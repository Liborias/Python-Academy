import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'hodiny', (2,), 48)
c.returns(ns, 'hodiny', (0,), 0)
c.returns(ns, 'hodiny', (7,), 168)
if ns is not None:
    c.add("Globální konstanta zachována", ns.get('HODIN_VE_DNI') == 24, "Konstantu uvnitř funkce nepřepisujte.")
    ns['HODIN_VE_DNI'] = 25
c.returns(ns, 'hodiny', (2,), 50)

c.done()
