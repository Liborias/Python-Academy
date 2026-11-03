import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'prvni', ([5, 7],), 5)
c.returns(ns, 'prvni', ([],), None)
c.returns(ns, 'prvni', (['a'],), 'a')
c.uses(ast.Try, "Zachyťte konkrétní chybu.")
c.done()
