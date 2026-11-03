class Batoh:
    def __init__(self):
        self.veci = []

    def pridej(self, predmet):
        self.veci.append(predmet)
        return len(self.veci)

    def obsah(self):
        return list(self.veci)
