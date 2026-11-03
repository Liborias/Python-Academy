import ast
from dilna_check import check
c = check()
ns = c.load()
if ns is not None:
    c.add("Hodnota proměnné", ns.get('delka') == 8.5, "Vytvořte požadovanou proměnnou.")
names = {v.value.id for node in ast.walk(c.tree) if isinstance(node, ast.JoinedStr) for v in node.values if isinstance(v, ast.FormattedValue) and isinstance(v.value, ast.Name)} if c.tree else set()
c.add("F-řetězec používá proměnnou", 'delka' in names, "Vložte proměnnou do f-řetězce.")
r = c.run(stdin='')
if c.no_error(r):
    c.output_equals(r, '8.5 km', "Porovnejte zadání, vstup a požadovaný výstup.")

c.done()
