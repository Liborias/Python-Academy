# Ceny jsou celé koruny, hmotnosti celé gramy.
# Výpočet nabídky nic neodesílá a nemění zásoby.
from balik import Balik


class Doprava:
    def cena(self, balik):
        raise NotImplementedError("Cenu určuje konkrétní doprava")


class OsobniOdber(Doprava):
    def __init__(self, misto):
        if not isinstance(misto, str) or not misto.strip():
            raise ValueError("Osobní odběr potřebuje výdejní místo")
        self._misto = misto

    @property
    def misto(self):
        return self._misto

    def cena(self, balik):
        return 0


class Kuryr(Doprava):
    def __init__(self, adresa, limit_g=10000):
        if not isinstance(adresa, str) or not adresa.strip():
            raise ValueError("Kurýr potřebuje adresu")
        if type(limit_g) is not int or limit_g <= 0:
            raise ValueError("Limit musí být kladný celý počet gramů")
        self._adresa = adresa
        self._limit_g = limit_g

    @property
    def adresa(self):
        return self._adresa

    @property
    def limit_g(self):
        return self._limit_g

    def cena(self, balik):
        # Přepravitelnost ověřujeme před výpočtem cenového pásma.
        if balik.hmotnost_g > self.limit_g:
            raise ValueError("Balík překračuje limit kurýra")
        if balik.hmotnost_g <= 5000:
            return 99
        return 149


def ceny_dopravy(dopravy, balik):
    ceny = []
    # Konkrétní objekt vybere vlastní implementaci cena.
    for doprava in dopravy:
        ceny.append(doprava.cena(balik))
    return ceny


if __name__ == "__main__":
    moznosti = [OsobniOdber("Dílna Brno"), Kuryr("Javorová 1, Brno")]
    print("Lehký balík:", ceny_dopravy(moznosti, Balik("B-001", 1200)))
    print("Těžší balík:", ceny_dopravy(moznosti, Balik("B-002", 8000)))
    try:
        moznosti[1].cena(Balik("B-003", 10001))
    except ValueError:
        print("Nadlimitní balík kurýr odmítl.")
