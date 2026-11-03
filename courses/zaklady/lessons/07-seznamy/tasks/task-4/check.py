import ast
from dilna_check import check
c = check()
ns = c.load()
c.add("Výsledný seznam", ns is not None and ns.get('zastavky') == ['Škola', 'Hrad', 'Les'], "Upravte skutečný seznam.")
r = c.run(stdin='')
if c.no_error(r):
    c.output_equals(r, "['Škola', 'Hrad', 'Les']", "Porovnejte zadání, vstup a požadovaný výstup.")

c.done()
