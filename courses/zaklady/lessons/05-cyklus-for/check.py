import ast
from dilna_check import check
c = check()
c.uses(ast.For, "Použijte cyklus for s range().")
c.uses_call("range", "Použijte range(1, 6).")
c.no_hardcoded("15", "Součet nepište natvrdo, spočítejte ho v cyklu.")
r = c.run()
if c.no_error(r):
    c.output_equals(r, "1\n2\n3\n4\n5\nSoučet: 15", "Očekávám řádky 1 až 5 a poslední řádek „Součet: 15“.")
c.done()
