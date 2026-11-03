import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'celkem', ([{'cena': 20}, {'cena': 5}],), 25)
c.returns(ns, 'celkem', ([],), 0)
c.returns(ns, 'celkem', ([{'cena': 0}],), 0)

c.done()
