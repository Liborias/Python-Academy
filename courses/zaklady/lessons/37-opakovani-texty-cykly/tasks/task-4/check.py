import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'bez_znaku', ('banan', 'a'), 'bnn')
c.returns(ns, 'bez_znaku', ('abc', 'x'), 'abc')
c.returns(ns, 'bez_znaku', ('', 'a'), '')

c.done()
