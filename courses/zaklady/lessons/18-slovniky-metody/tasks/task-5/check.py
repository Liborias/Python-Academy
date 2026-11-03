import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'ma_jmeno', ({'Ema': 0}, 'Ema'), True)
c.returns(ns, 'ma_jmeno', ({}, 'Ema'), False)
c.returns(ns, 'ma_jmeno', ({'Jan': 3}, 'Ema'), False)

c.done()
