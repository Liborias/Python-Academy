import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'klice', ({'b': 2, 'a': 1},), ['a', 'b'])
c.returns(ns, 'klice', ({},), [])
c.returns(ns, 'klice', ({'ž': 1, 'a': 0},), ['a', 'ž'])

c.done()
