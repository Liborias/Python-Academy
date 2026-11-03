import ast
from dilna_check import check
c = check()
c.uses_call("print")
r = c.run(stdin='')
if c.no_error(r):
    c.output_equals(r, '7 + 2\n9', "Porovnejte zadání, vstup a požadovaný výstup.")

c.done()
