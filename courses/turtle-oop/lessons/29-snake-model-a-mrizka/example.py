class Had:
    def __init__(self, body, sirka=20, vyska=16):
        # Seznam patří této instanci, první buňka je hlava.
        self.body = list(body)
        self.sirka = sirka
        self.vyska = vyska
        self.smer = (1, 0)

    def krok(self):
        x, y = self.body[0]
        dx, dy = self.smer
        # Modulo vrátí hada z okraje na protější stranu.
        nova = ((x + dx) % self.sirka, (y + dy) % self.vyska)
        self.body.insert(0, nova)
        self.body.pop()
        return nova


had = Had([(4, 1), (3, 1), (2, 1)], sirka=6, vyska=4)
print("Start:", had.body)
for _ in range(3):
    print("Hlava:", had.krok(), "Tělo:", had.body)
had.smer = (0, 1)
print("Nahoru:", had.krok())
