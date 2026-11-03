import ast
from dilna_check import check
c = check()
c.uses_call("input")
r = c.run(stdin='3\n')
if c.no_error(r):
    c.output_equals(r, '12', "Porovnejte zadání, vstup a požadovaný výstup.")
r = c.run(stdin='0\n')
if c.no_error(r):
    c.output_equals(r, '0', "Porovnejte zadání, vstup a požadovaný výstup.")
r = c.run(stdin='12\n')
if c.no_error(r):
    c.output_equals(r, '48', "Porovnejte zadání, vstup a požadovaný výstup.")

c.done()
