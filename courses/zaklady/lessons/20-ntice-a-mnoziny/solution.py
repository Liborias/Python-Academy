def pocet_ruznych(seznam):
    return len(set(seznam))


def spolecne(a, b):
    return sorted(set(a) & set(b))


def prohod(dvojice):
    x, y = dvojice
    return y, x
