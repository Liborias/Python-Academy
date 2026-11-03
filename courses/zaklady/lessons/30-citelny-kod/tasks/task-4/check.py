import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'zbyvajici_strany', (100, 20), 80)
c.returns(ns, 'zbyvajici_strany', (50, 50), 0)
c.returns(ns, 'zbyvajici_strany', (30, 0), 30)
node = c.function('zbyvajici_strany')
c.add("Docstring", node is not None and bool(ast.get_docstring(node)), "Přidejte popis funkce.")

c.done()
