import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'obvod_trojuhelniku', (3, 4, 5), 12)
c.returns(ns, 'obvod_trojuhelniku', (2, 2, 2), 6)
c.returns(ns, 'obvod_trojuhelniku', (5, 5, 8), 18)
node = c.function('obvod_trojuhelniku')
c.add("Docstring", node is not None and bool(ast.get_docstring(node)), "Přidejte popis funkce.")
c.add("Styl řádků", all(len(line) <= 79 and "\t" not in line for line in c.code.splitlines()), "Řádky nejvýše 79 znaků, bez tabulátorů.")

c.done()
