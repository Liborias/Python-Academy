import ast
from dilna_check import check
c = check()
c.uses(ast.For, "Použijte for pro průchod seznamem.")
r = c.run(stdin='')
if c.no_error(r):
    c.output_equals(r, '[4, 8, -2]', "Porovnejte zadání, vstup a požadovaný výstup.")

c.done()
