import ast
from pathlib import Path
from dilna_check import check
c = check()
c.utf8()
for _jmeno in ("nacti_bezpecne", "nacti_cisla_bezpecne"):
    _f = c.function(_jmeno)
    c.add(f"Funkce {_jmeno} zachytává chyby pomocí try a except",
          _f is not None and any(isinstance(n, ast.Try) for n in ast.walk(_f)),
          f"Ve funkci {_jmeno} použijte try a except.")
ns = c.load()
if ns is not None:
    with open("hezky.txt", "w", encoding="utf-8") as f:
        f.write("Příliš žluťoučký kůň\n")
    Path("slozka").mkdir(exist_ok=True)
    c.returns(ns, "nacti_bezpecne", ("hezky.txt",), "Příliš žluťoučký kůň\n")
    c.returns(ns, "nacti_bezpecne", ("chybi.txt",), "")
    c.returns(ns, "nacti_bezpecne", ("chybi.txt", "nic"), "nic")
    c.returns(ns, "nacti_bezpecne", ("slozka", "je to složka"), "je to složka")
    c.returns(ns, "nacti_cisla_bezpecne", ("ok.txt",), [10, 20, 30])
    c.returns(ns, "nacti_cisla_bezpecne", ("teploty.txt",), [5, -2, 8])
    c.returns(ns, "nacti_cisla_bezpecne", ("chybi.txt",), [])
    c.returns(ns, "nacti_cisla_bezpecne", ("slozka",), [])
    c.returns(ns, "nacti_cisla_bezpecne", ("hezky.txt",), [])
    ok, v = c.call(ns, "zaloha", ("hezky.txt",))
    c.add("zaloha vrací True a vytvoří .bak", ok and v is True and Path("hezky.txt.bak").is_file()
          and Path("hezky.txt.bak").read_text(encoding="utf-8") == "Příliš žluťoučký kůň\n", f"Vrátila {v!r}.")
    ok, v = c.call(ns, "zaloha", ("neni.txt",))
    c.add("zaloha pro chybějící soubor vrací False a nic nevytvoří", ok and v is False and not Path("neni.txt.bak").exists(),
          "Když soubor neexistuje, vraťte False a nevytvářejte .bak.")
c.done()
