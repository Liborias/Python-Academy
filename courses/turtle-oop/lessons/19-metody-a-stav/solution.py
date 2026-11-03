class Pocitadlo:
    def __init__(self, zacatek=0):
        self.hodnota = zacatek

    def pridej(self, kolik):
        self.hodnota += kolik
        return self.hodnota

    def vynuluj(self):
        self.hodnota = 0
