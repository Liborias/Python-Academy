class Teplomer:
    def __init__(self, teplota=20):
        self.teplota = teplota

    @property
    def teplota(self):
        return self._teplota

    @teplota.setter
    def teplota(self, hodnota):
        if hodnota < -50 or hodnota > 100:
            raise ValueError("Teplota mimo rozsah")
        self._teplota = hodnota

    @property
    def fahrenheit(self):
        return self._teplota * 1.8 + 32
