cisla = []
for i in range(5):
    cisla.append(int(input("Číslo: ")))
print(f"Průměr: {sum(cisla) / len(cisla)}")
print(f"Největší: {max(cisla)}")
