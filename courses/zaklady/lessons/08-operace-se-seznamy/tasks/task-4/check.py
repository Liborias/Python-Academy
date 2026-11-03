import ast
from dilna_check import check
c = check()
c.uses(ast.Subscript, "Použijte řez seznamu.")
r = c.run(stdin='')
if c.no_error(r):
    c.output_equals(r, '[7, 8]', "Porovnejte zadání, vstup a požadovaný výstup.")

c.done()
