import json
import requests
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser

AGENT = "Dilna-Sberac"


def nejlevnejsi(knihy):
    if not knihy:
        return None
    return min(knihy, key=lambda k: k["cena"])


def prumerna_cena(knihy):
    if not knihy:
        return 0
    return round(sum(k["cena"] for k in knihy) / len(knihy), 1)


def sber_cen(adresa, nazev_json, cesta="/knihy.html"):
    hlavicky = {"User-Agent": AGENT + "/1.0"}
    try:
        odpoved = requests.get(adresa + "/robots.txt", headers=hlavicky, timeout=3)
        pravidla = RobotFileParser()
        if odpoved.status_code != 404:
            pravidla.parse(odpoved.text.splitlines())
            if not pravidla.can_fetch(AGENT, adresa + cesta):
                return None
        odpoved = requests.get(adresa + cesta, headers=hlavicky, timeout=3)
        odpoved.raise_for_status()
    except requests.RequestException:
        return None
    soup = BeautifulSoup(odpoved.text, "html.parser")
    knihy = []
    for li in soup.select(".kniha"):
        if "vyprodano" in li.get("class", []):
            continue
        knihy.append({
            "nazev": li.select_one(".nazev").get_text(strip=True),
            "cena": int(li.select_one(".cena").get_text(strip=True).split()[0]),
            "skladem": True,
        })
    nejl = nejlevnejsi(knihy)
    vysledek = {
        "pocet": len(knihy),
        "nejlevnejsi": nejl["nazev"] if nejl else None,
        "prumer": prumerna_cena(knihy),
        "knihy": knihy,
    }
    with open(nazev_json, "w", encoding="utf-8") as soubor:
        json.dump(vysledek, soubor, ensure_ascii=False, indent=2)
    return vysledek
