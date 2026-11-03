import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns_close(ns, 'prumer', ([1, 2],), 1.5)
c.returns_close(ns, 'prumer', ([5],), 5.0)
c.returns(ns, 'prumer', ([],), None)

c.done()
