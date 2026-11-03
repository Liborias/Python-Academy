import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'nejdelsi', (['pes', 'kočka', 'kůň'],), 'kočka')
c.returns(ns, 'nejdelsi', ([],), '')
c.returns(ns, 'nejdelsi', (['les', 'pes'],), 'les')
c.uses(ast.Assert, "Doplňte vlastní ověření pomocí assert.")
c.done()
