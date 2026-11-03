import ast
from dilna_check import check
c = check()
c.uses(ast.For, "Použijte for.")
r = c.run(stdin='3\n')
if c.no_error(r):
    c.output_equals(r, '3\n6\n9', "Porovnejte zadání, vstup a požadovaný výstup.")
r = c.run(stdin='-2\n')
if c.no_error(r):
    c.output_equals(r, '-2\n-4\n-6', "Porovnejte zadání, vstup a požadovaný výstup.")

c.done()
