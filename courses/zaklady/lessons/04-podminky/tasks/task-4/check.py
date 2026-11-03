import ast
from dilna_check import check
c = check()
c.uses(ast.If, "Použijte podmínku if.")
r = c.run(stdin='3\n8\n')
if c.no_error(r):
    c.output_equals(r, '8', "Porovnejte zadání, vstup a požadovaný výstup.")
r = c.run(stdin='9\n2\n')
if c.no_error(r):
    c.output_equals(r, '9', "Porovnejte zadání, vstup a požadovaný výstup.")
r = c.run(stdin='4\n4\n')
if c.no_error(r):
    c.output_equals(r, '4', "Porovnejte zadání, vstup a požadovaný výstup.")

c.done()
