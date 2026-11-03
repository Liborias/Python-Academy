import ast
from dilna_check import check
c = check()
c.function('znacka')
c.uses_call('znacka')
r = c.run(stdin='')
if c.no_error(r):
    c.output_equals(r, '***\n***', "Porovnejte zadání, vstup a požadovaný výstup.")

c.done()
