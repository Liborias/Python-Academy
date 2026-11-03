import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'obsah_ctverce', (2,), 4)
c.returns(ns, 'obsah_ctverce', (5,), 25)
c.uses(ast.Raise, "Použijte raise.")
c.raises(ns, 'obsah_ctverce', (0,), ValueError)
c.raises(ns, 'obsah_ctverce', (-2,), ValueError)

c.done()
