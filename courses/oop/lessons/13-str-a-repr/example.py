# print použije __str__, seznam zobrazí prvky přes __repr__.
# Oba dotazy vracejí text a nemění balík.
from balik import Balik


class PopsanyBalik(Balik):
    def __str__(self):
        # Použijeme již existující veřejnou metodu.
        return self.popis()

    def __repr__(self):
        # !r zapíše text včetně uvozovek a únikových znaků.
        return f"PopsanyBalik({self.kod!r}, {self.hmotnost_g!r})"


if __name__ == "__main__":
    balik = PopsanyBalik("B-001", 1200)
    print("Pro zákazníka:", balik)
    print("Pro vývojáře:", repr(balik))
    print("V seznamu:", [balik])
