import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns_close(ns, 'bezpecne_del', (8, 2), 4.0)
c.returns(ns, 'bezpecne_del', (2, 0), None)
c.returns_close(ns, 'bezpecne_del', (0, 3), 0.0)
c.uses(ast.Try, "Zachyťte konkrétní chybu.")
c.done()
