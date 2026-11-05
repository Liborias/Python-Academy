class Zasilka:
    pass


def vytvor_zasilku(kod, prijemce):
    zasilka = Zasilka()
    zasilka.kod = kod
    zasilka.prijemce = prijemce
    zasilka.stav = "prijata"
    return zasilka


if __name__ == "__main__":
    prvni = vytvor_zasilku("Z-101", "Ema")
    druha = vytvor_zasilku("Z-102", "Jan")
    print(prvni.kod, prvni.prijemce, prvni.stav)
    print(druha.kod, druha.prijemce, druha.stav)
