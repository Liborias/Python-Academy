def slova_textu(text):
    slova = []
    for slovo in text.split():
        cisty = slovo.strip(".,!?;:").lower()
        if cisty:
            slova.append(cisty)
    return slova


def analyzuj_text(text):
    slova = slova_textu(text)
    if not slova:
        return {"slov": 0, "unikatnich": 0, "nejdelsi": "", "prumerna_delka": 0}
    nejdelsi = slova[0]
    soucet_delek = 0
    for slovo in slova:
        soucet_delek += len(slovo)
        if len(slovo) > len(nejdelsi):
            nejdelsi = slovo
    return {
        "slov": len(slova),
        "unikatnich": len(set(slova)),
        "nejdelsi": nejdelsi,
        "prumerna_delka": round(soucet_delek / len(slova), 1),
    }


def popis_analyzy(vysledek):
    radky = [
        f"Slov: {vysledek['slov']}",
        f"Unikátních: {vysledek['unikatnich']}",
        f"Nejdelší: {vysledek['nejdelsi']}",
        f"Průměrná délka: {vysledek['prumerna_delka']}",
    ]
    return "\n".join(radky)


def hlavni():
    text = input("Text: ")
    print(popis_analyzy(analyzuj_text(text)))


if __name__ == "__main__":
    hlavni()
