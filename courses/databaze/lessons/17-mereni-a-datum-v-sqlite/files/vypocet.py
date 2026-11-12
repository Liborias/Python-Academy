# Hmotnost zadáváme v kg, výšku v cm; výsledek předčasně nezaokrouhlujeme.
import math
from validace import kladne_cislo

def bmi(hmotnost_kg, vyska_cm):
    hmotnost_kg = kladne_cislo(hmotnost_kg)
    vyska_m = kladne_cislo(vyska_cm) / 100
    try:
        hodnota = (hmotnost_kg / vyska_m) / vyska_m
    except ZeroDivisionError:
        raise ValueError('Výška je pro výpočet příliš malá.') from None
    if not math.isfinite(hodnota) or hodnota <= 0:
        raise ValueError('Výsledek nelze reprezentovat jako kladný konečný float.')
    return hodnota

def pasmo(hodnota):
    hodnota = kladne_cislo(hodnota)
    if hodnota < 18.5:
        return 'pod 18,5'
    if hodnota < 25:
        return '18,5 až pod 25'
    if hodnota < 30:
        return '25 až pod 30'
    return '30 a více'
