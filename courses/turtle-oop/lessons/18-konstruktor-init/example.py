class Kniha:
    def __init__(self, nazev, stran):
        self.nazev = nazev     # Atribut konkrétní knihy, ne lokální proměnná.
        self.stran = stran


prvni = Kniha("Řeka", 80)      # self předá Python sám.
druha = Kniha("Hory", 200)
print(prvni.nazev, prvni.stran)
prvni.stran += 1               # Změní se jen první instance.
print(prvni.stran, druha.stran)  # 81 200
