from balik import Balik


class PopsanyBalik(Balik):
    def __str__(self):
        # Vraťte aktuální veřejný popis balíku.
        pass

    def __repr__(self):
        # Vraťte text podobný volání konstruktoru, s bezpečným zápisem kódu.
        pass


if __name__ == "__main__":
    balik = PopsanyBalik("B-001", 1200)
    print("Pro zákazníka:", balik)
    print("Pro vývojáře:", repr(balik))
    print("V seznamu:", [balik])
