import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'pocet_vyskytu', ([2, 1, 2], 2), 2)
c.returns(ns, 'pocet_vyskytu', ([], 1), 0)
c.returns(ns, 'pocet_vyskytu', ([1, 1], 3), 0)

c.done()
