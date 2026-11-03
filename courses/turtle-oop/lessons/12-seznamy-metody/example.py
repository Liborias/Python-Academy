cisla = [5, 3, 8, 1]
cisla.append(7)                     # přidá na konec
cisla.sort()                        # seřadí přímo v seznamu
print(cisla)                        # [1, 3, 5, 7, 8]

slova = ["pes", "kočka", "kráva", "ryba"]
print(sorted(slova, key=len))       # podle délky, původní seznam zůstává
print(slova)

a = [1, 2]
b = a                               # stejný seznam
b.append(3)
print(a)                            # [1, 2, 3]  (a se změnil také!)
c = a.copy()                        # skutečná kopie
c.append(4)
print(a, c)
