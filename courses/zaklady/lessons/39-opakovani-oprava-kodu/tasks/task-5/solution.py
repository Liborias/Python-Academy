def pocet_vyskytu(data, hledany):
    pocet = 0
    for x in data:
        if x == hledany:
            pocet += 1
    return pocet

print(pocet_vyskytu([2, 1, 2], 2))
