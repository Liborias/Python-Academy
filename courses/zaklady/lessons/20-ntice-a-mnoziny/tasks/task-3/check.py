import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'prunik', ([3, 1, 3], [3, 2]), [3])
c.returns(ns, 'prunik', ([], [1]), [])
c.returns(ns, 'prunik', (['z', 'a'], ['a', 'z']), ['a', 'z'])

c.done()
