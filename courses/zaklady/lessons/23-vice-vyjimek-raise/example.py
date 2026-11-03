def sudy_polovina(n):
    if n % 2 != 0:
        raise ValueError("Číslo musí být sudé")  # vlastní výjimka s vysvětlením
    return n // 2


for hodnota in (8, 5, 0):
    try:
        print(sudy_polovina(hodnota))             # zkusíme zavolat funkci
    except ValueError as chyba:                   # as chyba: uloží výjimku do proměnné
        print("Chyba:", chyba)                    # vypíše zprávu z raise
    else:
        print("Bez chyby")                        # proběhne jen bez výjimky
    finally:
        print("--")                               # vypíše se pokaždé
