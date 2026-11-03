import requests
from dilna_web import spust

adresa = spust()


def stahni(url):
    try:
        odpoved = requests.get(url, timeout=1)   # čekáme nejvýš 1 sekundu
        odpoved.raise_for_status()               # kódy 404 a 500 změní na výjimku
    except requests.HTTPError:
        return "chyba stránky"
    except requests.ConnectionError:
        return "nepodařilo se připojit"
    except requests.Timeout:
        return "server je moc pomalý"
    return odpoved.text.strip()


print(stahni(adresa + "/clanky/1.html"))        # <h1>Článek 1</h1>
print(stahni(adresa + "/neexistuje"))          # chyba stránky
print(stahni(adresa + "/_pomalu/3"))           # server je moc pomalý
print(stahni("http://127.0.0.1:1/"))           # nepodařilo se připojit: na portu 1 nikdo neposlouchá
