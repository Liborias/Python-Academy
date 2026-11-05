import json
from urllib.request import urlopen
from kviz_data import nacti_soubor, preved_otazky

API_URL = "https://opentdb.com/api.php?amount=5&type=boolean"
MAX_BAJTU = 65_536


def stahni_json(url):
    with urlopen(url, timeout=5) as odpoved:
        obsah = odpoved.read(MAX_BAJTU + 1)
    if len(obsah) > MAX_BAJTU:
        raise ValueError("Odpověď je příliš velká")
    return json.loads(obsah.decode("utf-8"))


def ziskej_otazky(online=False, cesta="otazky.json", stahni=stahni_json):
    if not online:
        return nacti_soubor(cesta), "offline", ""
    try:
        otazky = preved_otazky(stahni(API_URL))
        return otazky, "API", ""
    except (OSError, ValueError) as chyba:
        return nacti_soubor(cesta), "záloha", f"API nelze použít: {chyba}"


if __name__ == "__main__":
    otazky, zdroj, zprava = ziskej_otazky()
    print("Zdroj:", zdroj)
    print("Počet otázek:", len(otazky))
