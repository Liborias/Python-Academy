import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'okraje', ([3, 7, 9],), (3, 9))
c.returns(ns, 'okraje', ([5],), (5, 5))
c.returns(ns, 'okraje', ([-2, 4],), (-2, 4))
node = c.function('okraje')
c.add("Docstring", node is not None and bool(ast.get_docstring(node)), "Přidejte popis funkce.")
c.done()
