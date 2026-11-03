class Zvire:
    def __init__(self, jmeno):
        self.jmeno = jmeno

    def pozdrav(self):
        return f"Ahoj, jsem {self.jmeno}."


class Pes(Zvire):
    def pozdrav(self):
        return f"Haf, jsem {self.jmeno}."


class Kocka(Zvire):
    def pozdrav(self):
        return f"Mňau, jsem {self.jmeno}."
