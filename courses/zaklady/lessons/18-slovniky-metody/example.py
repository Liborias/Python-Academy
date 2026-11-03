znamky = {"Eva": 1, "Petr": 3, "Jana": 2}

print("Petr" in znamky)               # True: klíč ve slovníku je
print(znamky.get("Karel", 5))         # 5: klíč chybí, vrátí se náhradní hodnota

for jmeno, znamka in znamky.items():  # každá dvojice se rozbalí do dvou proměnných
    if znamka > 1:
        print(jmeno, "má horší než jedničku")

del znamky["Eva"]                     # smaže dvojici s klíčem Eva
print(list(znamky.values()))          # [3, 2]: hodnoty jako seznam
