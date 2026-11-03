def slova(data):
    pocty = {}
    for x in data.split():
        klic = x
        pocty[klic] = pocty.get(klic, 0) + 1
    return pocty

print(slova('a b a'))
