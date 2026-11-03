import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'pocet_kladnych', ([-1, 0, 2, 4],), 2)
c.returns(ns, 'pocet_kladnych', ([],), 0)
c.returns(ns, 'pocet_kladnych', ([0, -2],), 0)
c.uses(ast.Assert, "Doplňte vlastní ověření pomocí assert.")
c.done()
