import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns_close(ns, 'cena', ('12.5',), 12.5)
c.returns(ns, 'cena', ('chyba',), None)
c.returns_close(ns, 'cena', ('0',), 0.0)

c.done()
