from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def stahni_soubor(url, cil):
    try:
        odpoved = requests.get(url, timeout=3)
        odpoved.raise_for_status()
    except requests.RequestException:
        return None
    with open(cil, "wb") as soubor:
        soubor.write(odpoved.content)
    return len(odpoved.content)


def stahni_obrazky(url_stranky, slozka):
    Path(slozka).mkdir(exist_ok=True)
    odpoved = requests.get(url_stranky, timeout=3)
    soup = BeautifulSoup(odpoved.text, "html.parser")
    jmena = []
    for img in soup.find_all("img", src=True):
        url = urljoin(url_stranky, img["src"])
        jmeno = url.rsplit("/", 1)[1]
        if stahni_soubor(url, Path(slozka) / jmeno) is not None:
            jmena.append(jmeno)
    return jmena
