class Playlist:
    def __init__(self, nazev):
        self.nazev = nazev
        self.skladby = []          # Nový seznam pro každou instanci.

    def pridej(self, skladba):
        self.skladby.append(skladba)
        return len(self.skladby)

    def seznam_skladeb(self):
        return list(self.skladby)  # Kopie chrání vlastní seznam objektu.


rano = Playlist("Ráno")
vecer = Playlist("Večer")
print(rano.pridej("Lesní cesta"))  # 1
kopie = rano.seznam_skladeb()
kopie.append("Jen v kopii")        # Původní playlist se nezmění.
print(rano.seznam_skladeb())       # ['Lesní cesta']
print(vecer.seznam_skladeb())      # []: druhá instance má svůj seznam.
