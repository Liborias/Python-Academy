import ast
import json
from dilna_check import check
c = check()
c.imports("json", "Použijte modul json.")
c.utf8()
_f = c.function("nastav_hodnotu")
c.add("Funkce nastav_hodnotu zachytává chybějící soubor pomocí try a except",
      _f is not None and any(isinstance(n, ast.Try) for n in ast.walk(_f)),
      "Chybějící soubor ošetřete pomocí try a except.")
ns = c.load()
if ns is not None:
    c.returns(ns, "nacti_json", ("profil.json",), {"jmeno": "Eva", "vek": 31, "mesto": "Plzeň", "zajmy": ["šachy", "kolo"]})
    c.returns(ns, "nacti_json", ("ukoly.json",), [{"text": "uklidit", "hotovo": True}, {"text": "uvařit", "hotovo": False},
                                                  {"text": "nakoupit", "hotovo": True}])
    c.returns(ns, "pocet_hotovych", ("ukoly.json",), 2)
    with open("u2.json", "w", encoding="utf-8") as f:
        f.write('[{"text": "a", "hotovo": false}]')
    c.returns(ns, "pocet_hotovych", ("u2.json",), 0)
    c.call(ns, "uloz_json", ("v.json", {"mesto": "Příbram", "seznam": [1, 2]}))
    try:
        with open("v.json", "rb") as f:
            surove = f.read().decode("utf-8")
        c.add("uloz_json: čeština je čitelná", "Příbram" in surove, "Použijte ensure_ascii=False.")
        c.add("uloz_json: zápis je odsazený po dvou mezerách", '\n  "mesto"' in surove, "Použijte indent=2.")
        c.add("uloz_json: data se dají načíst zpět", json.loads(surove) == {"mesto": "Příbram", "seznam": [1, 2]}, "Zapsaná data nejsou platný JSON.")
    except (OSError, UnicodeDecodeError, ValueError) as e:
        c.add("uloz_json vytvoří platný soubor", False, f"{type(e).__name__}: {e}")
    c.returns(ns, "nastav_hodnotu", ("novy_profil.json", "jmeno", "Ondřej"), {"jmeno": "Ondřej"})
    c.returns(ns, "nastav_hodnotu", ("novy_profil.json", "vek", 40), {"jmeno": "Ondřej", "vek": 40})
    c.returns(ns, "nastav_hodnotu", ("novy_profil.json", "jmeno", "Zuzana"), {"jmeno": "Zuzana", "vek": 40})
    c.returns(ns, "nacti_json", ("novy_profil.json",), {"jmeno": "Zuzana", "vek": 40})
c.done()
