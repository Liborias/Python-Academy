def skladem(data, nazev):
    return data.get(nazev, 0)

print(skladem({'čaj': 3}, 'čaj'))
