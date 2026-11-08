import requests
from cvicne_api import cvicne_api

# Funkce dostává základní adresu, nevybírá si tajně jiný server.
def nacti_kurz(adresa, mena):
    symbol = mena.strip().upper()
    odpoved = requests.get(adresa.rstrip("/") + "/kurz", params={"mena": symbol}, timeout=2)
    odpoved.raise_for_status()
    return odpoved.json()


if __name__ == "__main__":
    # Server běží jen během with na vašem počítači, žádná bankovní služba.
    with cvicne_api() as adresa:
        print(nacti_kurz(adresa, " eur "))
        print(nacti_kurz(adresa, "USD"))
