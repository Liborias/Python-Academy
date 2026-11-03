from dilna_check import check
c = check()
c.uses_call("input", "Funkce hlavni má načíst text pomocí input().")
ns = c.load()
if ns is not None:
    c.returns(ns, "analyzuj_text", ("Ahoj, světe! Ahoj python",),
              {"slov": 4, "unikatnich": 3, "nejdelsi": "python", "prumerna_delka": 4.8})
    c.returns(ns, "analyzuj_text", ("",), {"slov": 0, "unikatnich": 0, "nejdelsi": "", "prumerna_delka": 0})
    c.returns(ns, "analyzuj_text", ("... !!! ,",), {"slov": 0, "unikatnich": 0, "nejdelsi": "", "prumerna_delka": 0})
    c.returns(ns, "analyzuj_text", ("pes KOCKA kun",), {"slov": 3, "unikatnich": 3, "nejdelsi": "kocka", "prumerna_delka": 3.7})
    c.returns(ns, "analyzuj_text", ("ahoj; svete:",), {"slov": 2, "unikatnich": 2, "nejdelsi": "svete", "prumerna_delka": 4.5})
    c.returns(ns, "analyzuj_text", ("A a A.",), {"slov": 3, "unikatnich": 1, "nejdelsi": "a", "prumerna_delka": 1.0})
    c.returns(ns, "analyzuj_text", ("ab cd ef",), {"slov": 3, "unikatnich": 3, "nejdelsi": "ab", "prumerna_delka": 2.0})
    c.returns(ns, "popis_analyzy", ({"slov": 6, "unikatnich": 5, "nejdelsi": "python", "prumerna_delka": 4.2},),
              "Slov: 6\nUnikátních: 5\nNejdelší: python\nPrůměrná délka: 4.2")
    c.returns(ns, "popis_analyzy", ({"slov": 1, "unikatnich": 1, "nejdelsi": "a", "prumerna_delka": 1.0},),
              "Slov: 1\nUnikátních: 1\nNejdelší: a\nPrůměrná délka: 1.0")
    ok, v = c.call(ns, "hlavni", (), stdin="Ahoj ahoj svete\n")
    c.add("hlavni vypíše popis rozboru", ok and "Slov: 3" in c.last_output and "Unikátních: 2" in c.last_output
          and "Nejdelší: svete" in c.last_output, f"Výstup: {c.last_output!r}")
c.done()
