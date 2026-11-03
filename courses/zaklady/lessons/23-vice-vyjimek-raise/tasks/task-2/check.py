import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'nezaporne', (0,), 0)
c.returns(ns, 'nezaporne', (4,), 4)
c.uses(ast.Raise, "Použijte raise.")
c.raises(ns, 'nezaporne', (-1,), ValueError)
c.raises(ns, 'nezaporne', (-8,), ValueError)

c.done()
