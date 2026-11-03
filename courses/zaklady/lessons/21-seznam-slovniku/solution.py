def nejlepsi(studenti):
    nej = studenti[0]
    for s in studenti:
        if s["body"] > nej["body"]:
            nej = s
    return nej["jmeno"]


def prumer_bodu(studenti):
    soucet = 0
    for s in studenti:
        soucet += s["body"]
    return soucet / len(studenti)


def uspesni(studenti, hranice):
    jmena = []
    for s in studenti:
        if s["body"] >= hranice:
            jmena.append(s["jmeno"])
    return jmena


def pridej_studenta(studenti, jmeno, body):
    studenti.append({"jmeno": jmeno, "body": body})
    return studenti
