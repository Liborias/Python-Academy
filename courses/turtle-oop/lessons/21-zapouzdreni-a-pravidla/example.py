class Baterie:
    def __init__(self, energie):
        if energie < 0 or energie > 100:
            raise ValueError("Energie musí být od 0 do 100")
        self._energie = energie       # Vnitřní údaj podle dohody.

    def stav(self):
        return self._energie          # Čtení stav nemění.

    def dobij(self, kolik):
        if kolik < 0 or self._energie + kolik > 100:
            raise ValueError("Takto baterii dobít nelze")
        self._energie += kolik        # Změna až po ověření pravidel.
        return self._energie


baterie = Baterie(60)
print(baterie.dobij(20))               # 80
try:
    baterie.dobij(30)
except ValueError:
    print("Dobití odmítnuto")
print(baterie.stav())                  # Stále 80, chybný pokus nic nezměnil.
