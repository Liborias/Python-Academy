def pocet_dlouhych(text, minimum):
    pocet = 0
    for slovo in text.split():
        if len(slovo) >= minimum:
            pocet += 1
    return pocet

print(pocet_dlouhych('pes kočka les', 4))
