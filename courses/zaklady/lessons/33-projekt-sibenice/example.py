def pocet_samohlasek(slovo):
    samohlasky = set("aeiouy")                  # množina vznikne z textu: každé písmeno je prvek
    pocet = 0
    for pismeno in slovo:
        if pismeno in samohlasky:               # hledání v množině je rychlé
            pocet += 1
    return pocet


zkusena = set()                                 # prázdná množina
zkusena.add("a")                                # přidání prvku
zkusena.add("a")                                # duplicita se nepřidá
print(zkusena)                                  # {'a'}
print(pocet_samohlasek("kocka"))                # 2
