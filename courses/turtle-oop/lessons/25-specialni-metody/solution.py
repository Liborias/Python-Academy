class Trasa:
    def __init__(self, jmeno, body):
        self.jmeno = jmeno
        self.body = list(body)

    def __str__(self):
        return f"Trasa {self.jmeno}, bodů: {len(self.body)}"

    def __repr__(self):
        return f"Trasa(jmeno={self.jmeno!r}, body={self.body!r})"

    def __len__(self):
        return len(self.body)
