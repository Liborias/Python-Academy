def prvni_a_posledni(s):
    if not s:
        return ""
    return s[0] + s[-1]


def obrat(s):
    return s[::-1]


def kazde_druhe(s):
    return s[::2]


def bez_okraju(s):
    return s[1:-1]


def je_palindrom(s):
    t = s.lower().replace(" ", "")
    return t == t[::-1]
