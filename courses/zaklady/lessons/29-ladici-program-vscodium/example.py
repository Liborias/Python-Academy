def zdvojnasob(cisla):
    vysledek = []
    for x in cisla:
        dvojnasobek = x * 2                    # sem dejte bod přerušení a sledujte proměnné
        vysledek.append(dvojnasobek)
    return vysledek


print(zdvojnasob([1, 2, 3]))                   # [2, 4, 6]
# breakpoint()                                 # odkomentováním se program zastaví v ladicím programu pdb
