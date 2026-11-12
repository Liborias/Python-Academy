# Zkušební inventární číslo má na konci jednu kontrolní číslici.
from pravidla_kodu import telo_kodu

def kontrolni_cislice(telo):
    telo = telo_kodu(telo)
    soucet = 0
    for index, znak in enumerate(reversed(telo)):
        cislo = int(znak)
        if index % 2 == 0:
            cislo *= 2
            if cislo > 9:
                cislo -= 9
        soucet += cislo
    return str((-soucet) % 10)

def platny_kod(kod):
    if not isinstance(kod,str) or not 2<=len(kod)<=33 or not all('0'<=c<='9' for c in kod):
        return False
    return kontrolni_cislice(kod[:-1]) == kod[-1]
