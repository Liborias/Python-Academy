import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'dny_od_zacatku', (2026, 1, 1), 0)
c.returns(ns, 'dny_od_zacatku', (2026, 1, 2), 1)
c.returns(ns, 'dny_od_zacatku', (2028, 3, 1), 60)

c.done()
