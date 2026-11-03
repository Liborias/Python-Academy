import ast
from dilna_check import check
c = check()
c.uses(ast.While, "Použijte while.")
r = c.run(stdin='2\n-3\n4\n0\n')
if c.no_error(r):
    c.output_equals(r, '6', "Porovnejte zadání, vstup a požadovaný výstup.")
r = c.run(stdin='0\n')
if c.no_error(r):
    c.output_equals(r, '0', "Porovnejte zadání, vstup a požadovaný výstup.")
r = c.run(stdin='-2\n0\n')
if c.no_error(r):
    c.output_equals(r, '0', "Porovnejte zadání, vstup a požadovaný výstup.")

c.done()
