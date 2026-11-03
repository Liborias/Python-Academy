import ast
from dilna_check import check
c = check()
c.uses_call("input")
r = c.run(stdin='7\n')
if c.no_error(r):
    c.output_equals(r, '12', "Porovnejte zadání, vstup a požadovaný výstup.")
r = c.run(stdin='0\n')
if c.no_error(r):
    c.output_equals(r, '5', "Porovnejte zadání, vstup a požadovaný výstup.")
r = c.run(stdin='-8\n')
if c.no_error(r):
    c.output_equals(r, '-3', "Porovnejte zadání, vstup a požadovaný výstup.")

c.done()
