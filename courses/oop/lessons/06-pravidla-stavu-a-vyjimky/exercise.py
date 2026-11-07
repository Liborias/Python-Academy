class Zasoba:
    def __init__(self, nazev, pocet=0):
        # Neplatný počáteční počet odmítněte před přiřazením.
        self.nazev = nazev
        self._pocet = pocet

    def stav(self):
        return self._pocet

    def prijmi(self, kolik):
        # Nejprve ověřte kladné celé množství, potom změňte stav.
        pass

    def vydej(self, kolik):
        # Po kontrole typu a rozsahu ověřte i dostatek kusů.
        pass


if __name__ == "__main__":
    knihy = Zasoba("Průvodce Pythonem", 5)
    try:
        knihy.vydej(6)
    except ValueError:
        print("Nedostupný výdej odmítnut.")
    print("Po odmítnutí:", knihy.stav())
    print("Výdej posledních kusů:", knihy.vydej(5))
    print("Nový příjem:", knihy.prijmi(2))
