import random

PLANETY = {
    "Merkur": {"vzdalenost": 58, "prumer": 4879},
    "Venuše": {"vzdalenost": 108, "prumer": 12104},
    "Země": {"vzdalenost": 150, "prumer": 12742},
    "Mars": {"vzdalenost": 228, "prumer": 6779},
    "Jupiter": {"vzdalenost": 778, "prumer": 139820},
    "Saturn": {"vzdalenost": 1434, "prumer": 116460},
    "Uran": {"vzdalenost": 2871, "prumer": 50724},
    "Neptun": {"vzdalenost": 4495, "prumer": 49244},
}


def napoveda(planety, jmeno):
    udaje = planety[jmeno]
    return f"Je {udaje['vzdalenost']} mil. km od Slunce a má průměr {udaje['prumer']} km."


def je_spravne(tip, jmeno):
    return tip.strip().lower() == jmeno.lower()


def vyber_planetu(planety):
    return random.choice(list(planety))


def pocet_pokusu(tipy, jmeno):
    poradi = 0
    for tip in tipy:
        poradi += 1
        if je_spravne(tip, jmeno):
            return poradi
    return None


def hra(planety, jmeno):
    print(napoveda(planety, jmeno))
    pokusy = 0
    while True:
        tip = input("Která planeta to je? ")
        pokusy += 1
        if je_spravne(tip, jmeno):
            print("Správně!")
            return pokusy
        print("Ne, zkuste to znovu.")


if __name__ == "__main__":
    hra(PLANETY, vyber_planetu(PLANETY))
