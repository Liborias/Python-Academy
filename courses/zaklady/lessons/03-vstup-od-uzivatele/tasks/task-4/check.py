import ast
from dilna_check import check
c = check()
c.uses_call("input")
r = c.run(stdin='Ema\n')
if c.no_error(r):
    c.output_equals(r, 'Ahoj, Ema!', "Porovnejte zadání, vstup a požadovaný výstup.")
r = c.run(stdin='Žaneta\n')
if c.no_error(r):
    c.output_equals(r, 'Ahoj, Žaneta!', "Porovnejte zadání, vstup a požadovaný výstup.")

c.done()
