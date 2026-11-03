import ast
from dilna_check import check
c = check()
c.uses_call("input")
r = c.run(stdin='  Ahoj  \n')
if c.no_error(r):
    c.output_equals(r, 'Ahoj', "Porovnejte zadání, vstup a požadovaný výstup.")
r = c.run(stdin=' x y \n')
if c.no_error(r):
    c.output_equals(r, 'x y', "Porovnejte zadání, vstup a požadovaný výstup.")

c.done()
