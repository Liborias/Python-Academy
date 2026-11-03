import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns_close(ns, 'podil', (6, 2), 3.0)
c.returns(ns, 'podil', (5, 0), None)
c.returns_close(ns, 'podil', (0, 4), 0.0)
c.uses(ast.Try, "Použijte try/except.")
c.done()
