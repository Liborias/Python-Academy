import ast
from dilna_check import check
c = check()
c.uses_call("input")
r = c.run(stdin='ahoj  světe\n')
if c.no_error(r):
    c.output_equals(r, 'ahoj-světe', "Porovnejte zadání, vstup a požadovaný výstup.")
r = c.run(stdin=' x \n')
if c.no_error(r):
    c.output_equals(r, 'x', "Porovnejte zadání, vstup a požadovaný výstup.")
r = c.run(stdin='\n')
if c.no_error(r):
    c.output_equals(r, '', "Porovnejte zadání, vstup a požadovaný výstup.")

c.done()
