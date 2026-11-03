a = {1, 2, 3, 4}
b = {3, 4, 5}
print(a & b, a | b, a - b, a ^ b)       # průnik, sjednocení, rozdíl, symetrický rozdíl

slova = ["pes", "kočka", "pes", "ryba", "kočka"]
unikatni = set(slova)
print(len(unikatni), sorted(unikatni))  # množina nemá pořadí, proto sorted

videno = set()
for x in [4, 2, 4, 7, 2]:
    if x in videno:                     # rychlý test výskytu
        print("duplicita:", x)
    videno.add(x)
