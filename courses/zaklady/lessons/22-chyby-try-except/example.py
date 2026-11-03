def na_cislo(text):
    try:
        return int(text)                      # pokus o převod, může vyvolat ValueError
    except ValueError:
        return None                           # při chybě vrátíme None a program nespadne


print(na_cislo("42"))                         # 42
print(na_cislo("abc"))                        # None
print(na_cislo("3.5"))                        # None: int() desetinný zápis nepřijme

vek = None
while vek is None:                            # is None: ptáme se, jestli hodnota je None (nic)
    vek = na_cislo(input("Kolik je vám let? "))
print("Zadali jste", vek)
