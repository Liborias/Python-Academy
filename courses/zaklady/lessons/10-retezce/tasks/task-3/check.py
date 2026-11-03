import ast
from dilna_check import check
c = check()
c.uses_call("input")
r = c.run(stdin='ahoj\n')
if c.no_error(r):
    c.output_equals(r, 'AHOJ', "Porovnejte zadání, vstup a požadovaný výstup.")
r = c.run(stdin='Žluťoučký\n')
if c.no_error(r):
    c.output_equals(r, 'ŽLUŤOUČKÝ', "Porovnejte zadání, vstup a požadovaný výstup.")

c.done()
