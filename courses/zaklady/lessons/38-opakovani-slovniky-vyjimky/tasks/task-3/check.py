import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'cetnosti', (['a', 'b', 'a'],), {'a': 2, 'b': 1})
c.returns(ns, 'cetnosti', ([],), {})
c.returns(ns, 'cetnosti', ([1, 1, 2],), {1: 2, 2: 1})

c.done()
