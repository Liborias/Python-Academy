veta = "  Učím se Python  "                # text s mezerami na krajích

cista = veta.strip()                       # strip odstraní okrajové mezery -> nový řetězec
print(cista.upper())                       # UČÍM SE PYTHON
print(len(cista))                          # počet znaků: 14

slova = cista.split()                      # rozdělí na seznam slov podle mezer
print(slova)                               # ['Učím', 'se', 'Python']
print(len(slova))                          # počet slov: 3
print("_".join(slova))                     # spojí slova podtržítky: Učím_se_Python
print(cista.replace("Python", "Pythonu"))  # nahradí část textu
