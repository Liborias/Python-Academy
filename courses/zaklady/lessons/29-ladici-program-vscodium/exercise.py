def fibonacci(n):
    """Prvních n Fibonacciho čísel (n je alespoň 2): 0, 1, 1, 2, 3, 5, ..."""
    cisla = [0, 1]
    while len(cisla) < n:
        cisla.append(cisla[-1] + cisla[0])
    return cisla


def nejdelsi_slovo(veta):
    """Nejdelší slovo věty. Při shodě první z nich."""
    nejdelsi = ""
    for slovo in veta.split():
        if len(slovo) >= len(nejdelsi):
            nejdelsi = slovo
    return nejdelsi


def pocet_vyskytu(seznam, hodnota):
    """Kolikrát se hodnota v seznamu vyskytuje."""
    pocet = 0
    for prvek in seznam:
        if prvek == hodnota:
            pocet = 1
    return pocet


print(fibonacci(7))
print(nejdelsi_slovo("pes kocka kun"))
print(pocet_vyskytu([1, 2, 1], 1))
