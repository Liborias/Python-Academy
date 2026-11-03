import random

ZVIRATA = ["pes", "kocka", "kralik", "krokodyl", "papousek", "slon", "zirafa", "tygr"]


def odhal(slovo, hadana):
    znaky = []
    for pismeno in slovo:
        if pismeno in hadana:
            znaky.append(pismeno)
        else:
            znaky.append("_")
    return " ".join(znaky)


def vyhrano(slovo, hadana):
    for pismeno in slovo:
        if pismeno not in hadana:
            return False
    return True


def pocet_chyb(slovo, hadana):
    chyby = 0
    for pismeno in hadana:
        if pismeno not in slovo:
            chyby += 1
    return chyby


def hra(slovo, zivoty=7):
    hadana = set()
    while True:
        print(odhal(slovo, hadana))
        pismeno = input("Písmeno: ").strip().lower()
        if len(pismeno) != 1:
            print("Zadejte jedno písmeno.")
            continue
        if pismeno in hadana:
            print("Už bylo.")
            continue
        hadana.add(pismeno)
        if vyhrano(slovo, hadana):
            print("Vyhráli jste!")
            return True
        if pocet_chyb(slovo, hadana) >= zivoty:
            print("Prohráli jste. Slovo bylo", slovo)
            return False


if __name__ == "__main__":
    hra(random.choice(ZVIRATA))
