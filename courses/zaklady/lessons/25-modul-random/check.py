from dilna_check import check
c = check()
c.imports("random", "Na začátek souboru přidejte import random.")
ns = c.load()


def vzorek(func, args=(), n=200):
    vysledky = []
    for _ in range(n):
        ok, v = c.call(ns, func, args)
        if not ok:
            return None, v
        vysledky.append(v)
    return vysledky, None


if ns is not None:
    v, err = vzorek("hod_kostkou")
    if v is None:
        c.add("hod_kostkou() jde zavolat", False, f"Volání skončilo chybou: {err!r}")
    else:
        c.add("hod_kostkou() vrací čísla 1 až 6", all(isinstance(x, int) and 1 <= x <= 6 for x in v),
              "Použijte random.randint(1, 6).")
        c.add("hod_kostkou() vrací všechny hodnoty 1 až 6", set(v) == {1, 2, 3, 4, 5, 6},
              "Hod kostkou má dávat všechna čísla od 1 do 6, každé volání losuje znovu.")

    data = [10, 20, 30]
    v, err = vzorek("vyber", (data,))
    if v is None:
        c.add("vyber(seznam) jde zavolat", False, f"Volání skončilo chybou: {err!r}")
    else:
        c.add("vyber(seznam) vrací prvky seznamu", all(x in data for x in v), "Použijte random.choice(seznam).")
        c.add("vyber(seznam) losuje všechny prvky", set(v) == set(data), "Výběr má být z celého seznamu a každé volání losuje znovu.")

    puvodni = list(range(8))
    zkus = list(puvodni)
    ok, z = c.call(ns, "zamichej", (zkus,))
    c.add("zamichej() vrací seznam", ok and isinstance(z, list), "Funkce má vrátit seznam (shuffle sám nic nevrací).")
    c.add("zamichej() nezmění původní seznam", zkus == puvodni, "Zamíchejte kopii: list(seznam).")
    if ok and isinstance(z, list):
        c.add("zamichej() zachová stejné prvky", sorted(z) == puvodni, "Zamíchaný seznam musí mít stejné prvky.")
        varianty = set()
        for _ in range(30):
            ok2, z2 = c.call(ns, "zamichej", (list(puvodni),))
            if ok2 and isinstance(z2, list):
                varianty.add(tuple(z2))
        c.add("zamichej() opravdu míchá náhodně", len(varianty) >= 2, "Každé zamíchání musí dopadnout jinak (použijte random.shuffle).")

    ok1, a = c.call(ns, "tajne_cislo", (42,))
    ok2, b = c.call(ns, "tajne_cislo", (42,))
    c.add("tajne_cislo(42) vrací dvakrát totéž", ok1 and ok2 and a == b, "Na začátku funkce zavolejte random.seed(seed).")
    c.add("tajne_cislo vrací 1 až 100", ok1 and isinstance(a, int) and 1 <= a <= 100, "Použijte random.randint(1, 100).")
    hodnoty = []
    for sd in range(200):
        oks, h = c.call(ns, "tajne_cislo", (sd,))
        hodnoty.append(h if oks else None)
    c.add("tajne_cislo vrací 1 až 100 pro různé seed", all(isinstance(h, int) and 1 <= h <= 100 for h in hodnoty),
          "Použijte random.randint(1, 100).")
    c.add("tajne_cislo dává pro různé seed různá čísla", len({h for h in hodnoty if h is not None}) >= 30,
          "Různé hodnoty seed mají dát různá čísla.")
    platne = [h for h in hodnoty if isinstance(h, int)]
    c.add("tajne_cislo pokrývá celý rozsah 1 až 100", bool(platne) and min(platne) <= 10 and max(platne) >= 90,
          "Čísla mají vycházet z celého rozsahu 1 až 100.")
    c.uses_call("seed", "Použijte random.seed(seed).")
c.done()
