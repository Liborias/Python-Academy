nazev = "Merkur"              # řetězec (str) uložíme do proměnné nazev
prumer = 4879                 # celé číslo (int), průměr planety v km
hustota = 5.43                # desetinné číslo (float), s tečkou

print(type(nazev))            # vypíše <class 'str'>
print(type(hustota))          # vypíše <class 'float'>

# f-řetězec: hodnoty proměnných se vloží na místo {...}
print(f"{nazev} má průměr {prumer} km a hustotu {hustota} g/cm3.")

prumer = prumer + 1           # proměnnou lze změnit; nová hodnota se spočítá z té staré
print(prumer)                 # vypíše 4880
