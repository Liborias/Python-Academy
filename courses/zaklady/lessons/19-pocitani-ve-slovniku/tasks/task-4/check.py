import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'delky', (['pes', 'hrad', 'les'],), {3: 2, 4: 1})
c.returns(ns, 'delky', ([],), {})
c.returns(ns, 'delky', (['', 'a', 'a'],), {0: 1, 1: 2})

c.done()
