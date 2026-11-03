soucet = 0
with open("cisla.txt", encoding="utf-8") as soubor:
    for radek in soubor:                      # cyklus bere řádky souboru jeden po druhém
        radek = radek.strip()                 # strip() odstraní \n i mezery na okrajích
        if radek:                             # prázdný řádek je False, takže se přeskočí
            soucet += int(radek)

print("Součet čísel:", soucet)                # 54
