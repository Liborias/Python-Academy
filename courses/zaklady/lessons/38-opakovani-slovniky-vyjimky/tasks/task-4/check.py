import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'skladem', ({'čaj': 3}, 'čaj'), 3)
c.returns(ns, 'skladem', ({}, 'x'), 0)
c.returns(ns, 'skladem', ({'x': 0}, 'x'), 0)

c.done()
