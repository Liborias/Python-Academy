class Zamestnanec:
    def __init__(self, jmeno):
        self.jmeno = jmeno

    def vizitka(self):
        return f"Jméno: {self.jmeno}"


class Technik(Zamestnanec):
    def __init__(self, jmeno, obor):
        super().__init__(jmeno)        # Nastaví základní údaje téhož objektu.
        self.obor = obor

    def vizitka(self):
        return f"{super().vizitka()}, obor: {self.obor}"  # Rozšíří výsledek.


t = Technik("Ema", "elektro")
print(t.vizitka())
t.jmeno = "Jan"                       # Další volání čte aktuální atributy.
print(t.vizitka())
print(Zamestnanec("Lada").vizitka())  # Základní třída dál funguje sama.
