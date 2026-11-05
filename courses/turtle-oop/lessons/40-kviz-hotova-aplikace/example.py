# Celý kvíz lze ovládat v konzoli pomocí a, n a q.
# Enter při výběru zdroje použije přiložené české otázky.
from kviz_model import Kviz
from kviz_api import ziskej_otazky


def hraj(otazky, vstup=input, vypis=print):
    kviz = Kviz(otazky)
    while kviz.aktualni() is not None:
        otazka = kviz.aktualni()
        vypis(f"{kviz.index + 1}/{len(kviz.otazky)}: {otazka.text}")
        while True:
            try:
                volba = vstup("Pravda (a), nepravda (n), konec (q): ").strip().casefold()
            except EOFError:
                vypis("Vstup skončil.")
                vypis(f"Průběžné skóre: {kviz.skore}/{kviz.index}")
                return kviz.skore, kviz.index
            if volba == "q":
                vypis("Kvíz ukončen.")
                vypis(f"Průběžné skóre: {kviz.skore}/{kviz.index}")
                return kviz.skore, kviz.index
            if volba not in ("a", "n"):
                vypis("Zadejte a, n nebo q.")
                continue
            if kviz.odpovez(volba == "a"):
                vypis("Správně.")
            else:
                spravna = "n"
                if otazka.spravne:
                    spravna = "a"
                vypis(f"Nesprávně. Správná odpověď: {spravna}.")
            break
    vypis(f"Výsledek: {kviz.skore}/{kviz.index}")
    return kviz.skore, kviz.index


def hlavni(vstup=input, vypis=print):
    try:
        volba = vstup("Zdroj [Enter = offline, api = internet]: ").strip().casefold()
    except EOFError:
        vypis("Vstup skončil.")
        return
    try:
        otazky, zdroj, zprava = ziskej_otazky(online=volba == "api")
    except (OSError, ValueError) as chyba:
        vypis(f"Otázky se nepodařilo načíst: {chyba}")
        return
    vypis(f"Zdroj: {zdroj}")
    if zprava:
        vypis(zprava)
    return hraj(otazky, vstup, vypis)


if __name__ == "__main__":
    hlavni()
