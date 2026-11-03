import ast
from dilna_check import check
c = check()
c.uses_call("input", "Hra se má ptát hráče pomocí input().")
_t = c.tree
c.add("Na konci je blok if __name__ == \"__main__\":",
      _t is not None and any(isinstance(n, ast.If) and "__name__" in ast.dump(n.test) for n in _t.body),
      "Spuštění hry dejte do bloku if __name__ == \"__main__\":")
ns = c.load()
P = {
    "Mars": {"vzdalenost": 228, "prumer": 6779},
    "Jupiter": {"vzdalenost": 778, "prumer": 139820},
    "Země": {"vzdalenost": 150, "prumer": 12742},
}
if ns is not None:
    c.returns(ns, "napoveda", (P, "Mars"), "Je 228 mil. km od Slunce a má průměr 6779 km.")
    c.returns(ns, "napoveda", (P, "Jupiter"), "Je 778 mil. km od Slunce a má průměr 139820 km.")
    ok, t = c.call(ns, "napoveda", (P, "Mars"))
    c.add("Nápověda neprozradí jméno planety", ok and "Mars" not in str(t), "Jméno planety se v nápovědě objevit nesmí.")
    c.returns(ns, "je_spravne", ("Mars", "Mars"), True)
    c.returns(ns, "je_spravne", ("  mars ", "Mars"), True)
    c.returns(ns, "je_spravne", ("Země", "Mars"), False)
    c.returns(ns, "je_spravne", ("", "Mars"), False)
    zvolene = set()
    chyba = None
    for _ in range(100):
        ok, v = c.call(ns, "vyber_planetu", (P,))
        if not ok:
            chyba = v
            break
        zvolene.add(v)
    c.add("vyber_planetu vrací jména ze slovníku", chyba is None and zvolene <= set(P),
          f"Použijte random.choice(list(planety)). {chyba!r}" if chyba else "Použijte random.choice(list(planety)).")
    c.add("vyber_planetu vybírá všechny planety", zvolene == set(P), "Každé volání musí losovat znovu z celého slovníku.")
    c.returns(ns, "pocet_pokusu", (["Země", "mars", "Jupiter"], "Mars"), 2)
    c.returns(ns, "pocet_pokusu", (["Mars"], "Mars"), 1)
    c.returns(ns, "pocet_pokusu", (["Země", "Jupiter"], "Mars"), None)
    c.returns(ns, "pocet_pokusu", ([], "Mars"), None)
    ok, v = c.call(ns, "hra", (P, "Mars"), stdin="Země\nJupiter\n mars \n")
    c.add("hra: tři pokusy se vrátí jako 3", ok and v == 3, f"Funkce hra má vrátit počet pokusů (3). Vrátila {v!r}.")
    c.add("hra vypíše Správně!", "Správně!" in c.last_output, "Po správném tipu vypište Správně!")
    c.add("hra vypíše Ne, zkuste to znovu.", c.last_output.count("Ne, zkuste to znovu.") == 2,
          "Po každém špatném tipu vypište Ne, zkuste to znovu.")
    c.add("hra ukáže nápovědu", "228 mil. km" in c.last_output and "6779 km" in c.last_output, "Na začátku hry vypište nápovědu.")
    ok, v = c.call(ns, "hra", (P, "Jupiter"), stdin="jupiter\n")
    c.add("hra ukáže nápovědu podle zvolené planety", "778 mil. km" in c.last_output and "139820 km" in c.last_output,
          "Nápověda se musí vypsat pro tutéž planetu, kterou se hádá.")
    ok, v = c.call(ns, "hra", (P, "Země"), stdin="Země\n")
    c.add("hra: správný tip hned napoprvé vrátí 1", ok and v == 1, f"Vrátila {v!r}.")
c.done()
