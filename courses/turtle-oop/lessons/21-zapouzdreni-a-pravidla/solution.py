class Ucet:
    def __init__(self, zacatek=0):
        if zacatek < 0:
            raise ValueError("Počáteční zůstatek nesmí být záporný")
        self._zustatek = zacatek

    def stav(self):
        return self._zustatek

    def vloz(self, castka):
        if castka <= 0:
            raise ValueError("Vklad musí být kladný")
        self._zustatek += castka
        return self._zustatek

    def vyber(self, castka):
        if castka <= 0 or castka > self._zustatek:
            raise ValueError("Neplatný výběr")
        self._zustatek -= castka
        return self._zustatek
