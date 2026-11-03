def slova_textu(text):
    slova = []
    for slovo in text.split():
        cisty = slovo.strip(".,!?;:").lower()   # strip s parametrem odebere vyjmenované znaky
        if cisty:                               # prázdný text se v podmínce chová jako False
            slova.append(cisty)
    return slova


print(slova_textu("Ahoj, světe! Ahoj..."))      # ['ahoj', 'světe', 'ahoj']
print(round(4.666, 1))                          # 4.7: zaokrouhlení na jedno desetinné místo
