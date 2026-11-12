# Hmotnost zadáváme v kg, výšku v cm; výsledek předčasně nezaokrouhlujeme.
import math
from validace import kladne_cislo

def bmi(hmotnost_kg, vyska_cm):
    # TODO: doplňte podle zadání.
    raise NotImplementedError('Doplňte úkol.')

def pasmo(hodnota):
    # TODO: doplňte podle zadání.
    raise NotImplementedError('Doplňte úkol.')
# Pásmo určí původní hodnota, formátování mění pouze zobrazení.
if __name__ == '__main__':
    hodnota = bmi(81, 180)
    print(f'BMI: {hodnota:.2f}; pásmo: {pasmo(hodnota)}')
    print('Orientační ukazatel pro dospělé, ne posouzení zdraví.')
