def vitez(data):
    nej = data[0]
    for polozka in data:
        if polozka["body"] > nej["body"]:
            nej = polozka
    return nej["jmeno"]

print(vitez([{'jmeno': 'Ema', 'body': 2}, {'jmeno': 'Jan', 'body': 4}]))
