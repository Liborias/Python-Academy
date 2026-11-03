import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'slevy', ([10, 20],), [5, 10])
c.returns(ns, 'slevy', ([],), [])
c.returns(ns, 'slevy', ([0, 8],), [0, 4])

import copy
data = [2, -1, 0]
original = copy.deepcopy(data)
c.call(ns, 'slevy', (data,))
c.add("Vstup se nemění", data == original, "Vytvořte nové výsledky, neměňte vstupní data.")
c.done()
