import random

HRY = {"kostka": 6, "mince": 2}                 # slovník: kolik možností má která hra


def vyber_hru(hry):
    return random.choice(list(hry))             # list() změní klíče slovníku na seznam


def hra_na_hadani():
    tajne = random.randint(1, 3)
    while True:                                 # opakuje se, dokud hráč neuhodne
        tip = int(input("Hádej číslo 1 až 3: "))
        if tip == tajne:
            print("Správně!")
            return                              # return cyklus i funkci ukončí
        print("Ne, zkuste to znovu.")


if __name__ == "__main__":                      # spustí se jen při přímém spuštění souboru
    print("Dnes hrajeme:", vyber_hru(HRY))
    hra_na_hadani()
