from bs4 import BeautifulSoup


def polozky(html, trida=None):
    soup = BeautifulSoup(html, "html.parser")
    if trida is None:
        nalezene = soup.find_all("li")
    else:
        nalezene = soup.find_all("li", class_=trida)
    texty = []
    for li in nalezene:
        texty.append(li.get_text(strip=True))
    return texty


def odkazy(html):
    soup = BeautifulSoup(html, "html.parser")
    dvojice = []
    for a in soup.find_all("a", href=True):
        dvojice.append((a.get_text(strip=True), a["href"]))
    return dvojice


def tabulka(html):
    soup = BeautifulSoup(html, "html.parser")
    radky = []
    for tr in soup.find_all("tr"):
        bunky = tr.find_all("td")
        if bunky:
            radky.append([b.get_text(strip=True) for b in bunky])
    return radky


def ceny(html):
    vysledek = {}
    for radek in tabulka(html):
        vysledek[radek[0]] = int(radek[1])
    return vysledek
