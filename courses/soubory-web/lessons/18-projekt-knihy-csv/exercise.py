import csv
import requests
from bs4 import BeautifulSoup

# Úkol (stránka knihy.html je na místním serveru, viz lekce 16):
#   ziskej_knihy(html)             -> seznam slovníků {"nazev", "autor", "cena" (int), "skladem" (bool)}
#                                     pro každou knihu na stránce (bez poštovného v patičce)
#   uloz_csv(knihy, nazev)         -> zapíše knihy do CSV se sloupci nazev, autor, cena, skladem
#                                     (skladem jako "ano" / "ne")
#   stahni_knihy(url, nazev_csv)   -> stáhne stránku, zpracuje ji, uloží CSV a vrátí počet knih;
#                                     při chybě stahování vrátí 0 a soubor nevytvoří
