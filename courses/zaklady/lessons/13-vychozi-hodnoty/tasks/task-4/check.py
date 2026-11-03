import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns_close(ns, 'navys', (100,), 110.0)
c.returns_close(ns, 'navys', (80, 25), 100.0)
c.returns_close(ns, 'navys', (50, 0), 50.0)

c.done()
