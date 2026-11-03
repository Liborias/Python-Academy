import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'krabice', (21, 10), 3)
c.returns(ns, 'krabice', (20, 10), 2)
c.returns(ns, 'krabice', (0, 5), 0)
c.imports("math")
c.done()
