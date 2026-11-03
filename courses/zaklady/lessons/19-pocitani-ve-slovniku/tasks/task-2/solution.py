def hlasy(data):
    pocty = {}
    for x in data:
        klic = x
        pocty[klic] = pocty.get(klic, 0) + 1
    return pocty

print(hlasy(['les', 'hrad', 'les']))
