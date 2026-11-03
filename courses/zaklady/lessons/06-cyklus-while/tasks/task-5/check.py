import ast
from dilna_check import check
c = check()
c.uses(ast.While, "Použijte while.")
r = c.run(stdin='ne\nhotovo\n')
if c.no_error(r):
    c.output_equals(r, 'OK', "Porovnejte zadání, vstup a požadovaný výstup.")
r = c.run(stdin='hotovo\n')
if c.no_error(r):
    c.output_equals(r, 'OK', "Porovnejte zadání, vstup a požadovaný výstup.")

c.done()
