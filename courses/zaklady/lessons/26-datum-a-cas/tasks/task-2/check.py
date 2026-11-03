import ast
from dilna_check import check
c = check()
ns = c.load()
c.returns(ns, 'posun', (2026, 12, 31, 1), '2027-01-01')
c.returns(ns, 'posun', (2028, 2, 28, 1), '2028-02-29')
c.returns(ns, 'posun', (2026, 5, 1, -1), '2026-04-30')

c.done()
