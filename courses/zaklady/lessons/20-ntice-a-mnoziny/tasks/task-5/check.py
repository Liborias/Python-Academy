import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'otoc_bod', ((2, 7),), (7, 2))
c.returns(ns, 'otoc_bod', ((0, -3),), (-3, 0))
c.returns(ns, 'otoc_bod', (('x', 'y'),), ('y', 'x'))

c.done()
