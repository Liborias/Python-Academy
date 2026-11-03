import os, sys
sys.path.insert(0, os.getcwd())
from dilna_web import spust
from dilna_check import check
import csv
from pathlib import Path
c = check()
c.utf8()
c.imports("requests", "Použijte balíček requests.")
c.imports("bs4", "Použijte BeautifulSoup.")
fs = c.function("stahni_knihy")
c.add("stahni_knihy volá obě pomocné funkce",
      fs is not None and bool(c.calls_in(fs, "ziskej_knihy")) and bool(c.calls_in(fs, "uloz_csv")),
      "Ve stahni_knihy využijte ziskej_knihy a uloz_csv.")
ns = c.load()
if ns is not None:
    A = spust()
    with open("web/knihy.html", encoding="utf-8") as f:
        S = f.read()
    ocekavane = [
        {"nazev": "Lesní stezka", "autor": "Jana Novotná", "cena": 249, "skladem": True},
        {"nazev": "Půlnoční vlak", "autor": "Petr Dvořák", "cena": 329, "skladem": False},
        {"nazev": "Kuchařka pro líné", "autor": "Eva Králová", "cena": 199, "skladem": True},
        {"nazev": "Hvězdy nad Šumavou", "autor": "Marek Svoboda", "cena": 289, "skladem": True},
    ]
    c.returns(ns, "ziskej_knihy", (S,), ocekavane)
    c.returns(ns, "ziskej_knihy", ("<p>nic</p>",), [])
    c.returns(ns, "ziskej_knihy", ('<li class="kniha"><span class="nazev">X</span><span class="autor">Y</span><span class="cena">5 Kč</span></li>',),
              [{"nazev": "X", "autor": "Y", "cena": 5, "skladem": True}])
    ok, v = c.call(ns, "uloz_csv", (ocekavane[:2], "test.csv"))
    radky = []
    if Path("test.csv").is_file():
        with open("test.csv", encoding="utf-8", newline="") as f:
            radky = list(csv.reader(f))
    c.add("uloz_csv zapíše hlavičku a řádky",
          ok and radky == [["nazev", "autor", "cena", "skladem"], ["Lesní stezka", "Jana Novotná", "249", "ano"],
                           ["Půlnoční vlak", "Petr Dvořák", "329", "ne"]],
          f"Soubor obsahuje: {radky!r}")
    ok, v = c.call(ns, "stahni_knihy", (A + "/knihy.html", "knihy.csv"))
    radky = []
    if Path("knihy.csv").is_file():
        with open("knihy.csv", encoding="utf-8", newline="") as f:
            radky = list(csv.DictReader(f))
    c.add("stahni_knihy vrací počet knih", ok and v == 4, f"Vrátila {v!r}, čekáme 4.")
    ok2, v2 = c.call(ns, "stahni_knihy", (A + "/knihy.html", "jine_jmeno.csv"))
    c.add("stahni_knihy uloží do zadaného souboru", ok2 and v2 == 4 and Path("jine_jmeno.csv").is_file(), "Název souboru bere funkce z parametru nazev_csv.")
    c.add("knihy.csv obsahuje všechny knihy", [r.get("nazev") for r in radky] == [k["nazev"] for k in ocekavane]
          and [r.get("skladem") for r in radky] == ["ano", "ne", "ano", "ano"], f"V souboru je {radky!r}")
    ok, v = c.call(ns, "stahni_knihy", (A + "/_status/404", "chyba.csv"))
    c.add("Při chybě stahování se vrací 0 a nevzniká soubor", ok and v == 0 and not Path("chyba.csv").exists(),
          f"Vrátila {v!r}; soubor chyba.csv nesmí vzniknout.")
    ok, v = c.call(ns, "stahni_knihy", ("http://127.0.0.1:1/", "chyba2.csv"))
    c.add("Nepřipojení se také ošetří", ok and v == 0 and not Path("chyba2.csv").exists(), "Zachyťte requests.RequestException.")
c.done()
