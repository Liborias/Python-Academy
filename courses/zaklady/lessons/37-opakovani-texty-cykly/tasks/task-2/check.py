import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'samohlasky', ('Ahoj',), 2)
c.returns(ns, 'samohlasky', ('',), 0)
c.returns(ns, 'samohlasky', ('Rytmus',), 2)

c.done()
