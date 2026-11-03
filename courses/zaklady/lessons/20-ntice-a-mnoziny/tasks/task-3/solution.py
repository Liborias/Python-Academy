def prunik(a, b):
    return sorted(set(a) & set(b))

print(prunik([3, 1, 3], [3, 2]))
