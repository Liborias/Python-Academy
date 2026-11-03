def delky(data):
    pocty = {}
    for x in data:
        klic = len(x)
        pocty[klic] = pocty.get(klic, 0) + 1
    return pocty

print(delky(['pes', 'hrad', 'les']))
