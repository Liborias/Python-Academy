import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns_close(ns, 'obvod_kruhu', (1,), 6.283185307179586)
c.returns_close(ns, 'obvod_kruhu', (0,), 0.0)
c.returns_close(ns, 'obvod_kruhu', (3,), 18.84955592153876)
c.imports("math")
c.done()
