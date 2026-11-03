import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'den_tydne', (2026, 11, 2), 0)
c.returns(ns, 'den_tydne', (2026, 11, 8), 6)
c.returns(ns, 'den_tydne', (2026, 11, 3), 1)

c.done()
