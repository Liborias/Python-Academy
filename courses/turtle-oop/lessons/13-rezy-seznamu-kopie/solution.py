def poslednich(s, n):
    if n <= 0:
        return []
    return s[-n:]


def obrat_seznam(s):
    return s[::-1]


def rozdel_na_poloviny(s):
    stred = len(s) // 2
    return s[:stred], s[stred:]


def kopie_matice(m):
    return [radek[:] for radek in m]
