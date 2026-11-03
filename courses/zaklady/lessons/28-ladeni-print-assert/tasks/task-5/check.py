import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'cena_nakupu', (20, 3), 60)
c.returns(ns, 'cena_nakupu', (5, 0), 0)
c.returns(ns, 'cena_nakupu', (0, 5), 0)
c.uses(ast.Assert, "Doplňte vlastní ověření pomocí assert.")
c.done()
