import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'vitez', ([{'jmeno': 'Ema', 'body': 2}, {'jmeno': 'Jan', 'body': 4}],), 'Jan')
c.returns(ns, 'vitez', ([{'jmeno': 'A', 'body': 3}, {'jmeno': 'B', 'body': 3}],), 'A')
c.returns(ns, 'vitez', ([{'jmeno': 'X', 'body': -5}],), 'X')

c.done()
