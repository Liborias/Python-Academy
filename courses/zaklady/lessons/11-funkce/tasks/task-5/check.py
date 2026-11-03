import ast
from dilna_check import check
c = check()
c.function('nadpis')
c.uses_call('nadpis')
r = c.run(stdin='')
if c.no_error(r):
    c.output_equals(r, 'MOJE DÍLNA\nMOJE DÍLNA', "Porovnejte zadání, vstup a požadovaný výstup.")

c.done()
