import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'obsah_obdelniku', (3, 5), 15)
c.returns(ns, 'obsah_obdelniku', (0, 8), 0)
c.returns(ns, 'obsah_obdelniku', (2, 2), 4)
node = c.function('obsah_obdelniku')
c.add("Docstring", node is not None and bool(ast.get_docstring(node)), "Přidejte popis funkce.")
c.add("Styl řádků", all(len(line) <= 79 and "\t" not in line for line in c.code.splitlines()), "Řádky nejvýše 79 znaků, bez tabulátorů.")

c.done()
