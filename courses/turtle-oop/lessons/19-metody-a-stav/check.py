from dilna_check import check
c = check()
c.defines_class("Pocitadlo")
ns = c.load()
cls = (ns or {}).get("Pocitadlo")
c.add("Pocitadlo je třída", isinstance(cls, type), "Definujte class Pocitadlo.")
if ns is not None and isinstance(cls, type):
    try:
        ok_a, a = c.call(ns, "Pocitadlo")
        ok_b, b = c.call(ns, "Pocitadlo", (7,))
        ok_c, d = c.call(ns, "Pocitadlo", (-2,))
        valid = ok_a and ok_b and ok_c and all(isinstance(x, cls) for x in (a, b, d))
        c.add("Počítadla lze vytvořit", valid, "Konstruktor má výchozí začátek 0 i možnost zadat jiné celé číslo.")
        if valid:
            c.add("Počáteční hodnoty", [getattr(x, "hodnota", None) for x in (a, b, d)] == [0, 7, -2], "Uložte argument do self.hodnota.")
            for obj, kolik, ocek in [(a, 4, 4), (a, -3, 1), (a, 0, 1), (b, 5, 12), (d, 2, 0)]:
                ok, vysledek = c.call({"metoda": getattr(obj, "pridej", None)}, "metoda", (kolik,))
                c.add("Přičtení mění stav a vrací výsledek", ok and vysledek == ocek and getattr(obj, "hodnota", None) == ocek,
                      "Přičítejte k dosavadní hodnotě, uložte změnu a vraťte novou hodnotu.")
            ok, vysledek = c.call({"metoda": getattr(b, "vynuluj", None)}, "metoda")
            c.add("Vynulování", ok and vysledek is None and getattr(b, "hodnota", None) == 0, "Nastavte hodnota = 0, metoda vrací None.")
            ok, vysledek = c.call({"metoda": getattr(b, "pridej", None)}, "metoda", (9,))
            c.add("Pokračování po vynulování", ok and vysledek == 9 and getattr(b, "hodnota", None) == 9, "Po resetu přičítejte od nuly.")
            c.add("Nezávislé instance", getattr(a, "hodnota", None) == 1 and getattr(d, "hodnota", None) == 0,
                  "Metody mění stav pouze své instance.")
    except BaseException as exc:
        c.add("Práce s objekty bez chyby", False, f"Při ověření metod vznikla chyba {type(exc).__name__}: {exc}")
c.done()
