import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'ruzna', ([4, 2, 4],), [2, 4])
c.returns(ns, 'ruzna', ([],), [])
c.returns(ns, 'ruzna', (['b', 'a', 'b'],), ['a', 'b'])

c.done()
