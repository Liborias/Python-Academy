def cetnosti(data):
    pocty = {}
    for x in data:
        pocty[x] = pocty.get(x, 0) + 1
    return pocty

print(cetnosti(['a', 'b', 'a']))
