from dilna_check import check
c = check()
ns = c.load()
if ns is not None:
    c.returns(ns, 'poslednich', ([1, 2, 3, 4], 2), [3, 4])
    c.returns(ns, 'poslednich', ([1, 2, 3], 0), [])
    c.returns(ns, 'poslednich', ([1, 2], 5), [1, 2])
    c.returns(ns, 'poslednich', ([], 3), [])
    c.returns(ns, 'poslednich', ([1, 2, 3], 3), [1, 2, 3])
    c.returns(ns, 'obrat_seznam', ([1, 2, 3],), [3, 2, 1])
    c.returns(ns, 'obrat_seznam', ([],), [])
    c.returns(ns, 'obrat_seznam', (['a'],), ['a'])
    c.returns(ns, 'rozdel_na_poloviny', ([1, 2, 3, 4, 5],), ([1, 2], [3, 4, 5]))
    c.returns(ns, 'rozdel_na_poloviny', ([1, 2, 3, 4],), ([1, 2], [3, 4]))
    c.returns(ns, 'rozdel_na_poloviny', ([],), ([], []))
    c.returns(ns, 'rozdel_na_poloviny', ([9],), ([], [9]))
    c.returns(ns, 'kopie_matice', ([[1, 2], [3]],), [[1, 2], [3]])
    c.returns(ns, 'kopie_matice', ([],), [])
    for f, vstup, extra in (("poslednich", [1, 2, 3, 4], (2,)), ("obrat_seznam", [1, 2, 3], ()), ("rozdel_na_poloviny", [1, 2, 3, 4, 5], ()), ("kopie_matice", [[1, 2], [3]], ())):
        if callable(ns.get(f)):
            kopie = [list(x) if isinstance(x, list) else x for x in vstup]
            try:
                ns[f](vstup, *extra)
            except Exception:
                pass
            c.add(f"{f} nemění vstup", vstup == kopie, f"Po zavolání funkce se vstupní seznam změnil na {vstup}.")
    if callable(ns.get("obrat_seznam")):
        c.add("obrat_seznam vrací nový seznam", ns["obrat_seznam"]([1, 2]) is not None and isinstance(ns["obrat_seznam"]([1, 2]), list), "Funkce má vrátit seznam.")
    if callable(ns.get("kopie_matice")):
        m = [[1, 2], [3, 4]]
        k = ns["kopie_matice"](m)
        try:
            k[0].append(99)
            k[1][0] = 0
        except Exception:
            pass
        c.add("kopie_matice je hluboká (změna kopie nezmění původní)", m == [[1, 2], [3, 4]], f"Změna kopie se promítla do originálu: {m}. Zkopírujte i vnitřní seznamy.")
    if callable(ns.get("rozdel_na_poloviny")):
        r = ns["rozdel_na_poloviny"]([1, 2, 3])
        c.add("rozdel_na_poloviny vrací dvojici (tuple)", isinstance(r, tuple) and len(r) == 2, "Vraťte dvojici: return levá, pravá.")
c.done()
