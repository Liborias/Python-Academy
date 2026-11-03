SLEVA = 10                                 # globální konstanta, funkce ji může číst


def po_sleve(cena):
    snizeni = cena * SLEVA / 100           # snizeni je lokální, existuje jen ve funkci
    return cena - snizeni


def pokus():
    SLEVA = 50                             # POZOR: vytvoří NOVOU lokální SLEVA, globální se nezmění
    return SLEVA


print(po_sleve(200))                       # 180.0
print(pokus())                             # 50
print(SLEVA)                               # stále 10: globální proměnná zůstala
# print(snizeni)                           # kdybychom odkomentovali: NameError
