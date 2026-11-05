# Ukázka API je simulace z přiloženého JSON, žádný požadavek na internet.
# Stejná funkce se zkouší při úspěchu i výpadku služby.
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
    from pathlib import Path

    def ukazkovy_server(url):
        return json.loads(Path("api_ukazka.json").read_text(encoding="utf-8"))

    def vypadek(url):
        raise OSError("Ukázkový výpadek spojení")

    for online, stahni in [(False, vypadek), (True, ukazkovy_server), (True, vypadek)]:
        otazky, zdroj, zprava = ziskej_otazky(online=online, stahni=stahni)
        print("Zdroj:", zdroj, "otázky:", len(otazky))
        if zprava:
            print(zprava)
