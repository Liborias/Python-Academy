class Ctverec:
    def __init__(self, strana):
        self.strana = strana       # I první nastavení projde setterem.

    @property
    def strana(self):
        return self._strana

    @strana.setter
    def strana(self, hodnota):
        if hodnota < 0:
            raise ValueError("Strana nesmí být záporná")
        self._strana = hodnota

    @property
    def obsah(self):
        return self._strana * self._strana  # Výpočet při každém čtení.


ctverec = Ctverec(3)
print(ctverec.obsah)                # 9: property čteme bez závorek.
ctverec.strana = 5
print(ctverec.obsah)                # 25: žádná zastaralá uložená hodnota.
try:
    ctverec.strana = -1
except ValueError:
    print("Záporná strana odmítnuta")
print(ctverec.strana)               # Stále 5.
