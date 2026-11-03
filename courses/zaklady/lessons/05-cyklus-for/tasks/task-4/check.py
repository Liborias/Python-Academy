import ast
from dilna_check import check
c = check()
c.uses(ast.For, "Použijte for.")
r = c.run(stdin='2\n')
if c.no_error(r):
    c.output_equals(r, 'Ahoj\nAhoj', "Porovnejte zadání, vstup a požadovaný výstup.")
r = c.run(stdin='0\n')
if c.no_error(r):
    c.output_equals(r, '', "Porovnejte zadání, vstup a požadovaný výstup.")
r = c.run(stdin='1\n')
if c.no_error(r):
    c.output_equals(r, 'Ahoj', "Porovnejte zadání, vstup a požadovaný výstup.")

c.done()
