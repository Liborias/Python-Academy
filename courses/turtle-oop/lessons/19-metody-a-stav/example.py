class Teplomer:
    def __init__(self, teplota):
        self.teplota = teplota

    def posun(self, rozdil):
        self.teplota += rozdil       # Stav zůstane změněný i po konci metody.
        return self.teplota         # Návrat je další, samostatná činnost.


venku = Teplomer(18)
uvnitr = Teplomer(22)
print(venku.posun(3))                # 21
print(venku.posun(-2))               # 19: navazuje na předchozí hodnotu.
print(venku.teplota, uvnitr.teplota)  # 19 22: instance jsou nezávislé.
