import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'ceske_datum', (2026, 1, 2), '02. 01. 2026')
c.returns(ns, 'ceske_datum', (2028, 12, 31), '31. 12. 2028')

c.done()
