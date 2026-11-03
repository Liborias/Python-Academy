def nezaporne(data):
    """Vraťte nový seznam nezáporných čísel v původním pořadí."""
    vysledek = []
    for x in data:
        if x >= 0:
            vysledek.append(x)
    return vysledek

print(nezaporne([-2, 0, 3]))
