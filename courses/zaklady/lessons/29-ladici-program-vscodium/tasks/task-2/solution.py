def dvojnasobky(data):
    """Vraťte nový seznam dvojnásobků."""
    vysledek = []
    for x in data:
        hodnota = x * 2
        vysledek.append(hodnota)
    return vysledek

print(dvojnasobky([2, -1, 0]))
