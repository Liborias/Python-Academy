import ast
import csv
from dilna_check import check
c = check()
c.imports("csv", "Použijte modul csv.")
c.utf8()
otevreni = [n for n in c._walk() if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "open"]
c.add('Soubory se otevírají s newline=""', bool(otevreni) and all(any(k.arg == "newline" for k in n.keywords) for n in otevreni),
      'Při práci s csv otevírejte soubor s newline="".')
ns = c.load()
if ns is not None:
    Z = [{"jmeno": "Eva", "trida": "3A", "body": 85}, {"jmeno": "Petr", "trida": "3B", "body": 62},
         {"jmeno": "Jana", "trida": "3A", "body": 91}, {"jmeno": "Karel", "trida": "3B", "body": 78}]
    c.returns(ns, "nacti_zaky", ("zaci.csv",), Z)
    c.returns(ns, "nejlepsi_zak", ("zaci.csv",), "Jana")
    c.returns(ns, "prumer_podle_trid", ("zaci.csv",), {"3A": 88.0, "3B": 70.0})
    with open("jiny.csv", "w", encoding="utf-8", newline="") as f:
        f.write("jmeno,trida,body\nŠárka,1A,5\nOndřej,1A,50\nZdeněk,2B,7\n")
    c.returns(ns, "nejlepsi_zak", ("jiny.csv",), "Ondřej")
    c.returns(ns, "prumer_podle_trid", ("jiny.csv",), {"1A": 27.5, "2B": 7.0})
    nove = [{"jmeno": "Šárka", "trida": "1A", "body": 5}, {"jmeno": "Ondřej, ml.", "trida": "2B", "body": 50}]
    c.call(ns, "uloz_zaky", ("vystup.csv", nove))
    try:
        with open("vystup.csv", encoding="utf-8", newline="") as f:
            radky = f.read().splitlines()
        c.add("uloz_zaky: hlavička jmeno,trida,body", bool(radky) and radky[0] == "jmeno,trida,body", f"První řádek je {radky[:1]!r}.")
        with open("vystup.csv", encoding="utf-8", newline="") as f:
            zpet = list(csv.DictReader(f))
        c.add("uloz_zaky: data se dají přečíst zpět", zpet == [{k: str(v) for k, v in z.items()} for z in nove], f"Přečteno: {zpet!r}.")
    except (OSError, UnicodeDecodeError) as e:
        c.add("uloz_zaky vytvoří soubor", False, f"{type(e).__name__}: {e}")
c.done()
