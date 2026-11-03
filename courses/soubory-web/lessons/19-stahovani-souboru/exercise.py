from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

# Úkol:
#   stahni_soubor(url, cil)
#       -> stáhne soubor z adresy do souboru `cil` a vrátí počet stažených bajtů;
#          při chybě vrátí None a soubor nevytvoří
#   stahni_obrazky(url_stranky, slozka)
#       -> stáhne všechny obrázky (img se src) ze stránky do složky `slozka` (vytvoří ji)
#          a vrátí seznam jmen uložených souborů v pořadí na stránce, např. ["a.png", "b.png"]
