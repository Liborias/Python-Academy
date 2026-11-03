def prumer(cisla):
    # průměr čísel, pro prázdný seznam 0
    return sum(cisla) / len(cisla)


def druha_nejvetsi(cisla):
    # druhá největší RŮZNÁ hodnota, nebo None, pokud neexistuje
    seznam = sorted(cisla)
    return seznam[-2]


def kolik_slov(veta):
    # počet slov ve větě
    return veta.count(" ")


def bez_duplicit(seznam):
    # seznam bez opakování v pořadí prvního výskytu
    return list(set(seznam))
