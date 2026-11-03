import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'dlouhe', (['pes', 'kočka', 'hrad'],), ['kočka', 'hrad'])
c.returns(ns, 'dlouhe', ([],), [])
c.returns(ns, 'dlouhe', (['a'],), [])
data = ['pes', 'kočka', 'hrad']
puvodni = list(data)
c.call(ns, 'dlouhe', (data,))
c.add("Vstup se nemění", data == puvodni, "Vytvářejte nový seznam, neměňte vstup.")

c.done()
