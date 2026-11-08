import math
from datetime import date
import requests
from cvicne_api import cvicne_api

# Ověření dat je samostatná funkce použitelná i pro soubor bez HTTP.
def over_kurz(data, mena):
    symbol = mena.strip().upper()
    if not isinstance(data, dict) or data.get("mena") != symbol:
        raise ValueError("Odpověď má jinou měnu nebo nesprávný tvar.")
    kurz = data.get("czk_za_jednotku")
    if isinstance(kurz, bool) or not isinstance(kurz, (int, float)):
        raise ValueError("Kurz musí být číslo.")
    try:
        kurz = float(kurz)
    except OverflowError:
        raise ValueError("Kurz je příliš velký.") from None
    if not math.isfinite(kurz) or kurz <= 0:
        raise ValueError("Kurz musí být konečné kladné číslo.")
    datum = data.get("datum")
    if not isinstance(datum, str) or date.fromisoformat(datum).isoformat() != datum:
        raise ValueError("Datum musí mít tvar RRRR-MM-DD.")
    zdroj = data.get("zdroj")
    if not isinstance(zdroj, str) or not zdroj.strip():
        raise ValueError("Chybí zdroj kurzu.")
    return {"mena": symbol, "czk_za_jednotku": kurz, "datum": datum, "zdroj": zdroj.strip()}


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
