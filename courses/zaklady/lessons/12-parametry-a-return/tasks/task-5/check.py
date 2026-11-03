import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'staci_body', (5, 5), True)
c.returns(ns, 'staci_body', (3, 5), False)
c.returns(ns, 'staci_body', (8, 5), True)

c.done()
