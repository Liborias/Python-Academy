import requests
from cvicne_api import cvicne_api

# Funkce dostává základní adresu, nevybírá si tajně jiný server.
def nacti_kurz(adresa, mena):
    # Sestavte požadavek s params a timeout, ověřte stav a vraťte JSON.
    pass


if __name__ == "__main__":
    # Server běží jen během with na vašem počítači, žádná bankovní služba.
    with cvicne_api() as adresa:
        print(nacti_kurz(adresa, " eur "))
        print(nacti_kurz(adresa, "USD"))
