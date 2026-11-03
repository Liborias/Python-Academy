import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'serad_dvojici', (8, 2), (2, 8))
c.returns(ns, 'serad_dvojici', (3, 3), (3, 3))
c.returns(ns, 'serad_dvojici', (-2, -5), (-5, -2))
node = c.function('serad_dvojici')
c.add("Docstring", node is not None and bool(ast.get_docstring(node)), "Přidejte popis funkce.")
c.done()
