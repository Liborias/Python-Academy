from dilna_check import check
c = check()
c.uses_call("input", "Hra se má ptát hráče pomocí input().")
ns = c.load()
if ns is not None:
    T = ("kámen", "nůžky", "papír")
    vysledky = {("kámen", "nůžky"): "prvni", ("nůžky", "papír"): "prvni", ("papír", "kámen"): "prvni",
                ("nůžky", "kámen"): "druhy", ("papír", "nůžky"): "druhy", ("kámen", "papír"): "druhy"}
    for a in T:
        for b in T:
            c.returns(ns, "vitez_kola", (a, b), vysledky.get((a, b), "remiza"))
    zvolene = set()
    for _ in range(100):
        ok, v = c.call(ns, "nahodny_tah")
        if ok:
            zvolene.add(v)
    c.add("nahodny_tah vrací platné tahy", bool(zvolene) and zvolene <= set(T), "Použijte random.choice(list(PORAZI)).")
    c.add("nahodny_tah vybírá všechny tři tahy", zvolene == set(T), "Každé volání musí losovat znovu z celého slovníku.")
    c.returns(ns, "skore", ([("kámen", "nůžky"), ("papír", "nůžky"), ("kámen", "kámen")],), (1, 1, 1))
    c.returns(ns, "skore", ([],), (0, 0, 0))
    c.returns(ns, "skore", ([("papír", "kámen")] * 3,), (3, 0, 0))
    for vstup, kol in (("kámen\n", 1), ("blbost\nkámen\npapír\n", 2), ("nůžky\nnůžky\nnůžky\nnůžky\n", 4)):
        ok, v = c.call(ns, "hra", (kol,), stdin=vstup)
        spravne = ok and isinstance(v, tuple) and len(v) == 3 and sum(v) == kol
        c.add(f"hra({kol}) vrací skóre se součtem {kol}", spravne, f"Vrátila {v!r}. Očekávám n-tici tří čísel se součtem {kol}.")
    ok, v = c.call(ns, "hra", (1,), stdin="blbost\nkámen\n")
    c.add("hra: neplatný tah vypíše hlášku a kolo se nepočítá",
          ok and "Takový tah neexistuje." in c.last_output and sum(v) == 1, "Neplatný tah: vypište hlášku a ptejte se znovu.")
    c.add("hra: po kole se vypíše výsledek", any(t in c.last_output for t in ("Vyhráli jste.", "Vyhrál počítač.", "Remíza.")),
          "Po každém kole vypište Vyhráli jste., Vyhrál počítač. nebo Remíza.")
    f_hra = c.function("hra")
    c.add("hra používá funkci nahodny_tah", f_hra is not None and bool(c.calls_in(f_hra, "nahodny_tah")),
          "Tah počítače vezměte voláním nahodny_tah().")
    puvodni = ns.get("nahodny_tah")
    ns["nahodny_tah"] = lambda: "nůžky"
    for tah, ocek, zprava in (("kámen", (1, 0, 0), "Vyhráli jste."), ("papír", (0, 1, 0), "Vyhrál počítač."),
                              ("nůžky", (0, 0, 1), "Remíza.")):
        ok, v = c.call(ns, "hra", (1,), stdin=tah + "\n")
        c.add(f"hra: hráč {tah}, počítač nůžky vede ke skóre {ocek}", ok and v == ocek and zprava in c.last_output,
              f"Vrátila {v!r} a vypsala {c.last_output!r}. Očekávám skóre {ocek} a hlášku {zprava!r}.")
    ok, v = c.call(ns, "hra", (3,), stdin="kámen\nkámen\npapír\n")
    c.add("hra: tři kola se sečtou do skóre (2, 1, 0)", ok and v == (2, 1, 0), f"Vrátila {v!r}.")
    ns["nahodny_tah"] = puvodni
c.done()
