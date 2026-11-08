import math
from datetime import date
import requests
from cvicne_api import cvicne_api

# Ověření dat je samostatná funkce použitelná i pro soubor bez HTTP.
def over_kurz(data, mena):
    # Ověřte celý záznam a vraťte čtyři očekávané údaje.
    pass


def nacti_kurz(adresa, mena, timeout=2):
    symbol = mena.strip().upper()
    odpoved = requests.get(adresa.rstrip("/") + "/kurz", params={"mena": symbol}, timeout=timeout)
    odpoved.raise_for_status()
    return over_kurz(odpoved.json(), symbol)


if __name__ == "__main__":
    # Neúspěch předá řízení konkrétní větvi except, další pokus může pokračovat.
    with cvicne_api() as adresa:
        for cesta in ["", "/chyba", "/neplatny-json", "/spatna-data", ""]:
            try:
                print(nacti_kurz(adresa + cesta, "EUR"))
            except requests.Timeout:
                print("Vypršel čas čekání.")
            except ValueError:
                print("Odpověď nemá platná data.")
            except requests.RequestException:
                print("Přenos se nepodařil.")
