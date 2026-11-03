def nejvetsi(cisla):
    vysledek = cisla[0]
    for x in cisla:
        if x > vysledek:
            vysledek = x
    return vysledek


assert nejvetsi([3, 9, 2]) == 9                # test: tvrzení musí platit
assert nejvetsi([5]) == 5                      # krajní případ: jeden prvek
assert nejvetsi([-4, -1, -8]) == -1, "záporná čísla"   # za čárkou je zpráva při selhání
print("Všechny testy prošly")                  # vypíše se, jen když žádný assert neselhal
