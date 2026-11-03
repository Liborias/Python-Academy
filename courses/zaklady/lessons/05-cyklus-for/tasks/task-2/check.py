import ast
from dilna_check import check
c = check()
c.uses(ast.For, "Použijte for.")
r = c.run(stdin='4\n')
if c.no_error(r):
    c.output_equals(r, '10', "Porovnejte zadání, vstup a požadovaný výstup.")
r = c.run(stdin='0\n')
if c.no_error(r):
    c.output_equals(r, '0', "Porovnejte zadání, vstup a požadovaný výstup.")
r = c.run(stdin='7\n')
if c.no_error(r):
    c.output_equals(r, '28', "Porovnejte zadání, vstup a požadovaný výstup.")

c.done()
