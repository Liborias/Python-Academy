with open("nakup.txt", "w", encoding="utf-8") as soubor:   # "w": soubor vznikne, starý obsah zmizí
    soubor.write("chleba\n")                                  # write nepřidává nový řádek, \n píšeme sami
    soubor.write("mléko\n")

with open("nakup.txt", "a", encoding="utf-8") as soubor:   # "a": přidáváme na konec
    print("sýr", file=soubor)                              # print s file= nový řádek přidá sám

with open("nakup.txt", encoding="utf-8") as soubor:        # bez režimu se čte
    print(soubor.read())
