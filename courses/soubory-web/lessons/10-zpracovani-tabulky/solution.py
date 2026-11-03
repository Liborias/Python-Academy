import csv


def nacti_prodej(nazev):
    radky = []
    with open(nazev, encoding="utf-8", newline="") as soubor:
        for radek in csv.DictReader(soubor):
            radek["kusy"] = int(radek["kusy"])
            radek["cena"] = int(radek["cena"])
            radky.append(radek)
    return radky


def trzby_podle_zbozi(radky):
    trzby = {}
    for radek in radky:
        trzby[radek["zbozi"]] = trzby.get(radek["zbozi"], 0) + radek["kusy"] * radek["cena"]
    return trzby


def nejlepsi_mesic(radky):
    trzby = {}
    for radek in radky:
        trzby[radek["mesic"]] = trzby.get(radek["mesic"], 0) + radek["kusy"] * radek["cena"]
    return max(trzby, key=trzby.get)


def nejvic_kusu(radky, n):
    podle_kusu = sorted(radky, key=lambda r: r["kusy"], reverse=True)
    return podle_kusu[:n]
