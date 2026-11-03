def pocet_slov(text):
    pocty = {}
    for slovo in text.lower().split():
        pocty[slovo] = pocty.get(slovo, 0) + 1
    return pocty


def nejcastejsi(text):
    pocty = pocet_slov(text)
    return max(pocty, key=pocty.get)
