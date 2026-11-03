import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'slova', ('a b a',), {'a': 2, 'b': 1})
c.returns(ns, 'slova', ('  ',), {})
c.returns(ns, 'slova', ('A a',), {'A': 1, 'a': 1})

c.done()
