with open("basen.txt", encoding="utf-8") as soubor:   # with soubor po bloku sám zavře
    text = soubor.read()                              # read() přečte celý soubor jako jeden řetězec

print(text)                                           # výpis včetně přechodů na nové řádky
print("Počet znaků:", len(text))                      # řetězec je obyčejný text, funguje len
print("Počet slov:", len(text.split()))               # split() rozdělí podle mezer i nových řádků
