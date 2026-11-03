# Najděte a opravte chyby podle zadání.
def minimum(data):
    nej = 0
    for x in data:
        if x > nej:
            nej = x
    return nej
