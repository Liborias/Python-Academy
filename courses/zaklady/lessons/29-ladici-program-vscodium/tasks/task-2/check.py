import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'dvojnasobky', ([2, -1, 0],), [4, -2, 0])
c.returns(ns, 'dvojnasobky', ([],), [])
c.returns(ns, 'dvojnasobky', ([5],), [10])

import copy
data = [2, -1, 0]
original = copy.deepcopy(data)
c.call(ns, 'dvojnasobky', (data,))
c.add("Vstup se nemění", data == original, "Vytvořte nové výsledky, neměňte vstupní data.")
c.done()
