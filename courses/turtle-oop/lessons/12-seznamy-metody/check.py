from dilna_check import check
c = check()
ns = c.load()
if ns is not None:
    c.returns(ns, 'bez_duplicit', ([3, 1, 3, 2, 1],), [3, 1, 2])
    c.returns(ns, 'bez_duplicit', ([],), [])
    c.returns(ns, 'bez_duplicit', (['a', 'a'],), ['a'])
    c.returns(ns, 'bez_duplicit', ([1, 2, 3],), [1, 2, 3])
    c.returns(ns, 'serad_podle_delky', (['ccc', 'b', 'aa', 'a'],), ['a', 'b', 'aa', 'ccc'])
    c.returns(ns, 'serad_podle_delky', ([],), [])
    c.returns(ns, 'serad_podle_delky', (['pes', 'ara', 'kos'],), ['ara', 'kos', 'pes'])
    c.returns(ns, 'posun', ([1, 2, 3, 4], 1), [2, 3, 4, 1])
    c.returns(ns, 'posun', ([1, 2, 3, 4], -1), [4, 1, 2, 3])
    c.returns(ns, 'posun', ([1, 2, 3, 4], 5), [2, 3, 4, 1])
    c.returns(ns, 'posun', ([1, 2, 3, 4], 0), [1, 2, 3, 4])
    c.returns(ns, 'posun', ([], 3), [])
    c.returns(ns, 'posun', ([7], 10), [7])
    c.returns(ns, 'posun', ([1, 2, 3], 3), [1, 2, 3])
    c.returns(ns, 'odeber_vsechny', ([1, 2, 1, 3, 1], 1), [2, 3])
    c.returns(ns, 'odeber_vsechny', ([], 1), [])
    c.returns(ns, 'odeber_vsechny', ([1, 2], 5), [1, 2])
    c.returns(ns, 'odeber_vsechny', (['a', 'b', 'a'], 'a'), ['b'])
    for f, vstup, extra in (("bez_duplicit", [3, 1, 3, 2, 1], ()), ("serad_podle_delky", ["ccc", "b", "aa"], ()), ("posun", [1, 2, 3, 4], (1,)), ("odeber_vsechny", [1, 2, 1], (1,))):
        if callable(ns.get(f)):
            kopie = list(vstup)
            try:
                ns[f](vstup, *extra)
            except Exception:
                pass
            c.add(f"{f} nemění vstupní seznam", vstup == kopie, f"Po zavolání funkce se původní seznam změnil na {vstup}. Vytvořte nový seznam, původní neměňte.")
    if callable(ns.get("bez_duplicit")):
        vstup = [1, 2]
        vysl = ns["bez_duplicit"](vstup)
        c.add("bez_duplicit vrací nový seznam (ne tentýž)", vysl is not vstup, "Funkce vrátila tentýž seznam, který dostala. Vraťte nový.")
c.done()
