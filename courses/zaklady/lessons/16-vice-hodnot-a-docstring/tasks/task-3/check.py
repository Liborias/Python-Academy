import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'soucet_pocet', ([2, 3],), (5, 2))
c.returns(ns, 'soucet_pocet', ([],), (0, 0))
c.returns(ns, 'soucet_pocet', ([-2],), (-2, 1))
node = c.function('soucet_pocet')
c.add("Docstring", node is not None and bool(ast.get_docstring(node)), "Přidejte popis funkce.")
c.done()
