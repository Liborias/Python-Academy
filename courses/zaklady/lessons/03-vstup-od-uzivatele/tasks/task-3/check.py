import ast
from dilna_check import check
c = check()
c.uses_call("input")
r = c.run(stdin='2\n8\n')
if c.no_error(r):
    c.output_equals(r, '10', "Porovnejte zadání, vstup a požadovaný výstup.")
r = c.run(stdin='-3\n1\n')
if c.no_error(r):
    c.output_equals(r, '-2', "Porovnejte zadání, vstup a požadovaný výstup.")
r = c.run(stdin='0\n0\n')
if c.no_error(r):
    c.output_equals(r, '0', "Porovnejte zadání, vstup a požadovaný výstup.")

c.done()
