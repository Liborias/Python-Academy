def pulka(n):
    if n % 2 != 0:
        raise ValueError("Nepovolená hodnota")
    return n // 2

print(pulka(8))
