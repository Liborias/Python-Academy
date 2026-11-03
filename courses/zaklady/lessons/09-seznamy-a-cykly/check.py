import ast
from dilna_check import check
c = check()
c.uses(ast.For, "Použijte cyklus for.")
c.uses_call("append", "Čísla přidávejte do seznamu metodou append().")
for vstup, prumer, nej in (("4\n8\n6\n2\n10\n", "6.0", "10"), ("1\n2\n3\n4\n5\n", "3.0", "5"), ("-2\n-4\n-6\n-8\n-10\n", "-6.0", "-2")):
    r = c.run(stdin=vstup)
    if c.no_error(r, f"Běh se vstupem {' '.join(vstup.split())}"):
        c.output_has_line(r, f"Průměr: {prumer}", f"Očekávám „Průměr: {prumer}“. Máte: {c._short(r.out)}")
        c.output_has_line(r, f"Největší: {nej}", f"Očekávám „Největší: {nej}“. Máte: {c._short(r.out)}")
c.done()
