import ast
from dilna_check import check
c = check()
c.uses(ast.While, "Použijte cyklus while.")
for vstup, ocek in (("5\n3\n0\n", 8), ("0\n", 0), ("10\n20\n30\n0\n", 60), ("-4\n9\n0\n", 5)):
    r = c.run(stdin=vstup)
    if c.no_error(r, f"Běh se vstupem {vstup.split()}"):
        c.output_has_line(r, f"Součet: {ocek}", f"Pro vstup {vstup.split()} očekávám „Součet: {ocek}“. Máte: {c._short(r.out)}")
c.done()
