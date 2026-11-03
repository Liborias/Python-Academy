jmeno = input("Jak se jmenuješ? ")      # input vrátí vždy text
print("Ahoj,", jmeno)

text = input("Kolik je ti let? ")        # zatím je to jen text, například "15"
vek = int(text)                          # int() ho převede na celé číslo
print("Za pět let ti bude", vek + 5)     # s číslem už můžeme počítat
