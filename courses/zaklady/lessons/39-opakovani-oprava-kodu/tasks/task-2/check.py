import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'minimum', ([3, 1, 2],), 1)
c.returns(ns, 'minimum', ([-4, -8],), -8)
c.returns(ns, 'minimum', ([],), None)

c.done()
