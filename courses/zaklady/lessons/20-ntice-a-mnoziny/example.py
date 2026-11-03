cisla = [4, 2, 4, 9, 2, 2]
ruzna = set(cisla)                            # množina zahodí duplicity
print(len(ruzna))                             # 3 různé hodnoty
print(sorted(ruzna))                          # [2, 4, 9]: množinu seřadíme do seznamu

a = {1, 2, 3, 4}
b = {3, 4, 5}
print(sorted(a & b))                          # [3, 4]: průnik, tedy co mají společné
print(sorted(a | b))                          # [1, 2, 3, 4, 5]: sjednocení

x, y = 10, 20
x, y = y, x                                   # prohození dvou proměnných
print(x, y)                                   # 20 10
