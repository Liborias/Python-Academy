from contextlib import closing
def ukazka(Evidence):
    # Předvídatelný pokus, který nezapisuje do vašeho trvalého souboru.
    with closing(Evidence(':memory:')) as klub:
        kategorie = klub.pridej_kategorii('Sport')
        mic = klub.pridej_pomucku("Míč O'Neil", 2, kategorie)
        klub.pridej_pomucku('Krabice', 0)
        cislo = klub.pujc(mic, 'Žofie')
        print('Po půjčení:', klub.prehled())
        print('Aktivní:', klub.aktivni_vypujcky())
        print('Vráceno:', klub.vrat(cislo))
        print('Podruhé:', klub.vrat(cislo))
        print('Konečný stav:', klub.prehled())
