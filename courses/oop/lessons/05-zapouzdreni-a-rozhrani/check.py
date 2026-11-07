import ast
from dilna_check import check

c = check()
c.defines_class("Zasoba")
ns = c.load()
cls = (ns or {}).get("Zasoba")
node = next((n for n in (c.tree.body if c.tree else []) if isinstance(n, ast.ClassDef) and n.name == "Zasoba"), None)
c.add("Vnitřní údaj má podtržítko", node is not None and any(isinstance(n, ast.Attribute) and isinstance(n.ctx, ast.Store)
      and n.attr.startswith("_") for n in ast.walk(node)), "Pro vnitřní stav použijte instanční atribut s podtržítkem.")
try:
    if ns is not None and isinstance(cls, type):
        records = []
        for name, start in [("Knihy", 5), ("Žluté obaly", 0), ("Dárky", 11)]:
            obj = cls(name, start)
            expected = start
            for method, amount in [("prijmi", 3), ("vydej", 1), ("prijmi", 2), ("vydej", start + 4), ("prijmi", 4)]:
                for _ in range(2):
                    ok, value = c.call({"stav": obj.stav}, "stav")
                    c.add("Stav čte aktuální počet", ok and value == expected and c.last_output == "",
                          "Vraťte aktuální vnitřní počet bez výpisu nebo změny.")
                expected += amount if method == "prijmi" else -amount
                ok, value = c.call({"operace": getattr(obj, method)}, "operace", (amount,))
                c.add("Operace změní stav a vrátí počet", ok and value == expected and obj.stav() == expected and c.last_output == "",
                      "Příjem přičítá, výdej odečítá; oba vracejí nový stav.")
                c.add("Název zůstává", obj.nazev == name, "Množstevní operace nemění název.")
            records.append((obj, name, expected))
        default = cls("Prázdná zásoba")
        c.add("Výchozí počet je nula", default.stav() == 0, "Ponechte výchozí počet 0.")
        for obj, name, expected in records:
            c.add("Zásoby jsou nezávislé", obj.nazev == name and obj.stav() == expected,
                  "Množství patří konkrétní instanci, ne společnému třídnímu atributu.")
    else:
        c.add("Zasoba je třída", False, "Definujte třídu Zasoba.")
except BaseException as exc:
    c.add("Rozhraní zásoby lze ověřit", False, f"{type(exc).__name__}: {exc}")
c.done()
