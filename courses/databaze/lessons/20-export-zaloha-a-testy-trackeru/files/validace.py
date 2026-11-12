import math

def kladne_cislo(hodnota):
    if type(hodnota) not in (int, float):
        raise ValueError('Očekávám kladné konečné číslo, ne text nebo bool.')
    try:
        cislo = float(hodnota)
    except OverflowError:
        raise ValueError('Číslo nelze zpracovat jako float.') from None
    if not math.isfinite(cislo) or cislo <= 0:
        raise ValueError('Číslo musí být kladné a konečné.')
    return cislo

def cti_cislo(text):
    try:
        cislo = float(text.strip().replace(',', '.'))
    except ValueError:
        raise ValueError('Napište číslo, například 72,5.') from None
    return kladne_cislo(cislo)
