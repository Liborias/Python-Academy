from dilna_check import check
c = check()
c.uses_call("input", "Hlavní smyčka čte příkazy pomocí input().")
ns = c.load()
if ns is not None:
    c.returns(ns, "pridej_ukol", ([], "uklidit"), [{"text": "uklidit", "hotovo": False}])
    c.returns(ns, "pridej_ukol", ([{"text": "a", "hotovo": True}], "b"),
              [{"text": "a", "hotovo": True}, {"text": "b", "hotovo": False}])
    U = lambda: [{"text": "a", "hotovo": False}, {"text": "b", "hotovo": False}]
    ok, v = c.call(ns, "dokonc_ukol", (U(), 2))
    c.add("dokonc_ukol(…, 2) vrací True", ok and v is True, f"Vrátila {v!r}.")
    seznam = U()
    c.call(ns, "dokonc_ukol", (seznam, 2))
    c.add("dokonc_ukol označí správný úkol", seznam == [{"text": "a", "hotovo": False}, {"text": "b", "hotovo": True}],
          "Úkoly se číslují od 1, takže číslo 2 je druhý úkol (index 1).")
    for cislo in (0, 3, -1):
        seznam = U()
        ok, v = c.call(ns, "dokonc_ukol", (seznam, cislo))
        c.add(f"dokonc_ukol(…, {cislo}) vrací False a nic nemění", ok and v is False and seznam == U(),
              "Neplatné číslo: vraťte False a seznam nechte beze změny (pozor na záporný index).")
    c.returns(ns, "procento_hotovo", ([],), 0)
    c.returns_close(ns, "procento_hotovo", ([{"text": "a", "hotovo": True}, {"text": "b", "hotovo": False}],), 50.0)
    c.returns_close(ns, "procento_hotovo", ([{"text": "a", "hotovo": True}],), 100.0)
    c.returns_close(ns, "procento_hotovo", ([{"text": "a", "hotovo": False}, {"text": "b", "hotovo": True},
                                             {"text": "c", "hotovo": False}],), 100 / 3)
    s = []
    ok, v = c.call(ns, "zpracuj_prikaz", (s, "seznam"))
    c.add("zpracuj_prikaz: prázdný seznam", ok and v == "Žádné úkoly.", f"Vrátila {v!r}.")
    ok, v = c.call(ns, "zpracuj_prikaz", (s, "pridej Koupit mléko"))
    c.add("zpracuj_prikaz: pridej", ok and v == "Přidáno: Koupit mléko" and len(s) == 1, f"Vrátila {v!r}.")
    c.call(ns, "zpracuj_prikaz", (s, "pridej Napsat úkol"))
    ok, v = c.call(ns, "zpracuj_prikaz", (s, "hotovo 2"))
    c.add("zpracuj_prikaz: hotovo", ok and v == "Hotovo: Napsat úkol" and s[1]["hotovo"] is True, f"Vrátila {v!r}.")
    ok, v = c.call(ns, "zpracuj_prikaz", (s, "seznam"))
    c.add("zpracuj_prikaz: seznam", ok and v == "1. [ ] Koupit mléko\n2. [x] Napsat úkol", f"Vrátila {v!r}.")
    for p in ("hotovo 9", "hotovo abc", "hotovo", "hotovo 0"):
        ok, v = c.call(ns, "zpracuj_prikaz", (s, p))
        c.add(f"zpracuj_prikaz: {p!r} je neplatné číslo", ok and v == "Neplatné číslo.", f"Vrátila {v!r}.")
    for p in ("smaz 1", "", "pridejx"):
        ok, v = c.call(ns, "zpracuj_prikaz", (s, p))
        c.add(f"zpracuj_prikaz: {p!r} je neznámý příkaz", ok and v == "Neznámý příkaz.", f"Vrátila {v!r}.")
    s2 = [{"text": "Koupit mléko", "hotovo": False}, {"text": "Napsat úkol", "hotovo": False}]
    ok, v = c.call(ns, "zpracuj_prikaz", (s2, "hotovo 1"))
    c.add("zpracuj_prikaz: hotovo 1 vrátí text prvního úkolu", ok and v == "Hotovo: Koupit mléko" and s2[0]["hotovo"] is True, f"Vrátila {v!r}.")
    s = []
    ok, v = c.call(ns, "hlavni_smycka", (s,), stdin="pridej Prvni\nhotovo 1\nseznam\nblabla\nkonec\n")
    c.add("hlavni_smycka zpracuje příkazy a skončí na konec",
          ok and s == [{"text": "Prvni", "hotovo": True}] and "1. [x] Prvni" in c.last_output
          and "Neznámý příkaz." in c.last_output, "Vypište odpověď na každý příkaz a na konec skončete.")
c.done()
