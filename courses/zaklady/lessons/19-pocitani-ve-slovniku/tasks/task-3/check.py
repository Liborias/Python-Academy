import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'pismena', ('aba',), {'a': 2, 'b': 1})
c.returns(ns, 'pismena', ('',), {})
c.returns(ns, 'pismena', ('a a',), {'a': 2, ' ': 1})

c.done()
