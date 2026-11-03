cisla = [40, 10, 30, 20]

print(min(cisla))                 # nejmenší hodnota: 10
print(max(cisla))                 # největší hodnota: 40
print(sum(cisla))                 # součet: 100
print(sorted(cisla))              # nový seřazený seznam; cisla se nezměnilo
print(20 in cisla)                # True, hodnota v seznamu je

cisla.remove(30)                  # odstraní hodnotu 30
posledni = cisla.pop()            # odebere poslední prvek a uloží ho
print(posledni, cisla)            # 20 [40, 10]
print(cisla[:1])                  # řez: jen první prvek -> [40]
cisla.sort()                      # .sort() seřadí původní seznam a nic nevrací
print(cisla)                      # [10, 40]
