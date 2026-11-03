import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'telefon', ({'Ema': '123'}, 'Ema'), '123')
c.returns(ns, 'telefon', ({}, 'Jan'), 'nenalezeno')
c.returns(ns, 'telefon', ({'Jan': '456'}, 'Ema'), 'nenalezeno')

c.done()
