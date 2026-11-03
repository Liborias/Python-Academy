import ast
from dilna_check import check
c = check()
c.uses(ast.If, "Použijte podmínku if.")
r = c.run(stdin='8\n')
if c.no_error(r):
    c.output_equals(r, 'zavřeno', "Porovnejte zadání, vstup a požadovaný výstup.")
r = c.run(stdin='9\n')
if c.no_error(r):
    c.output_equals(r, 'otevřeno', "Porovnejte zadání, vstup a požadovaný výstup.")
r = c.run(stdin='16\n')
if c.no_error(r):
    c.output_equals(r, 'otevřeno', "Porovnejte zadání, vstup a požadovaný výstup.")
r = c.run(stdin='17\n')
if c.no_error(r):
    c.output_equals(r, 'zavřeno', "Porovnejte zadání, vstup a požadovaný výstup.")

c.done()
