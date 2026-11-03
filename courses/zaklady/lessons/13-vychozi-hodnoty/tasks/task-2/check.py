import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 's_dopravou', (100,), 179)
c.returns(ns, 's_dopravou', (100, 0), 100)
c.returns(ns, 's_dopravou', (20, 30), 50)

c.done()
