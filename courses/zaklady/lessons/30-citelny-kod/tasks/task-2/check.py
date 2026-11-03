import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'na_sekundy', (2,), 120)
c.returns(ns, 'na_sekundy', (0,), 0)
c.returns(ns, 'na_sekundy', (7,), 420)
node = c.function('na_sekundy')
c.add("Docstring", node is not None and bool(ast.get_docstring(node)), "Přidejte popis funkce.")

c.done()
