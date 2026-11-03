import ast
from dilna_check import check
c = check()
r = c.run()
if c.no_error(r):
    c.output_equals(r, "Mars je 227.9 milionů km od Slunce.", "Vypište přesně větu „Mars je 227.9 milionů km od Slunce.“")
ns = c.load()
if ns is not None:
    c.add("Proměnná planeta je „Mars“", ns.get("planeta") == "Mars", "Vytvořte proměnnou planeta = \"Mars\".")
    c.add("Proměnná vzdalenost je 227.9", ns.get("vzdalenost") == 227.9, "Vytvořte proměnnou vzdalenost = 227.9 (s tečkou).")
names = {v.value.id for n in ast.walk(c.tree) if isinstance(n, ast.JoinedStr) for v in n.values
         if isinstance(v, ast.FormattedValue) and isinstance(v.value, ast.Name)} if c.tree else set()
c.add("F-řetězec vkládá proměnné planeta a vzdalenost", {"planeta", "vzdalenost"} <= names,
      "Použijte f-řetězec s proměnnými: f\"{planeta} je {vzdalenost} ...\" (hodnoty nepište natvrdo).")
c.done()
