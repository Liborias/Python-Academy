class Karta:
    def __init__(self, kod):
        self.kod = kod

    def __eq__(self, other):
        if not isinstance(other, Karta):
            return NotImplemented  # Jiný typ dostane možnost porovnání.
        return self.kod == other.kod


a = Karta("A1")
b = Karta("A1")
kopie = a                         # Pouze další odkaz na tentýž objekt.
print(a == b)                     # True
print(a is b)                     # False
print(a is kopie)                 # True
b.kod = "B2"
print(a == b)                     # False: porovnává se aktuální stav.
print(a == "A1")                  # False, bez chyby neznámého atributu.
