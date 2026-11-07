from adresa import Adresa
from balik import Balik
from centrum import Cyklodoprava, ExpedicniCentrum
from doprava import OsobniOdber, Kuryr
from nakupni_objednavka import NakupniObjednavka
from rezervacni_sklad import RezervacniSklad


NAPOVEDA = "Příkazy: stav | nova ČÍSLO KNIHY OBALY GRAMY | prehled ČÍSLO | doprava ČÍSLO odber/kuryr/kolo | poznamka ČÍSLO TEXT | storno ČÍSLO | konec"


def vytvor_demo():
    sklad = RezervacniSklad()
    sklad.pridej("KNIHA", "Průvodce Pythonem", 5)
    sklad.pridej("OBAL", "Dárkový obal", 2)
    return ExpedicniCentrum(sklad)


def formatuj_souhrn(souhrn):
    poznamky = "; ".join(souhrn["poznamky"]) or "žádné"
    return (f"{souhrn['cislo']}: {souhrn['stav']}\n"
            f"Zboží: {souhrn['zbozi']} Kč | Doprava: {souhrn['doprava']} Kč | Nabídka: {souhrn['celkem']} Kč\n"
            f"Balík: {souhrn['balik']} | Adresa: {souhrn['adresa']}\n"
            f"Poznámky: {poznamky}")


def proved_prikaz(centrum, radek):
    # Doplňte podle rozhraní vysvětleného v lekci.
    pass


def spust():
    centrum = vytvor_demo()
    print("Chytré expediční centrum — cvičná data")
    print(NAPOVEDA)
    while True:
        try:
            radek = input("> ")
        except EOFError:
            break
        if radek.strip() == "konec":
            break
        try:
            zprava = proved_prikaz(centrum, radek)
            if zprava:
                print(zprava)
        except ValueError as chyba:
            print(f"Odmítnuto: {chyba}")
    print("Na shledanou.")


if __name__ == "__main__":
    spust()
