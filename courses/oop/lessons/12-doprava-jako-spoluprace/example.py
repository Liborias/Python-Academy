# Ceny jsou celé koruny, hmotnosti celé gramy.
# Výpočet nabídky nic neodesílá a nemění zásoby.
from balik import Balik
from doprava import OsobniOdber, Kuryr
from expres import ExpresniKuryr


class Expedice:
    def __init__(self, balik, doprava):
        # Neplatná kombinace vyvolá výjimku dřív, než uložíme volbu.
        doprava.cena(balik)
        self._balik = balik
        self._doprava = doprava

    @property
    def balik(self):
        return self._balik

    @property
    def doprava(self):
        return self._doprava

    def nabidka(self):
        # Aktuální cenu vždy získáme od zvolené dopravy.
        return self.doprava.cena(self.balik)

    def zmen_dopravu(self, nova):
        cena = nova.cena(self.balik)
        # Sem se dostaneme pouze po úspěšném ověření nabídky.
        self._doprava = nova
        return cena


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

    # Stačí společná metoda cena; dědění zde není podmínkou.
    class Cyklodoprava:
        def cena(self, balik):
            if balik.hmotnost_g > 2000:
                raise ValueError("Na kolo je balík těžký")
            return 59

    print("Nová doprava bez změny Expedice:", expedice.zmen_dopravu(Cyklodoprava()))
