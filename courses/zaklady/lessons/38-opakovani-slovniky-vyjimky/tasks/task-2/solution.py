def soucet_platnych(texty):
    celkem = 0
    for text in texty:
        try:
            celkem += int(text)
        except ValueError:
            celkem += 0
    return celkem

print(soucet_platnych(['2', 'x', '3']))
