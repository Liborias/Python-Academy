class Zprava:
    def __init__(self, text):
        self.text = text

    def zobraz(self):
        return f"Zpráva: {self.text}"


class DulezitaZprava(Zprava):
    def zobraz(self):
        return f"DŮLEŽITÉ: {self.text}"  # Přepisuje jen toto chování.


bezna = Zprava("Schůzka ve tři")
dulezita = DulezitaZprava("Změna místa")  # __init__ přebírá ze Zprava.
for zprava in [bezna, dulezita]:
    print(zprava.zobraz())               # Stejné volání, různé provedení.
print(isinstance(dulezita, Zprava))       # True: je také zprávou.
