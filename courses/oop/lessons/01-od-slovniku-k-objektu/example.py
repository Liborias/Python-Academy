# Slovník seskupí údaje. Třída navíc pojmenuje jejich vlastní typ.
stitek = {"kod": "B-001", "hmotnost": 2}
print("Slovník:", stitek["kod"], stitek["hmotnost"])


class Balicek:
    pass


def vytvor_balicek(kod, hmotnost):
    novy = Balicek()
    novy.kod = kod
    novy.hmotnost = hmotnost
    return novy


prvni = vytvor_balicek("B-001", 2)
druhy = vytvor_balicek("B-002", 5)
# Změna jednoho balíčku nepřepisuje druhou instanci.
prvni.hmotnost = 3
print("První balíček:", prvni.kod, prvni.hmotnost)
print("Druhý balíček:", druhy.kod, druhy.hmotnost)
