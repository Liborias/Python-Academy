import json
from urllib.request import urlopen
from kviz_data import nacti_soubor, preved_otazky

API_URL = "https://opentdb.com/api.php?amount=5&type=boolean"
MAX_BAJTU = 65_536


def stahni_json(url):
    # Timeout 5 s, nejvýš MAX_BAJTU + 1 bajtů, UTF-8 a JSON.
    pass


def ziskej_otazky(online=False, cesta="otazky.json", stahni=stahni_json):
    # Offline nevolá síť. Selhání API použije soubor a přizná důvod.
    pass


if __name__ == "__main__":
    otazky, zdroj, zprava = ziskej_otazky()
    print("Zdroj:", zdroj)
    print("Počet otázek:", len(otazky))
