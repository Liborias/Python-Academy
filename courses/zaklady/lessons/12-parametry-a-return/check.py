import ast
from dilna_check import check
c = check()
c.defines_function("obsah_obdelniku", 2)
c.defines_function("je_sude", 1)
c.uses(ast.Return, "Funkce má hodnotu vracet pomocí return, ne vypisovat.")
ns = c.load()
for a, b, o in ((3, 4, 12), (0, 5, 0), (2.5, 2, 5.0), (10, 10, 100)):
    c.returns(ns, "obsah_obdelniku", (a, b), o)
for n, o in ((4, True), (7, False), (0, True), (-3, False), (-2, True)):
    c.returns(ns, "je_sude", (n,), o)
c.done()
