import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'soucet_dvojnasobku', ([1, 2, 3],), 12)
c.returns(ns, 'soucet_dvojnasobku', ([],), 0)
c.returns(ns, 'soucet_dvojnasobku', ([-2, 1],), -2)
node = c.function('soucet_dvojnasobku')
c.add("Docstring", node is not None and bool(ast.get_docstring(node)), "Přidejte popis funkce.")
c.add("Styl řádků", all(len(line) <= 79 and "\t" not in line for line in c.code.splitlines()), "Řádky nejvýše 79 znaků, bez tabulátorů.")

c.done()
