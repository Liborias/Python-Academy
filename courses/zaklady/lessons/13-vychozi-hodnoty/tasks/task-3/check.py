import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'opakuj', ('ha',), 'haha')
c.returns(ns, 'opakuj', ('x', 0), '')
c.returns(ns, 'opakuj', ('a', 3), 'aaa')

c.done()
