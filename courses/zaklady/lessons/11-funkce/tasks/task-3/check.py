import ast
from dilna_check import check
c = check()
c.function('pozdrav')
c.uses_call('pozdrav')
r = c.run(stdin='')
if c.no_error(r):
    c.output_equals(r, 'Dobrý den!\nDobrý den!\nDobrý den!', "Porovnejte zadání, vstup a požadovaný výstup.")

c.done()
