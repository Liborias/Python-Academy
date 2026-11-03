def obdelnik(sirka, vyska=1, znak="#"):     # vyska a znak mají výchozí hodnoty
    for _ in range(vyska):                   # _ je jméno proměnné, kterou nepoužijeme
        print(znak * sirka)                  # řádek ze znaků


obdelnik(5)                                  # jen šířka: 1 řádek znaků #
obdelnik(5, 2)                               # šířka a výška: 2 řádky
obdelnik(3, znak="*", vyska=2)               # pojmenované argumenty, pořadí nevadí
print("a", "b", "c", sep="-")                # hotová funkce print také: a-b-c
