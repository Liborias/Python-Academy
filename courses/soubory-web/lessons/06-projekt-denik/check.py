import ast
from dilna_check import check
c = check()
c.utf8()
_f = c.function("nacti_zapisy")
c.add("Funkce nacti_zapisy zachytává chybějící soubor pomocí try a except",
      _f is not None and any(isinstance(n, ast.Try) for n in ast.walk(_f)),
      "Chybějící soubor ošetřete ve funkci nacti_zapisy pomocí try a except.")
ns = c.load()
if ns is not None:
    D = [("2026-10-20", "Začal jsem se učit Python"), ("2026-10-21", "Nákup: chleba a mléko"),
         ("2026-10-21", "Napsal jsem první program se soubory"), ("2026-10-23", "Python je zábava"),
         ("2026-10-24", "Zítra odevzdat úkol")]
    c.returns(ns, "nacti_zapisy", ("denik.txt",), D)
    c.returns(ns, "nacti_zapisy", ("chybi.txt",), [])
    c.returns(ns, "hledej", ("denik.txt", "python"), [D[0], D[3]])
    c.returns(ns, "hledej", ("denik.txt", "NÁKUP"), [D[1]])
    c.returns(ns, "hledej", ("denik.txt", "zebra"), [])
    c.returns(ns, "hledej", ("denik.txt", "2026"), [])         # datum se nehledá
    c.returns(ns, "zapisy_podle_dne", ("denik.txt",), {"2026-10-20": 1, "2026-10-21": 2, "2026-10-23": 1, "2026-10-24": 1})
    c.returns(ns, "zapisy_podle_dne", ("chybi.txt",), {})
    c.call(ns, "pridej_zapis", ("novy.txt", "2026-11-01", "Příliš žluťoučký kůň"))
    c.call(ns, "pridej_zapis", ("novy.txt", "2026-11-01", "a | b"))
    with open("novy.txt", "rb") as f:
        surove = f.read().decode("utf-8")
    c.add("pridej_zapis: řádky ve tvaru datum | text", surove == "2026-11-01 | Příliš žluťoučký kůň\n2026-11-01 | a | b\n",
          f"V souboru je {surove!r}.")
    c.returns(ns, "nacti_zapisy", ("novy.txt",), [("2026-11-01", "Příliš žluťoučký kůň"), ("2026-11-01", "a | b")])
    with open("divny.txt", "w", encoding="utf-8") as f:
        f.write("bez oddelovace\n\n2026-01-01 | ok\n   \n")
    c.returns(ns, "nacti_zapisy", ("divny.txt",), [("2026-01-01", "ok")])
c.done()
