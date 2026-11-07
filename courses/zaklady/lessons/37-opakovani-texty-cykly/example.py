def pocet_znaku(text, hledany):
    pocet = 0
    for znak in text:                           # cyklus prochází text po znacích
        if znak == hledany:
            pocet += 1
    return pocet


def ciferne_cislo(n):
    return len(str(n))                          # str() převede číslo na text, len spočítá znaky


print(pocet_znaku("banan", "a"))                # 2
print(ciferne_cislo(12345))                     # 5
for znak in str(472):                           # po převodu na text lze číslici po číslici procházet
    print(int(znak) + 1)                        # 5, 8, 3
