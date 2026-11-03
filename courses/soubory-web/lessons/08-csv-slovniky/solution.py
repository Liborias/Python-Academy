import csv


def nacti_zaky(nazev):
    zaci = []
    with open(nazev, encoding="utf-8", newline="") as soubor:
        for radek in csv.DictReader(soubor):
            radek["body"] = int(radek["body"])
            zaci.append(radek)
    return zaci


def nejlepsi_zak(nazev):
    nejlepsi = None
    for zak in nacti_zaky(nazev):
        if nejlepsi is None or zak["body"] > nejlepsi["body"]:
            nejlepsi = zak
    return nejlepsi["jmeno"]


def prumer_podle_trid(nazev):
    souhrny = {}
    for zak in nacti_zaky(nazev):
        body = souhrny.get(zak["trida"], [])
        body.append(zak["body"])
        souhrny[zak["trida"]] = body
    prumery = {}
    for trida, body in souhrny.items():
        prumery[trida] = sum(body) / len(body)
    return prumery


def uloz_zaky(nazev, zaci):
    with open(nazev, "w", encoding="utf-8", newline="") as soubor:
        zapisovac = csv.DictWriter(soubor, fieldnames=["jmeno", "trida", "body"])
        zapisovac.writeheader()
        zapisovac.writerows(zaci)
