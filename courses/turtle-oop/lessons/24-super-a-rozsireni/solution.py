class Hrac:
    def __init__(self, jmeno):
        self.jmeno = jmeno

    def popis(self):
        return f"Hráč: {self.jmeno}"


class BodovanyHrac(Hrac):
    def __init__(self, jmeno, body=0):
        super().__init__(jmeno)
        self.body = body

    def popis(self):
        return f"{super().popis()}, body: {self.body}"

    def pridej_body(self, kolik):
        self.body += kolik
        return self.body
