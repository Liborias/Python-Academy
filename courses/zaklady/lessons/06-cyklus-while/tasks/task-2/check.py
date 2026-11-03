import ast
from dilna_check import check
c = check()
c.uses(ast.While, "Použijte while.")
r = c.run(stdin='3\n')
if c.no_error(r):
    c.output_equals(r, '3\n2\n1', "Porovnejte zadání, vstup a požadovaný výstup.")
r = c.run(stdin='0\n')
if c.no_error(r):
    c.output_equals(r, '', "Porovnejte zadání, vstup a požadovaný výstup.")

c.done()
