class Had:
    def __init__(self, body, sirka=20, vyska=16):
        self.body = list(body)
        self.sirka = sirka
        self.vyska = vyska
        self.smer = (1, 0)

    def krok(self):
        # Vytvořte novou hlavu, přidejte ji dopředu a odeberte konec.
        # Souřadnice zůstanou v mřížce díky zbytku po dělení.
        pass


if __name__ == "__main__":
    had = Had([(4, 1), (3, 1), (2, 1)], sirka=6, vyska=4)
    print("Start:", had.body)
    for _ in range(3):
        print("Hlava:", had.krok(), "Tělo:", had.body)
