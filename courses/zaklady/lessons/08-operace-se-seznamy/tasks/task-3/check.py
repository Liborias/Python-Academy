import ast
from dilna_check import check
c = check()
c.uses_call('sorted')
r = c.run(stdin='')
if c.no_error(r):
    c.output_equals(r, '[10, 20, 30, 50]', "Porovnejte zadání, vstup a požadovaný výstup.")

c.done()
