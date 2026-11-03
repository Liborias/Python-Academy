import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'obvod', (3, 5), 16)
c.returns(ns, 'obvod', (0, 4), 8)
c.returns(ns, 'obvod', (2, 2), 8)

c.done()
