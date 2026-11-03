import ast
from dilna_check import check
c = check()
c.uses_call('sum')
r = c.run(stdin='')
if c.no_error(r):
    c.output_equals(r, '2 9 22', "Porovnejte zadání, vstup a požadovaný výstup.")

c.done()
