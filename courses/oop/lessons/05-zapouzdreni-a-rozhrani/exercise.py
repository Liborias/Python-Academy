class Zasoba:
    def __init__(self, nazev, pocet=0):
        self.nazev = nazev
        # Počet patří do vnitřního atributu, například _pocet.
        pass

    def stav(self):
        pass

    def prijmi(self, kolik):
        pass

    def vydej(self, kolik):
        pass


if __name__ == "__main__":
    knihy = Zasoba("Průvodce Pythonem", 5)
    obaly = Zasoba("Dárkový obal", 2)
    print("Na začátku:", knihy.stav())
    print("Po příjmu:", knihy.prijmi(3))
    print("Po výdeji:", knihy.vydej(2))
    print("Obaly zůstaly:", obaly.stav())
