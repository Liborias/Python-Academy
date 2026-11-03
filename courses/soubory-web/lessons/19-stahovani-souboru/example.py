from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from dilna_web import spust

adresa = spust()
stranka = adresa + "/galerie.html"

soup = BeautifulSoup(requests.get(stranka, timeout=3).text, "html.parser")
Path("stazene").mkdir(exist_ok=True)                  # složka pro soubory; exist_ok=True nehlásí chybu, když už je

for img in soup.find_all("img", src=True):            # jen značky, které mají src
    url = urljoin(stranka, img["src"])                # z "img/a.png" udělá úplnou adresu
    odpoved = requests.get(url, timeout=3)
    odpoved.raise_for_status()                        # při chybě se nic nezapíše
    cil = Path("stazene") / url.rsplit("/", 1)[1]     # např. stazene/a.png
    cil.write_bytes(odpoved.content)                  # binární zápis: obrázek není text
    print(cil.name, cil.stat().st_size, "bajtů")
