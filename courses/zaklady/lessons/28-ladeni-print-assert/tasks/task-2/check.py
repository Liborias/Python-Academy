import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'secti', ([2, 3],), 5)
c.returns(ns, 'secti', ([],), 0)
c.returns(ns, 'secti', ([-2, 1],), -1)
c.uses(ast.Assert, "Doplňte vlastní ověření pomocí assert.")
c.done()
