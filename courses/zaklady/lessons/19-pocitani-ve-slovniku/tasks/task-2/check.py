import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'hlasy', (['les', 'hrad', 'les'],), {'les': 2, 'hrad': 1})
c.returns(ns, 'hlasy', ([],), {})
c.returns(ns, 'hlasy', (['x'],), {'x': 1})

c.done()
