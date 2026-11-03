import ast
from dilna_check import check
c = check()
c.imports("csv", "Použijte modul csv.")
c.utf8()
otevreni = [n for n in c._walk() if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "open"]
c.add('Soubory se otevírají s newline=""', bool(otevreni) and all(any(k.arg == "newline" for k in n.keywords) for n in otevreni),
      'Při práci s csv otevírejte soubor s newline="".')
ns = c.load()
if ns is not None:
    c.returns(ns, "hlavicka", ("znamky.csv",), ["jmeno", "matematika", "cestina", "dejepis"])
    c.returns(ns, "hlavicka", ("ceny.csv", ";"), ["zbozi", "cena", "jednotka"])
    c.returns(ns, "nacti_radky", ("znamky.csv",), [["Eva", "1", "2", "1"], ["Petr", "3", "2", "2"], ["Jana", "2", "1", "1"]])
    c.returns(ns, "nacti_radky", ("ceny.csv", ";"), [["Mléko", "25", "litr"], ["Chléb", "40", "kus"], ["Máslo", "60", "kus"]])
    c.returns(ns, "sloupec", ("znamky.csv", 0), ["Eva", "Petr", "Jana"])
    c.returns(ns, "sloupec", ("ceny.csv", 2, ";"), ["litr", "kus", "kus"])
    c.returns_close(ns, "prumer_sloupce", ("znamky.csv", 1), 2.0)
    c.returns_close(ns, "prumer_sloupce", ("znamky.csv", 3), 4 / 3)
    c.returns_close(ns, "prumer_sloupce", ("ceny.csv", 1, ";"), 125 / 3)
    with open("citaty.csv", "w", encoding="utf-8", newline="") as f:
        f.write('autor,veta\nEva,"Ahoj, svete"\nPetr,"Řekl: ""dobře"""\n')
    c.returns(ns, "nacti_radky", ("citaty.csv",), [["Eva", "Ahoj, svete"], ["Petr", 'Řekl: "dobře"']])
c.done()
