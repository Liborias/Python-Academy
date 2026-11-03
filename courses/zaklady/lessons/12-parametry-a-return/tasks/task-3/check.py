import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'na_minuty', (2,), 120)
c.returns(ns, 'na_minuty', (0,), 0)
c.returns(ns, 'na_minuty', (5,), 300)

c.done()
