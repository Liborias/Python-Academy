import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'soucet_cen', ({'a': 20, 'b': 5},), 25)
c.returns(ns, 'soucet_cen', ({},), 0)
c.returns(ns, 'soucet_cen', ({'x': -2},), -2)

c.done()
