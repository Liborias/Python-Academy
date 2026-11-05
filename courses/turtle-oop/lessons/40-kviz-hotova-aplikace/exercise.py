from kviz_model import Kviz
from kviz_api import ziskej_otazky


def hraj(otazky, vstup=input, vypis=print):
    # Opakujte neplatný vstup, vyhodnoťte a/n a ošetřete q i EOF.
    # Vraťte dvojici (skóre, počet zodpovězených otázek).
    pass


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
