from balik import Balik
from doprava import OsobniOdber, Kuryr
from expres import ExpresniKuryr


class Expedice:
    def __init__(self, balik, doprava):
        # Nejdřív ověřte nabídku, pak uchovejte stejné objekty.
        pass

    @property
    def balik(self):
        return self._balik

    @property
    def doprava(self):
        return self._doprava

    def nabidka(self):
        # Čtěte nabídku aktuálně zvolené dopravy.
        pass

    def zmen_dopravu(self, nova):
        # Novou dopravu uložte až po úspěšném ověření.
        pass


if __name__ == "__main__":
    balik = Balik("B-001", 1200)
    expedice = Expedice(balik, OsobniOdber("Dílna Brno"))
    print("Osobní odběr:", expedice.nabidka())
    print("Kurýr:", expedice.zmen_dopravu(Kuryr("Javorová 1, Brno")))
    print("Expres:", expedice.zmen_dopravu(ExpresniKuryr("Javorová 1, Brno", "dopoledne")))
    try:
        expedice.zmen_dopravu(Kuryr("Javorová 1, Brno", 1000))
    except ValueError:
        print("Volba odmítnuta, cena zůstává:", expedice.nabidka())
