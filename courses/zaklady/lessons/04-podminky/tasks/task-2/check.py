import ast
from dilna_check import check
c = check()
c.uses(ast.If, "Použijte podmínku if.")
r = c.run(stdin='5\n')
if c.no_error(r):
    c.output_equals(r, 'kladné', "Porovnejte zadání, vstup a požadovaný výstup.")
r = c.run(stdin='-1\n')
if c.no_error(r):
    c.output_equals(r, 'záporné', "Porovnejte zadání, vstup a požadovaný výstup.")
r = c.run(stdin='0\n')
if c.no_error(r):
    c.output_equals(r, 'nula', "Porovnejte zadání, vstup a požadovaný výstup.")

c.done()
