import os
import sys
from collections import Counter
sys.path.insert(0, os.getcwd())
from dilna_check import check
from polozka import Polozka

c = check()
c.defines_class("Objednavka")
ns = c.load()
cls = (ns or {}).get("Objednavka")
c.add("Objednavka je třída", isinstance(cls, type), "Ponechte definici Objednavka.")
try:
    if ns is not None and isinstance(cls, type):
        first, second = cls("OBJ-žlutá"), cls("OBJ-002")
        c.add("Počáteční nezávislé seznamy", first.cislo == "OBJ-žlutá" and second.cislo == "OBJ-002"
              and isinstance(first.polozky, list) and isinstance(second.polozky, list)
              and first.polozky == second.polozky == [] and first.polozky is not second.polozky,
              "Každý konstruktor vytváří vlastní prázdný seznam.")
        ok, value = c.call({"celkem": first.celkem}, "celkem")
        c.add("Prázdná objednávka stojí nula", ok and value == 0, "Začněte součtem nula.")
        book, wrap, gift = Polozka("Kniha", 250), Polozka("Obal", 30, 2), Polozka("Dárek", 0, 3)
        expected = []
        for item in [book, wrap, book, gift]:
            expected.append(item)
            ok, value = c.call({"pridej": first.pridej}, "pridej", (item,))
            c.add("Přidání vrací počet řádků", ok and value == len(expected) and c.last_output == "",
                  "Přidejte předaný objekt a vraťte počet řádků, ne počet kusů.")
            c.add("Odkazy a pořadí se uchovají", len(first.polozky) == len(expected)
                  and all(a is b for a, b in zip(first.polozky, expected)), "Nevytvářejte kopie položek a zachovejte i opakovaný řádek.")
            c.add("Druhá objednávka je prázdná", second.polozky == [], "Seznamy různých objednávek nesdílejte.")
        for change in [lambda: None, lambda: book.pridej(2), lambda: setattr(book, "cena_za_kus", 99)]:
            change()
            wanted = sum(p.cena_za_kus * p.pocet for p in expected)
            state = [(id(p), p.nazev, p.cena_za_kus, p.pocet) for p in expected]
            for _ in range(2):
                ok, value = c.call({"celkem": first.celkem}, "celkem")
                c.add("Součet používá aktuální položky", ok and value == wanted and c.last_output == "",
                      "Po změně sdílené položky přepočítejte součet.")
                c.add("Čtení nezměnilo data", [(id(p), p.nazev, p.cena_za_kus, p.pocet) for p in first.polozky] == state,
                      "Součet nesmí upravovat řádky nebo položky.")
        for _ in range(2):
            ok, view = c.call({"prehled": first.prehled}, "prehled")
            valid = ok and isinstance(view, list) and view is not first.polozky and len(view) == len(expected)
            c.add("Přehled má nový seznam a stejné objekty", valid and all(a is b for a, b in zip(view, expected)),
                  "Vraťte mělkou kopii seznamu, zachovejte pořadí a identity položek.")
            if valid:
                view.clear()
                c.add("Úprava přehledu nemění řádky objednávky", first.polozky == expected,
                      "Nevracejte původní seznam přímo.")
        original = Polozka.celkem
        calls = []
        prices = {id(book): 17, id(wrap): 41, id(gift): 0}
        def changed(item):
            calls.append(id(item))
            return prices[id(item)]
        try:
            Polozka.celkem = changed
            ok, value = c.call({"celkem": first.celkem}, "celkem")
            c.add("Objednávka využívá metody položek", ok and value == sum(prices[id(p)] for p in expected)
                  and Counter(calls) == Counter(id(p) for p in expected),
                  "Každý řádek požádá svou položku o celkem; neopisujte její vnitřní výpočet.")
        finally:
            Polozka.celkem = original
        ok, value = c.call({"celkem": second.celkem}, "celkem")
        c.add("Prázdná druhá objednávka zůstala nezávislá", ok and value == 0 and second.polozky == [],
              "Změny první objednávky se nepřenášejí do druhé.")
except BaseException as exc:
    c.add("Objednávku lze ověřit", False, f"{type(exc).__name__}: {exc}")
c.done()
