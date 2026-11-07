from balik import Balik


class PopsanyBalik(Balik):
    def __str__(self):
        return self.popis()

    def __repr__(self):
        return f"PopsanyBalik({self.kod!r}, {self.hmotnost_g!r})"


if __name__ == "__main__":
    balik = PopsanyBalik("B-001", 1200)
    print("Pro zákazníka:", balik)
    print("Pro vývojáře:", repr(balik))
    print("V seznamu:", [balik])
