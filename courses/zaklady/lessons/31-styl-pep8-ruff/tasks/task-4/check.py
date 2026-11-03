import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'delka_textu', ('ahoj',), 4)
c.returns(ns, 'delka_textu', ('',), 0)
c.returns(ns, 'delka_textu', ('žába',), 4)
node = c.function('delka_textu')
c.add("Docstring", node is not None and bool(ast.get_docstring(node)), "Přidejte popis funkce.")
c.add("Styl řádků", all(len(line) <= 79 and "\t" not in line for line in c.code.splitlines()), "Řádky nejvýše 79 znaků, bez tabulátorů.")

c.done()
