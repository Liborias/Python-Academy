import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'soucet_cen', ([{'cena': 20}, {'cena': 5}],), 25)
c.returns(ns, 'soucet_cen', ([],), 0)
c.returns(ns, 'soucet_cen', ([{'cena': 0}],), 0)

import copy
data = [{'cena': 20}, {'cena': 5}]
original = copy.deepcopy(data)
c.call(ns, 'soucet_cen', (data,))
c.add("Vstup se nemění", data == original, "Vytvořte nové výsledky, neměňte vstupní data.")
c.done()
