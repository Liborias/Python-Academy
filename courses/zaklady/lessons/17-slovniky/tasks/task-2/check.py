import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'vizitka', ('Ema', 'Brno'), {'jmeno': 'Ema', 'mesto': 'Brno'})
c.returns(ns, 'vizitka', ('Jan', 'Praha'), {'jmeno': 'Jan', 'mesto': 'Praha'})
c.returns(ns, 'vizitka', ('', ''), {'jmeno': '', 'mesto': ''})

c.done()
