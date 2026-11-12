# Zkušební inventární číslo má na konci jednu kontrolní číslici.
from pravidla_kodu import telo_kodu

def kontrolni_cislice(telo):
    # TODO: doplňte podle zadání.
    raise NotImplementedError('Doplňte úkol.')

def platny_kod(kod):
    # TODO: doplňte podle zadání.
    raise NotImplementedError('Doplňte úkol.')
# Kontrolní číslice odhalí některé překlepy, není důkazem totožnosti ani oprávnění.
if __name__ == '__main__':
    for telo in ['1','12','0007','109']:
        kod = telo + kontrolni_cislice(telo)
        print('Tělo:', telo, 'kód:', kod, 'platný:', platny_kod(kod))
