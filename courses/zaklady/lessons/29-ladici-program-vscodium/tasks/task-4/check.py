import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'nezaporne', ([-2, 0, 3],), [0, 3])
c.returns(ns, 'nezaporne', ([],), [])
c.returns(ns, 'nezaporne', ([-1],), [])

import copy
data = [2, -1, 0]
original = copy.deepcopy(data)
c.call(ns, 'nezaporne', (data,))
c.add("Vstup se nemění", data == original, "Vytvořte nové výsledky, neměňte vstupní data.")
c.done()
