from bs4 import BeautifulSoup


def nazvy(html):
    soup = BeautifulSoup(html, "html.parser")
    nazvy_produktu = []
    for h3 in soup.select(".produkt h3"):
        nazvy_produktu.append(h3.get_text(strip=True))
    return nazvy_produktu


def ceny(html):
    soup = BeautifulSoup(html, "html.parser")
    ceny_produktu = []
    for cena in soup.select(".produkt .cena"):
        ceny_produktu.append(int(cena.get_text(strip=True).split()[0]))
    return ceny_produktu


def skladem(html):
    soup = BeautifulSoup(html, "html.parser")
    nazvy_skladem = []
    for produkt in soup.select("div.produkt"):
        if "vyprodano" not in produkt.get("class", []):
            nazvy_skladem.append(produkt.find("h3").get_text(strip=True))
    return nazvy_skladem


def odkaz_produktu(html, id_):
    soup = BeautifulSoup(html, "html.parser")
    odkaz = soup.select_one(f"#{id_} a")
    if odkaz is None:
        return None
    return odkaz.get("href")
