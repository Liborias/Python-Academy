def analyza(text):
    slova = []
    for hrube in text.split():
        slovo = hrube.strip(".,!?;:\"()-").lower()
        if slovo:
            slova.append(slovo)
    if not slova:
        return {"slov": 0, "unikatnich": 0, "nejdelsi": "", "nejcastejsi": "", "prumerna_delka": 0}
    pocty = {}
    for slovo in slova:
        pocty[slovo] = pocty.get(slovo, 0) + 1
    nejdelsi = ""
    for slovo in slova:
        if len(slovo) > len(nejdelsi):
            nejdelsi = slovo
    return {
        "slov": len(slova),
        "unikatnich": len(set(slova)),
        "nejdelsi": nejdelsi,
        "nejcastejsi": min(pocty, key=lambda s: (-pocty[s], s)),
        "prumerna_delka": round(sum(len(s) for s in slova) / len(slova), 2),
    }
