import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'prevod', ('3',), 3)
c.returns(ns, 'prevod', ('x',), None)
c.returns(ns, 'prevod', ('',), None)
c.uses(ast.Try, "Zachyťte konkrétní chybu.")
c.done()
