def soucet_do(n):
    """Součet čísel 1 až n včetně."""
    soucet = 0
    for i in range(1, n + 1):
        soucet += i
    return soucet


def prumer_kladnych(cisla):
    """Průměr kladných čísel v seznamu, nebo 0, když žádné není."""
    soucet = 0
    pocet = 0
    for x in cisla:
        if x > 0:
            soucet += x
            pocet += 1
    if pocet == 0:
        return 0
    return soucet / pocet


def je_palindrom(text):
    """True, když se text čte stejně odpředu i odzadu (velikost písmen nehraje roli)."""
    text = text.lower()
    for i in range(len(text)):
        if text[i] != text[len(text) - 1 - i]:
            return False
    return True


print(soucet_do(3), prumer_kladnych([2, -5, 4]), je_palindrom("Kajak"))

assert soucet_do(3) == 6
assert prumer_kladnych([]) == 0
assert je_palindrom("Kajak")
