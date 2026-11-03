import csv
import json
from bs4 import BeautifulSoup


def _nacti(nazev_csv):
    try:
        with open(nazev_csv, encoding="utf-8", newline="") as soubor:
            radky = list(csv.DictReader(soubor))
    except FileNotFoundError:
        return []
    for radek in radky:
        radek["body"] = int(radek["body"])
    return radky


def body_podle_tridy(nazev_csv):
    soucty = {}
    for radek in _nacti(nazev_csv):
        soucty[radek["trida"]] = soucty.get(radek["trida"], 0) + radek["body"]
    return soucty


def nejlepsi_zak(nazev_csv):
    radky = _nacti(nazev_csv)
    if not radky:
        return None
    return max(radky, key=lambda r: r["body"])["jmeno"]


def uloz_jako_json(nazev_csv, cil):
    radky = _nacti(nazev_csv)
    if not radky:
        return 0
    with open(cil, "w", encoding="utf-8") as soubor:
        json.dump(radky, soubor, ensure_ascii=False, indent=2)
    return len(radky)


def odkazy(html):
    soup = BeautifulSoup(html, "html.parser")
    return [a["href"] for a in soup.find_all("a", href=True)]
