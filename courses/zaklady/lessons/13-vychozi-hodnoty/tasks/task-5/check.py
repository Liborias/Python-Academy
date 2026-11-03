import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'obal', ('A',), '*A*')
c.returns(ns, 'obal', ('B', '#'), '#B#')
c.returns(ns, 'obal', ('',), '**')

c.done()
