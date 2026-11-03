import ast
import json
import shutil
from dilna_check import check
c = check()
c.imports("json", "Použijte modul json.")
c.utf8()
_f = c.function("nacti_kontakty")
c.add("Funkce nacti_kontakty zachytává chybějící soubor pomocí try a except",
      _f is not None and any(isinstance(n, ast.Try) for n in ast.walk(_f)),
      "Chybějící soubor ošetřete pomocí try a except.")
ns = c.load()
if ns is not None:
    K = [{"jmeno": "Eva Nováková", "telefon": "777111222", "email": "eva@example.com"},
         {"jmeno": "Petr Svoboda", "telefon": "602333444", "email": ""},
         {"jmeno": "Šárka Dvořáková", "telefon": "731555666", "email": "sarka@example.com"}]
    c.returns(ns, "nacti_kontakty", ("kontakty.json",), K)
    c.returns(ns, "nacti_kontakty", ("neni.json",), [])
    c.returns(ns, "najdi", ("kontakty.json", "VA"), [K[0]])
    c.returns(ns, "najdi", ("kontakty.json", "o"), [K[0], K[1], K[2]])
    c.returns(ns, "najdi", ("kontakty.json", "xyz"), [])
    c.returns(ns, "najdi", ("kontakty.json", "example"), [])   # e-mail se nehledá
    c.returns(ns, "najdi", ("kontakty.json", "602"), [])       # telefon se nehledá
    shutil.copy("kontakty.json", "k1.json")
    c.returns(ns, "pridej_kontakt", ("k1.json", "Jan Dlouhý", "123456789"), True)
    c.returns(ns, "pridej_kontakt", ("k1.json", "jan dlouhý", "999"), False)
    c.returns(ns, "pridej_kontakt", ("k1.json", "Žaneta", "1", "z@example.com"), True)
    c.returns(ns, "nacti_kontakty", ("k1.json",), K + [{"jmeno": "Jan Dlouhý", "telefon": "123456789", "email": ""},
                                                       {"jmeno": "Žaneta", "telefon": "1", "email": "z@example.com"}])
    with open("k1.json", "rb") as f:
        surove = f.read().decode("utf-8")
    c.add("Soubor je uložený čitelně (čeština, odsazení 2)", "Žaneta" in surove and '\n  {' in surove,
          "Uložte soubor s ensure_ascii=False a indent=2.")
    shutil.copy("kontakty.json", "k2.json")
    c.returns(ns, "smaz_kontakt", ("k2.json", "petr svoboda"), True)
    c.returns(ns, "smaz_kontakt", ("k2.json", "Petr Svoboda"), False)
    c.returns(ns, "smaz_kontakt", ("k2.json", "Eva"), False)
    c.returns(ns, "nacti_kontakty", ("k2.json",), [K[0], K[2]])
    c.returns(ns, "vypis", ("kontakty.json",), "Eva Nováková: 777111222\nPetr Svoboda: 602333444\nŠárka Dvořáková: 731555666")
    c.returns(ns, "vypis", ("neni.json",), "Žádné kontakty.")
    with open("k3.json", "w", encoding="utf-8") as f:
        json.dump([{"jmeno": "Zdenek", "telefon": "2", "email": ""}, {"jmeno": "Adam", "telefon": "1", "email": ""}], f)
    c.returns(ns, "vypis", ("k3.json",), "Adam: 1\nZdenek: 2")
c.done()
