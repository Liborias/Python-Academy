import csv
import requests
from bs4 import BeautifulSoup


def ziskej_knihy(html):
    soup = BeautifulSoup(html, "html.parser")
    knihy = []
    for li in soup.select(".kniha"):
        knihy.append({
            "nazev": li.select_one(".nazev").get_text(strip=True),
            "autor": li.select_one(".autor").get_text(strip=True),
            "cena": int(li.select_one(".cena").get_text(strip=True).split()[0]),
            "skladem": "vyprodano" not in li.get("class", []),
        })
    return knihy


def uloz_csv(knihy, nazev):
    with open(nazev, "w", encoding="utf-8", newline="") as soubor:
        zapisovac = csv.DictWriter(soubor, fieldnames=["nazev", "autor", "cena", "skladem"])
        zapisovac.writeheader()
        for kniha in knihy:
            radek = dict(kniha)
            radek["skladem"] = "ano" if kniha["skladem"] else "ne"
            zapisovac.writerow(radek)


def stahni_knihy(url, nazev_csv):
    try:
        odpoved = requests.get(url, timeout=3)
        odpoved.raise_for_status()
    except requests.RequestException:
        return 0
    knihy = ziskej_knihy(odpoved.text)
    uloz_csv(knihy, nazev_csv)
    return len(knihy)
