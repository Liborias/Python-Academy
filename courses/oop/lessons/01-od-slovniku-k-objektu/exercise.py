class Zasilka:
    pass


def vytvor_zasilku(kod, prijemce):
    # Vytvořte novou instanci a uložte kod, prijemce a stav prijata.
    # Vraťte objekt, aby s ním mohl volající dál pracovat.
    pass


if __name__ == "__main__":
    prvni = vytvor_zasilku("Z-101", "Ema")
    druha = vytvor_zasilku("Z-102", "Jan")
    print(prvni.kod, prvni.prijemce, prvni.stav)
    print(druha.kod, druha.prijemce, druha.stav)
