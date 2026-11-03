import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'celkova_cena', (100, 79), 179)
c.returns(ns, 'celkova_cena', (0, 0), 0)
c.returns(ns, 'celkova_cena', (50, 0), 50)
node = c.function('celkova_cena')
c.add("Docstring", node is not None and bool(ast.get_docstring(node)), "Přidejte popis funkce.")

c.done()
