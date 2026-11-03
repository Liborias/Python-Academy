def najdi(data, jmeno):
    try:
        return data[jmeno]
    except KeyError:
        return "chybí"

print(najdi({'Ema': 2}, 'Ema'))
