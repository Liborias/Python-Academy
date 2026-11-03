import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'obvod_obsah', (3, 5), (16, 15))
c.returns(ns, 'obvod_obsah', (0, 4), (8, 0))
c.returns(ns, 'obvod_obsah', (2, 2), (8, 4))
node = c.function('obvod_obsah')
c.add("Docstring", node is not None and bool(ast.get_docstring(node)), "Přidejte popis funkce.")
c.done()
