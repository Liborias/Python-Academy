import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'cele_metry', (2.9,), 2)
c.returns(ns, 'cele_metry', (3.0,), 3)
c.returns(ns, 'cele_metry', (0.4,), 0)
c.imports("math")
c.done()
