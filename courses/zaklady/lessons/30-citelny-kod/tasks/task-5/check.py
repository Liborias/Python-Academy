import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'delka_vyletu', (3, 5), 8)
c.returns(ns, 'delka_vyletu', (0, 0), 0)
c.returns(ns, 'delka_vyletu', (2, 2), 4)
node = c.function('delka_vyletu')
c.add("Docstring", node is not None and bool(ast.get_docstring(node)), "Přidejte popis funkce.")

c.done()
