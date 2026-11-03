import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'cista_slova', (' AHOJ   Světe ',), ['ahoj', 'světe'])
c.returns(ns, 'cista_slova', (' ',), [])
c.returns(ns, 'cista_slova', ('X',), ['x'])

c.done()
