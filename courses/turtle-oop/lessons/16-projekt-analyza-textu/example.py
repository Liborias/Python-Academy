text = "Ahoj světe, ahoj Pythone!"
slova = [s.strip(".,!?;:").lower() for s in text.split()]   # očištěná malá slova
print(slova)

pocty = {}                                   # slovník: slovo -> počet výskytů
for slovo in slova:
    pocty[slovo] = pocty.get(slovo, 0) + 1
print(pocty)

nejcastejsi = max(pocty, key=pocty.get)       # nejčastější slovo
print(nejcastejsi, pocty[nejcastejsi])
print(len(set(slova)), "různá slova")
