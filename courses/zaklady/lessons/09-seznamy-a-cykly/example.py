jmena = ["Ema", "Jan", "Petr"]            # seznam řetězců

for jmeno in jmena:                        # jmeno postupně: Ema, Jan, Petr
    print("Ahoj,", jmeno)

delky = []                                 # prázdný seznam, naplníme ho v cyklu
for jmeno in jmena:
    delky.append(len(jmeno))               # přidáme délku každého jména

print(delky)                               # [3, 3, 4]
print("Průměrná délka:", sum(delky) / len(delky))   # součet děleno počtem
