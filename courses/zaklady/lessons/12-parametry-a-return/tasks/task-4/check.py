import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'rozdil', (80, 100), 20)
c.returns(ns, 'rozdil', (50, 50), 0)
c.returns(ns, 'rozdil', (20, 10), -10)

c.done()
