import ast
from dilna_check import check
c = check()
c.uses(ast.While, "Použijte while.")
r = c.run(stdin='2\n-1\n0\n')
if c.no_error(r):
    c.output_equals(r, '2', "Porovnejte zadání, vstup a požadovaný výstup.")
r = c.run(stdin='0\n')
if c.no_error(r):
    c.output_equals(r, '0', "Porovnejte zadání, vstup a požadovaný výstup.")
r = c.run(stdin='7\n0\n')
if c.no_error(r):
    c.output_equals(r, '1', "Porovnejte zadání, vstup a požadovaný výstup.")

c.done()
