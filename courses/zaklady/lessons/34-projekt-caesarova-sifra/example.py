ABECEDA = "abcdefghijklmnopqrstuvwxyz"


def posun_male(pismeno, posun):
    pozice = ABECEDA.index(pismeno)             # kolikáté písmeno abecedy to je (a = 0)
    nova = (pozice + posun) % len(ABECEDA)      # % zajistí návrat na začátek abecedy
    return ABECEDA[nova]


print(posun_male("a", 3))                       # d
print(posun_male("y", 3))                       # b: za z se pokračuje od a
print("Ahoj"[0].isupper(), "ahoj"[0].isupper()) # True False
