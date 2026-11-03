import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'pulka', (8,), 4)
c.returns(ns, 'pulka', (0,), 0)
c.returns(ns, 'pulka', (-4,), -2)
c.uses(ast.Raise, "Použijte raise.")
c.raises(ns, 'pulka', (3,), ValueError)
c.raises(ns, 'pulka', (-1,), ValueError)

c.done()
