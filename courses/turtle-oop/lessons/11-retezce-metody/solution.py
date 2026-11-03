def pocet_slov(text):
    return len(text.split())


def nejdelsi_slovo(text):
    nejdelsi = ""
    for slovo in text.split():
        if len(slovo) > len(nejdelsi):
            nejdelsi = slovo
    return nejdelsi


def titulek(text):
    return " ".join(slovo.capitalize() for slovo in text.split())


def zamen_samohlasky(text, znak):
    vysledek = ""
    for pismeno in text:
        if pismeno.lower() in "aeiouy":
            vysledek += znak
        else:
            vysledek += pismeno
    return vysledek
