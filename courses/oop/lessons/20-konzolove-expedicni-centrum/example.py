# Pracujeme jen v paměti s vlastními cvičnými údaji.
# Odmítnutí má ponechat poslední platný stav.
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
    # Rozdělení a převod vstupu patří ovladači, pravidla objektům.
    casti = radek.split()
    if not casti:
        return ""
    prikaz = casti[0]
    if prikaz == "stav" and len(casti) == 1:
        prehled = centrum.sklad.prehled()
        udaje = []
        for kod in sorted(prehled):
            udaje.append(f"{kod}={prehled[kod]}")
        return "Sklad: " + ", ".join(udaje)
    if prikaz == "nova" and len(casti) == 5:
        cislo = casti[1]
        knihy = int(casti[2])
        obaly = int(casti[3])
        gramy = int(casti[4])
        if knihy < 0 or obaly < 0 or knihy + obaly == 0:
            raise ValueError("Zvolte nezáporné počty a alespoň jeden kus")
        objednavka = NakupniObjednavka(cislo)
        if knihy:
            objednavka.pridej("KNIHA", "Průvodce Pythonem", 250, knihy)
        if obaly:
            objednavka.pridej("OBAL", "Dárkový obal", 30, obaly)
        centrum.prijmi(objednavka, Balik(f"B-{cislo}", gramy), OsobniOdber("Dílna Brno"), Adresa("Javorová 1", "Brno", "60200"))
        return f"Přijato: {cislo}"
    if prikaz == "prehled" and len(casti) == 2:
        return formatuj_souhrn(centrum.souhrn(casti[1]))
    if prikaz == "doprava" and len(casti) == 3:
        moznosti = {"odber": OsobniOdber("Dílna Brno"), "kuryr": Kuryr("Javorová 1, Brno"), "kolo": Cyklodoprava("Brno-střed")}
        if casti[2] not in moznosti:
            raise ValueError("Neznámý způsob dopravy")
        cena = centrum.zmen_dopravu(casti[1], moznosti[casti[2]])
        return f"Doprava: {cena} Kč"
    if prikaz == "poznamka" and len(casti) >= 3:
        pocet = centrum.pridej_poznamku(casti[1], " ".join(casti[2:]))
        return f"Poznámek: {pocet}"
    if prikaz == "storno" and len(casti) == 2:
        centrum.storno(casti[1])
        return f"Stornováno: {casti[1]}"
    raise ValueError("Neznámý příkaz nebo chybný počet argumentů")


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
