def pozdrav(jmeno)
    # vrátí text "Ahoj, <jméno>!"
    return "Ahoj, " + jmeno + "!"


def vek_za_rok(vek):
    # vrátí věk o rok později jako číslo
    return vek + "1"


def obsah_obdelniku(sirka, delka):
    # vrátí obsah obdélníku
    return sirka * vyska


def posledni(seznam):
    # vrátí poslední prvek seznamu
    return seznam[len(seznam)]


print(pozdrav("Eva"))
print(vek_za_rok(30))
print(obsah_obdelniku(3, 4))
print(posledni([1, 2, 3]))
