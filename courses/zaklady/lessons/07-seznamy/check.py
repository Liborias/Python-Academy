from dilna_check import check
c = check()
r = c.run()
if c.no_error(r):
    c.output_equals(r, "Merkur\nMars\n5\n['Merkur', 'Venuše', 'Země', 'Mars', 'Jupiter']",
                    "Očekávám 4 řádky: Merkur, Mars, 5 a celý seznam. Máte: " + c._short(r.out))
ns = c.load()
if ns is not None:
    c.add("Proměnná planety obsahuje Jupiter", ns.get("planety", [])[-1:] == ["Jupiter"], "Přidejte Jupiter metodou append().")
prints = [n for n in c._walk() if isinstance(n, __import__("ast").Call) and getattr(n.func, "id", "") == "print"]
tvrde = [a for p in prints for a in p.args if isinstance(a, __import__("ast").Constant) and a.value in ("Merkur", "Mars", 5)]
vypis = any(isinstance(a, (__import__("ast").Subscript, __import__("ast").Call)) for p in prints for a in p.args)
c.add("Hodnoty se vypisují ze seznamu, ne natvrdo", vypis and not tvrde,
      "Vypište planety[0], planety[-1] a len(planety) místo napsaného textu nebo čísla.")
c.done()
