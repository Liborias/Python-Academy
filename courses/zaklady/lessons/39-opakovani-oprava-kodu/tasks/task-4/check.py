import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'posledni', ([3, 8],), 8)
c.returns(ns, 'posledni', ([0],), 0)
c.returns(ns, 'posledni', ([],), None)

c.done()
