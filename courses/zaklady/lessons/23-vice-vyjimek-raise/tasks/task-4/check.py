import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns_close(ns, 'deleni', (6, 2), 3.0)
c.returns_close(ns, 'deleni', (0, 5), 0.0)
c.uses(ast.Raise, "Použijte raise.")
c.raises(ns, 'deleni', (4, 0), ValueError)

c.done()
