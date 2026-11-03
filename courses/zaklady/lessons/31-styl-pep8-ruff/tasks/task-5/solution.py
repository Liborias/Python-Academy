def soucet_dvojnasobku(cisla):
    """Vrátí součet dvojnásobků zadaných čísel."""
    soucet = 0
    for cislo in cisla:
        soucet += 2 * cislo
    return soucet

print(soucet_dvojnasobku([1, 2, 3]))
