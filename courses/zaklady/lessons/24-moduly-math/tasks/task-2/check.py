import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns_close(ns, 'prepona', (3, 4), 5.0)
c.returns_close(ns, 'prepona', (0, 0), 0.0)
c.returns_close(ns, 'prepona', (5, 12), 13.0)
c.imports("math")
c.done()
