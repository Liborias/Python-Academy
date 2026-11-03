def samohlasky(text):
    pocet = 0
    for znak in text:
        if znak in "aeiouyAEIOUY":
            pocet += 1
    return pocet

print(samohlasky('Ahoj'))
