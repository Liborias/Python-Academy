import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'sjednoceni', ([3, 1], [2, 3]), [1, 2, 3])
c.returns(ns, 'sjednoceni', ([], []), [])
c.returns(ns, 'sjednoceni', (['ž', 'a'], ['b']), ['a', 'b', 'ž'])

c.done()
