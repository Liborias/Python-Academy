import ast
from dilna_check import check
c = check()
c.uses_call("input")
r = c.run(stdin='a  b c\n')
if c.no_error(r):
    c.output_equals(r, '3', "Porovnejte zadání, vstup a požadovaný výstup.")
r = c.run(stdin='\n')
if c.no_error(r):
    c.output_equals(r, '0', "Porovnejte zadání, vstup a požadovaný výstup.")
r = c.run(stdin='jedno\n')
if c.no_error(r):
    c.output_equals(r, '1', "Porovnejte zadání, vstup a požadovaný výstup.")

c.done()
