a, b = 1, 2
a, b = b, a                              # prohození
print(a, b)

prvni, *zbytek = [10, 20, 30, 40]        # rozbalení se zbytkem
print(prvni, zbytek)

jmena = ["Ada", "Bob", "Cyril"]
veky = [30, 25, 41]
for cislo, (jmeno, vek) in enumerate(zip(jmena, veky), start=1):
    print(f"{cislo}. {jmeno} ({vek})")

def delka_a_prvni(slovo):
    return len(slovo), slovo[0]           # vrací dvojici

d, p = delka_a_prvni("python")
print(d, p)
