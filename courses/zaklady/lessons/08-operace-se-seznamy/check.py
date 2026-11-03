from dilna_check import check
c = check()
c.uses_call("min", "Použijte min().")
c.uses_call("max", "Použijte max().")
c.uses_call("sum", "Použijte sum().")
c.uses_call("sorted", "Použijte sorted().")
for t in ("Nejmenší: 1", "Největší: 9", "Součet: 25", "[1, 3, 5, 7, 9]"):
    c.no_hardcoded(t, "Hodnoty spočítejte funkcemi min, max, sum a sorted, nepište je natvrdo.")
r = c.run()
if c.no_error(r):
    c.output_equals(r, "Nejmenší: 1\nNejvětší: 9\nSoučet: 25\nSeřazeno: [1, 3, 5, 7, 9]",
                    "Očekávám čtyři řádky: Nejmenší: 1, Největší: 9, Součet: 25, Seřazeno: [1, 3, 5, 7, 9]. Máte: " + c._short(r.out))
ns = c.load()
if ns is not None:
    c.add("Seznam cisla zůstal původní", ns.get("cisla") == [7, 3, 9, 1, 5], "Seznam cisla nesmíte měnit, použijte sorted(), ne .sort().")
c.done()
