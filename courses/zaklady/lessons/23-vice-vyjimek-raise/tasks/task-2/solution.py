def nezaporne(n):
    if n < 0:
        raise ValueError("Nepovolená hodnota")
    return n

print(nezaporne(0))
