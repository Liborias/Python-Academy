def fizzbuzz(n):
    vysledek = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            vysledek.append("FizzBuzz")
        elif i % 3 == 0:
            vysledek.append("Fizz")
        elif i % 5 == 0:
            vysledek.append("Buzz")
        else:
            vysledek.append(str(i))
    return vysledek


def je_prvocislo(n):
    if n < 2:
        return False
    for delitel in range(2, n):
        if n % delitel == 0:
            return False
    return True


def obrat_slova(veta):
    nove = []
    for slovo in veta.split():
        nove.insert(0, slovo)
    return " ".join(nove)


def pocet_samohlasek(text):
    pocet = 0
    for znak in text.lower():
        if znak in "aeiouy":
            pocet += 1
    return pocet


def ciferny_soucet(n):
    soucet = 0
    for cifra in str(n):
        soucet += int(cifra)
    return soucet
