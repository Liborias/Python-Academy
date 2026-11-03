import os, sys
sys.path.insert(0, os.getcwd())
from dilna_web import spust
from dilna_check import check
import ast
import json
import requests
from pathlib import Path
c = check()
c.utf8()
c.imports("requests", "Použijte balíček requests.")
c.imports("bs4", "Použijte BeautifulSoup.")
fs = c.function("sber_cen")
c.add("sber_cen kontroluje robots.txt pomocí RobotFileParser", fs is not None and bool(c.calls_in(fs, "RobotFileParser")),
      "Pravidla čtěte pomocí RobotFileParser.")
c.add("sber_cen používá timeout a raise_for_status",
      fs is not None and bool(c.calls_in(fs, "raise_for_status")) and any(k.arg == "timeout" for call in c.calls_in(fs, "get") for k in call.keywords),
      "Použijte requests.get(..., timeout=...) a raise_for_status().")
c.add("sber_cen posílá User-Agent", fs is not None and any(k.arg == "headers" for call in c.calls_in(fs, "get") for k in call.keywords),
      "Do požadavku přidejte headers={\"User-Agent\": \"Dilna-Sberac/1.0\"}.")
_rg = [x for x in (c.calls_in(fs, "get") if fs is not None else []) if isinstance(x.func.value, ast.Name) and x.func.value.id == "requests"]
c.add("Všechny požadavky mají timeout", fs is not None and bool(_rg) and all(any(k.arg == "timeout" for k in call.keywords) for call in _rg),
      "Každé requests.get musí mít timeout=...")
ns = c.load()
if ns is not None:
    A = spust()
    k = [{"nazev": "A", "cena": 300, "skladem": True}, {"nazev": "B", "cena": 100, "skladem": False}, {"nazev": "C", "cena": 200, "skladem": True}]
    c.returns(ns, "nejlevnejsi", (k,), k[1])
    c.returns(ns, "nejlevnejsi", ([],), None)
    c.returns(ns, "prumerna_cena", (k,), 200.0)
    c.returns(ns, "prumerna_cena", ([{"nazev": "X", "cena": 10, "skladem": True}, {"nazev": "Y", "cena": 15, "skladem": True}],), 12.5)
    c.returns(ns, "prumerna_cena", ([],), 0)
    c.returns(ns, "prumerna_cena", ([{"nazev": "X", "cena": 10, "skladem": True}, {"nazev": "Y", "cena": 11, "skladem": True}, {"nazev": "Z", "cena": 11, "skladem": True}],), 10.7)
    ZAZN = []
    _orig = requests.get

    def _zaznam(url, *args, **kwargs):          # zapisuje, co student posílá, a pak dotaz opravdu provede
        ZAZN.append((url, kwargs))
        return _orig(url, *args, **kwargs)

    requests.get = _zaznam
    ok, v = c.call(ns, "sber_cen", (A, "vysledek.json"))
    c.add("Nejdřív se čte robots.txt, až potom stránka", len(ZAZN) >= 2 and ZAZN[0][0].endswith("/robots.txt") and ZAZN[1][0].endswith("/knihy.html"),
          f"Pořadí dotazů: {[u for u, _ in ZAZN]!r}.")
    c.add("Všechny dotazy se představují jako Dilna-Sberac/1.0",
          bool(ZAZN) and all((k.get("headers") or {}).get("User-Agent") == "Dilna-Sberac/1.0" for _, k in ZAZN),
          "Do každého requests.get přidejte headers={\"User-Agent\": \"Dilna-Sberac/1.0\"}.")
    ocek = {"pocet": 3, "nejlevnejsi": "Kuchařka pro líné", "prumer": 245.7,
            "knihy": [{"nazev": "Lesní stezka", "cena": 249, "skladem": True}, {"nazev": "Kuchařka pro líné", "cena": 199, "skladem": True},
                      {"nazev": "Hvězdy nad Šumavou", "cena": 289, "skladem": True}]}
    c.add("sber_cen vrací správný výsledek", ok and v == ocek, f"Vrátila {v!r}.")
    try:
        text = Path("vysledek.json").read_text(encoding="utf-8")
        data = json.loads(text)
    except Exception:
        text, data = "", None
    c.add("JSON soubor obsahuje stejný výsledek", data == ocek, f"V souboru je {data!r}.")
    c.add("Čeština v JSON je čitelná", "Šumavou" in text, "Použijte ensure_ascii=False.")
    ZAZN.clear()
    ok, v = c.call(ns, "sber_cen", (A, "zakazano.json", "/soukrome/knihy.html"))
    c.add("Zakázaná stránka se vůbec nepožaduje", not any(u.endswith("/soukrome/knihy.html") for u, _ in ZAZN), "Zakázanou stránku nestahujte ani „jen na zkoušku“.")
    c.add("Zakázaná cesta: vrací None a nic se neukládá", ok and v is None and not Path("zakazano.json").exists(),
          "robots.txt zakazuje /soukrome/. Funkce nesmí stránku stáhnout.")
    ok, v = c.call(ns, "sber_cen", (A, "chyba.json", "/neexistuje.html"))
    c.add("Chyba 404: vrací None a nevytvoří soubor", ok and v is None and not Path("chyba.json").exists(), "Použijte raise_for_status.")
    ok, v = c.call(ns, "sber_cen", ("http://127.0.0.1:1", "chyba2.json"))
    c.add("Nedostupný server: vrací None", ok and v is None and not Path("chyba2.json").exists(), "Zachyťte requests.RequestException.")
c.done()
