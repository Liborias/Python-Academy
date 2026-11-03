import random

PORAZI = {"kámen": "nůžky", "nůžky": "papír", "papír": "kámen"}


def vitez_kola(a, b):
    if a == b:
        return "remiza"
    if PORAZI[a] == b:
        return "prvni"
    return "druhy"


def nahodny_tah():
    return random.choice(list(PORAZI))


def skore(tahy):
    prvni = 0
    druhy = 0
    remizy = 0
    for a, b in tahy:
        vitez = vitez_kola(a, b)
        if vitez == "prvni":
            prvni += 1
        elif vitez == "druhy":
            druhy += 1
        else:
            remizy += 1
    return prvni, druhy, remizy


def hra(kol):
    tahy = []
    while len(tahy) < kol:
        tah = input("Váš tah: ").strip().lower()
        if tah not in PORAZI:
            print("Takový tah neexistuje.")
            continue
        pocitac = nahodny_tah()
        vitez = vitez_kola(tah, pocitac)
        if vitez == "prvni":
            print("Vyhráli jste.")
        elif vitez == "druhy":
            print("Vyhrál počítač.")
        else:
            print("Remíza.")
        tahy.append((tah, pocitac))
    return skore(tahy)


if __name__ == "__main__":
    print(hra(3))
