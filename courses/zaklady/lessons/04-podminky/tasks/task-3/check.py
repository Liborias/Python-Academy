import ast
from dilna_check import check
c = check()
c.uses(ast.If, "Použijte podmínku if.")
r = c.run(stdin='14\n')
if c.no_error(r):
    c.output_equals(r, '50', "Porovnejte zadání, vstup a požadovaný výstup.")
r = c.run(stdin='15\n')
if c.no_error(r):
    c.output_equals(r, '100', "Porovnejte zadání, vstup a požadovaný výstup.")
r = c.run(stdin='30\n')
if c.no_error(r):
    c.output_equals(r, '100', "Porovnejte zadání, vstup a požadovaný výstup.")

c.done()
