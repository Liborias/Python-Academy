def cena(text):
    try:
        return float(text)
    except ValueError:
        return None

print(cena('12.5'))
