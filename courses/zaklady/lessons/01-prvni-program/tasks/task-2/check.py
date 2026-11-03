import ast
from dilna_check import check
c = check()
c.uses_call("print")
r = c.run(stdin='')
if c.no_error(r):
    c.output_equals(r, 'Ahoj, akademie!\n15', "Porovnejte zadání, vstup a požadovaný výstup.")

c.done()
