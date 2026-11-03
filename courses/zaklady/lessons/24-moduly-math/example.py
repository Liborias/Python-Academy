import math                                   # modul se importuje na začátku souboru

polomer = 3
print(math.pi * polomer ** 2)                 # obsah kruhu: 28.274333882308138
print(math.sqrt(49))                          # 7.0: odmocnina vždy vrací desetinné číslo
print(math.ceil(2.1), math.floor(2.9))        # 3 2: zaokrouhlení nahoru a dolů

from math import hypot                        # jen jedna funkce, píše se bez math.
print(hypot(3, 4))                            # 5.0: přepona pravoúhlého trojúhelníku
