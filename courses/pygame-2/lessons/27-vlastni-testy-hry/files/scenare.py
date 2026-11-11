# Záznam modelu: žádné kreslení, čekání ani změna světa.
def snimek(kolo):
    return {
        'cas': round(kolo.cas, 6),
        'pozice': tuple(round(v, 6) for v in kolo.hrac.pozice),
        'skore': kolo.skore,
        'zivoty': kolo.zivoty,
        'vlna': kolo.vlny.cislo,
        'droni': tuple((type(d).__name__, *[round(v, 6) for v in d.pozice]) for d in kolo.drony),
        'konec': kolo.konec,
        'duvod': kolo.duvod,
    }
