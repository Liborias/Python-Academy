def sjednoceni(a, b):
    return sorted(set(a) | set(b))

print(sjednoceni([3, 1], [2, 3]))
