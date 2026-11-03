import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'soucet_platnych', (['2', 'x', '3'],), 5)
c.returns(ns, 'soucet_platnych', ([],), 0)
c.returns(ns, 'soucet_platnych', (['-2', '1', ''],), -1)

c.done()
